#!/usr/bin/env python3
"""Unified discover/generate entry for generate_yaml_semantic skill."""

from __future__ import annotations

import argparse
import json
import os
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Tuple
from uuid import UUID
import sys

from sqlalchemy import create_engine, inspect, text

from excel_utils import (
    create_subset_excel,
    list_excel_sheets,
    upload_database_for_knowledge,
    upload_excel_for_knowledge,
)
from generate_yaml import generate_yaml_file


def _error(code: str, message: str, **extra: Any) -> Dict[str, Any]:
    payload = {"success": False, "code": code, "message": message}
    payload.update(extra)
    return payload


def _normalize_for_json(value: Any) -> Any:
    """Convert common database/python objects to JSON-safe values recursively."""
    if isinstance(value, dict):
        return {k: _normalize_for_json(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize_for_json(v) for v in value]
    if isinstance(value, (tuple, set, frozenset)):
        return [_normalize_for_json(v) for v in value]
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Enum):
        return _normalize_for_json(value.value)
    if isinstance(value, memoryview):
        return bytes(value).hex()
    if isinstance(value, (bytes, bytearray)):
        try:
            return bytes(value).decode("utf-8")
        except UnicodeDecodeError:
            return bytes(value).hex()
    if hasattr(value, "isoformat") and callable(getattr(value, "isoformat")):
        try:
            return value.isoformat()
        except Exception:
            pass
    try:
        json.dumps(value, ensure_ascii=False)
        return value
    except TypeError:
        return str(value)


def _detect_db_type(db_url: str) -> str:
    """Detect database type from URL prefix."""
    if any(db_url.startswith(p) for p in ("mysql://", "mysql+pymysql://")):
        return "mysql"
    if any(db_url.startswith(p) for p in ("postgresql://", "postgresql+psycopg2://")):
        return "postgresql"
    if any(db_url.startswith(p) for p in ("mssql://", "mssql+pymssql://")):
        return "sqlserver"
    if any(db_url.startswith(p) for p in ("oracle://", "oracle+cx_oracle://", "oracle+oracledb://")):
        return "oracle"
    return "unknown"


def _to_yaml_db_type(db_type: str) -> str:
    """Map internal db_type token to YAML standard token."""
    value = str(db_type or "").strip().lower()
    if value in ("mysql", "postgresql", "oracle"):
        return value
    if value in ("sqlserver", "sql_server", "mssql"):
        return "sql_server"
    return "unknown"


def _normalize_db_url(db_url: str) -> str:
    """Normalize database URL with appropriate driver prefix."""
    if db_url.startswith("mysql://") and "+pymysql" not in db_url:
        return db_url.replace("mysql://", "mysql+pymysql://", 1)
    if db_url.startswith("postgresql://") and "+psycopg2" not in db_url:
        return db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
    if db_url.startswith("mssql://") and "+pymssql" not in db_url:
        return db_url.replace("mssql://", "mssql+pymssql://", 1)
    # Oracle: use oracledb driver by default for Python 3.13+ compatibility
    if db_url.startswith("oracle://") and ("+cx_oracle" not in db_url and "+oracledb" not in db_url):
        return db_url.replace("oracle://", "oracle+oracledb://", 1)
    # If explicitly using cx_oracle, suggest migration to oracledb (but still allow it)
    if db_url.startswith("oracle+cx_oracle://"):
        pass  # Allow cx_oracle but warn in documentation
    return db_url


def _validate_oracle_url_format(db_url: str) -> Dict[str, Any] | None:
    """
    Validate Oracle URL format requirements.

    Oracle connection must use format:
      oracle+oracledb://user:password@host:1521/?service_name=ORCL
    The service_name parameter is required.
    """
    if not db_url.startswith(("oracle://", "oracle+cx_oracle://", "oracle+oracledb://")):
        return None

    # Check if service_name parameter exists in URL
    if "service_name=" not in db_url:
        return _error(
            "INVALID_ORACLE_URL",
            "Oracle URL must include service_name parameter. "
            "Correct format: oracle+oracledb://user:password@host:port/?service_name=YOUR_SERVICE_NAME "
            "(e.g., oracle+oracledb://system:pwd@3.215.150.193:1521/?service_name=FREEPDB1)"
        )

    return None


def _split_csv(value: str) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _quote_identifier(name: str, db_type: str) -> str:
    """Quote identifier according to database dialect."""
    if db_type == "mysql":
        return f"`{name}`"
    elif db_type == "postgresql":
        return f'"{name}"'
    elif db_type == "sqlserver":
        return f"[{name}]"
    elif db_type == "oracle":
        return f'"{name}"'
    else:
        return f"`{name}`"


def _quote_table_name(table_name: str, db_type: str, schema_name: str = "") -> str:
    """Build a fully qualified table name when schema/database is available."""
    quoted_table = _quote_identifier(table_name, db_type)
    if schema_name:
        return f"{_quote_identifier(schema_name, db_type)}.{quoted_table}"
    return quoted_table


def _random_order_func(db_type: str) -> str:
    """Return database-specific random order function."""
    if db_type == "mysql":
        return "RAND()"
    elif db_type == "postgresql":
        return "RANDOM()"
    elif db_type == "sqlserver":
        return "NEWID()"
    elif db_type == "oracle":
        return "DBMS_RANDOM.RANDOM"
    else:
        return "RAND()"


