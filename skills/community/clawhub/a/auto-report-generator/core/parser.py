"""数据解析模块 - 支持 CSV/Excel 文件加载与统计分析"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_csv(path: str) -> pd.DataFrame:
    """加载 CSV 文件

    Args:
        path: CSV 文件路径

    Returns:
        pd.DataFrame: 加载的数据框
    """
    try:
        df = pd.read_csv(path, encoding='utf-8-sig')
        return df
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding='gbk')
        return df
    except Exception as e:
        raise ValueError(f"无法加载 CSV 文件 {path}: {str(e)}")


def load_excel(path: str, sheet: str = None) -> pd.DataFrame:
    """加载 Excel 文件

    Args:
        path: Excel 文件路径
        sheet: 工作表名称或索引，默认为 None（读取第一个工作表）

    Returns:
        pd.DataFrame: 加载的数据框
    """
    try:
        if sheet is None:
            df = pd.read_excel(path, engine='openpyxl')
        else:
            df = pd.read_excel(path, sheet_name=sheet, engine='openpyxl')
        return df
    except Exception as e:
        raise ValueError(f"无法加载 Excel 文件 {path}: {str(e)}")


def get_stats(df: pd.DataFrame) -> dict:
    """获取数据框的统计摘要

    Args:
        df: 数据框

    Returns:
        dict: 包含以下键的统计字典
            - row_count: 行数
            - col_count: 列数
            - means: 各列均值
            - medians: 各列中位数
            - mins: 各列最小值
            - maxs: 各列最大值
            - missing_values: 各列缺失值数量
    """
    numeric_df = df.select_dtypes(include=[np.number])

    stats = {
        'row_count': len(df),
        'col_count': len(df.columns),
        'means': numeric_df.mean().to_dict(),
        'medians': numeric_df.median().to_dict(),
        'mins': numeric_df.min().to_dict(),
        'maxs': numeric_df.max().to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'column_types': df.dtypes.astype(str).to_dict(),
    }

    return stats


def detect_anomalies(df: pd.DataFrame, column: str) -> dict:
    """检测指定列的异常值（基于 IQR 方法）

    Args:
        df: 数据框
        column: 列名

    Returns:
        dict: 异常值检测结果
            - count: 异常值数量
            - indices: 异常值所在行索引
            - lower_bound: 下界
            - upper_bound: 上界
            - method: 检测方法
    """
    if column not in df.columns:
        raise ValueError(f"列 '{column}' 不存在于数据框中")

    series = df[column].dropna()

    if not pd.api.types.is_numeric_dtype(series):
        raise TypeError(f"列 '{column}' 不是数值类型，无法进行异常值检测")

    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    anomalies_mask = (series < lower_bound) | (series > upper_bound)
    anomaly_indices = series[anomalies_mask].index.tolist()

    return {
        'count': int(anomalies_mask.sum()),
        'indices': anomaly_indices,
        'lower_bound': float(lower_bound),
        'upper_bound': float(upper_bound),
        'method': 'IQR (1.5x)',
        'column': column,
    }


def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """计算数值列之间的相关系数矩阵

    Args:
        df: 数据框

    Returns:
        pd.DataFrame: 相关系数矩阵
    """
    numeric_df = df.select_dtypes(include=[np.number])
    return numeric_df.corr()


def sample_data(df: pd.DataFrame, n: int = 5, random: bool = True) -> pd.DataFrame:
    """随机抽样数据

    Args:
        df: 数据框
        n: 抽样数量
        random: 是否随机抽样

    Returns:
        pd.DataFrame: 抽样后的数据框
    """
    if random:
        return df.sample(n=min(n, len(df)))
    else:
        return df.head(n)
