import pandas as pd
from qiskit import BasicAer
from qiskit.utils import QuantumInstance, algorithm_globals
from qiskit.circuit.library import ZZFeatureMap
from qiskit_machine_learning.kernels import QuantumKernel
from qiskit_machine_learning.algorithms import classifiers
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from evalmole import get_mol, get_mol_set, get_128fp_set
# 超参
SEED = 1376
FEATURE_DIM = 6
TEST_SIZE = 0.2
algorithm_globals.random_seed = SEED
#数据
def load_and_filter_data(filepath):
    """Load SMILES and labels, filter out invalid molecules."""
    df = pd.read_csv(filepath)
    data = [(smi, label) for smi, label in zip(df['X'], df['Y']) if get_mol(smi) is not None]
    X, y = zip(*data)
    return list(X), list(y)
def prepare_fingerprints(smiles_list):
    """Convert SMILES to fingerprints."""
    mols = get_mol_set(smiles_list)
    return get_128fp_set(mols)
#量子模块
def get_quantum_kernel():
    """Build the quantum kernel with a ZZFeatureMap."""
    feature_map = ZZFeatureMap(feature_dimension=FEATURE_DIM, reps=2, entanglement="linear")
    backend = QuantumInstance(
        BasicAer.get_backend("qasm_simulator"),
        shots=1024,
        seed_simulator=SEED,
        seed_transpiler=SEED,
    )
    return QuantumKernel(feature_map=feature_map, quantum_instance=backend)
# QSVM模型
X, y = load_and_filter_data('classification_dataset/XY-c2.csv')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=SEED)
fp_train = prepare_fingerprints(X_train)
fp_test = prepare_fingerprints(X_test)
pca = PCA(n_components=FEATURE_DIM)
X_train_pca = pca.fit_transform(fp_train)
X_test_pca = pca.transform(fp_test)
quantum_kernel = get_quantum_kernel()
qsvc = classifiers.QSVC(quantum_kernel=quantum_kernel)
qsvc.fit(X_train_pca, y_train)

# 评估
y_pred = qsvc.predict(X_test_pca)