def _build_sample_query(
    db_type: str,
    table_name: str,
    column_name: str,
    sample_size: int,
    schema_name: str = "",
):
    """Build a database-specific query for fetching random non-null samples."""
    limit = max(int(sample_size or 0), 1)
    quoted_col = _quote_identifier(column_name, db_type)
    quoted_table = _quote_table_name(table_name, db_type, schema_name=schema_name)

    if db_type in ("mysql", "postgresql"):
        random_func = _random_order_func(db_type)
        return text(
            f"SELECT {quoted_col} FROM {quoted_table} "
            f"WHERE {quoted_col} IS NOT NULL "
            f"ORDER BY {random_func} LIMIT {limit}"
        )

    if db_type == "sqlserver":
        return text(
            f"SELECT TOP {limit} {quoted_col} FROM {quoted_table} "
            f"WHERE {quoted_col} IS NOT NULL "
            f"ORDER BY NEWID()"
        )

    if db_type == "oracle":
        return text(
            f"SELECT {quoted_col} FROM {quoted_table} "
            f"WHERE {quoted_col} IS NOT NULL "
            f"ORDER BY DBMS_RANDOM.VALUE FETCH FIRST {limit} ROWS ONLY"
        )

    random_func = _random_order_func(db_type)
    return text(
        f"SELECT {quoted_col} FROM {quoted_table} "
        f"WHERE {quoted_col} IS NOT NULL "
        f"ORDER BY {random_func}"
    )


def _validate_schema_required(db_url: str, schema_name: str) -> Dict[str, Any] | None:
    """Validate that schema_name is provided for PostgreSQL, SQL Server and Oracle."""
    db_type = _detect_db_type(db_url)
    if db_type in ("postgresql", "sqlserver", "oracle"):
        if not schema_name or not schema_name.strip():
            examples = {
                "postgresql": "'public' for PostgreSQL",
                "sqlserver": "'dbo' for SQL Server",
                "oracle": "schema name (e.g., 'HR', 'SCOTT') for Oracle"
            }
            return _error(
                "SCHEMA_NAME_REQUIRED",
                f"--schema-name is required for {db_type}. Please specify the schema name (e.g., {examples[db_type]})"
            )
    return None


def _extract_schema_name(db_url: str, schema_name_override: str = "") -> str:
    """
    Extract schema/database name from URL.

    For MySQL/SQL Server without explicit schema: extract database name from URL path.
    For PostgreSQL/SQL Server with --schema-name parameter: use the provided value.
    """
    db_type = _detect_db_type(db_url)

    # Use explicit schema name parameter if provided
    if schema_name_override:
        return schema_name_override.strip()

    # MySQL: extract from URL path
    if db_type == "mysql":
        base = db_url.split("?")[0]
        name = base.rsplit("/", 1)[-1] if "/" in base else ""
        return name or "unknown_db"

    # PostgreSQL/SQL Server without explicit schema (should be caught by validation)
    # This is a fallback that should not normally be reached
    return ""


def _resolve_db_tables(all_tables: List[str], selected_tables: List[str]) -> Tuple[List[str], List[str], List[str]]:
    """
    Return (full_names, short_names, missing_selected_names)
    DB sampling helper expects short table names.
    """
    if not selected_tables:
        full_names = sorted(all_tables)
        short_names = [name.split(".")[-1] for name in full_names]
        return full_names, short_names, []

    full_set = set(all_tables)
    short_map = {name.split(".")[-1]: name for name in all_tables}
    resolved_full: List[str] = []
    resolved_short: List[str] = []
    missing: List[str] = []

    for item in selected_tables:
        full_name = item if item in full_set else short_map.get(item)
        if not full_name:
            missing.append(item)
            continue
        if full_name not in resolved_full:
            resolved_full.append(full_name)
            resolved_short.append(full_name.split(".")[-1])
    return resolved_full, resolved_short, missing


def _get_table_comment_mysql(engine, schema_name: str, table_name: str) -> str:
    """Get table comment from MySQL INFORMATION_SCHEMA."""
    try:
        sql = text(
            """
            SELECT TABLE_COMMENT
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = :schema_name
              AND TABLE_NAME = :table_name
            """
        )
        with engine.connect() as conn:
            row = conn.execute(sql, {"schema_name": schema_name, "table_name": table_name}).fetchone()
        if row and row[0]:
            return str(row[0])
    except Exception:
        pass
    return ""


def _get_table_comment_postgresql(engine, schema_name: str, table_name: str) -> str:
    """Get table comment from PostgreSQL pg_catalog."""
    try:
        sql = text(
            """
            SELECT obj_description(c.oid, 'pg_class') as comment
            FROM pg_catalog.pg_class c
            JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname = :schema_name
              AND c.relname = :table_name
              AND c.relkind = 'r'
            """
        )
        with engine.connect() as conn:
            row = conn.execute(sql, {"schema_name": schema_name, "table_name": table_name}).fetchone()
        if row and row[0]:
            return str(row[0])
    except Exception:
        pass
    return ""


