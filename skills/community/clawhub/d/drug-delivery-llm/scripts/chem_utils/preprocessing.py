import numpy as np
from rdkit import Chem
#去空
def remove_empty_strings(smiles_list):
return np.array([smi for smi in smiles_list if smi != ''])
#去平凡分子
def remove_short_strings(smiles_list, min_length=3):
return np.array([smi for smi in smiles_list if len(smi) >= min_length])
#去重
def get_unique_smiles(smiles_list):
return np.unique(smiles_list)
#去无构象
def remove_invalid_molecules(smiles_list):
    return np.array([smi for smi in smiles_list if Chem.MolFromSmiles(smi) is not None])
#批处理
def preprocess_smiles(smiles_list):
    cleaned = remove_short_strings(smiles_list)
    unique = get_unique_smiles(cleaned)
    valid = remove_invalid_molecules(unique)
return valid