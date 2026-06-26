# Script 14: Result Comparator

import numpy as np

python_results = np.array([220, 225, 230])
reference_results = np.array([221, 224, 229])

error = python_results - reference_results

print("Errors:", error)
print("Mean Error:", np.mean(error))