def _get_table_comment_sqlserver(engine, schema_name: str, table_name: str) -> str:
    """Get table comment from SQL Server extended properties."""
    try:
        sql = text(
            """
            SELECT P.value
            FROM sys.extended_properties P
            JOIN sys.tables T ON P.major_id = T.object_id
            JOIN sys.schemas S ON T.schema_id = S.schema_id
            WHERE T.name = :table_name
              AND S.name = :schema_name
              AND P.name = 'MS_Description'
              AND P.minor_id = 0
            """
        )
        with engine.connect() as conn:
            row = conn.execute(sql, {"table_name": table_name, "schema_name": schema_name}).fetchone()
        if row and row[0]:
            return str(row[0])
    except Exception:
        pass
    return ""


def _get_table_comment_oracle(engine, schema_name: str, table_name: str) -> str:
    """Get table comment from Oracle ALL_TAB_COMMENTS."""
    try:
        sql = text(
            """
            SELECT COMMENTS
            FROM ALL_TAB_COMMENTS
            WHERE OWNER = UPPER(:schema_name)
              AND TABLE_NAME = UPPER(:table_name)
              AND TABLE_TYPE = 'TABLE'
            """
        )
        with engine.connect() as conn:
            row = conn.execute(sql, {"schema_name": schema_name, "table_name": table_name}).fetchone()
        if row and row[0]:
            return str(row[0])
    except Exception:
        pass
    return ""


def _get_table_comment(engine, db_type: str, schema_name: str, table_name: str) -> str:
    """Dispatch to database-specific table comment retrieval."""
    if db_type == "mysql":
        return _get_table_comment_mysql(engine, schema_name, table_name)
    elif db_type == "postgresql":
        return _get_table_comment_postgresql(engine, schema_name, table_name)
    elif db_type == "sqlserver":
        return _get_table_comment_sqlserver(engine, schema_name, table_name)
    elif db_type == "oracle":
        return _get_table_comment_oracle(engine, schema_name, table_name)
    else:
        return _get_table_comment_mysql(engine, schema_name, table_name)


def _get_column_comments_mysql(engine, schema_name: str, table_name: str) -> Dict[str, str]:
    """Get column comments from MySQL INFORMATION_SCHEMA."""
    column_comments: Dict[str, str] = {}
    try:
        sql = text(
            """
            SELECT COLUMN_NAME, COLUMN_COMMENT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = :schema_name
              AND TABLE_NAME = :table_name
            """
        )
        with engine.connect() as conn:
            rows = conn.execute(sql, {"schema_name": schema_name, "table_name": table_name}).fetchall()
        for row in rows:
            if row and row[0]:
                column_comments[str(row[0])] = str(row[1] or "")
    except Exception:
        pass
    return column_comments


def _get_column_comments_postgresql(engine, schema_name: str, table_name: str) -> Dict[str, str]:
    """Get column comments from PostgreSQL pg_catalog."""
    column_comments: Dict[str, str] = {}
    try:
        sql = text(
            """
            SELECT a.attname, pgd.description
            FROM pg_catalog.pg_attribute a
            JOIN pg_catalog.pg_class c ON a.attrelid = c.oid
            JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
            LEFT JOIN pg_catalog.pg_description pgd ON pgd.objoid = c.oid AND pgd.objsubid = a.attnum
            WHERE n.nspname = :schema_name
              AND c.relname = :table_name
              AND a.attnum > 0
              AND NOT a.attisdropped
            """
        )
        with engine.connect() as conn:
            rows = conn.execute(sql, {"schema_name": schema_name, "table_name": table_name}).fetchall()
        for row in rows:
            if row and row[0]:
                column_comments[str(row[0])] = str(row[1]) if row[1] else ""
    except Exception:
        pass
    return column_comments


def _get_column_comments_sqlserver(engine, schema_name: str, table_name: str) -> Dict[str, str]:
    """Get column comments from SQL Server extended properties."""
    column_comments: Dict[str, str] = {}
    try:
        sql = text(
            """
            SELECT C.name, P.value
            FROM sys.columns C
            INNER JOIN sys.tables T ON C.object_id = T.object_id
            INNER JOIN sys.schemas S ON T.schema_id = S.schema_id
            LEFT JOIN sys.extended_properties P ON P.major_id = C.object_id
                AND P.minor_id = C.column_id
                AND P.name = 'MS_Description'
            WHERE T.name = :table_name
              AND S.name = :schema_name
            """
        )
        with engine.connect() as conn:
            rows = conn.execute(sql, {"table_name": table_name, "schema_name": schema_name}).fetchall()
        for row in rows:
            if row and row[0]:
                column_comments[str(row[0])] = str(row[1]) if row[1] else ""
    except Exception:
        pass
    return column_comments


def _get_column_comments_oracle(engine, schema_name: str, table_name: str) -> Dict[str, str]:
    """Get column comments from Oracle ALL_COL_COMMENTS."""
    column_comments: Dict[str, str] = {}
    try:
        sql = text(
            """
            SELECT COLUMN_NAME, COMMENTS
            FROM ALL_COL_COMMENTS
            WHERE OWNER = UPPER(:schema_name)
              AND TABLE_NAME = UPPER(:table_name)
            """
        )
        with engine.connect() as conn:
            rows = conn.execute(sql, {"schema_name": schema_name, "table_name": table_name}).fetchall()
        for row in rows:
            if row and row[0]:
                column_comments[str(row[0])] = str(row[1]) if row[1] else ""
    except Exception:
        pass
    return column_comments


