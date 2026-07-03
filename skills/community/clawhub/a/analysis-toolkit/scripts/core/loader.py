"""
数据加载与验证模块
"""
import pandas as pd
import numpy as np


def load_data(path, date_col=None, date_format=None):
    """
    通用数据加载，自动识别格式。
    
    Parameters
    ----------
    path : str
        文件路径 (.xlsx 或 .csv)
    date_col : str, optional
        需解析的日期列名
    date_format : str, optional
        显式日期格式，不指定则自动推断
    
    Returns
    -------
    pd.DataFrame
    """
    if path.endswith('.xlsx'):
        df = pd.read_excel(path, engine='openpyxl')
    elif path.endswith('.csv'):
        # 尝试常见中文编码
        for enc in ['utf-8', 'gb18030', 'gbk', 'latin-1']:
            try:
                df = pd.read_csv(path, encoding=enc)
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        else:
            raise ValueError("无法识别CSV文件编码，请手动指定")
    else:
        raise ValueError(f"不支持的文件格式: {path}")
    
    # 解析日期列
    if date_col and date_col in df.columns:
        try:
            if date_format:
                df[date_col] = pd.to_datetime(df[date_col], format=date_format)
            else:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        except Exception:
            # 处理Excel数值日期
            if np.issubdtype(df[date_col].dtype, np.number):
                df[date_col] = (pd.to_datetime('1899-12-30') + 
                                pd.to_timedelta(df[date_col].astype(int), unit='D') +
                                pd.Timedelta(days=1))  # 修正1900闰年
            else:
                raise
    
    return df


def validate_data(df, required_columns=None):
    """
    通用数据验证。
    
    Parameters
    ----------
    df : pd.DataFrame
    required_columns : set, optional
        必需的列名集合
    
    Returns
    -------
    dict
        {"valid": bool, "missing": list, "errors": list}
    """
    result = {"valid": True, "missing": [], "errors": [], "info": {}}
    
    # 检查空数据
    if df is None or df.empty:
        result["valid"] = False
        result["errors"].append("数据为空")
        return result
    
    # 检查必需列
    if required_columns:
        missing = required_columns - set(df.columns)
        if missing:
            result["valid"] = False
            result["missing"] = list(missing)
            result["errors"].append(f"缺失字段: {', '.join(missing)}")
    
    # 统计信息
    result["info"] = {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": {col: str(dt) for col, dt in df.dtypes.items()},
    }
    
    return result
