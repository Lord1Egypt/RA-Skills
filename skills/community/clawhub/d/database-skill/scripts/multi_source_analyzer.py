"""
Multi-Source Data Analysis Engine
=================================
A simple, unified interface for analyzing data from multiple sources.
Uses DuckDB as the local analysis engine.

Usage:
    # Python API
    from multi_source_analyzer import MultiSourceAnalyzer
    analyzer = MultiSourceAnalyzer()
    analyzer.register_file('sales', 'data/sales.csv')
    result = analyzer.query("SELECT * FROM sales")

    # CLI
    python multi_source_analyzer.py register_file --name sales --file data/sales.csv
    python multi_source_analyzer.py query --sql "SELECT * FROM sales LIMIT 5"
"""

import os
import sys
import json
import argparse
import pandas as pd
import duckdb
import tempfile
import atexit
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
from pathlib import Path


# 持久化 DuckDB 数据库路径
DB_PATH = os.path.join(tempfile.gettempdir(), 'multi_source_analyzer.duckdb')


@dataclass
class DataSource:
    name: str
    source_type: str
    _df: Optional[pd.DataFrame] = field(default=None, repr=False)
    
    @property
    def dataframe(self) -> Optional[pd.DataFrame]:
        return self._df
    
    def set_dataframe(self, df: pd.DataFrame):
        self._df = df
    
    @property
    def schema(self) -> Dict[str, str]:
        if self._df is None:
            return {}
        return {col: str(dtype) for col, dtype in self._df.dtypes.items()}


class MultiSourceAnalyzer:
    """
    Local data analysis engine using DuckDB.
    
    Features:
    - Register multiple data sources (files, DataFrames)
    - Execute cross-source SQL queries
    - Automatic data type inference
    
    Usage:
        # 1. 用户用 Database Toolbox 获取数据
        df_orders = toolbox.execute_sql("SELECT * FROM orders LIMIT 100")
        df_customers = toolbox.execute_sql("SELECT * FROM customers")
        
        # 2. 注册数据到分析器
        analyzer = MultiSourceAnalyzer()
        analyzer.register_dataframe('orders', df_orders)
        analyzer.register_dataframe('customers', df_customers)
        
        # 3. 执行跨数据源查询
        result = analyzer.query('''
            SELECT c.name, SUM(o.amount) as total
            FROM customers c
            JOIN orders o ON c.id = o.customer_id
            GROUP BY c.name
        ''')
    """
    
    def __init__(self):
        # 如果数据库文件存在则连接，否则创建新的
        if os.path.exists(DB_PATH):
            self._duck_conn = duckdb.connect(database=DB_PATH, read_only=False)
        else:
            self._duck_conn = duckdb.connect(database=DB_PATH)
        self._sources: Dict[str, DataSource] = {}
        atexit.register(self._cleanup)
    
    def _cleanup(self):
        # 退出时不删除文件，下次可以继续使用
        pass
    
    @property
    def sources(self) -> Dict[str, DataSource]:
        return self._sources
    
    def register_dataframe(self, name: str, df: pd.DataFrame) -> DataSource:
        source = DataSource(name=name, source_type='dataframe')
        source.set_dataframe(df)
        self._sources[name] = source
        # 注册到 DuckDB 并持久化
        self._duck_conn.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM df")
        return source
    
    def register_file(self, name: str, file_path: str, sheet: Optional[str] = None) -> DataSource:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        ext = path.suffix.lower()
        
        if ext == '.csv':
            df = pd.read_csv(file_path)
        elif ext in ('.xlsx', '.xls'):
            sheet_name = sheet or 0
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        elif ext == '.json':
            df = pd.read_json(file_path)
        elif ext == '.parquet':
            df = pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
        print(f"Loaded {len(df)} rows from {file_path}")
        return self.register_dataframe(name, df)
    
    def list_sources(self) -> List[Dict[str, Any]]:
        result = []
        for name, source in self._sources.items():
            info = {
                'name': name,
                'type': source.source_type,
                'columns': list(source.schema.keys()) if source.dataframe is not None else [],
                'row_count': len(source.dataframe) if source.dataframe is not None else 0
            }
            result.append(info)
        return result
    
    def query(self, sql: str, limit: int = 100) -> pd.DataFrame:
        result = self._duck_conn.execute(sql).fetchdf()
        if limit and len(result) > limit:
            return result.head(limit)
        return result
    
    def describe(self, name: str) -> pd.DataFrame:
        return self.query(f"DESCRIBE {name}")
    
    def preview(self, name: str, n: int = 5) -> pd.DataFrame:
        return self.query(f"SELECT * FROM {name} LIMIT {n}")
    
    def get_schema_info(self) -> str:
        lines = ["=" * 60, "Data Sources Schema", "=" * 60]
        
        for name, source in self._sources.items():
            lines.append(f"\n[{name}] ({source.source_type})")
            if source.dataframe is not None:
                lines.append(f"  Rows: {len(source.dataframe)}")
                lines.append("  Columns:")
                for col, dtype in source.schema.items():
                    lines.append(f"    - {col}: {dtype}")
        
        return "\n".join(lines)
    
    def close(self):
        self._duck_conn.close()
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)