def _get_column_comments(engine, db_type: str, schema_name: str, table_name: str) -> Dict[str, str]:
    """Dispatch to database-specific column comment retrieval."""
    if db_type == "mysql":
        return _get_column_comments_mysql(engine, schema_name, table_name)
    elif db_type == "postgresql":
        return _get_column_comments_postgresql(engine, schema_name, table_name)
    elif db_type == "sqlserver":
        return _get_column_comments_sqlserver(engine, schema_name, table_name)
    elif db_type == "oracle":
        return _get_column_comments_oracle(engine, schema_name, table_name)
    else:
        return _get_column_comments_mysql(engine, schema_name, table_name)


def _replace_table_prefix(name: str, old_prefix: str, new_prefix: str) -> str:
    if not name:
        return name
    if old_prefix and name.startswith(f"{old_prefix}."):
        return f"{new_prefix}.{name.split('.', 1)[1]}"
    return name


def _remap_excel_table_prefix(
    content_data: Dict[str, Any],
    target_db_name: str,
    uploaded_db_name: str = "",
) -> Dict[str, Any]:
    """
    Remap upstream table prefix to original excel filename.

    The upstream may return prefixes such as:
    - db_name in payload
    - "excel"
    - uploaded temp filename stem
    """
    if not isinstance(content_data, dict):
        return content_data

    result = dict(content_data)

    candidate_old_prefixes: List[str] = []
    payload_db_name = str(result.get("db_name") or "").strip()
    if payload_db_name:
        candidate_old_prefixes.append(payload_db_name)
    if uploaded_db_name:
        candidate_old_prefixes.append(uploaded_db_name)
    candidate_old_prefixes.append("excel")
    # Keep order but remove duplicates
    candidate_old_prefixes = list(dict.fromkeys(candidate_old_prefixes))

    tables = result.get("tables", {})
    if isinstance(tables, dict):
        new_tables: Dict[str, Any] = {}
        for table_name, table_info in tables.items():
            new_name = str(table_name)
            for old_prefix in candidate_old_prefixes:
                if old_prefix and old_prefix != target_db_name:
                    new_name = _replace_table_prefix(new_name, old_prefix, target_db_name)
            new_tables[new_name] = table_info
        result["tables"] = new_tables

    table_names = result.get("table_names", [])
    if isinstance(table_names, list):
        remapped_table_names: List[str] = []
        for name in table_names:
            new_name = str(name)
            for old_prefix in candidate_old_prefixes:
                if old_prefix and old_prefix != target_db_name:
                    new_name = _replace_table_prefix(new_name, old_prefix, target_db_name)
            remapped_table_names.append(new_name)
        result["table_names"] = remapped_table_names

    semantic_model = result.get("semantic_model", [])
    if isinstance(semantic_model, list):
        for model in semantic_model:
            if not isinstance(model, dict):
                continue
            datasets = model.get("datasets", [])
            if not isinstance(datasets, list):
                continue
            for dataset in datasets:
                if not isinstance(dataset, dict):
                    continue
                source = dataset.get("source")
                if isinstance(source, str):
                    new_source = source
                    for old_prefix in candidate_old_prefixes:
                        if old_prefix and old_prefix != target_db_name:
                            new_source = _replace_table_prefix(new_source, old_prefix, target_db_name)
                    dataset["source"] = new_source

    result["db_name"] = target_db_name
    return result


def _enrich_enum_value_list(db_url: str, db_type: str, knowledge_data: Dict[str, Any]) -> Dict[str, Any]:
    """Fill enum value_list by SELECT DISTINCT for DB branch."""
    if not isinstance(knowledge_data, dict):
        return knowledge_data

    engine = create_engine(db_url)
    try:
        tables = knowledge_data.get("tables", {})
        if isinstance(tables, dict):
            for table_name, table_info in tables.items():
                fields = table_info.get("fields", []) if isinstance(table_info, dict) else []
                short_table = str(table_name).split(".")[-1]
                for field in fields:
                    ai_ctx = field.get("ai_context", {}) if isinstance(field, dict) else {}
                    if ai_ctx.get("ai_type") != "enum":
                        continue
                    col_name = field.get("name")
                    if not col_name:
                        continue
                    try:
                        quoted_col = _quote_identifier(col_name, db_type)
                        quoted_table = _quote_identifier(short_table, db_type)
                        random_func = _random_order_func(db_type)
                        distinct_query = text(
                            f"SELECT DISTINCT {quoted_col} FROM {quoted_table} "
                            f"WHERE {quoted_col} IS NOT NULL ORDER BY {random_func}"
                        )
                        with engine.connect() as conn:
                            values = conn.execute(distinct_query).fetchall()
                        ai_ctx["value_list"] = [str(v[0]) for v in values]
                        ai_ctx["ai_type"] = "enum"
                        field["ai_context"] = ai_ctx
                    except Exception:
                        continue
    finally:
        engine.dispose()
    return knowledge_data


