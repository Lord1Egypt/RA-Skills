#!/usr/bin/env python3
"""
biz-data-insight OpenClaw Skill — 安全 SQL 查询引擎

用法:
  python3 query_engine.py --type mysql --uri "mysql://user:pass@host:3306/db" --sql "SELECT ..."
  python3 query_engine.py --type csv --uri "./data.csv" --sql "SELECT * FROM data LIMIT 5"
  python3 query_engine.py --type mysql --uri "..." --template top_n --params '{"table":"orders","metric":"amount","dimension":"product","n":10}'
"""

import argparse
import json
import sqlite3
import sys
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from utils import (
    check_subscription,
    get_datasource_connection,
    output_error,
    output_success,
    validate_sql_readonly,
)

# ---------------------------------------------------------------------------
# 预定义查询模板
# ---------------------------------------------------------------------------

TEMPLATES: Dict[str, str] = {
    "top_n": (
        "SELECT {dimension}, SUM({metric}) AS total "
        "FROM {table} "
        "GROUP BY {dimension} "
        "ORDER BY total DESC "
        "LIMIT {n}"
    ),
    "yoy": (
        "SELECT "
        "  DATE_FORMAT({date_col}, '%Y-%m') AS period, "
        "  SUM(CASE WHEN YEAR({date_col}) = YEAR(CURDATE()) THEN {metric} ELSE 0 END) AS current_period, "
        "  SUM(CASE WHEN YEAR({date_col}) = YEAR(CURDATE()) - 1 THEN {metric} ELSE 0 END) AS last_year_period, "
        "  ROUND("
        "    (SUM(CASE WHEN YEAR({date_col}) = YEAR(CURDATE()) THEN {metric} ELSE 0 END) "
        "     - SUM(CASE WHEN YEAR({date_col}) = YEAR(CURDATE()) - 1 THEN {metric} ELSE 0 END)) "
        "    / NULLIF(SUM(CASE WHEN YEAR({date_col}) = YEAR(CURDATE()) - 1 THEN {metric} ELSE 0 END), 0) * 100, 2"
        "  ) AS yoy_pct "
        "FROM {table} "
        "GROUP BY period "
        "ORDER BY period"
    ),
    "mom": (
        "SELECT "
        "  DATE_FORMAT({date_col}, '%Y-%m') AS period, "
        "  SUM({metric}) AS total, "
        "  ROUND("
        "    (SUM({metric}) - LAG(SUM({metric})) OVER (ORDER BY DATE_FORMAT({date_col}, '%Y-%m'))) "
        "    / NULLIF(LAG(SUM({metric})) OVER (ORDER BY DATE_FORMAT({date_col}, '%Y-%m')), 0) * 100, 2"
        "  ) AS mom_pct "
        "FROM {table} "
        "GROUP BY period "
        "ORDER BY period"
    ),
    "distribution": (
        "SELECT {dimension}, SUM({metric}) AS total, "
        "ROUND(SUM({metric}) * 100.0 / (SELECT SUM({metric}) FROM {table}), 2) AS pct "
        "FROM {table} "
        "GROUP BY {dimension} "
        "ORDER BY total DESC"
    ),
    "trend": (
        "SELECT DATE_FORMAT({date_col}, '{date_format}') AS period, "
        "SUM({metric}) AS total "
        "FROM {table} "
        "GROUP BY period "
        "ORDER BY period"
    ),
}

# 模板所需参数
TEMPLATE_REQUIRED_PARAMS: Dict[str, List[str]] = {
    "top_n": ["table", "metric", "dimension", "n"],
    "yoy": ["table", "metric", "date_col"],
    "mom": ["table", "metric", "date_col"],
    "distribution": ["table", "metric", "dimension"],
    "trend": ["table", "metric", "date_col"],
}


def build_sql_from_template(template_name: str, params: Dict[str, Any]) -> str:
    """根据模板名称和参数生成 SQL 语句。"""
    if template_name not in TEMPLATES:
        raise ValueError(f"未知的查询模板: {template_name}，可用模板: {', '.join(TEMPLATES.keys())}")

    required = TEMPLATE_REQUIRED_PARAMS[template_name]
    missing = [p for p in required if p not in params]
    if missing:
        raise ValueError(f"模板 '{template_name}' 缺少必需参数: {', '.join(missing)}")

    # 为 trend 模板设置默认日期格式
    if template_name == "trend" and "date_format" not in params:
        params["date_format"] = "%Y-%m"

    # n 转为整数字符串
    if "n" in params:
        params["n"] = int(params["n"])

    return TEMPLATES[template_name].format(**params)


# ---------------------------------------------------------------------------
# 数据库执行
# ---------------------------------------------------------------------------

def execute_db_query(
    db_type: str,
    uri: str,
    sql: str,
    password: Optional[str] = None,
    max_rows: int = 1000,
) -> Tuple[List[str], List[list]]:
    """通过数据库驱动执行 SQL，返回 (columns, rows)。"""
    conn = get_datasource_connection(db_type, uri, password=password)
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchmany(max_rows)
        # 将行转为普通 list（部分驱动返回 tuple）
        rows = [list(row) for row in rows]
        return columns, rows
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conn.close()


# ---------------------------------------------------------------------------
# 文件数据源执行（CSV / Excel / JSON → sqlite3 内存库）
# ---------------------------------------------------------------------------

