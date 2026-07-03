"""
矩阵运算模块

从原始实现提取的通用矩阵操作。
"""
import numpy as np


def matrix_multiply(matrix_a, matrix_b):
    """
    通用矩阵乘法。
    
    优化策略：转置矩阵B后计算点积，避免重复索引列。
    
    Parameters
    ----------
    matrix_a : list[list] or np.ndarray
    matrix_b : list[list] or np.ndarray
    
    Returns
    -------
    list[list]
    """
    a = np.array(matrix_a, dtype=float)
    b = np.array(matrix_b, dtype=float)
    
    if a.shape[1] != b.shape[0]:
        raise ValueError(
            f"矩阵A的列数({a.shape[1]})与矩阵B的行数({b.shape[0]})不相等，无法相乘"
        )
    
    # 转置B使列变行
    b_t = b.T
    
    return [[sum(ai * bj for ai, bj in zip(row_a, col_b)) for col_b in b_t] for row_a in a]


def matrix_inverse(matrix):
    """
    高斯-约旦消元法求方阵逆矩阵。
    
    Parameters
    ----------
    matrix : list[list] or np.ndarray
    
    Returns
    -------
    list[list]
    """
    mat = np.array(matrix, dtype=float)
    n = mat.shape[0]
    
    if mat.shape[0] != mat.shape[1]:
        raise ValueError("必须为方阵")
    
    # 构造增广矩阵 [A|I]
    aug = np.hstack([mat, np.eye(n)])
    
    for col in range(n):
        # 选主元
        max_row = col + np.argmax(np.abs(aug[col:, col]))
        if np.abs(aug[max_row, col]) < 1e-10:
            raise ValueError("矩阵不可逆")
        
        # 交换行
        aug[[col, max_row]] = aug[[max_row, col]]
        
        # 归一化主元行
        pivot = aug[col, col]
        aug[col] = aug[col] / pivot
        
        # 消去其他行
        for r in range(n):
            if r != col:
                factor = aug[r, col]
                aug[r] = aug[r] - factor * aug[col]
    
    return aug[:, n:].tolist()