def _discover_db_tables(db_url: str, schema_name: str = "") -> Dict[str, Any]:
    engine = create_engine(db_url)
    try:
        inspector = inspect(engine)
        db_type = _detect_db_type(db_url)
        schema = _extract_schema_name(db_url, schema_name_override=schema_name)

        # Get table names (sqlalchemy handles schema filtering internally)
        if db_type in ("postgresql", "sqlserver", "oracle"):
            # For these databases, use schema-aware inspection
            table_names = sorted(inspector.get_table_names(schema=schema))
        else:
            table_names = sorted(inspector.get_table_names())

        full_names = [f"{schema}.{name}" for name in table_names]
        return {
            "success": True,
            "db_type": db_type,
            "db_name": schema,
            "table_names": full_names,
            "short_table_names": table_names,
        }
    finally:
        engine.dispose()


def _get_foreign_keys(engine, db_type: str, db_name: str, table_list: List[str]) -> Dict[str, Dict[str, Any]]:
    """

    Returns:
        Dict: {fk_name: {from_table, from_columns, to_table, to_columns}, ...}
    """
    fk_dict: Dict[str, Dict[str, Any]] = {}
    if not table_list:
        return fk_dict

    schema_name_list = sorted({t.split(".")[-2] for t in table_list if "." in t})
    if len(schema_name_list) == 1:
        schema_name_str = "('" + schema_name_list[0] + "')"
    else:
        schema_name_str = str(tuple(schema_name_list))

    table_name_list = sorted({t.split(".")[-1] for t in table_list})
    if len(table_name_list) == 1:
        table_name_str = "('" + table_name_list[0] + "')"
    else:
        table_name_str = str(tuple(table_name_list))

    try:
        if db_type == "mysql":
            sql = f"""
                SELECT
                    k.CONSTRAINT_NAME as fk_name,
                    k.TABLE_NAME as from_table,
                    k.COLUMN_NAME as from_column,
                    k.REFERENCED_TABLE_NAME as to_table,
                    k.REFERENCED_COLUMN_NAME as to_column
                FROM information_schema.KEY_COLUMN_USAGE k
                WHERE k.REFERENCED_TABLE_NAME IS NOT NULL
                AND k.TABLE_SCHEMA = '{db_name}'
                AND k.REFERENCED_TABLE_SCHEMA = '{db_name}'
            """
            if table_name_list:
                sql = sql + " AND k.TABLE_NAME in " + table_name_str
                sql = sql + " AND k.REFERENCED_TABLE_NAME in " + table_name_str

        elif db_type == "postgresql":
            sql = """
                SELECT
                    tc.constraint_name as fk_name,
                    tc.table_name as from_table,
                    kcu.column_name as from_column,
                    ccu.table_name AS to_table,
                    ccu.column_name AS to_column,
                    tc.constraint_schema AS from_schema,
                    ccu.constraint_schema AS to_schema
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
            """
            if schema_name_str and table_name_str:
                sql += f" AND tc.constraint_schema in {schema_name_str} AND tc.table_name in {table_name_str}"

        elif db_type in ("sqlserver", "mssql"):
            sql = """
                SELECT
                    fk.name AS fk_name,
                    tp.name AS from_table,
                    cp.name AS from_column,
                    tr.name AS to_table,
                    cr.name AS to_column,
                    SCHEMA_NAME(tp.schema_id) as from_schema,
                    SCHEMA_NAME(tr.schema_id) as to_schema
                FROM sys.foreign_keys AS fk
                INNER JOIN sys.foreign_key_columns AS fkc ON fk.object_id = fkc.constraint_object_id
                INNER JOIN sys.tables AS tp ON fkc.parent_object_id = tp.object_id
                INNER JOIN sys.columns AS cp ON fkc.parent_object_id = cp.object_id AND fkc.parent_column_id = cp.column_id
                INNER JOIN sys.tables AS tr ON fkc.referenced_object_id = tr.object_id
                INNER JOIN sys.columns AS cr ON fkc.referenced_object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id
            """
            if schema_name_str and table_name_str:
                sql += f" WHERE SCHEMA_NAME(tp.schema_id) in {schema_name_str} AND tp.name in {table_name_str}"

        elif db_type == "oracle":
            sql = """
                SELECT
                    a.constraint_name as fk_name,
                    a.table_name as from_table,
                    b.column_name as from_column,
                    c.table_name as to_table,
                    d.column_name as to_column,
                    a.owner as from_owner,
                    c.owner as to_owner
                FROM all_constraints a
                JOIN all_cons_columns b ON a.constraint_name = b.constraint_name AND a.table_name = b.table_name
                JOIN all_constraints c ON a.r_constraint_name = c.constraint_name
                JOIN all_cons_columns d ON c.constraint_name = d.constraint_name AND d.position = b.position
                WHERE a.constraint_type = 'R'
            """
            if schema_name_str and table_name_str:
                schema_name_str = schema_name_str.upper()
                table_name_str = table_name_str.upper()
                sql += f" AND a.owner in {schema_name_str} AND a.table_name in {table_name_str}"
        else:
            return fk_dict

        with engine.connect() as conn:
            result = conn.execute(text(sql))
            for row in result.fetchall():
                if row and row[0]:
                    if row[0] in fk_dict:
                        fk_dict[row[0]]["from_columns"].append(row[2])
                        fk_dict[row[0]]["to_columns"].append(row[4])
                    elif db_type in ("mssql", "sqlserver", "oracle", "postgresql"):
                        fk_dict[row[0]] = {
                            "from_table": row[5].lower() + "." + row[1].lower(),
                            "from_columns": [row[2]],
                            "to_table": row[6].lower() + "." + row[3].lower(),
                            "to_columns": [row[4]],
                        }
                    else:
                        fk_dict[row[0]] = {
                            "from_table": db_name + "." + row[1],
                            "from_columns": [row[2]],
                            "to_table": db_name + "." + row[3],
                            "to_columns": [row[4]],
                        }
    except Exception:
        return fk_dict

    return fk_dict


