#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用数据库知识库转换脚本

将导出的表结构文件（SQL/CSV/JSON）转换为知识库文件：
- tables.json: 表结构信息
- field_mapping.json: 字段映射和枚举值

用法:
    # 只转换表结构（单个文件）
    python3 convert_knowledge.py --input structure.sql
    
    # 转换表结构并生成字段映射（单个文件）
    python3 convert_knowledge.py --input structure.sql --mapping
    
    # 同时导入字典数据（单个文件）
    python3 convert_knowledge.py --input structure.sql --mapping --dict dict.csv
    
    # 强制覆盖
    python3 convert_knowledge.py --input structure.sql --mapping --force
    
    # 合并多个文件
    python3 convert_knowledge.py --inputs file1.sql file2.sql --mapping --force
"""

import os
import sys
import json
import re
import argparse
import csv
from io import StringIO
from datetime import datetime
from typing import Dict, Any, Optional

# 默认输出路径
# 获取脚本所在目录，支持作为模块导入时的路径计算
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 计算项目根目录（scripts/knowledge/ 的上两级）
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
DEFAULT_TABLES_FILE = os.path.join(PROJECT_ROOT, 'knowledge', 'dm', 'tables.json')
DEFAULT_MAPPING_FILE = os.path.join(PROJECT_ROOT, 'knowledge', 'dm', 'field_mapping.json')

# 模块映射
MODULE_MAPPING = {
    "wsd_sys": {"name": "系统管理", "code": "sys"},
    "wsd_plan": {"name": "计划管理", "code": "plan"},
    "wsd_wf": {"name": "工作流", "code": "wf"},
    "wsd_doc": {"name": "文档管理", "code": "doc"},
    "wsd_risk": {"name": "风险管理", "code": "risk"},
    "wsd_comu": {"name": "沟通交流", "code": "comu"},
    "wsd_dashboard": {"name": "仪表盘", "code": "dashboard"},
    "wsd_cntc": {"name": "联系人", "code": "cntc"},
    "wsd_rsrc": {"name": "资源管理", "code": "rsrc"},
    "wsd_base": {"name": "基础数据", "code": "base"},
    "wsd_adp": {"name": "敏捷开发", "code": "adp"},
    "wsd_cost": {"name": "成本管理", "code": "cost"},
    "wsd_ipd": {"name": "IPD管理", "code": "ipd"},
}


def get_table_module(table_name: str) -> str:
    """获取表所属模块"""
    t = table_name.lower()
    for prefix, info in MODULE_MAPPING.items():
        if t.startswith(prefix.lower()):
            return info["code"]
    return "other"


def parse_sql_script(sql_content: str) -> Dict[str, Any]:
    """解析 SQL 脚本，提取表结构"""
    tables = {}
    primary_keys = {}  # 存储每个表的主键字段
    
    # 匹配 CREATE TABLE 语句（支持多行，支持带schema的表名和STORAGE子句）
    create_table_pattern = re.compile(
        r'CREATE\s+TABLE\s+(?:"?[\w_]+"?\.)?"?([\w_]+)"?\s*\((.*?)\)\s*(?:STORAGE\([^)]*\))?\s*;',
        re.DOTALL | re.IGNORECASE
    )
    
    # 匹配字段定义（支持 COMMENT 'xxx'）
    column_pattern = re.compile(
        r'^\s*"?([\w_]+)"?\s+([\w\(\)]+(?:\s+\w+)*)\s*(?:NULL|NOT\s+NULL)?\s*(?:DEFAULT\s+[^,\n]+)?\s*(?:COMMENT\s+[\'"]([^\'"]*)[\'"])?\s*,?$',
        re.IGNORECASE | re.MULTILINE
    )
    
    # 匹配主键约束（支持两种格式）
    # 格式1: CONSTRAINT xxx PRIMARY KEY (col)
    # 格式2: PRIMARY KEY (col)
    pk_pattern = re.compile(
        r'(?:CONSTRAINT\s+\w+\s+)?PRIMARY\s+KEY\s*\(\s*"?([\w_]+)"?\s*\)',
        re.IGNORECASE
    )
    
    # 匹配表注释（支持带schema的表名）
    table_comment_pattern = re.compile(
        r'COMMENT\s+ON\s+TABLE\s+(?:"?[\w_]+"?\.)?"?([\w_]+)"?\s+IS\s+[\'"]([^\'"]*)[\'"]',
        re.IGNORECASE
    )
    
    # 第一步：提取所有表结构和字段
    for match in create_table_pattern.finditer(sql_content):
        table_name = match.group(1)
        columns_str = match.group(2)
        
        tables[table_name] = {
            "name": table_name,
            "comment": "",
            "module": get_table_module(table_name),
            "columns": []
        }
        
        # 提取主键
        pk_match = pk_pattern.search(columns_str)
        if pk_match:
            primary_keys[table_name] = pk_match.group(1)
        
        # 提取字段（按行分割处理）
        for line in columns_str.split('\n'):
            line = line.strip()
            # 跳过约束定义行
            if not line or line.upper().startswith('CONSTRAINT') or line.upper().startswith('PRIMARY'):
                continue
            # 跳过结尾的括号
            if line == ')':
                continue
                
            col_match = column_pattern.match(line)
            if col_match:
                column_name = col_match.group(1)
                column_type = col_match.group(2).strip()
                comment = col_match.group(3) if col_match.group(3) else ""
                
                # 判断是否为主键
                is_pk = primary_keys.get(table_name) == column_name
                
                # 判断是否为 NULL
                nullable = "NO" if "NOT NULL" in line.upper() else "YES"
                
                # 提取 DEFAULT
                default_match = re.search(r'DEFAULT\s+([^,\s]+)', line, re.IGNORECASE)
                default = default_match.group(1) if default_match else None
                
                tables[table_name]["columns"].append({
                    "name": column_name,
                    "type": column_type,
                    "comment": comment,
                    "nullable": nullable,
                    "key": "PRI" if is_pk else "",
                    "default": default,
                    "extra": "auto_increment" if "IDENTITY" in line.upper() else "",
                    "charset": "UTF8" if "VARCHAR" in column_type.upper() or "CHAR" in column_type.upper() else "",
                    "collation": "UTF8_GENERAL_CI" if "VARCHAR" in column_type.upper() or "CHAR" in column_type.upper() else ""
                })
    
    # 第二步：提取表注释
    for match in table_comment_pattern.finditer(sql_content):
        table_name = match.group(1)
        table_comment = match.group(2)
        if table_name in tables:
            tables[table_name]["comment"] = table_comment
    
    return tables


def parse_csv_file(csv_content: str) -> Dict[str, Any]:
    """解析 CSV 文件，提取表结构"""
    tables = {}
    
    reader = csv.DictReader(StringIO(csv_content))
    
    for row in reader:
        table_name = row.get('TABLE_NAME') or row.get('表名')
        if not table_name:
            continue
        
        if table_name not in tables:
            tables[table_name] = {
                "name": table_name,
                "comment": row.get('TABLE_COMMENT') or row.get('表注释') or "",
                "module": get_table_module(table_name),
                "columns": []
            }
        
        column_name = row.get('COLUMN_NAME') or row.get('字段名')
        if column_name:
            tables[table_name]["columns"].append({
                "name": column_name,
                "type": row.get('DATA_TYPE') or row.get('字段类型') or "",
                "comment": row.get('COLUMN_COMMENT') or row.get('字段注释') or "",
                "nullable": "YES" if row.get('NULLABLE') == 'Y' or row.get('是否为空') == '是' else "NO",
                "key": "PRI" if row.get('COLUMN_KEY') == 'PRI' or row.get('是否主键') == '是' else "",
                "default": row.get('DATA_DEFAULT') or row.get('默认值'),
                "extra": "",
                "charset": "UTF8" if "VARCHAR" in (row.get('DATA_TYPE') or row.get('字段类型') or "").upper() else "",
                "collation": "UTF8_GENERAL_CI" if "VARCHAR" in (row.get('DATA_TYPE') or row.get('字段类型') or "").upper() else ""
            })
    
    return tables


def parse_json_file(json_content: str) -> Dict[str, Any]:
    """解析 JSON 文件，提取表结构"""
    data = json.loads(json_content)
    tables = {}
    
    if isinstance(data, dict):
        # 直接是表结构
        tables = data
    elif isinstance(data, list):
        # 是字段列表
        for row in data:
            table_name = row.get('TABLE_NAME') or row.get('表名')
            if not table_name:
                continue
            
            if table_name not in tables:
                tables[table_name] = {
                    "name": table_name,
                    "comment": row.get('TABLE_COMMENT') or row.get('表注释') or "",
                    "module": get_table_module(table_name),
                    "columns": []
                }
            
            column_name = row.get('COLUMN_NAME') or row.get('字段名')
            if column_name:
                tables[table_name]["columns"].append({
                    "name": column_name,
                    "type": row.get('DATA_TYPE') or row.get('字段类型') or "",
                    "comment": row.get('COLUMN_COMMENT') or row.get('字段注释') or "",
                    "nullable": "YES" if row.get('NULLABLE') == 'Y' or row.get('是否为空') == '是' else "NO",
                    "key": "PRI" if row.get('COLUMN_KEY') == 'PRI' or row.get('是否主键') == '是' else "",
                    "default": row.get('DATA_DEFAULT') or row.get('默认值'),
                    "extra": "",
                    "charset": "UTF8" if "VARCHAR" in (row.get('DATA_TYPE') or row.get('字段类型') or "").upper() else "",
                    "collation": "UTF8_GENERAL_CI" if "VARCHAR" in (row.get('DATA_TYPE') or row.get('字段类型') or "").upper() else ""
                })
    
    return tables


def convert_tables(input_file: str, output_file: str) -> Dict[str, Any]:
    """转换表结构文件为知识库格式"""
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 根据文件扩展名选择解析方法
    ext = os.path.splitext(input_file)[1].lower()
    
    if ext in ['.sql']:
        tables = parse_sql_script(content)
    elif ext in ['.csv']:
        tables = parse_csv_file(content)
    elif ext in ['.json']:
        tables = parse_json_file(content)
    else:
        # 尝试自动检测
        if 'CREATE TABLE' in content:
            tables = parse_sql_script(content)
        elif 'TABLE_NAME' in content or '表名' in content:
            tables = parse_csv_file(content)
        else:
            try:
                tables = parse_json_file(content)
            except:
                raise ValueError("无法自动检测文件格式，请指定正确的输入文件")
    
    # 添加元信息
    result = {
        "_comment": "数据库知识库 - 表结构信息",
        "_source": f"从文件转换: {os.path.basename(input_file)}",
        "_updated": datetime.now().strftime("%Y-%m-%d"),
        **tables
    }
    
    # 写入输出文件
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return {
        'success': True,
        'tables_count': len(tables),
        'output_file': output_file
    }


def parse_dict_csv(csv_content: str) -> Dict[str, Dict[str, str]]:
    """解析字典表 CSV 文件"""
    dict_data = {}
    
    reader = csv.DictReader(StringIO(csv_content))
    
    for row in reader:
        type_code = row.get('TYPE_CODE') or row.get('类型编码') or row.get('type_code')
        dict_code = row.get('DICT_CODE') or row.get('字典编码') or row.get('dict_code')
        dict_name = row.get('DICT_NAME') or row.get('字典名称') or row.get('dict_name')
        
        if type_code and dict_code and dict_name:
            if type_code not in dict_data:
                dict_data[type_code] = {}
            dict_data[type_code][str(dict_code)] = dict_name
    
    return dict_data


def parse_dict_sql(sql_content: str) -> Dict[str, Dict[str, str]]:
    """解析字典表 SQL 文件（INSERT 语句）"""
    dict_data = {}
    
    # 匹配 INSERT 语句
    insert_pattern = re.compile(r'INSERT\s+INTO\s+\w+\s*\((.*?)\)\s*VALUES\s*\((.*?)\);', re.DOTALL | re.IGNORECASE)
    
    for match in insert_pattern.finditer(sql_content):
        columns = match.group(1).strip().split(',')
        values = match.group(2).strip().split(',')
        
        # 清理列名和值
        columns = [col.strip().strip('"\'') for col in columns]
        values = [val.strip().strip('"\'') for val in values]
        
        # 构建字典
        row = dict(zip(columns, values))
        
        type_code = row.get('TYPE_CODE') or row.get('type_code')
        dict_code = row.get('DICT_CODE') or row.get('dict_code')
        dict_name = row.get('DICT_NAME') or row.get('dict_name')
        
        if type_code and dict_code and dict_name:
            if type_code not in dict_data:
                dict_data[type_code] = {}
            dict_data[type_code][str(dict_code)] = dict_name
    
    return dict_data


def parse_dict_json(json_content: str) -> Dict[str, Dict[str, str]]:
    """解析字典表 JSON 文件"""
    data = json.loads(json_content)
    dict_data = {}
    
    if isinstance(data, list):
        for row in data:
            type_code = row.get('TYPE_CODE') or row.get('类型编码') or row.get('type_code')
            dict_code = row.get('DICT_CODE') or row.get('字典编码') or row.get('dict_code')
            dict_name = row.get('DICT_NAME') or row.get('字典名称') or row.get('dict_name')
            
            if type_code and dict_code and dict_name:
                if type_code not in dict_data:
                    dict_data[type_code] = {}
                dict_data[type_code][str(dict_code)] = dict_name
    elif isinstance(data, dict):
        # 直接是字典数据
        dict_data = data
    
    return dict_data


def generate_field_mapping(tables_file: str, dict_file: Optional[str], output_file: str) -> Dict[str, Any]:
    """生成 field_mapping.json 文件"""
    # 读取表结构
    with open(tables_file, 'r', encoding='utf-8') as f:
        tables_data = json.load(f)
    
    # 提取字段→中文名映射（支持同一字段名在不同表中的不同注释）
    field_mapping = {}
    for table_name, table_info in tables_data.items():
        if table_name.startswith('_'):
            continue
        if 'columns' in table_info:
            for column in table_info['columns']:
                column_name = column.get('name')
                column_comment = column.get('comment', '')
                if column_name and column_comment:
                    # 使用表名+字段名作为键，避免重复覆盖
                    key = f"{table_name}.{column_name}"
                    field_mapping[key] = column_comment
                    # 同时保留原始字段名映射（如果不冲突）
                    if column_name not in field_mapping:
                        field_mapping[column_name] = column_comment
    
    # 解析字典数据
    dict_data = {}
    if dict_file and os.path.exists(dict_file):
        with open(dict_file, 'r', encoding='utf-8') as f:
            dict_content = f.read()
        
        # 根据文件扩展名选择解析方法
        ext = os.path.splitext(dict_file)[1].lower()
        
        if ext in ['.csv']:
            dict_data = parse_dict_csv(dict_content)
        elif ext in ['.sql']:
            dict_data = parse_dict_sql(dict_content)
        elif ext in ['.json']:
            dict_data = parse_dict_json(dict_content)
        else:
            # 尝试自动检测
            if 'INSERT INTO' in dict_content:
                dict_data = parse_dict_sql(dict_content)
            elif 'TYPE_CODE' in dict_content or '类型编码' in dict_content:
                dict_data = parse_dict_csv(dict_content)
            else:
                try:
                    dict_data = parse_dict_json(dict_content)
                except:
                    print("⚠️  无法自动检测字典文件格式，跳过字典数据")
    
    # 生成结果
    result = {
        "_comment": "数据库知识库 - 字段映射表（中文注释 + 枚举值）",
        "_source": f"从表结构和字典数据生成",
        "_updated": datetime.now().strftime("%Y-%m-%d"),
        "字段→中文名": field_mapping,
        "枚举值映射": dict_data
    }
    
    # 写入输出文件
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return {
        'success': True,
        'field_count': len(field_mapping),
        'enum_count': len(dict_data),
        'output_file': output_file
    }


def merge_tables(all_tables):
    """合并多个文件的表结构，处理表名冲突"""
    merged_tables = {}
    
    for tables in all_tables:
        for table_name, table_info in tables.items():
            if table_name not in merged_tables:
                # 表不存在，直接添加
                merged_tables[table_name] = table_info
            else:
                # 表已存在，比较字段信息完整性
                existing_table = merged_tables[table_name]
                existing_columns = existing_table.get('columns', [])
                new_columns = table_info.get('columns', [])
                
                # 比较字段数量和注释完整性
                existing_comment_count = sum(1 for col in existing_columns if col.get('comment'))
                new_comment_count = sum(1 for col in new_columns if col.get('comment'))
                
                # 如果新表的字段信息更完整，替换现有表
                if len(new_columns) > len(existing_columns) or new_comment_count > existing_comment_count:
                    merged_tables[table_name] = table_info
                    print(f"⚠️  表 {table_name} 存在冲突，使用信息更完整的版本")
    
    return merged_tables

def convert_tables_multi(input_files, output_file):
    """转换多个表结构文件为知识库格式"""
    all_tables = []
    
    for input_file in input_files:
        print(f"🔄 正在解析文件: {input_file}")
        
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 根据文件扩展名选择解析方法
        ext = os.path.splitext(input_file)[1].lower()
        
        if ext in ['.sql']:
            tables = parse_sql_script(content)
        elif ext in ['.csv']:
            tables = parse_csv_file(content)
        elif ext in ['.json']:
            tables = parse_json_file(content)
        else:
            # 尝试自动检测
            if 'CREATE TABLE' in content:
                tables = parse_sql_script(content)
            elif 'TABLE_NAME' in content or '表名' in content:
                tables = parse_csv_file(content)
            else:
                try:
                    tables = parse_json_file(content)
                except:
                    raise ValueError(f"无法自动检测文件格式: {input_file}")
        
        all_tables.append(tables)
        print(f"   解析完成: {len(tables)} 个表")
    
    # 合并表结构
    merged_tables = merge_tables(all_tables)
    
    # 添加元信息
    result = {
        "_comment": "数据库知识库 - 表结构信息",
        "_source": f"从多个文件合并: {', '.join(os.path.basename(f) for f in input_files)}",
        "_updated": datetime.now().strftime("%Y-%m-%d"),
        **merged_tables
    }
    
    # 写入输出文件
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return {
        'success': True,
        'tables_count': len(merged_tables),
        'output_file': output_file
    }

def main():
    parser = argparse.ArgumentParser(
        description='通用数据库知识库转换脚本 - 将表结构文件转换为知识库',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 只转换表结构（单个文件）
  python convert_knowledge.py --input structure.sql
  
  # 转换表结构并生成字段映射（单个文件）
  python convert_knowledge.py --input structure.sql --mapping
  
  # 同时导入字典数据（单个文件）
  python convert_knowledge.py --input structure.sql --mapping --dict dict.csv
  
  # 合并多个文件
  python convert_knowledge.py --inputs file1.sql file2.sql --mapping --force
        """)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--input', '-i', help='输入文件路径 (SQL/CSV/JSON)')
    group.add_argument('--inputs', '-is', nargs='+', help='多个输入文件路径 (SQL/CSV/JSON)')
    parser.add_argument('--mapping', '-m', action='store_true', help='同时生成字段映射')
    parser.add_argument('--dict', '-d', help='字典表数据文件路径 (CSV/SQL/JSON)')
    parser.add_argument('--force', '-f', action='store_true', help='强制覆盖现有文件')
    args = parser.parse_args()
    
    # 检查是否覆盖 tables.json
    if os.path.exists(DEFAULT_TABLES_FILE) and not args.force:
        response = input(f"⚠️  文件 {DEFAULT_TABLES_FILE} 已存在，是否覆盖? (y/N): ")
        if response.lower() != 'y':
            print("已取消操作")
            return
    
    try:
        # 步骤1: 转换表结构
        if args.inputs:
            # 多个文件
            for input_file in args.inputs:
                if not os.path.exists(input_file):
                    print(f"❌ 输入文件不存在: {input_file}")
                    return
            
            print(f"🔄 正在合并表结构: {len(args.inputs)} 个文件")
            result = convert_tables_multi(args.inputs, DEFAULT_TABLES_FILE)
        else:
            # 单个文件
            if not os.path.exists(args.input):
                print(f"❌ 输入文件不存在: {args.input}")
                return
            
            print(f"🔄 正在转换表结构: {args.input}")
            result = convert_tables(args.input, DEFAULT_TABLES_FILE)
        
        if not result['success']:
            print(f"❌ 表结构转换失败")
            return
        
        print(f"✅ 表结构转换完成: {result['tables_count']} 个表")
        print(f"   输出: {result['output_file']}")
        
        # 步骤2: 生成字段映射（如果需要）
        if args.mapping:
            # 检查是否覆盖 field_mapping.json
            if os.path.exists(DEFAULT_MAPPING_FILE) and not args.force:
                response = input(f"⚠️  文件 {DEFAULT_MAPPING_FILE} 已存在，是否覆盖? (y/N): ")
                if response.lower() != 'y':
                    print("跳过字段映射生成")
                    return
            
            print(f"\n🔄 正在生成字段映射...")
            
            result = generate_field_mapping(DEFAULT_TABLES_FILE, args.dict, DEFAULT_MAPPING_FILE)
            if not result['success']:
                print(f"❌ 字段映射生成失败")
                return
            
            print(f"✅ 字段映射生成完成: {result['field_count']} 个字段")
            if result['enum_count'] > 0:
                print(f"   枚举值: {result['enum_count']} 个类型")
            print(f"   输出: {result['output_file']}")
        
        print("\n🎉 转换完成!")
        
    except Exception as e:
        print(f"\n❌ 转换失败: {e}")
        import traceback
        traceback.print_exc()


