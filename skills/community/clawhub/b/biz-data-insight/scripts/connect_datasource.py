#!/usr/bin/env python3
"""
biz-data-insight: 数据源连接与Schema探索脚本

用法:
    python3 connect_datasource.py --type mysql --uri "mysql://user:pass@host:3306/db" --action test
    python3 connect_datasource.py --type csv --uri "./data.csv" --action explore
"""

import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse

from utils import output_success, output_error, get_datasource_connection, check_subscription

# 业务指标字段匹配模式
METRIC_PATTERNS = re.compile(
    r"(amount|revenue|price|cost|quantity|order|sales|total|count|profit|"
    r"income|expense|fee|payment|rate|ratio|score|num|"
    r"金额|销售|收入|成本|数量|订单|利润|费用)",
    re.IGNORECASE,
)

# 时间维度字段匹配模式
TIME_PATTERNS = re.compile(
    r"(date|time|created|updated|year|month|day|日期|时间|创建|更新)",
    re.IGNORECASE,
)

SUPPORTED_TYPES = ("mysql", "postgresql", "csv", "excel", "json")
FILE_TYPES = ("csv", "excel", "json")
DB_TYPES = ("mysql", "postgresql")


def _classify_column(name: str, dtype_str: str):
    """根据字段名和类型判断字段角色。"""
    roles = []
    if METRIC_PATTERNS.search(name):
        roles.append("metric")
    if TIME_PATTERNS.search(name):
        roles.append("time_dimension")
    return roles


# ---------------------------------------------------------------------------
# 数据库连接相关
# ---------------------------------------------------------------------------

def _get_db_connection(ds_type: str, uri: str, password: str | None = None):
    """创建数据库连接。"""
    parsed = urlparse(uri)
    host = parsed.hostname or "localhost"
    port = parsed.port
    user = parsed.username or "root"
    pwd = password or parsed.password or os.environ.get("BDI_DB_PASSWORD", "")
    database = parsed.path.lstrip("/") if parsed.path else None

    if ds_type == "mysql":
        import mysql.connector
        port = port or 3306
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=pwd,
            database=database,
        )
        return conn
    elif ds_type == "postgresql":
        import psycopg2
        port = port or 5432
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=pwd,
            dbname=database,
        )
        return conn
    else:
        raise ValueError(f"不支持的数据库类型: {ds_type}")


def _test_db(ds_type: str, uri: str, password: str | None = None) -> dict:
    """测试数据库连接。"""
    conn = _get_db_connection(ds_type, uri, password)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()

        parsed = urlparse(uri)
        details = {
            "host": parsed.hostname or "localhost",
            "port": parsed.port or (3306 if ds_type == "mysql" else 5432),
            "database": (parsed.path.lstrip("/") if parsed.path else None),
            "user": parsed.username or "root",
        }
        return {"success": True, "message": "连接成功", "type": ds_type, "details": details}
    finally:
        conn.close()


def _explore_db(ds_type: str, uri: str, password: str | None = None) -> dict:
    """探索数据库Schema。"""
    conn = _get_db_connection(ds_type, uri, password)
    try:
        cursor = conn.cursor()

        # 获取所有表
        if ds_type == "mysql":
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]
        else:
            cursor.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public' ORDER BY table_name"
            )
            tables = [row[0] for row in cursor.fetchall()]

        schema = []
        for table in tables:
            table_info = {"table": table, "columns": [], "row_count": 0, "sample_data": []}

            # 列信息
            if ds_type == "mysql":
                cursor.execute(f"DESCRIBE `{table}`")
                for row in cursor.fetchall():
                    col_name = row[0]
                    col_type = row[1]
                    roles = _classify_column(col_name, col_type)
                    table_info["columns"].append({
                        "name": col_name,
                        "type": col_type,
                        "roles": roles,
                    })
            else:
                cursor.execute(
                    "SELECT column_name, data_type FROM information_schema.columns "
                    "WHERE table_schema = 'public' AND table_name = %s "
                    "ORDER BY ordinal_position",
                    (table,),
                )
                for row in cursor.fetchall():
                    col_name = row[0]
                    col_type = row[1]
                    roles = _classify_column(col_name, col_type)
                    table_info["columns"].append({
                        "name": col_name,
                        "type": col_type,
                        "roles": roles,
                    })

            # 行数
            cursor.execute(f'SELECT COUNT(*) FROM "{table}"' if ds_type == "postgresql" else f"SELECT COUNT(*) FROM `{table}`")
            table_info["row_count"] = cursor.fetchone()[0]

            # 样本数据 (5行)
            cursor.execute(f'SELECT * FROM "{table}" LIMIT 5' if ds_type == "postgresql" else f"SELECT * FROM `{table}` LIMIT 5")
            col_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            table_info["sample_data"] = [
                {col_names[i]: _serialize_value(val) for i, val in enumerate(row)}
                for row in rows
            ]

            schema.append(table_info)

        cursor.close()
        return {
            "success": True,
            "message": "Schema探索完成",
            "type": ds_type,
            "tables_count": len(tables),
            "schema": schema,
        }
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 文件数据源相关
# ---------------------------------------------------------------------------

