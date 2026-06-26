from __future__ import annotations

import logging
import os
import re
import sqlite3
import urllib.parse
from typing import Dict, Optional

import yaml

from exceptions import (
    DatabaseConnectionError,
    ConfigurationError,
    UnsupportedDatabaseError,
)

logger = logging.getLogger(__name__)

# Lazy-loaded driver references
_pymysql = None
_psycopg2 = None
_oracledb = None
_pymssql = None

_DRIVER_REGISTRY: Dict[str, str] = {
    "jdbc:mysql:": "pymysql",
    "jdbc:postgresql:": "psycopg2",
    "jdbc:oracle:": "oracledb",
    "jdbc:sqlserver:": "pymssql",
    "jdbc:microsoft:sqlserver:": "pymssql",
    "jdbc:h2:": "sqlite3",
    "jdbc:sqlite:": "sqlite3",
}

_ENV_VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")


def resolve_env_vars(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None

    def _replacer(match: re.Match) -> str:
        var_name = match.group(1)
        return os.environ.get(var_name, "")

    return _ENV_VAR_PATTERN.sub(_replacer, value)


def load_config(path: str) -> dict:
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.debug("Config file not found: %s", path)
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        fallback = os.path.join(script_dir, path)
        with open(fallback, "r") as f:
            return yaml.safe_load(f)
    except Exception as exc:
        raise ConfigurationError(
            f"Failed to load config from {path}: {exc}"
        ) from exc


def resolve_driver(jdbc_url: str) -> str:
    for prefix, driver in _DRIVER_REGISTRY.items():
        if jdbc_url.startswith(prefix):
            return driver
    raise UnsupportedDatabaseError(f"Unsupported JDBC URL prefix: {jdbc_url}")


def _import_pymysql():
    global _pymysql
    if _pymysql is None:
        try:
            import pymysql as _pymysql
        except ImportError:
            raise ImportError(
                "pymysql is required for MySQL connections. "
                "Install it with: pip install pymysql"
            )
    return _pymysql


def _import_psycopg2():
    global _psycopg2
    if _psycopg2 is None:
        try:
            import psycopg2 as _psycopg2
        except ImportError:
            raise ImportError(
                "psycopg2 is required for PostgreSQL connections. "
                "Install it with: pip install psycopg2-binary"
            )
    return _psycopg2


def _import_oracledb():
    global _oracledb
    if _oracledb is None:
        try:
            import oracledb
            _oracledb = oracledb
            _oracledb.defaults.fetch_lobs = False
        except ImportError:
            raise ImportError(
                "oracledb is required for Oracle connections. "
                "Install it with: pip install oracledb"
            )
    return _oracledb


def _import_pymssql():
    global _pymssql
    if _pymssql is None:
        try:
            import pymssql as _pymssql
        except ImportError:
            raise ImportError(
                "pymssql is required for SQL Server connections. "
                "Install it with: pip install pymssql"
            )
    return _pymssql


def _jdbc_url_to_python_url(jdbc_url: str) -> str:
    """Strip the 'jdbc:' prefix so urllib can parse the URL."""
    return jdbc_url.replace("jdbc:", "", 1)


class ConnectionManager:
    """Manages database connection lifecycle.

    Provides two connection modes:
    - ``get_connection()`` — returns an auto-commit connection for regular queries.
    - ``get_connection_for_transaction()`` — returns a manual-commit connection.
    """

    def __init__(
        self,
        url: str,
        username: str = "",
        password: str = "",
        driver: str = "pymysql",
    ) -> None:
        self._url = url
        self._username = username
        self._password = password
        self._driver = driver

    def get_connection(self):
        conn = self._connect()
        conn.autocommit = True
        return conn

    def get_connection_for_transaction(self):
        conn = self._connect()
        conn.autocommit = False
        return conn

    @staticmethod
    def close_connection(conn) -> None:
        if conn is None:
            return
        try:
            conn.close()
        except Exception:
            logger.debug("Ignored error while closing connection", exc_info=True)

    def shutdown(self) -> None:
        pass

    def _connect(self):
        python_url = _jdbc_url_to_python_url(self._url)

        if self._driver == "pymysql":
            pymysql = _import_pymysql()
            parsed = urllib.parse.urlparse(python_url)
            host = parsed.hostname or "localhost"
            port = parsed.port or 3306
            database = parsed.path.lstrip("/").split("?")[0] if parsed.path else ""
            try:
                return pymysql.connect(
                    host=host,
                    port=port,
                    database=database,
                    user=self._username,
                    password=self._password,
                    cursorclass=pymysql.cursors.DictCursor,
                    charset="utf8mb4",
                )
            except Exception as exc:
                raise DatabaseConnectionError(
                    f"Failed to connect to MySQL at {host}:{port}/{database}: {exc}"
                ) from exc

        if self._driver == "psycopg2":
            psycopg2 = _import_psycopg2()
            try:
                return psycopg2.connect(
                    python_url,
                    user=self._username,
                    password=self._password,
                )
            except Exception as exc:
                raise DatabaseConnectionError(
                    f"Failed to connect to PostgreSQL at {python_url}: {exc}"
                ) from exc

        if self._driver == "oracledb":
            oracledb = _import_oracledb()
            try:
                python_url = python_url.replace("oracle:", "oracle+cx_oracle:")
                return oracledb.connect(
                    user=self._username,
                    password=self._password,
                    dsn=python_url.replace("oracle:thin:@", "").replace("oracle:@", ""),
                )
            except Exception as exc:
                raise DatabaseConnectionError(
                    f"Failed to connect to Oracle: {exc}"
                ) from exc

        if self._driver == "pymssql":
            pymssql = _import_pymssql()
            try:
                host = "localhost"
                port = 1433
                database = ""
                # SQL Server JDBC URL uses semicolons, not standard URL query
                raw = python_url.replace("sqlserver://", "", 1)
                for part in raw.split(";"):
                    part = part.strip()
                    if "=" in part:
                        key, val = part.split("=", 1)
                        kl = key.lower()
                        if kl in ("databasename", "database"):
                            database = val
                    elif ":" in part:
                        h, p = part.split(":", 1)
                        if h:
                            host = h
                        try:
                            port = int(p)
                        except ValueError:
                            pass
                    elif part:
                        host = part
                return pymssql.connect(
                    server=host,
                    port=port,
                    database=database,
                    user=self._username,
                    password=self._password,
                )
            except Exception as exc:
                raise DatabaseConnectionError(
                    f"Failed to connect to SQL Server at {host}:{port}/{database}: {exc}"
                ) from exc

        if self._driver == "sqlite3":
            path = python_url.replace("sqlite:", "", 1) if python_url.startswith("sqlite:") else python_url
            if ":mem:" in path or ":memory:" in path:
                return sqlite3.connect(":memory:")
            return sqlite3.connect(path)

        raise UnsupportedDatabaseError(f"Unsupported driver: {self._driver}")