def _sample_table_data(
    engine,
    db_type: str,
    table_name: str,
    columns_info: List[Dict[str, Any]],
    sample_size: int,
) -> Dict[str, Any]:
    """

    Returns:
        Dict: {column_name: {"sample_values": [], "unique_count": int, "total_count": int}, ...}
    """
    result: Dict[str, Any] = {"_row_count": 0}
    if sample_size <= 0:
        return result

    try:
        if db_type in ("sqlserver", "mssql"):
            query = f"SELECT TOP {sample_size} * FROM {table_name} TABLESAMPLE ({sample_size} ROWS)"
        elif db_type == "postgresql":
            query = f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT {sample_size}"
        elif db_type == "oracle":
            query = f"SELECT * FROM {table_name} ORDER BY DBMS_RANDOM.VALUE FETCH FIRST {sample_size} ROWS ONLY"
        else:
            query = f"SELECT * FROM {table_name} ORDER BY RAND() LIMIT {sample_size}"

        with engine.connect() as conn:
            db_result = conn.execute(text(query))
            rows = db_result.fetchall()
            result["_row_count"] = len(rows)

            columns = db_result.keys()
            columns_map = {col: idx for idx, col in enumerate(columns)}

            for col_info in columns_info:
                col_name = col_info["name"]
                if col_name not in columns_map:
                    continue

                col_type = col_info["type"]
                col_idx = columns_map[col_name]
                sample_values = [row[col_idx] for row in rows if row[col_idx] is not None]
                unique_values = list(set(sample_values))

                if "char" in col_type.lower() and (
                    len(unique_values) < 10 or len(unique_values) < sample_size * 0.1
                ):
                    # Read all distinct values for low-cardinality varchar-like columns.
                    distinct_query = f"SELECT DISTINCT {_quote_identifier(col_name, db_type)} FROM {table_name}"
                    distinct_result = conn.execute(text(distinct_query))
                    all_unique_values = distinct_result.fetchall()
                    unique_values = [v[0] for v in all_unique_values]

                    result[col_name] = {
                        "sample_values": unique_values,
                        "unique_count": len(unique_values) if unique_values else 0,
                        "total_count": len(unique_values),
                    }
                else:
                    result[col_name] = {
                        "sample_values": unique_values[:100],
                        "unique_count": len(unique_values) if unique_values else 0,
                        "total_count": len(sample_values),
                    }
    except Exception:
        return result

    return result


def _read_with_samples(
    db_url: str,
    table_list: List[str],
    sample_size: int = 2000,
    schema_name: str = "",
) -> Dict[str, Any]:
    engine = create_engine(db_url)
    db_type = _detect_db_type(db_url)
    schema = _extract_schema_name(db_url, schema_name_override=schema_name)
    inspector = inspect(engine)

    if not table_list:
        if db_type in ("postgresql", "sqlserver", "oracle"):
            short_tables = inspector.get_table_names(schema=schema)
        else:
            short_tables = inspector.get_table_names()
    else:
        short_tables = table_list

    tables: Dict[str, Any] = {}

    try:
        for table_name in short_tables:
            if "." in table_name:
                full_name = table_name
                current_schema = table_name.split(".")[-2]
                short_table_name = table_name.split(".")[-1]
            else:
                short_table_name = table_name
                current_schema = schema
                full_name = f"{current_schema}.{short_table_name}"

            columns_raw = inspector.get_columns(
                short_table_name,
                schema=current_schema if db_type != "mysql" else None,
            )
            columns: List[Dict[str, Any]] = []
            column_comments = _get_column_comments(engine, db_type, current_schema, short_table_name)
            table_comment = _get_table_comment(engine, db_type, current_schema, short_table_name)

            for col in columns_raw:
                col_name = col["name"]
                if db_type == "oracle":
                    column_comment = column_comments.get(col_name.upper(), "")
                else:
                    column_comment = column_comments.get(col_name, str(col.get("comment", "") or ""))

                columns.append(
                    {
                        "name": col_name,
                        "type": str(col.get("type", "text")),
                        "nullable": bool(col.get("nullable", True)),
                        "default": str(col.get("default", "")) if col.get("default") is not None else "",
                        "primary_key": bool(col.get("primary_key", False)),
                        "comment": column_comment,
                    }
                )

            sample_data = {"_row_count": 0}
            if sample_size > 0:
                quoted_table = _quote_table_name(
                    short_table_name,
                    db_type,
                    schema_name=current_schema if db_type != "mysql" else current_schema,
                )
                sample_data = _sample_table_data(
                    engine=engine,
                    db_type=db_type,
                    table_name=quoted_table,
                    columns_info=columns,
                    sample_size=sample_size,
                )

                for col_info in columns:
                    col_name = col_info["name"]
                    if col_name in sample_data:
                        col_info["sample_values"] = sample_data[col_name]["sample_values"]
                        col_info["unique_count"] = sample_data[col_name]["unique_count"]
                        col_info["total_count"] = sample_data[col_name]["total_count"]

            tables[full_name] = {
                "columns": columns,
                "column_count": len(columns),
                "comment": table_comment,
                "row_count": sample_data.get("_row_count", 0),
            }

        foreign_keys = _get_foreign_keys(engine, db_type, schema, list(tables.keys()))

        return {
            "success": True,
            "source_type": "database",
            "db_url": db_url,
            "db_type": db_type,
            "db_name": schema,
            "table_count": len(tables),
            "table_names": list(tables.keys()),
            "tables": tables,
            "foreign_keys": foreign_keys,
        }
    finally:
        engine.dispose()


