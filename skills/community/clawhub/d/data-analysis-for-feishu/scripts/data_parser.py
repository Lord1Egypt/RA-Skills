#!/usr/bin/env python3
"""
通用数据解析工具，支持Excel、飞书多维表格、飞书电子表格数据解析
"""
import pandas as pd
import json
from typing import List, Dict, Any

def parse_excel(file_path: str, sheet_name: str = None) -> List[Dict[str, Any]]:
    """解析Excel文件，返回字典列表格式的数据"""
    if sheet_name:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        df = pd.read_excel(file_path)
    # 转换为字典列表，处理NaN值
    data = df.where(pd.notnull(df), None).to_dict('records')
    return data

def parse_csv(file_path: str) -> List[Dict[str, Any]]:
    """解析CSV文件，返回字典列表格式的数据"""
    df = pd.read_csv(file_path)
    data = df.where(pd.notnull(df), None).to_dict('records')
    return data

def parse_bitable_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """解析飞书多维表格的records数据，返回标准字典列表"""
    result = []
    for record in records:
        fields = record.get('fields', {})
        # 处理多维表格特殊字段类型
        parsed_fields = {}
        for key, value in fields.items():
            # 人员类型字段，提取名字
            if isinstance(value, list) and len(value) > 0 and 'name' in value[0]:
                parsed_fields[key] = ','.join([item['name'] for item in value])
            # 多选类型字段
            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], str):
                parsed_fields[key] = ','.join(value)
            # 其他类型直接返回
            else:
                parsed_fields[key] = value
        result.append(parsed_fields)
    return result

def parse_sheet_data(values: List[List[Any]]) -> List[Dict[str, Any]]:
    """解析飞书电子表格的values数据，返回标准字典列表"""
    if not values or len(values) < 2:
        return []
    # 第一行为表头
    headers = values[0]
    result = []
    for row in values[1:]:
        item = {}
        for i, header in enumerate(headers):
            if i < len(row):
                item[header] = row[i] if row[i] != '' else None
            else:
                item[header] = None
        result.append(item)
    return result

def extract_column(data: List[Dict[str, Any]], column_name: str) -> List[Any]:
    """从数据中提取指定列的数据，自动过滤空值"""
    column_data = [item.get(column_name) for item in data if item.get(column_name) is not None]
    return column_data

def get_column_names(data: List[Dict[str, Any]]) -> List[str]:
    """获取数据的所有列名"""
    if not data:
        return []
    return list(data[0].keys())

def save_to_json(data: List[Dict[str, Any]], output_path: str):
    """保存数据到JSON文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"数据已保存到：{output_path}")

if __name__ == "__main__":
    # 测试用例
    import argparse
    parser = argparse.ArgumentParser(description="数据解析工具")
    parser.add_argument("--excel", help="Excel文件路径")
    parser.add_argument("--sheet", help="工作表名称")
    parser.add_argument("--output", help="输出JSON文件路径")
    args = parser.parse_args()
    
    if args.excel:
        data = parse_excel(args.excel, args.sheet)
        print(f"解析到{len(data)}条数据")
        print("列名：", get_column_names(data))
        if args.output:
            save_to_json(data, args.output)
