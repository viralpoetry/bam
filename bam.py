"""
Bidirectional Associative Memory (BAM) Implementation
https://en.wikipedia.org/wiki/Bidirectional_associative_memory
"""

import pprint
from typing import List


class BAM:
    def __init__(self, data: List[List[List[int]]]) -> None:
        """
        Initializes the BAM with provided association pairs in bipolar form.

        Args:
            data (List[List[List[int]]]): List of input-output vector pairs in binary form.
        """
        # Store associations in bipolar form and determine matrix dimensions
        self.AB = [
            [self._to_bipolar(pair[0]), self._to_bipolar(pair[1])] for pair in data
        ]
        self.len_x = len(self.AB[0][1])
        self.len_y = len(self.AB[0][0])
        # Initialize empty BAM matrix
        self.M = [[0] * self.len_x for _ in range(self.len_y)]
        # Compute BAM matrix based on the associations
        self._create_bam_matrix()

    def _create_bam_matrix(self) -> None:
        """
        Constructs the BAM matrix by applying Hebbian learning on the associations.
        """
        for x_vec, y_vec in self.AB:
            for i, x_val in enumerate(x_vec):
                for j, y_val in enumerate(y_vec):
                    self.M[i][j] += x_val * y_val

    def get_association(self, A: List[int]) -> List[int]:
        """
        Returns the associated output vector for a given input vector using BAM.

        Args:
            A (List[int]): Input vector in binary form.

        Returns:
            List[int]: Associated output vector in binary form.
        """
        bipolar_A = self._mult_mat_vec(A)
        return self._threshold(bipolar_A)

    def get_bam_matrix(self) -> List[List[int]]:
        """
        Retrieves the BAM matrix.

        Returns:
            List[List[int]]: The BAM matrix.
        """
        return self.M

    def _mult_mat_vec(self, vec: List[int]) -> List[int]:
        """
        Multiplies the BAM matrix with an input vector.

        Args:
            vec (List[int]): Input vector in binary form.

        Returns:
            List[int]: Resulting vector after multiplication with BAM matrix.
        """
        v_res = [0] * self.len_x
        for i in range(self.len_y):
            for j in range(self.len_x):
                v_res[j] += vec[i] * self.M[i][j]
        return v_res

    def _threshold(self, vec: List[int]) -> List[int]:
        """
        Applies a threshold to transform a bipolar vector into binary form.

        Args:
            vec (List[int]): Input vector in bipolar form.

        Returns:
            List[int]: Output vector in binary form.
        """
        return [1 if val >= 0 else 0 for val in vec]

    def _to_bipolar(self, vec: List[int]) -> List[int]:
        """
        Converts a binary vector to bipolar form.

        Args:
            vec (List[int]): Binary input vector.

        Returns:
            List[int]: Converted bipolar vector.
        """
        return [1 if val == 1 else -1 for val in vec]


if __name__ == "__main__":
    # Define sample data pairs
    data_pairs = [
        [[1, 0, 1, 0, 1, 0], [1, 1, 0, 0]],
        [[1, 1, 1, 0, 0, 0], [1, 0, 1, 0]],
    ]

    # Initialize BAM with data pairs
    bam = BAM(data_pairs)

    # Pretty print the BAM matrix
    pp = pprint.PrettyPrinter(indent=4)
    print("BAM Matrix:")
    pp.pprint(bam.get_bam_matrix())

    # Test associations
    test_inputs = [
        [1, 0, 1, 0, 1, 0],
        [1, 1, 1, 0, 0, 0],
    ]

    for input_vector in test_inputs:
        print(f"{input_vector} ---> {bam.get_association(input_vector)}")
