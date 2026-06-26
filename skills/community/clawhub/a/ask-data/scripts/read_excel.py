#!/usr/bin/env python3
"""
读取Excel文件，返回结构信息
用法: python read_excel.py <文件路径>
输出: JSON格式，包含sheet列表、列名、样本数据
"""

import sys
import json
import pandas as pd
from pathlib import Path


def infer_dtype(series):
    """推断数据类型"""
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    elif pd.api.types.is_numeric_dtype(series):
        return "numeric"
    else:
        return "text"


def read_excel_structure(file_path):
    """读取Excel文件结构信息"""
    path = Path(file_path)
    
    if not path.exists():
        return {"error": f"文件不存在: {file_path}"}
    
    if not path.suffix.lower() in ['.xlsx', '.xls', '.xlsm']:
        return {"error": f"不支持的文件格式: {path.suffix}"}
    
    try:
        # 读取所有sheet
        xl = pd.ExcelFile(file_path)
        sheets = []
        
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=100)
            
            # 清理数据
            df = df.dropna(how='all')  # 删除全空行
            df.columns = df.columns.astype(str).str.strip()  # 清理列名
            
            sheet_info = {
                "name": sheet_name,
                "columns": [
                    {
                        "name": col,
                        "dtype": infer_dtype(df[col]),
                        "sample": str(df[col].dropna().iloc[0]) if not df[col].dropna().empty else None
                    }
                    for col in df.columns
                ],
                "row_count": len(df),
                "sample_data": df.head(5).to_dict(orient='records')
            }
            sheets.append(sheet_info)
        
        return {
            "file": str(path.absolute()),
            "sheets": sheets,
            "total_sheets": len(sheets)
        }
        
    except Exception as e:
        return {"error": f"读取失败: {str(e)}"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "请提供文件路径"}, ensure_ascii=False))
        sys.exit(1)
    
    result = read_excel_structure(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, default=str))
