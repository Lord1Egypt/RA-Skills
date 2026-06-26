import numpy as np
import pandas as pd
from evalmole import get_mol_set, get_nfp_set, get_mol
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import shap
from rdkit import Chem
from rdkit.Chem import AllChem
# Function to load the dataset
def load_dataset(filepath):
    df = pd.read_csv(filepath)
    return df['X'], df['Y']
# Function to prepare the dataset by filtering out invalid molecules
def prepare_data(X, Y):
    X_, Y_ = [], []
    for smi, y_ in zip(X, Y):
        try:
            get_mol(smi)  # Check if the molecule can be processed
            X_.append(smi)
            Y_.append(y_)
        except:
            pass
    return X_, Y_
# Function to train and evaluate the model
def train_and_evaluate(X_train, X_test, y_train, y_test):
    xmol_train, xmol_test = get_mol_set(X_train), get_mol_set(X_test)
    xfp_train, xfp_test = get_nfp_set(xmol_train, n_bits=1024), get_nfp_set(xmol_test, n_bits=1024)
    clf = RandomForestClassifier(random_state=32).fit(xfp_train, y_train)  
    y_pred = clf.predict(xfp_test)
    classification_report_str = classification_report(y_test, y_pred)
    accuracy_score_str = f"Accuracy Score: {accuracy_score(y_test, y_pred)}"   
    return clf, classification_report_str, accuracy_score_str, xfp_test
# Function to generate and save SHAP values plot
def save_shap_plot(clf, xfp_test):
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(xfp_test)
    shap.summary_plot(shap_values, xfp_test, max_display=10)
# Function to extract substructure and generate SMILES
def get_substructure_smiles(test_smi):
    test_mol = Chem.MolFromSmiles(test_smi)
    info = {}
    fp = AllChem.GetMorganFingerprintAsBitVect(test_mol, 2, nBits=1024, bitInfo=info)
    amap = {}
    env = Chem.FindAtomEnvironmentOfRadiusN(test_mol, 0, 1, 4)
    submol = Chem.PathToSubmol(test_mol, env, atomMap=amap)
    submol_smiles = Chem.MolToSmiles(submol)
    return amap, submol_smiles
# Function to save the results to a text file
def save_results(classification_report_str, accuracy_score_str, shap_summary, amap, submol_smiles):
    with open('output.txt', 'w') as file:
        file.write("Classification Report:\n")
        file.write(classification_report_str)
        file.write("\n")
        file.write(accuracy_score_str)
        file.write("\n\n")
        file.write("SHAP Summary Plot Information (Graph is saved separately):\n")
        file.write(str(shap_summary))  # Note: this may not work as intended, it's for informational purposes
        file.write("\n")
        file.write(f"Substructure Atom Map: {amap}\n")
        file.write(f"Substructure SMILES: {submol_smiles}\n")