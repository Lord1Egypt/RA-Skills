"""
输入输出工具

功能：
- 文件读写 (CSV, Excel, MAT, HDF5)
- 数据格式转换
- 结果导出
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, Union


def load_csv(path: Path) -> pd.DataFrame:
    """加载 CSV 文件"""
    return pd.read_csv(path)


def load_excel(path: Path, sheet_name: Optional[str] = None) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """加载 Excel 文件"""
    if sheet_name:
        return pd.read_excel(path, sheet_name=sheet_name)
    return pd.read_excel(path, sheet_name=None)


def load_mat(path: Path) -> Dict[str, Any]:
    """加载 MATLAB .mat 文件"""
    try:
        import scipy.io as sio
        return sio.loadmat(path)
    except ImportError:
        raise ImportError("请安装 scipy: pip install scipy")


def load_hdf5(path: Path) -> Dict[str, Any]:
    """加载 HDF5 文件"""
    try:
        import h5py
        data = {}
        with h5py.File(path, 'r') as f:
            for key in f.keys():
                data[key] = np.array(f[key])
        return data
    except ImportError:
        raise ImportError("请安装 h5py: pip install h5py")


def save_csv(data: Union[pd.DataFrame, np.ndarray], path: Path):
    """保存为 CSV 文件"""
    if isinstance(data, np.ndarray):
        data = pd.DataFrame(data)
    data.to_csv(path, index=False)


def save_json(data: Dict[str, Any], path: Path, indent: int = 2):
    """保存为 JSON 文件"""
    import json
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def save_mat(data: Dict[str, Any], path: Path):
    """保存为 MATLAB .mat 文件"""
    try:
        import scipy.io as sio
        sio.savemat(path, data)
    except ImportError:
        raise ImportError("请安装 scipy: pip install scipy")