def discover_from_db(db_url: str, schema_name: str = "") -> Dict[str, Any]:
    if not db_url:
        return _error("INVALID_INPUT", "db_url is required")

    db_type = _detect_db_type(db_url)
    supported_prefixes = (
        "mysql://",
        "mysql+pymysql://",
        "postgresql://",
        "postgresql+psycopg2://",
        "mssql://",
        "mssql+pymssql://",
        "oracle://",
        "oracle+cx_oracle://",
        "oracle+oracledb://",
    )
    if not any(db_url.startswith(p) for p in supported_prefixes):
        return _error("INVALID_INPUT", f"Unsupported db_url format. Supported: mysql, postgresql, mssql, oracle")

    # Validate schema name for PostgreSQL, SQL Server and Oracle
    schema_error = _validate_schema_required(db_url, schema_name)
    if schema_error:
        return schema_error

    # Validate Oracle URL format (must include service_name parameter)
    oracle_url_error = _validate_oracle_url_format(db_url)
    if oracle_url_error:
        return oracle_url_error

    normalized_url = _normalize_db_url(db_url)
    try:
        data = _discover_db_tables(normalized_url, schema_name=schema_name)
        if not data.get("success"):
            return _error("UPSTREAM_ERROR", "Failed to discover tables from database")
        tables = sorted(data.get("table_names", []))
        return {
            "success": True,
            "source_type": "database",
            "db_type": data.get("db_type", ""),
            "db_url": normalized_url,
            "db_name": data.get("db_name", ""),
            "table_names": tables,
            "table_count": len(tables),
        }
    except Exception as exc:  # noqa: BLE001
        return _error("UPSTREAM_ERROR", f"Failed to discover tables from database: {exc}")


def discover_from_excel(excel_file: str) -> Dict[str, Any]:
    if not excel_file:
        return _error("INVALID_INPUT", "excel_file is required")
    ext = os.path.splitext(excel_file)[1].lower()
    if ext not in (".xlsx", ".xls"):
        return _error("INVALID_INPUT", "excel_file must be .xlsx or .xls")
    try:
        sheets = list_excel_sheets(excel_file)
        return {
            "success": True,
            "source_type": "excel",
            "sheet_names": sheets,
            "sheet_count": len(sheets),
        }
    except Exception as exc:  # noqa: BLE001
        return _error("UPSTREAM_ERROR", f"Failed to read excel sheets: {exc}")


def generate_from_db(
    db_url: str,
    selected_tables: List[str],
    topic_name: str,
    output_path: str,
    schema_name: str = "",
) -> Dict[str, Any]:
    if not topic_name:
        return _error("INVALID_INPUT", "topic_name is required")

    # Validate schema name for PostgreSQL and SQL Server
    schema_error = _validate_schema_required(db_url, schema_name)
    if schema_error:
        return schema_error

    discover = discover_from_db(db_url, schema_name=schema_name)
    if not discover.get("success"):
        return discover

    all_tables = discover["table_names"]
    full_names, short_names, missing = _resolve_db_tables(all_tables, selected_tables)
    if missing:
        return _error(
            "TABLE_OR_SHEET_NOT_FOUND",
            f"Selected tables not found: {', '.join(missing)}",
            missing=missing,
        )

    db_type = discover.get("db_type", "mysql")

    try:
        data = _read_with_samples(discover["db_url"], short_names, schema_name=schema_name)
        if not data.get("success"):
            return _error("UPSTREAM_ERROR", data.get("message", "Failed to read selected tables"))
    except Exception as exc:  # noqa: BLE001
        return _error("UPSTREAM_ERROR", f"Failed to read selected tables: {exc}")

    try:
        upstream_data = {
            "tables": data.get("tables", {}),
            "foreign_keys": data.get("foreign_keys", {}),
            "source_type": "database",
            "db_name": data.get("db_name", _extract_schema_name(discover["db_url"], schema_name_override=schema_name)),
        }
        upstream_payload = _normalize_for_json(upstream_data)
        # print(upstream_data)
        upload_result = upload_database_for_knowledge(
            table_data=upstream_payload,
            api_url="https://asksql.ai/ask/api/generate_database_knowledge",
            timeout=30,
        )
        content_data = upload_result["content_data"]
        content_data = _enrich_enum_value_list(discover["db_url"], db_type, content_data)
        result = generate_yaml_file(
            topic_name=topic_name,
            tables_data=content_data,
            selected_tables=full_names,
            output_path=output_path,
            db_type=_to_yaml_db_type(db_type),
        )
        result["source_type"] = "database"
        result["db_type"] = db_type
        return result
    except Exception as exc:  # noqa: BLE001
        return _error("UPSTREAM_ERROR", f"Failed to call generate_database_knowledge for db tables: {exc}")


