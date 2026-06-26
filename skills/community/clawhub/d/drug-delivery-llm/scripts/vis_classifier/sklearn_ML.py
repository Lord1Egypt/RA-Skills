import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from rdkit import Chem
from rdkit.Chem import AllChem
import shap
import logging
from evalmole import get_mol_set, get_nfp_set, get_mol
#配置日志
logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.info
#数据加载
def load_and_clean_data(path):
    df = pd.read_csv(path)
    X, Y = df['X'], df['Y']
    X_clean, Y_clean = [], []
    for smi, label in zip(X, Y):
        try:
            get_mol(smi)
            X_clean.append(smi)
            Y_clean.append(label)
        except Exception:
            continue
    return X_clean, Y_clean
# 模型评估
def evaluate_model(model, x_train, x_test, y_train, y_test, label="Model"):
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    log(f"\n Evaluation - {label}")
    log(classification_report(y_test, y_pred))
    log(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
def prepare_fingerprints(X_train, X_test, n_bits):
    mol_train = get_mol_set(X_train)
    mol_test = get_mol_set(X_test)
    return get_nfp_set(mol_train, n_bits), get_nfp_set(mol_test, n_bits)
# 运行
def run_models_on_fp(X_train, X_test, y_train, y_test, n_bits):
    log(f"\n Fingerprint Size: {n_bits}")
    fp_train, fp_test = prepare_fingerprints(X_train, X_test, n_bits)
    models = {
        "RandomForest": RandomForestClassifier(random_state=32),
        "LogisticRegression": LogisticRegression(random_state=42),
        "DecisionTree": DecisionTreeClassifier(criterion='entropy', splitter='random', random_state=42),
        "SVM": make_pipeline(StandardScaler(), SVC(gamma='auto'))
    }
    for name, model in models.items():
        evaluate_model(model, fp_train, fp_test, y_train, y_test, f"{name} ({n_bits}-bit)")
    return fp_train, fp_test, models["RandomForest"]
# 可解释特征
def explain_with_shap(model, x_test_fp, max_display=10):
    explainer = shap.TreeExplainer(model, check_additivity=False)
    shap_values = explainer.shap_values(x_test_fp, check_additivity=False)
    shap.summary_plot(shap_values, x_test_fp, max_display=max_display)
    if isinstance(shap_values, list) and len(shap_values) > 1:
        shap.summary_plot(shap_values[1], x_test_fp, max_display=20)
# 子结构提取
def extract_substructure(smi, radius=0, atom_idx=1):
    mol = Chem.MolFromSmiles(smi)
    bit_info = {}
    AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024, bitInfo=bit_info)
    env = Chem.FindAtomEnvironmentOfRadiusN(mol, radius, atom_idx)
    atom_map = {}
    submol = Chem.PathToSubmol(mol, env, atomMap=atom_map)
    return Chem.MolToSmiles(submol), bit_info
if __name__ == "__main__":
    # Load and preprocess
    X, Y = load_and_clean_data("datasets/XY-c2.csv")
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    # Run for multiple fingerprint sizes
    for bits in [32, 128, 1024, 2048]:
        fp_train, fp_test, best_model = run_models_on_fp(X_train, X_test, y_train, y_test, bits)
        # Only run SHAP once for best case
        if bits == 1024:
            explain_with_shap(best_model, fp_test)
    # Optional: visualize one molecule’s substructure
    smi_example = X[2000]
    sub_smiles, bit_info = extract_substructure(smi_example)
    log(f"\n🔬 Substructure SMILES: {sub_smiles}")
    log(f"Bit Info: {bit_info}")