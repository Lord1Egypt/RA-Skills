#!/usr/bin/env python3
"""
数据质量检查脚本
Supports: SQLite, MySQL, PostgreSQL
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse


# ============ 安全验证 ============

def validate_table_name(table_name: str) -> bool:
    """验证表名，防止 SQL 注入"""
    # 只允许字母、数字、下划线，且以字母或下划线开头
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    if not re.match(pattern, table_name):
        print(f"❌ 错误：表名 '{table_name}' 包含非法字符", file=sys.stderr)
        print("表名只能包含字母、数字和下划线，且不能以数字开头", file=sys.stderr)
        return False
    return True


def get_connection_from_env(db_type: str) -> Optional[Any]:
    """从环境变量获取数据库连接（安全方式）"""
    if db_type == 'mysql':
        import pymysql
        return pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', ''),
            password=os.getenv('DB_PASS', ''),
            database=os.getenv('DB_NAME', ''),
            cursorclass=pymysql.cursors.DictCursor
        )
    elif db_type in ('postgresql', 'postgres'):
        import psycopg2
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 5432)),
            user=os.getenv('DB_USER', ''),
            password=os.getenv('DB_PASS', ''),
            database=os.getenv('DB_NAME', '')
        )
    elif db_type == 'sqlite':
        import sqlite3
        db_path = os.getenv('DB_PATH', 'data.db')
        return sqlite3.connect(db_path)
    return None


# ============ 连接解析 ============

def parse_connection_string(conn_str: str) -> Dict[str, str]:
    """解析数据库连接字符串"""
    if conn_str.startswith('sqlite'):
        return {'type': 'sqlite', 'path': conn_str.replace('sqlite:///', '')}
    
    parsed = urlparse(conn_str)
    return {
        'type': parsed.scheme,
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or (3306 if parsed.scheme == 'mysql' else 5432),
        'user': parsed.username or 'root',
        'password': parsed.password or '',
        'database': parsed.path.lstrip('/') if parsed.path else ''
    }


def get_connection(conn_str: str):
    """获取数据库连接"""
    config = parse_connection_string(conn_str)
    
    if config['type'] == 'sqlite':
        import sqlite3
        return sqlite3.connect(config['path'])
    
    elif config['type'] in ('mysql', 'mysql+pymysql'):
        import pymysql
        return pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            cursorclass=pymysql.cursors.DictCursor
        )
    
    elif config['type'] in ('postgresql', 'postgres'):
        import psycopg2
        return psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
    
    else:
        raise ValueError(f"Unsupported database: {config['type']}")


# ============ 数据质量检查 ============

def get_table_data(conn, table_name: str, limit: int = 10000) -> List[Dict]:
    """获取表数据（使用参数化查询）"""
    cursor = conn.cursor()
    
    try:
        # 使用参数化查询（虽然 LIMIT 不是用户输入，但这是好习惯）
        cursor.execute(f"SELECT * FROM {table_name} LIMIT ?", (limit,))
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        cursor.close()


def get_table_schema(conn, table_name: str) -> List[Dict]:
    """获取表结构"""
    cursor = conn.cursor()
    
    try:
        import pymysql
        if isinstance(conn, pymysql.Connection):
            cursor.execute(f"DESCRIBE `{table_name}`")
            return cursor.fetchall()
    except:
        pass
    
    try:
        cursor.execute(f"PRAGMA table_info(`{table_name}`)")
        return cursor.fetchall()
    except:
        pass
    
    return []


def check_data_quality(conn, table_name: str) -> Dict[str, Any]:
    """检查数据质量"""
    schema = get_table_schema(conn, table_name)
    data = get_table_data(conn, table_name)
    
    issues = []
    
    # 检查缺失值
    for field in schema:
        if isinstance(field, dict):
            field_name = field.get('name', field.get('Field', ''))
            null_count = sum(1 for row in data if row.get(field_name) is None)
            if null_count > 0:
                null_ratio = null_count / len(data) if data else 0
                if null_ratio > 0.1:
                    issues.append(f"字段 {field_name} 缺失率 {null_ratio:.1%}")
    
    # 检查重复
    if data:
        try:
            first_field = list(data[0].keys())[0]
            values = [row.get(first_field) for row in data]
            from collections import Counter
            duplicates = [k for k, v in Counter(values).items() if v > 1]
            if duplicates:
                issues.append(f"字段 {first_field} 存在 {len(duplicates)} 条重复")
        except:
            pass
    
    completeness = 1 - (len([i for i in issues if '缺失' in i]) / len(schema) if schema else 0)
    
    return {
        'total_records': len(data),
        'issues': issues,
        'completeness': completeness,
        'schema_fields': len(schema)
    }


# ============ 主程序 ============

def main():
    parser = argparse.ArgumentParser(description='数据质量检查')
    parser.add_argument('--table', required=True, help='表名')
    parser.add_argument('--db-type', required=True, choices=['sqlite', 'mysql', 'postgresql'], 
                       help='数据库类型（必须指定）')
    parser.add_argument('--limit', type=int, default=10000, help='最大记录数')
    
    args = parser.parse_args()
    
    # 验证表名
    if not validate_table_name(args.table):
        sys.exit(1)
    
    # 获取连接 - 仅从环境变量
    conn = None
    try:
        conn = get_connection_from_env(args.db_type)
        if not conn:
            print("❌ 请设置环境变量: DB_HOST, DB_USER, DB_PASS, DB_NAME", file=sys.stderr)
            print("SQLite 需要: DB_PATH", file=sys.stderr)
            sys.exit(1)
        
        print(f"✅ 已连接到数据库")
        
        # 检查质量
        result = check_data_quality(conn, args.table)
        
        print(f"\n📊 数据质量报告 - {args.table}")
        print(f"  总记录数: {result['total_records']}")
        print(f"  字段数量: {result['schema_fields']}")
        print(f"  完整性: {result['completeness']:.1%}")
        
        if result['issues']:
            print(f"\n⚠️ 发现问题:")
            for issue in result['issues']:
                print(f"  - {issue}")
        else:
            print(f"\n✅ 未发现问题")
        
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请安装: pip install pymysql psycopg2-binary")
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
