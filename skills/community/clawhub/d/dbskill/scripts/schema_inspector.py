from __future__ import annotations

import logging
from typing import Any, Dict, List

from connection_manager import ConnectionManager
from exceptions import QueryError

logger = logging.getLogger(__name__)

_DB_DIALECT = {
    "pymysql": "mysql",
    "psycopg2": "postgresql",
    "oracledb": "oracle",
    "pymssql": "sqlserver",
    "sqlite3": "sqlite",
}


def _detect_dialect(cm: ConnectionManager) -> str:
    return _DB_DIALECT.get(cm._driver, "mysql")


class SchemaInspector:
    """Introspects database schema metadata.

    Supports MySQL, PostgreSQL, Oracle, SQL Server, and SQLite
    via ``information_schema`` or database-specific queries.
    """

    def __init__(self, connection_manager: ConnectionManager) -> None:
        self._cm = connection_manager

    def get_tables(self) -> List[Dict[str, str]]:
        conn = None
        try:
            conn = self._cm.get_connection()
            dialect = _detect_dialect(self._cm)
            with conn.cursor() as cursor:
                if dialect == "mysql":
                    cursor.execute("SHOW FULL TABLES")
                elif dialect == "postgresql":
                    cursor.execute(
                        "SELECT table_name, table_type FROM information_schema.tables "
                        "WHERE table_schema = 'public'"
                    )
                elif dialect == "oracle":
                    cursor.execute(
                        "SELECT table_name, 'TABLE' FROM user_tables "
                        "UNION ALL "
                        "SELECT view_name, 'VIEW' FROM user_views"
                    )
                elif dialect == "sqlserver":
                    cursor.execute(
                        "SELECT table_name, table_type FROM information_schema.tables "
                        "WHERE table_catalog = DB_NAME()"
                    )
                else:
                    cursor.execute(
                        "SELECT name, type FROM sqlite_master "
                        "WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%'"
                    )
                rows = []
                for row in cursor.fetchall():
                    if isinstance(row, dict):
                        values = list(row.values())
                        rows.append({"name": values[0], "type": values[1]})
                    else:
                        rows.append({"name": row[0], "type": row[1]})
                return rows
        except Exception as exc:
            raise QueryError(f"Failed to retrieve tables: {exc}") from exc
        finally:
            self._cm.close_connection(conn)

    def get_columns(self, table_name: str) -> List[Dict[str, Any]]:
        conn = None
        try:
            conn = self._cm.get_connection()
            dialect = _detect_dialect(self._cm)
            safe_name = table_name.replace("'", "''")
            with conn.cursor() as cursor:
                if dialect == "mysql":
                    cursor.execute("SHOW FULL COLUMNS FROM `" + table_name.replace("`", "``") + "`")
                elif dialect == "postgresql":
                    cursor.execute(f"""
                        SELECT c.column_name, c.data_type, c.is_nullable,
                               c.column_default, tc.constraint_type
                        FROM information_schema.columns c
                        LEFT JOIN information_schema.key_column_usage kcu
                            ON c.table_name = kcu.table_name
                            AND c.column_name = kcu.column_name
                            AND kcu.table_schema = 'public'
                        LEFT JOIN information_schema.table_constraints tc
                            ON kcu.constraint_name = tc.constraint_name
                            AND tc.constraint_type = 'PRIMARY KEY'
                        WHERE c.table_name = '{safe_name}'
                    """)
                elif dialect == "oracle":
                    cursor.execute(f"""
                        SELECT c.column_name, c.data_type || '(' || c.data_length || ')',
                               c.nullable, c.data_default,
                               CASE WHEN pk.column_name IS NOT NULL THEN 'PRI' ELSE '' END
                        FROM user_tab_columns c
                        LEFT JOIN (
                            SELECT cc.column_name FROM user_cons_columns cc
                            JOIN user_constraints uc ON cc.constraint_name = uc.constraint_name
                            WHERE uc.constraint_type = 'P' AND cc.table_name = '{safe_name}'
                        ) pk ON c.column_name = pk.column_name
                        WHERE c.table_name = '{safe_name}'
                        ORDER BY c.column_id
                    """)
                elif dialect == "sqlserver":
                    cursor.execute(f"""
                        SELECT c.column_name, c.data_type + '(' + CAST(c.character_maximum_length AS VARCHAR) + ')',
                               c.is_nullable, c.column_default,
                               CASE WHEN pk.column_name IS NOT NULL THEN 'PRI' ELSE '' END
                        FROM information_schema.columns c
                        LEFT JOIN (
                            SELECT kcu.column_name FROM information_schema.key_column_usage kcu
                            JOIN information_schema.table_constraints tc
                                ON kcu.constraint_name = tc.constraint_name
                            WHERE tc.constraint_type = 'PRIMARY KEY'
                              AND kcu.table_name = '{safe_name}'
                        ) pk ON c.column_name = pk.column_name
                        WHERE c.table_name = '{safe_name}'
                        ORDER BY c.ordinal_position
                    """)
                else:
                    cursor.execute(f"PRAGMA table_info('{safe_name}')")

                columns: List[Dict[str, Any]] = []
                for row in cursor.fetchall():
                    if isinstance(row, dict):
                        if dialect == "mysql":
                            columns.append({
                                "name": row["Field"],
                                "type": row["Type"],
                                "nullable": row["Null"] == "YES",
                                "defaultValue": row.get("Default"),
                                "primaryKey": row["Key"] == "PRI",
                                "autoIncrement": "auto_increment" in (row.get("Extra") or "").lower(),
                            })
                        elif dialect == "sqlite":
                            columns.append({
                                "name": row["name"],
                                "type": row["type"],
                                "nullable": not row["notnull"],
                                "defaultValue": row.get("dflt_value"),
                                "primaryKey": bool(row["pk"]),
                                "autoIncrement": False,
                            })
                        else:
                            columns.append({
                                "name": row[0] if not isinstance(row, dict) else row.get("column_name"),
                                "type": row[1] if not isinstance(row, dict) else row.get("data_type"),
                                "nullable": (row[2] if not isinstance(row, dict) else row.get("is_nullable")) == "YES",
                                "defaultValue": row[3] if not isinstance(row, dict) else row.get("column_default"),
                                "primaryKey": (row[4] if not isinstance(row, dict) else row.get("constraint_type", "")) in ("PRI", "PRIMARY KEY", "P"),
                                "autoIncrement": False,
                            })
                    else:
                        if dialect == "mysql":
                            columns.append({
                                "name": row[0],
                                "type": row[1],
                                "nullable": row[3] == "YES",
                                "defaultValue": row[4],
                                "primaryKey": row[3] == "PRI",
                                "autoIncrement": "auto_increment" in str(row[5] or "").lower(),
                            })
                        elif dialect == "sqlite":
                            columns.append({
                                "name": row[1],
                                "type": row[2],
                                "nullable": not row[3],
                                "defaultValue": row[4],
                                "primaryKey": bool(row[5]),
                                "autoIncrement": False,
                            })
                        else:
                            columns.append({
                                "name": row[0],
                                "type": row[1],
                                "nullable": row[2] == "YES",
                                "defaultValue": row[3],
                                "primaryKey": row[4] in ("PRI", "PRIMARY KEY", "P"),
                                "autoIncrement": False,
                            })
                return columns
        except Exception as exc:
            raise QueryError(f"Failed to retrieve columns for {table_name}: {exc}") from exc
        finally:
            self._cm.close_connection(conn)

    def get_indexes(self, table_name: str) -> List[Dict[str, Any]]:
        conn = None
        try:
            conn = self._cm.get_connection()
            dialect = _detect_dialect(self._cm)
            safe_name = table_name.replace("'", "''")
            with conn.cursor() as cursor:
                if dialect == "mysql":
                    cursor.execute("SHOW INDEX FROM `" + table_name.replace("`", "``") + "`")
                elif dialect == "postgresql":
                    cursor.execute(f"""
                        SELECT i.relname, a.attname, ix.indisunique, ix.indisprimary
                        FROM pg_class t, pg_class i, pg_index ix, pg_attribute a
                        WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid
                          AND a.attrelid = t.oid AND a.attnum = ANY(ix.indkey)
                          AND t.relname = '{safe_name}'
                    """)
                elif dialect == "oracle":
                    cursor.execute(f"""
                        SELECT index_name, column_name, uniqueness
                        FROM user_ind_columns
                        JOIN user_indexes USING (index_name)
                        WHERE table_name = '{safe_name}'
                    """)
                elif dialect == "sqlserver":
                    cursor.execute(f"""
                        SELECT i.name, c.name, i.is_unique, i.is_primary_key
                        FROM sys.indexes i
                        JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
                        JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
                        WHERE i.object_id = OBJECT_ID('{safe_name}')
                    """)
                else:
                    cursor.execute(f"PRAGMA index_list('{safe_name}')")
                    pragma_rows = cursor.fetchall()
                    indexes = []
                    for idx_row in pragma_rows:
                        idx_name = idx_row[1] if not isinstance(idx_row, dict) else idx_row["name"]
                        unique = not idx_row[2] if not isinstance(idx_row, dict) else not idx_row["unique"]
                        cursor.execute(f"PRAGMA index_info('{idx_name.replace(chr(39), chr(39)+chr(39))}')")
                        for col_row in cursor.fetchall():
                            col_name = col_row[2] if not isinstance(col_row, dict) else col_row["name"]
                            ordinal = col_row[1] if not isinstance(col_row, dict) else col_row["seqno"]
                            indexes.append({
                                "name": idx_name,
                                "column": col_name,
                                "unique": unique,
                                "ordinal": ordinal,
                            })
                    return indexes
                indexes = []
                for row in cursor.fetchall():
                    if isinstance(row, dict):
                        if dialect == "mysql":
                            indexes.append({
                                "name": row["Key_name"],
                                "column": row["Column_name"],
                                "unique": not row["Non_unique"],
                                "ordinal": row["Seq_in_index"],
                            })
                        else:
                            indexes.append({
                                "name": row[0] if not isinstance(row, dict) else row.get("index_name") or row.get("name"),
                                "column": row[1] if not isinstance(row, dict) else row.get("column_name") or row.get("attname"),
                                "unique": not row[2] if not isinstance(row, dict) else not row.get("indisunique") or row.get("is_unique"),
                                "ordinal": 0,
                            })
                    else:
                        indexes.append({
                            "name": row[0],
                            "column": row[1],
                            "unique": not row[2],
                            "ordinal": 0,
                        })
                return indexes
        except Exception as exc:
            raise QueryError(f"Failed to retrieve indexes for {table_name}: {exc}") from exc
        finally:
            self._cm.close_connection(conn)

    def get_foreign_keys(self, table_name: str) -> List[Dict[str, Any]]:
        conn = None
        try:
            conn = self._cm.get_connection()
            dialect = _detect_dialect(self._cm)
            safe_name = table_name.replace("'", "''")
            with conn.cursor() as cursor:
                if dialect == "mysql":
                    cursor.execute(
                        "SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, "
                        "REFERENCED_COLUMN_NAME, CONSTRAINT_NAME "
                        "FROM information_schema.KEY_COLUMN_USAGE "
                        "WHERE TABLE_NAME = %s AND REFERENCED_TABLE_NAME IS NOT NULL",
                        (table_name,),
                    )
                elif dialect == "postgresql":
                    cursor.execute(f"""
                        SELECT kcu.column_name, ccu.table_name, ccu.column_name, rc.constraint_name
                        FROM information_schema.referential_constraints rc
                        JOIN information_schema.key_column_usage kcu
                            ON rc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage ccu
                            ON rc.unique_constraint_name = ccu.constraint_name
                        WHERE kcu.table_name = '{safe_name}'
                    """)
                elif dialect == "oracle":
                    cursor.execute(f"""
                        SELECT c.column_name, uc.table_name, uc.column_name, c.constraint_name
                        FROM user_cons_columns c
                        JOIN user_constraints u ON c.constraint_name = u.constraint_name
                        JOIN user_cons_columns uc ON u.r_constraint_name = uc.constraint_name
                        WHERE u.constraint_type = 'R' AND c.table_name = '{safe_name}'
                    """)
                elif dialect == "sqlserver":
                    cursor.execute(f"""
                        SELECT COL_NAME(fkc.parent_object_id, fkc.parent_column_id),
                               OBJECT_NAME(fkc.referenced_object_id),
                               COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id),
                               fk.name
                        FROM sys.foreign_keys fk
                        JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
                        WHERE OBJECT_NAME(fk.parent_object_id) = '{safe_name}'
                    """)
                else:
                    cursor.execute(f"PRAGMA foreign_key_list('{safe_name}')")
                    fks = []
                    for row in cursor.fetchall():
                        if isinstance(row, dict):
                            fks.append({
                                "fkColumn": row["from"],
                                "pkTable": row["table"],
                                "pkColumn": row["to"],
                                "fkName": "",
                            })
                        else:
                            fks.append({
                                "fkColumn": row[3],
                                "pkTable": row[2],
                                "pkColumn": row[4],
                                "fkName": "",
                            })
                    return fks

                fks: List[Dict[str, Any]] = []
                for row in cursor.fetchall():
                    if isinstance(row, dict):
                        fks.append({
                            "fkColumn": row.get("COLUMN_NAME") or row.get("column_name"),
                            "pkTable": row.get("REFERENCED_TABLE_NAME") or row.get("table_name") or row.get("TABLE_NAME"),
                            "pkColumn": row.get("REFERENCED_COLUMN_NAME") or row.get("column_name") or row.get("COLUMN_NAME"),
                            "fkName": row.get("CONSTRAINT_NAME") or row.get("constraint_name") or row.get("name"),
                        })
                    else:
                        fks.append({
                            "fkColumn": row[0],
                            "pkTable": row[1],
                            "pkColumn": row[2],
                            "fkName": row[3],
                        })
                return fks
        except Exception as exc:
            raise QueryError(
                f"Failed to retrieve foreign keys for {table_name}: {exc}"
            ) from exc
        finally:
            self._cm.close_connection(conn)
