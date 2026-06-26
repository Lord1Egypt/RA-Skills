#!/usr/bin/env python3
"""
数据血缘分析脚本
"""

import sys
import re
import json
from typing import Dict, List, Any, Set
from collections import defaultdict

def validate_table_name(table_name: str) -> bool:
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
    if not re.match(pattern, table_name):
        print(f"Error: Invalid table name: {table_name}", file=sys.stderr)
        return False
    return True


"""
数据血缘分析脚本
Supports: SQLite, MySQL, PostgreSQL
Usage: 
  sqlite: python lineage_analysis.py --table users --db sqlite:///data.db
  mysql:  python lineage_analysis.py --table users --db mysql://user:pass@localhost:3306/db
  pg:     python lineage_analysis.py --table users --db postgresql://user:pass@localhost:5432/db
"""

from typing import Dict, List, Set, Any
from urllib.parse import urlparse


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


class LineageGraph:
    """血缘图"""
    
    def __init__(self):
        self.upstream: Dict[str, Set[str]] = defaultdict(set)
        self.downstream: Dict[str, Set[str]] = defaultdict(set)
        self.transformations: Dict[str, List[Dict]] = defaultdict(list)
    
    def add_lineage(self, source: str, target: str, transformation: str = ""):
        self.upstream[target].add(source)
        self.downstream[source].add(target)
        
        if transformation:
            self.transformations[target].append({
                "from": source,
                "transformation": transformation
            })
    
    def get_upstream(self, table: str, depth: int = -1) -> Set[str]:
        if depth == 0:
            return set()
        
        result = set()
        for parent in self.upstream.get(table, set()):
            result.add(parent)
            if depth != 1:
                result.update(self.get_upstream(parent, depth - 1))
        
        return result
    
    def get_downstream(self, table: str, depth: int = -1) -> Set[str]:
        if depth == 0:
            return set()
        
        result = set()
        for child in self.downstream.get(table, set()):
            result.add(child)
            if depth != 1:
                result.update(self.get_downstream(child, depth - 1))
        
        return result
    
    def get_full_lineage(self, table: str) -> Dict[str, Any]:
        upstream = self.get_upstream(table)
        downstream = self.get_downstream(table)
        
        return {
            "table": table,
            "upstream": list(upstream),
            "downstream": list(downstream),
            "transformations": self.transformations.get(table, []),
            "upstream_count": len(upstream),
            "downstream_count": len(downstream)
        }


def parse_sql_dependencies(sql: str, target_table: str) -> List[tuple]:
    """从 SQL 中解析表依赖"""
    # SELECT FROM
    from_pattern = r'FROM\s+([a-zA-Z0-9_\.]+)'
    # JOIN
    join_pattern = r'JOIN\s+([a-zA-Z0-9_\.]+)'
    
    sources = set()
    sources.update(re.findall(from_pattern, sql, re.IGNORECASE))
    sources.update(re.findall(join_pattern, sql, re.IGNORECASE))
    
    # 清理表名（去掉别名）
    cleaned_sources = []
    for s in sources:
        s = s.strip().split()[0]  # 去掉 AS 别名
        cleaned_sources.append(s)
    
    return [(s, target_table) for s in cleaned_sources]


def get_etl_history(conn, table_name: str) -> List[Dict]:
    """从数据库获取 ETL 历史（如果有的话）"""
    cursor = conn.cursor()
    etl_configs = []
    
    # 尝试从 information_schema 获取视图/存储过程信息
    try:
        # 获取基于该表的所有视图
        cursor.execute(f"""
            SELECT VIEW_NAME, VIEW_DEFINITION 
            FROM INFORMATION_SCHEMA.VIEWS 
            WHERE TABLE_NAME = '{table_name}'
        """)
        
        for row in cursor.fetchall():
            view_name = row[0]
            view_def = row[1] or ""
            deps = parse_sql_dependencies(view_def, view_name)
            for src, tgt in deps:
                etl_configs.append({
                    "source": [src],
                    "target": tgt,
                    "type": "VIEW"
                })
    except:
        pass
    
    cursor.close()
    return etl_configs


def infer_lineage_from_foreign_keys(conn, table_name: str) -> List[Dict]:
    """从外键推断血缘"""
    cursor = conn.cursor()
    lineage = []
    
    try:
        # SQLite
        cursor.execute(f"PRAGMA foreign_key_list(`{table_name}`)")
        for row in cursor.fetchall():
            lineage.append({
                "source": [row[2]],  # 父表
                "target": table_name,
                "type": "FOREIGN_KEY"
            })
    except:
        pass
    
    # 尝试 MySQL
    if not lineage:
        try:
            cursor.execute(f"""
                SELECT TABLE_NAME, REFERENCED_TABLE_NAME 
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND REFERENCED_TABLE_NAME IS NOT NULL
                AND TABLE_NAME = '{table_name}'
            """)
            for row in cursor.fetchall():
                lineage.append({
                    "source": [row[1]],
                    "target": table_name,
                    "type": "FOREIGN_KEY"
                })
        except:
            pass
    
    cursor.close()
    return lineage