def generate_from_excel(
    excel_file: str,
    selected_tables: List[str],
    topic_name: str,
    output_path: str,
    api_url: str,
    timeout: int,
    target_db_type: str,
) -> Dict[str, Any]:
    if not topic_name:
        return _error("INVALID_INPUT", "topic_name is required")
    normalized_target_db_type = _to_yaml_db_type(target_db_type)
    if normalized_target_db_type not in ("mysql", "sql_server", "postgresql", "oracle"):
        return _error(
            "INVALID_INPUT",
            "target_db_type is required for excel source and must be one of: mysql, sql_server, postgresql, oracle",
        )

    discover = discover_from_excel(excel_file)
    if not discover.get("success"):
        return discover

    all_sheets = discover["sheet_names"]
    target_sheets = selected_tables or all_sheets

    temp_excel = ""
    try:
        temp_excel, missing = create_subset_excel(excel_file, target_sheets)
        if missing:
            return _error(
                "TABLE_OR_SHEET_NOT_FOUND",
                f"Selected sheets not found: {', '.join(missing)}",
                missing=missing,
            )
        if not temp_excel:
            return _error("INVALID_INPUT", "No valid sheets selected")
        upload_result = upload_excel_for_knowledge(temp_excel, api_url=api_url, timeout=timeout)
        content_data = upload_result["content_data"]
        original_db_name = os.path.splitext(os.path.basename(excel_file))[0]
        uploaded_db_name = os.path.splitext(os.path.basename(temp_excel))[0]
        content_data = _remap_excel_table_prefix(
            content_data,
            target_db_name=original_db_name,
            uploaded_db_name=uploaded_db_name,
        )

        try:
            result = generate_yaml_file(
                topic_name=topic_name,
                tables_data=content_data,
                selected_tables=target_sheets,
                output_path=output_path,
                db_type=normalized_target_db_type,
            )
            result["source_type"] = "excel"
            return result
        except Exception as exc:  # noqa: BLE001
            return _error("YAML_GENERATION_ERROR", f"Failed to generate yaml: {exc}")
    except Exception as exc:  # noqa: BLE001
        return _error("UPSTREAM_ERROR", f"Failed to process excel/upload: {exc}")
    finally:
        if temp_excel and os.path.exists(temp_excel):
            os.remove(temp_excel)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate yaml semantic file from db url or excel")
    parser.add_argument("--action", required=True, choices=["discover", "generate"], help="discover or generate")
    parser.add_argument("--db-url", help="Database url (mysql/postgresql/mssql/oracle)")
    parser.add_argument("--excel-file", help="Excel file path (.xlsx/.xls)")
    parser.add_argument("--selected-tables", default="", help="Comma-separated selected tables")
    parser.add_argument("--topic-name", default="", help="Topic name for generated yaml")
    parser.add_argument("--output-path", default="./output", help="Output directory for yaml")
    parser.add_argument("--api-url", default="https://asksql.ai/ask/api/generate_database_knowledge", help="Excel upload API")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout seconds")
    parser.add_argument("--schema-name", required=False, help="Schema name (REQUIRED for PostgreSQL/SQL Server, e.g., 'public' or 'dbo')")
    parser.add_argument("--target-db-type", required=False, help="Target db type for excel source: mysql/sql_server/postgresql/oracle")
    args = parser.parse_args()

    if bool(args.db_url) == bool(args.excel_file):
        print(json.dumps(_error("INVALID_INPUT", "Provide exactly one of --db-url or --excel-file"), ensure_ascii=False, indent=2))
        sys.exit(1)

    if args.action == "discover":
        if args.db_url:
            result = discover_from_db(args.db_url, schema_name=args.schema_name or "")
        else:
            result = discover_from_excel(args.excel_file)
    else:
        if not args.topic_name:
            result = _error("INVALID_INPUT", "topic_name is required when action=generate")
        elif args.db_url:
            result = generate_from_db(
                db_url=args.db_url,
                selected_tables=_split_csv(args.selected_tables),
                topic_name=args.topic_name,
                output_path=args.output_path,
                schema_name=args.schema_name or "",
            )
        else:
            result = generate_from_excel(
                excel_file=args.excel_file,
                selected_tables=_split_csv(args.selected_tables),
                topic_name=args.topic_name,
                output_path=args.output_path,
                api_url=args.api_url,
                timeout=args.timeout,
                target_db_type=args.target_db_type or "",
            )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
