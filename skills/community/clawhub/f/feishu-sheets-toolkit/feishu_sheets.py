#!/usr/bin/env python3
"""
Feishu Sheets 操作工具
飞书在线表格 (Sheets) 操作: 创建/读取/写入/追加/管理
注意: 这是操作在线电子表格,不是多维表格(Bitable)
"""

import os
import json
import re
from typing import Union, List, Dict, Any, Optional, Tuple


class FeishuSheets:
    """飞书表格操作类"""
    
    def __init__(self, spreadsheet_token: str = None):
        self.spreadsheet_token = spreadsheet_token
        self.sheet_id = None
        
    # ============== Token提取 ==============
    @staticmethod
    def extract_token(url: str) -> str:
        """从URL提取spreadsheet_token"""
        # 例如: https://xxx.feishu.cn/sheets/shtABC123 -> shtABC123
        match = re.search(r'sheets/([a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
        return url
    
    @staticmethod
    def extract_sheet_id(url: str) -> str:
        """从URL提取sheet_id"""
        # 例如: ?sheet=0bxxxx -> 0bxxxx
        match = re.search(r'sheet=([a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
        return None
    
    # ============== 数据转换 ==============
    @staticmethod
    def prepare_values(data: Union[List, Dict]) -> List[List]:
        """准备写入的数据格式"""
        if isinstance(data, dict):
            # 字典转为单行
            return [list(data.values())]
        return data
    
    @staticmethod
    def parse_range(range_str: str, sheet_id: str = None) -> str:
        """解析区域格式"""
        if sheet_id and '!' not in range_str:
            return f'{sheet_id}!{range_str}'
        elif '!' in range_str:
            return range_str
        else:
            return f'{range_str}'
    
    # ============== 构建请求 ==============
    def build_create_request(self, title: str, folder_token: str = None) -> dict:
        """构建创建表格请求"""
        req = {"action": "create", "title": title}
        if folder_token:
            req["folder_token"] = folder_token
        return req
    
    def build_write_request(self, spreadsheet_token: str, sheet_id: str,
                          range_str: str, values: List[List]) -> dict:
        """构建写入请求"""
        return {
            "action": "write",
            "spreadsheet_token": spreadsheet_token,
            "sheet_id": sheet_id,
            "range": range_str,
            "values": values
        }
    
    def build_read_request(self, spreadsheet_token: str, sheet_id: str,
                          range_str: str) -> dict:
        """构建读取请求"""
        return {
            "action": "read",
            "spreadsheet_token": spreadsheet_token,
            "sheet_id": sheet_id,
            "range": range_str
        }
    
    def build_append_request(self, spreadsheet_token: str, sheet_id: str,
                           values: List[List]) -> dict:
        """构建追加请求"""
        return {
            "action": "append",
            "spreadsheet_token": spreadsheet_token,
            "sheet_id": sheet_id,
            "values": values
        }
    
    def build_get_info_request(self, spreadsheet_token: str) -> dict:
        """构建获取信息请求"""
        return {"action": "get_info", "spreadsheet_token": spreadsheet_token}
    
    def build_add_sheet_request(self, spreadsheet_token: str, title: str) -> dict:
        """构建添加Sheet请求"""
        return {
            "action": "add_sheet",
            "spreadsheet_token": spreadsheet_token,
            "title": title
        }
    
    def build_delete_sheet_request(self, spreadsheet_token: str, sheet_id: str) -> dict:
        """构建删除Sheet请求"""
        return {
            "action": "delete_sheet",
            "spreadsheet_token": spreadsheet_token,
            "sheet_id": sheet_id
        }
    
    def build_insert_dimension_request(self, spreadsheet_token: str, sheet_id: str,
                                      dimension: str, start_index: int, 
                                      end_index: int = None) -> dict:
        """构建插入行/列请求"""
        if end_index is None:
            end_index = start_index + 1
            
        return {
            "action": "insert_dimension",
            "spreadsheet_token": spreadsheet_token,
            "sheet_id": sheet_id,
            "dimension": dimension,  # ROWS 或 COLS
            "start_index": start_index,
            "end_index": end_index
        }
    
    def build_delete_dimension_request(self, spreadsheet_token: str, sheet_id: str,
                                      dimension: str, start_index: int,
                                      end_index: int = None) -> dict:
        """构建删除行/列请求"""
        if end_index is None:
            end_index = start_index + 1
            
        return {
            "action": "delete_dimension",
            "spreadsheet_token": spreadsheet_token,
            "sheet_id": sheet_id,
            "dimension": dimension,
            "start_index": start_index,
            "end_index": end_index
        }
    
    # ============== 数据类型 ==============
    @staticmethod
    def make_formula(text: str) -> dict:
        """创建公式类型"""
        return {"type": "formula", "text": text}
    
    @staticmethod
    def make_link(text: str, url: str) -> dict:
        """创建链接类型"""
        return {"type": "url", "text": text, "link": url}
    
    # ============== 便捷方法 ==============
    def write_single_value(self, spreadsheet_token: str, sheet_id: str,
                          row: int, col: int, value: Any) -> dict:
        """写入单个值"""
        cell = f'{get_column_letter(col)}{row}'
        range_str = f'{sheet_id}!{cell}:{cell}'
        
        # 转换值为列表格式
        values = [[value]]
        
        return self.build_write_request(spreadsheet_token, sheet_id, range_str, values)


# ============== 辅助函数 ==============
def get_column_letter(col_idx: int) -> str:
    """列索引转字母"""
    result = ""
    while col_idx > 0:
        col_idx -= 1
        result = chr(65 + col_idx % 26) + result
        col_idx //= 26
    return result


def parse_cell(cell: str) -> Tuple[int, int]:
    """解析单元格坐标"""
    import re
    match = re.match(r'([A-Z]+)(\d+)', cell.upper())
    if match:
        col = column_index_from_string(match.group(1))
        row = int(match.group(2))
        return row, col
    return 1, 1


def column_index_from_string(col_str: str) -> int:
    """字母转列索引"""
    result = 0
    for c in col_str.upper():
        result = result * 26 + (ord(c) - 64)
    return result


# ============== 与DataParser集成 ==============
def import_from_dataframe(df, spreadsheet_token: str = None) -> List[Dict]:
    """从DataFrame导入数据"""
    data = df.values.tolist()
    headers = df.columns.tolist()
    
    # 添加表头
    result = [headers] + data
    
    return result


# ============== 测试 ==============
if __name__ == '__main__':
    print('Feishu Sheets toolkit loaded')
    
    # 测试Token提取
    url = 'https://xxx.feishu.cn/sheets/shtABC123?sheet=0bxxxx'
    token = FeishuSheets.extract_token(url)
    sheet_id = FeishuSheets.extract_sheet_id(url)
    print(f'Token: {token}, Sheet ID: {sheet_id}')
    
    # 测试请求构建
    fs = FeishuSheets()
    
    # 创建
    req = fs.build_create_request('Test Sheet')
    print(f'Create: {req}')
    
    # 写入
    req = fs.build_write_request('shtABC', '0bxxxx', 'A1:C3', [['a','b','c'],[1,2,3]])
    print(f'Write: {req}')
    
    # 追加
    req = fs.build_append_request('shtABC', '0bxxxx', [['d',4,5]])
    print(f'Append: {req}')