def load_dataframe(file_type: str, uri: str) -> pd.DataFrame:
    """根据文件类型加载 DataFrame。"""
    loaders = {
        "csv": lambda p: pd.read_csv(p),
        "excel": lambda p: pd.read_excel(p),
        "json": lambda p: pd.read_json(p),
    }
    loader = loaders.get(file_type)
    if loader is None:
        raise ValueError(f"不支持的文件类型: {file_type}")
    return loader(uri)


def execute_file_query(
    file_type: str,
    uri: str,
    sql: str,
    max_rows: int = 1000,
) -> Tuple[List[str], List[list]]:
    """将文件数据加载到 sqlite3 内存库并执行 SQL。"""
    df = load_dataframe(file_type, uri)

    conn = sqlite3.connect(":memory:")
    try:
        # 表名固定为 "data"，用户 SQL 中应引用 "data"
        df.to_sql("data", conn, index=False, if_exists="replace")
        cursor = conn.execute(sql)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = [list(row) for row in cursor.fetchmany(max_rows)]
        return columns, rows
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 结果统计
# ---------------------------------------------------------------------------

def compute_stats(columns: List[str], rows: List[list]) -> Dict[str, Dict[str, Any]]:
    """为所有数值列计算 sum / avg / min / max / count。"""
    if not rows or not columns:
        return {}

    stats: Dict[str, Dict[str, Any]] = {}
    for idx, col_name in enumerate(columns):
        numeric_values: List[float] = []
        for row in rows:
            val = row[idx]
            if val is None:
                continue
            try:
                numeric_values.append(float(val))
            except (TypeError, ValueError):
                continue

        if not numeric_values:
            continue

        stats[col_name] = {
            "sum": round(sum(numeric_values), 4),
            "avg": round(sum(numeric_values) / len(numeric_values), 4),
            "min": round(min(numeric_values), 4),
            "max": round(max(numeric_values), 4),
            "count": len(numeric_values),
        }

    return stats


# ---------------------------------------------------------------------------
# 序列化辅助
# ---------------------------------------------------------------------------

def _make_serializable(rows: List[list]) -> List[list]:
    """确保所有值可被 JSON 序列化。"""
    import datetime
    import decimal

    cleaned: List[list] = []
    for row in rows:
        new_row: list = []
        for val in row:
            if isinstance(val, decimal.Decimal):
                val = float(val)
            elif isinstance(val, (datetime.date, datetime.datetime)):
                val = val.isoformat()
            elif isinstance(val, bytes):
                val = val.decode("utf-8", errors="replace")
            new_row.append(val)
        cleaned.append(new_row)
    return cleaned


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

DB_TYPES = {"mysql", "postgresql"}
FILE_TYPES = {"csv", "excel", "json"}


def main() -> None:
    parser = argparse.ArgumentParser(description="biz-data-insight 安全 SQL 查询引擎")
    parser.add_argument("--type", required=True, choices=sorted(DB_TYPES | FILE_TYPES),
                        help="数据源类型: mysql, postgresql, csv, excel, json")
    parser.add_argument("--uri", required=True, help="数据库连接字符串或文件路径")
    parser.add_argument("--password", default=None, help="数据库密码（可选）")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sql", default=None, help="要执行的 SQL 查询语句")
    group.add_argument("--template", default=None, choices=sorted(TEMPLATES.keys()),
                       help="预定义查询模板名称")

    parser.add_argument("--params", default=None, help="模板参数（JSON 字符串）")
    parser.add_argument("--max-rows", type=int, default=None, help="最大返回行数")

    args = parser.parse_args()

    # ---- 订阅层级 & 行数上限 ----
    try:
        subscription = check_subscription()
        default_max_rows = subscription.get("max_rows", 1000)
    except Exception:
        default_max_rows = 1000

    max_rows = args.max_rows if args.max_rows is not None else default_max_rows

    # ---- 构造 SQL ----
    if args.template:
        if not args.params:
            output_error("使用模板时必须通过 --params 提供参数（JSON 字符串）")
            sys.exit(1)
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError as exc:
            output_error(f"--params JSON 解析失败: {exc}")
            sys.exit(1)

        try:
            sql = build_sql_from_template(args.template, params)
        except ValueError as exc:
            output_error(str(exc))
            sys.exit(1)
    else:
        sql = args.sql

    # ---- SQL 安全校验 ----
    try:
        validate_sql_readonly(sql)
    except Exception as exc:
        output_error(f"SQL 安全校验未通过: {exc}")
        sys.exit(1)

    # ---- 执行查询 ----
    try:
        ds_type = args.type
        if ds_type in DB_TYPES:
            columns, rows = execute_db_query(ds_type, args.uri, sql,
                                             password=args.password, max_rows=max_rows)
        elif ds_type in FILE_TYPES:
            columns, rows = execute_file_query(ds_type, args.uri, sql, max_rows=max_rows)
        else:
            output_error(f"不支持的数据源类型: {ds_type}")
            sys.exit(1)
    except Exception as exc:
        output_error(f"查询执行失败: {exc}")
        sys.exit(1)

    # ---- 格式化输出 ----
    rows = _make_serializable(rows)
    stats = compute_stats(columns, rows)

    output_success({
        "columns": columns,
        "rows": rows,
        "row_count": len(rows),
        "stats": stats,
    })


if __name__ == "__main__":
    main()
