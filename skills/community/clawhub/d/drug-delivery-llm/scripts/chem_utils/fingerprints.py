import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
#计算指纹1
def compute_fingerprint(mol, n_bits=128):
    radius = 2
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
    return [int(bit) for bit in fp.ToBitString()]
#计算指纹2
def compute_fingerprint_from_smiles(smiles, n_bits=128):
    mol = Chem.MolFromSmiles(smiles)
    return compute_fingerprint(mol, n_bits)
#计算指纹3
def generate_fingerprints(mol_list, n_bits=128):
return np.array([compute_fingerprint(mol, n_bits) for mol in mol_list])