_analyzer = None

def get_analyzer() -> MultiSourceAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = MultiSourceAnalyzer()
    return _analyzer


def cmd_register_file(args):
    analyzer = get_analyzer()
    result = analyzer.register_file(args.name, args.file, args.sheet)
    return {"success": True, "message": f"Registered: {args.name}"}


def cmd_register_dataframe(args):
    analyzer = get_analyzer()
    if args.json:
        import ast
        data = json.loads(args.json)
        df = pd.DataFrame(data)
    else:
        raise ValueError("Please provide --json data")
    analyzer.register_dataframe(args.name, df)
    return {"success": True, "message": f"Registered: {args.name}"}


def cmd_query(args):
    analyzer = get_analyzer()
    result = analyzer.query(args.sql, limit=args.limit)
    return {"success": True, "data": json.loads(result.to_json(orient="records"))}


def cmd_list_sources(args):
    analyzer = get_analyzer()
    # 从 DuckDB 查询表列表
    tables = analyzer._duck_conn.execute("SHOW TABLES").fetchall()
    result = []
    for (table_name,) in tables:
        info = {
            'name': table_name,
            'type': 'file',
            'row_count': analyzer._duck_conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0],
            'columns': [col[0] for col in analyzer._duck_conn.execute(f"DESCRIBE {table_name}").fetchall()]
        }
        result.append(info)
    return {"success": True, "data": result}


def cmd_schema(args):
    analyzer = get_analyzer()
    return {"success": True, "data": analyzer.get_schema_info()}


def cmd_preview(args):
    analyzer = get_analyzer()
    result = analyzer.preview(args.name, args.n)
    return {"success": True, "data": json.loads(result.to_json(orient="records"))}


def cmd_describe(args):
    analyzer = get_analyzer()
    result = analyzer.describe(args.name)
    return {"success": True, "data": json.loads(result.to_json(orient="records"))}


def main():
    parser = argparse.ArgumentParser(description="Multi-Source Analysis CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # register_file
    parser_register = subparsers.add_parser("register_file", help="Register a file")
    parser_register.add_argument("--name", required=True, help="Table name")
    parser_register.add_argument("--file", required=True, help="File path")
    parser_register.add_argument("--sheet", help="Sheet name (for Excel)")
    
    # register_dataframe
    parser_df = subparsers.add_parser("register_dataframe", help="Register a DataFrame from JSON")
    parser_df.add_argument("--name", required=True, help="Table name")
    parser_df.add_argument("--json", required=True, help="JSON data")
    
    # query
    parser_query = subparsers.add_parser("query", help="Execute SQL query")
    parser_query.add_argument("--sql", required=True, help="SQL query")
    parser_query.add_argument("--limit", type=int, default=100, help="Result limit")
    
    # list_sources
    subparsers.add_parser("list_sources", help="List all registered sources")
    
    # schema
    subparsers.add_parser("schema", help="Show schema of all sources")
    
    # preview
    parser_preview = subparsers.add_parser("preview", help="Preview table data")
    parser_preview.add_argument("--name", required=True, help="Table name")
    parser_preview.add_argument("--n", type=int, default=5, help="Number of rows")
    
    # describe
    parser_desc = subparsers.add_parser("describe", help="Describe table schema")
    parser_desc.add_argument("--name", required=True, help="Table name")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    commands = {
        "register_file": cmd_register_file,
        "register_dataframe": cmd_register_dataframe,
        "query": cmd_query,
        "list_sources": cmd_list_sources,
        "schema": cmd_schema,
        "preview": cmd_preview,
        "describe": cmd_describe,
    }
    
    if args.command in commands:
        result = commands[args.command](args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"success": False, "message": f"Unknown command: {args.command}"}))


if __name__ == "__main__":
    main()