def _read_file(ds_type: str, uri: str):
    """用 pandas 读取文件，返回 DataFrame。"""
    import pandas as pd

    if ds_type == "csv":
        return pd.read_csv(uri)
    elif ds_type == "excel":
        return pd.read_excel(uri)
    elif ds_type == "json":
        return pd.read_json(uri)
    else:
        raise ValueError(f"不支持的文件类型: {ds_type}")


def _test_file(ds_type: str, uri: str) -> dict:
    """测试文件数据源可读性。"""
    if not os.path.exists(uri):
        raise FileNotFoundError(f"文件不存在: {uri}")

    df = _read_file(ds_type, uri)
    details = {
        "path": os.path.abspath(uri),
        "rows": len(df),
        "columns": len(df.columns),
    }
    return {"success": True, "message": "连接成功", "type": ds_type, "details": details}


def _explore_file(ds_type: str, uri: str) -> dict:
    """探索文件数据源Schema。"""
    import pandas as pd

    if not os.path.exists(uri):
        raise FileNotFoundError(f"文件不存在: {uri}")

    df = _read_file(ds_type, uri)

    columns = []
    for col in df.columns:
        dtype_str = str(df[col].dtype)
        roles = _classify_column(str(col), dtype_str)

        # 自动识别: 数值列视为指标, datetime列视为时间维度
        if pd.api.types.is_numeric_dtype(df[col]) and "metric" not in roles:
            roles.append("metric")
        if pd.api.types.is_datetime64_any_dtype(df[col]) and "time_dimension" not in roles:
            roles.append("time_dimension")

        columns.append({
            "name": str(col),
            "type": dtype_str,
            "roles": roles,
        })

    # 样本数据 (5行)
    sample_df = df.head(5)
    sample_data = json.loads(sample_df.to_json(orient="records", force_ascii=False, date_format="iso"))

    table_info = {
        "table": "data",
        "columns": columns,
        "row_count": len(df),
        "sample_data": sample_data,
    }

    return {
        "success": True,
        "message": "Schema探索完成",
        "type": ds_type,
        "tables_count": 1,
        "schema": [table_info],
    }


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def _serialize_value(val):
    """将数据库值序列化为JSON兼容类型。"""
    if val is None:
        return None
    if isinstance(val, (int, float, bool, str)):
        return val
    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace")
    # datetime, date, Decimal 等
    return str(val)


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="biz-data-insight 数据源连接与Schema探索")
    parser.add_argument("--type", required=True, choices=SUPPORTED_TYPES, help="数据源类型")
    parser.add_argument("--uri", required=True, help="连接字符串或文件路径")
    parser.add_argument("--password", default=None, help="数据库密码（可选，也可通过URI或环境变量 BDI_DB_PASSWORD 提供）")
    parser.add_argument("--action", required=True, choices=("test", "explore"), help="操作类型: test=测试连接, explore=探索Schema")

    args = parser.parse_args()

    try:
        if args.action == "test":
            if args.type in DB_TYPES:
                result = _test_db(args.type, args.uri, args.password)
            else:
                result = _test_file(args.type, args.uri)
        elif args.action == "explore":
            if args.type in DB_TYPES:
                result = _explore_db(args.type, args.uri, args.password)
            else:
                result = _explore_file(args.type, args.uri)
        else:
            result = {"success": False, "message": f"未知操作: {args.action}"}

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except FileNotFoundError as e:
        print(json.dumps({"success": False, "message": f"文件未找到: {e}"}, ensure_ascii=False))
        sys.exit(1)
    except ImportError as e:
        print(json.dumps({"success": False, "message": f"缺少依赖包，请安装: {e}"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"success": False, "message": f"操作失败: {e}"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
