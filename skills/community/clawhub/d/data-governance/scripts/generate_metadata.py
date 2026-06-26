#!/usr/bin/env python3
"""
元数据生成脚本
支持 SQLite, MySQL, PostgreSQL
"""

import sys
import re
import argparse
import json
from typing import Dict, List, Any
from urllib.parse import urlparse


def validate_table_name(table_name: str) -> bool:
    """验证表名，防止 SQL 注入"""
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    if not re.match(pattern, table_name):
        print(f"Error: Invalid table name: {table_name}", file=sys.stderr)
        return False
    return True


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


def get_table_schema(conn, table_name: str) -> List[Dict]:
    """获取表结构"""
    cursor = conn.cursor()
    schema = []
    
    try:
        cursor.execute(f'PRAGMA table_info(`{table_name}`)')
        for row in cursor.fetchall():
            schema.append({
                'name': row[1],
                'type': row[2],
            })
    except:
        pass
    
    if not schema:
        try:
            cursor.execute(f'DESCRIBE `{table_name}`')
            for row in cursor.fetchall():
                schema.append({
                    'name': row['Field'],
                    'type': row['Type'],
                })
        except:
            pass
    
    cursor.close()
    return schema


def get_indexes(conn, table_name: str) -> List[Dict]:
    """获取索引信息"""
    cursor = conn.cursor()
    indexes = []
    
    try:
        cursor.execute(f"PRAGMA index_list(`{table_name}`)")
        for row in cursor.fetchall():
            indexes.append({
                'name': row[1],
                'unique': bool(row[2])
            })
    except:
        pass
    
    cursor.close()
    return indexes


def get_foreign_keys(conn, table_name: str) -> List[Dict]:
    """获取外键信息"""
    cursor = conn.cursor()
    fks = []
    
    try:
        cursor.execute(f"PRAGMA foreign_key_list(`{table_name}`)")
        for row in cursor.fetchall():
            fks.append({
                'from': row[3],
                'to': row[2],
                'table': row[2]
            })
    except:
        pass
    
    cursor.close()
    return fks


def generate_metadata(conn, table_name: str) -> Dict[str, Any]:
    """生成元数据"""
    schema = get_table_schema(conn, table_name)
    indexes = get_indexes(conn, table_name)
    foreign_keys = get_foreign_keys(conn, table_name)
    
    return {
        'table_name': table_name,
        'column_count': len(schema),
        'columns': schema,
        'indexes': indexes,
        'foreign_keys': foreign_keys
    }


def generate_data_dict(metadata: Dict) -> str:
    """生成 Markdown 数据字典"""
    md = f"# {metadata['table_name']}\n\n"
    md += f"字段数: {metadata['column_count']}\n\n"
    md += "## 字段\n\n"
    md += "| 字段名 | 类型 |\n"
    md += "|--------|------|\n"
    
    for col in metadata.get('columns', []):
        md += f"| {col['name']} | {col['type']} |\n"
    
    if metadata.get('indexes'):
        md += "\n## 索引\n\n"
        for idx in metadata['indexes']:
            md += f"- {idx['name']} {'(UNIQUE)' if idx.get('unique') else ''}\n"
    
    if metadata.get('foreign_keys'):
        md += "\n## 外键\n\n"
        for fk in metadata['foreign_keys']:
            md += f"- {fk['from']} -> {fk['table']}.{fk['to']}\n"
    
    return md


def main():
    parser = argparse.ArgumentParser(description='生成元数据')
    parser.add_argument('--source', required=True, help='表名')
    parser.add_argument('--db', '--connection', dest='db', 
                       help='数据库连接字符串')
    parser.add_argument('--db-type', choices=['sqlite', 'mysql', 'postgresql'],
                       help='数据库类型（配合环境变量使用）')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--format', choices=['json', 'markdown'], default='json', 
                       help='输出格式')
    args = parser.parse_args()
    
    # 验证表名
    if not validate_table_name(args.source):
        sys.exit(1)
    
    conn = None
    try:
        if args.db:
            conn = get_connection(args.db)
        elif args.db_type:
            import os
            if args.db_type == 'sqlite':
                import sqlite3
                conn = sqlite3.connect(os.getenv('DB_PATH', 'data.db'))
            elif args.db_type == 'mysql':
                import pymysql
                conn = pymysql.connect(
                    host=os.getenv('DB_HOST', 'localhost'),
                    port=int(os.getenv('DB_PORT', 3306)),
                    user=os.getenv('DB_USER', ''),
                    password=os.getenv('DB_PASS', ''),
                    database=os.getenv('DB_NAME', ''),
                    cursorclass=pymysql.cursors.DictCursor
                )
            elif args.db_type in ('postgresql', 'postgres'):
                import psycopg2
                conn = psycopg2.connect(
                    host=os.getenv('DB_HOST', 'localhost'),
                    port=int(os.getenv('DB_PORT', 5432)),
                    user=os.getenv('DB_USER', ''),
                    password=os.getenv('DB_PASS', ''),
                    database=os.getenv('DB_NAME', '')
                )
        else:
            print("Error: Please provide --db or --db-type", file=sys.stderr)
            sys.exit(1)
        
        print(f"✅ Connected to database")
        
        metadata = generate_metadata(conn, args.source)
        print(f"✅ Generated metadata: {metadata['column_count']} columns")
        
        conn.close()
        
        if args.format == 'markdown':
            output = generate_data_dict(metadata)
        else:
            output = json.dumps(metadata, indent=2, ensure_ascii=False)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"✅ Output saved to {args.output}")
        else:
            print(output)
        
    except ImportError as e:
        print(f"Error: Missing dependency: {e}")
        print("Please install: pip install pymysql psycopg2-binary")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
