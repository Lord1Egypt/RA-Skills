from __future__ import annotations

import logging
import re
from typing import Any, Callable, Dict, List, Optional

from connection_manager import ConnectionManager
from exceptions import QueryError

logger = logging.getLogger(__name__)

# Match '?' that is NOT preceded by another '?' (i.e. not a literal '??')
_PLACEHOLDER_RE = re.compile(r"(?<!\?)\?(?!\?)")


def convert_placeholders(sql: str) -> str:
    """Replace JDBC-style '?' placeholders with Python-style '%s'.

    '??' can be used as an escaped literal question mark (not recommended).
    """
    return _PLACEHOLDER_RE.sub("%s", sql)


class CaseInsensitiveDict(Dict[str, Any]):
    """A dictionary whose string-key lookups are case-insensitive.

    Stores the original casing as the canonical key and maintains a
    mapping from both ``upper()`` and ``lower()`` forms back to it.

    Example::

        d = CaseInsensitiveDict({"Name": "Alice"})
        d["name"]   # "Alice"
        d["NAME"]   # "Alice"
        d["Name"]   # "Alice"
    """

    def __init__(self, mapping: Optional[Dict[str, Any]] = None) -> None:
        super().__init__()
        self._key_map: Dict[str, str] = {}
        if mapping:
            for k, v in mapping.items():
                super().__setitem__(k, v)
                if isinstance(k, str):
                    self._key_map[k.upper()] = k
                    self._key_map[k.lower()] = k

    def __getitem__(self, key: Any) -> Any:
        if isinstance(key, str):
            mapped = self._key_map.get(key)
            if mapped is not None:
                return super().__getitem__(mapped)
            mapped = self._key_map.get(key.upper())
            if mapped is not None:
                return super().__getitem__(mapped)
            mapped = self._key_map.get(key.lower())
            if mapped is not None:
                return super().__getitem__(mapped)
        return super().__getitem__(key)

    def get(self, key: Any, default: Optional[Any] = None) -> Optional[Any]:
        try:
            return self[key]
        except (KeyError, TypeError):
            return default


class QueryExecutor:
    """Executes SQL queries with parameterized bindings.

    All user-supplied values MUST be passed as separate parameters,
    never concatenated into the SQL string, to prevent SQL injection.
    """

    def __init__(self, connection_manager: ConnectionManager) -> None:
        self._cm = connection_manager

    def execute_query(self, sql: str, *params: Any) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return the result rows.

        Args:
            sql: SQL statement with ``?`` placeholders.
            *params: Values to bind to each placeholder.

        Returns:
            A list of dicts (each dict is a row). Column names are
            case-insensitive via :class:`CaseInsensitiveDict`.

        Raises:
            QueryError: If the database returns an error.
        """
        conn = None
        try:
            conn = self._cm.get_connection()
            with conn.cursor() as cursor:
                converted_sql = convert_placeholders(sql)
                cursor.execute(converted_sql, params)
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = []
                for row in cursor.fetchall():
                    row_dict = {}
                    if isinstance(row, dict):
                        for col in columns:
                            row_dict[col] = row[col]
                    else:
                        for i, col in enumerate(columns):
                            row_dict[col] = row[i]
                    rows.append(CaseInsensitiveDict(row_dict))
                return rows
        except Exception as exc:
            raise QueryError(f"Query execution failed: {exc}") from exc
        finally:
            self._cm.close_connection(conn)

    def execute_update(self, sql: str, *params: Any) -> int:
        """Execute an UPDATE, INSERT, or DELETE statement.

        Args:
            sql: SQL statement with ``?`` placeholders.
            *params: Values to bind to each placeholder.

        Returns:
            Number of affected rows.

        Raises:
            QueryError: If the database returns an error.
        """
        conn = None
        try:
            conn = self._cm.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(convert_placeholders(sql), params)
                affected = cursor.rowcount
                if not conn.autocommit:
                    conn.commit()
                return affected
        except Exception as exc:
            raise QueryError(f"Update execution failed: {exc}") from exc
        finally:
            self._cm.close_connection(conn)

    def execute_batch(self, sql_list: List[str]) -> List[int]:
        """Execute multiple SQL statements sequentially.

        .. warning::
            Statements are executed **without** parameterized binding.
            Only use this with trusted, hard-coded SQL strings.

        Args:
            sql_list: Plain SQL statements (one per element).

        Returns:
            List of row counts, one per statement.

        Raises:
            QueryError: If any statement fails.
        """
        conn = None
        try:
            conn = self._cm.get_connection()
            with conn.cursor() as cursor:
                results: List[int] = []
                for sql in sql_list:
                    cursor.execute(sql)
                    results.append(cursor.rowcount)
                if not conn.autocommit:
                    conn.commit()
                return results
        except Exception as exc:
            raise QueryError(f"Batch execution failed: {exc}") from exc
        finally:
            self._cm.close_connection(conn)

    def execute_transaction(
        self, transaction_block: Callable[["QueryExecutor"], None]
    ) -> None:
        """Execute a block of operations inside a single transaction.

        The transaction is **committed** if the block returns normally,
        or **rolled back** if any exception propagates out of the block.

        Args:
            transaction_block: A callable that receives a ``QueryExecutor``
                whose connections are all bound to the same transaction.

        Raises:
            QueryError: On transaction failure (includes the original cause).
        """
        conn = None
        try:
            conn = self._cm.get_connection_for_transaction()
            tx_executor = QueryExecutor(_TxConnectionManager(conn))
            transaction_block(tx_executor)
            conn.commit()
        except Exception as exc:
            if conn is not None:
                try:
                    conn.rollback()
                except Exception:
                    logger.debug("Ignored rollback error", exc_info=True)
            raise QueryError(f"Transaction failed: {exc}") from exc
        finally:
            if conn is not None:
                try:
                    conn.autocommit = True
                except Exception:
                    logger.debug("Failed to reset autocommit", exc_info=True)
                self._cm.close_connection(conn)


class _TxConnectionManager(ConnectionManager):
    """ConnectionManager that routes every call to the transaction connection."""

    def __init__(self, tx_conn: Any) -> None:
        super().__init__("")
        self._tx_conn = tx_conn

    def get_connection(self):
        return self._tx_conn

    def get_connection_for_transaction(self):
        return self._tx_conn

    @staticmethod
    def close_connection(conn: Any) -> None:
        pass
