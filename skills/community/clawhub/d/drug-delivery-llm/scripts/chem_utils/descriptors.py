import numpy as np
from rdkit import Chem
from rdkit.Chem import QED
# 从辅助工具中导入 SA (可合成性) 计算模块
# 注意：这通常依赖于 Ertl 等人开发的 sascorer.py 脚本
from chem_utils.utils import cal_SA 
from chem_utils.utils.cal_SA import sascorer 

# ---------------------------------------------------------
# 分子格式转换函数
# ---------------------------------------------------------

# 批处理格式转换：将 SMILES 字符串列表转换为 RDKit 分子对象(Mol)列表
def smiles_to_mol_list(smiles_list):
    mol_list = []
    for i, smi in enumerate(smiles_list):
        # 将 SMILES 字符串转化为 Mol 对象
        mol = Chem.MolFromSmiles(smi)
        # 检查转化是否成功
        if mol is None:
            print(f"Invalid SMILES at index {i}") # 如果 SMILES 无效，打印索引报错
        else:
            mol_list.append(mol) # 仅将有效的分子对象加入列表
    return mol_list

# 单个格式转换：将单个 SMILES 字符串转换为 Mol 对象
def smiles_to_mol(smiles):
    return Chem.MolFromSmiles(smiles)

# ---------------------------------------------------------
# QED (类药性) 计算函数
# ---------------------------------------------------------

# QED计算1：直接从 SMILES 列表计算 QED 分数
def compute_qed_from_smiles(smiles_list):
    qed_scores = []
    for i, smi in enumerate(smiles_list):
        mol = smiles_to_mol(smi)
        # 如果分子有效，计算 QED；如果无效，赋值为 0
        qed = QED.qed(mol) if mol else 0
        
        # 错误日志记录
        if mol is None:
            print(f"Invalid SMILES at index {i}")
            
        qed_scores.append(qed)
    # 返回 Numpy 数组，便于后续向量化计算
    return np.array(qed_scores)

# QED计算2：从 Mol 对象列表计算 QED 分数 (效率更高，因为省去了转换步骤)
def compute_qed_from_mols(mol_list):
    # 使用列表推导式批量计算
    return np.array([QED.qed(mol) for mol in mol_list])

# ---------------------------------------------------------
# SA (可合成性) 计算函数
# 分数越低越容易合成 (通常 1=容易, 10=极难)
# ---------------------------------------------------------

# SA计算1：从 Mol 对象列表计算 SA 分数
def compute_sa_from_mols(mol_list):
    # 调用 sascorer 工具进行打分
    return np.array([sascorer.calculateScore(mol) for mol in mol_list])

# SA计算2：从 SMILES 列表计算 SA 分数
def compute_sa_from_smiles(smiles_list):
    sa_scores = []
    for i, smi in enumerate(smiles_list):
        mol = smiles_to_mol(smi)
        # 如果分子有效，计算 SA 分数；如果无效，赋值为 0
        # 注意：SA分数通常>=1，这里赋值0作为异常值的占位符
        sa = sascorer.calculateScore(mol) if mol else 0
        
        if mol is None:
            print(f"Invalid SMILES at index {i}")
            
        sa_scores.append(sa)
    return np.array(sa_scores)