# 对外接口：供 agent 调用
def convert(input_file: str, generate_mapping: bool = False, dict_file: Optional[str] = None) -> Dict[str, Any]:
    """
    转换表结构为知识库
    
    参数:
        input_file: 输入文件路径 (SQL/CSV/JSON)
        generate_mapping: 是否同时生成字段映射
        dict_file: 字典数据文件路径（可选）
    
    返回:
        {
            'success': True/False,
            'tables_count': 10,
            'field_count': 50,  # 如果生成映射
            'enum_count': 5,    # 如果生成映射
            'message': '...'
        }
    """
    import traceback
    
    if not os.path.exists(input_file):
        return {
            'success': False,
            'message': f'输入文件不存在: {input_file}'
        }
    
    try:
        # 转换表结构
        result = convert_tables(input_file, DEFAULT_TABLES_FILE)
        if not result['success']:
            return result
        
        response = {
            'success': True,
            'tables_count': result['tables_count'],
            'message': f'成功转换 {result["tables_count"]} 个表结构'
        }
        
        # 生成字段映射
        if generate_mapping:
            mapping_result = generate_field_mapping(DEFAULT_TABLES_FILE, dict_file, DEFAULT_MAPPING_FILE)
            if mapping_result['success']:
                response['field_count'] = mapping_result['field_count']
                response['enum_count'] = mapping_result['enum_count']
                response['message'] += f'，生成 {mapping_result["field_count"]} 个字段映射'
                if mapping_result['enum_count'] > 0:
                    response['message'] += f'，{mapping_result["enum_count"]} 个枚举类型'
        
        return response
        
    except Exception as e:
        return {
            'success': False,
            'message': f'转换失败: {str(e)}\n{traceback.format_exc()}'
        }


if __name__ == '__main__':
    main()