def build_lineage_from_db(conn, table_name: str) -> LineageGraph:
    """从数据库构建血缘"""
    graph = LineageGraph()
    
    # 1. 从外键推断
    fk_lineage = infer_lineage_from_foreign_keys(conn, table_name)
    for item in fk_lineage:
        graph.add_lineage(item['source'][0], item['target'], item['type'])
    
    # 2. 获取 ETL/视图依赖
    try:
        etl_configs = get_etl_history(conn, table_name)
        for config in etl_configs:
            for src in config['source']:
                graph.add_lineage(src, config['target'], config['type'])
    except:
        pass
    
    return graph


def generate_lineage_report(lineage: Dict) -> str:
    """生成血缘报告"""
    report = f"""## 数据血缘分析 - {lineage['table']}

### 上游 ({lineage['upstream_count']} 个)
"""
    
    if lineage['upstream']:
        for t in lineage['upstream']:
            report += f"- {t}\n"
    else:
        report += "- 无\n"
    
    report += f"\n### 下游 ({lineage['downstream_count']} 个)\n"
    
    if lineage['downstream']:
        for t in lineage['downstream']:
            report += f"- {t}\n"
    else:
        report += "- 无\n"
    
    if lineage['transformations']:
        report += "\n### 转换过程\n"
        for t in lineage['transformations']:
            report += f"- {t['from']} → {t['transformation']} → {lineage['table']}\n"
    
    return report


def generate_mermaid_diagram(lineage: Dict) -> str:
    """生成 Mermaid 血缘图"""
    lines = ["```mermaid", "flowchart TD"]
    
    for t in lineage.get('upstream', []):
        lines.append(f"    {t}[{t}] --> {lineage['table']}")
    
    for t in lineage.get('downstream', []):
        lines.append(f"    {lineage['table']} --> {t}[{t}]")
    
    lines.append("```")
    
    return "\n".join(lines)


def build_lineage_example(table_name: str) -> LineageGraph:
    """示例血缘数据（当无数据库时使用）"""
    graph = LineageGraph(table_name)
    
    # 添加示例上游
    graph.add_lineage(f"{table_name}_staging")
    graph.add_lineage("raw_data")
    
    # 添加示例转换
    graph.add_lineage(f"{table_name}_staging", "清洗")
    graph.add_lineage("raw_data", "ETL")
    
    return graph


def main():
    parser = argparse.ArgumentParser(description='数据血缘分析')
    parser.add_argument('--table', required=True, help='表名')
    parser.add_argument('--db-type', choices=['sqlite', 'mysql', 'postgresql'],
                       help='数据库类型（配合环境变量使用）')
    parser.add_argument('--direction', choices=['upstream', 'downstream', 'both'], 
                       default='both', help='分析方向')
    parser.add_argument('--format', choices=['json', 'markdown', 'mermaid'], 
                       default='markdown', help='输出格式')
    parser.add_argument('--depth', type=int, default=-1, help='追溯深度')
    args = parser.parse_args()
    
    # 验证表名
    if not validate_table_name(args.table):
        sys.exit(1)
    
    # 仅从环境变量获取连接
    conn = None
    if args.db_type:
        import os
        try:
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
        except ImportError as e:
            print(f"❌ 缺少依赖: {e}")
            print("请安装: pip install pymysql psycopg2-binary")
            return
        except Exception as e:
            print(f"❌ 连接错误: {e}")
            return
        
        print(f"✅ 已连接到数据库")
        graph = build_lineage_from_db(conn, args.table)
        conn.close()
    else:
        # 无数据库时使用示例数据
        graph = build_lineage_example(args.table)
    
    lineage = graph.get_full_lineage(args.table)
    
    if args.direction == 'upstream':
        lineage['downstream'] = []
        lineage['downstream_count'] = 0
    elif args.direction == 'downstream':
        lineage['upstream'] = []
        lineage['upstream_count'] = 0
    
    if args.format == 'json':
        print(json.dumps(lineage, indent=2, ensure_ascii=False))
    elif args.format == 'mermaid':
        print(generate_mermaid_diagram(lineage))
    else:
        print(generate_markdown_report(lineage))


if __name__ == '__main__':
    main()
