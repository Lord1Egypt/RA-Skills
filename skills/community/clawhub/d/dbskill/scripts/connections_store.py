from __future__ import annotations

import json
import logging
import os
import tempfile
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_STORE_FILE = os.path.join(tempfile.gettempdir(), ".database-skill-connections.json")


def _store_path() -> str:
    return _STORE_FILE


class ConnectionRecord:
    """A saved database connection record.

    Passwords are handled as follows:
    - If ``password_env_var`` is set (e.g. ``DB_PASS``), the value is read
      from the environment at connection time.  This is the **safe** path.
    - If ``password_env_var`` is empty, the password was entered as plain text
      and is **never** persisted to disk.
    """

    def __init__(self, url: str, username: str, driver: str,
                 label: str = "", password_env_var: str = "") -> None:
        self.url = url
        self.username = username
        self.driver = driver
        self.label = label or _auto_label(url, username)
        self.password_env_var = password_env_var

    def has_password(self) -> bool:
        return bool(self.password_env_var)

    def get_password(self) -> str:
        if self.password_env_var:
            return os.environ.get(self.password_env_var, "")
        return ""

    def identity(self) -> str:
        """Return a stable key: ``host:port/database`` — ignores URL query params."""
        return f"{self.username}@{_extract_host_db(self.url)}"

    def to_dict(self) -> Dict[str, str]:
        d: Dict[str, str] = {
            "url": self.url,
            "username": self.username,
            "driver": self.driver,
            "label": self.label,
        }
        if self.password_env_var:
            d["password_env_var"] = self.password_env_var
        return d

    @staticmethod
    def from_dict(d: Dict[str, str]) -> ConnectionRecord:
        return ConnectionRecord(
            url=d["url"],
            username=d.get("username", ""),
            driver=d.get("driver", "pymysql"),
            label=d.get("label", ""),
            password_env_var=d.get("password_env_var", ""),
        )


def _extract_host_db(url: str) -> str:
    """Extract ``host:port/database`` from a JDBC URL."""
    url_lower = url.lower()
    for scheme in ("mysql", "postgresql", "oracle:thin", "oracle", "sqlserver", "sqlite", "h2"):
        prefix = f"jdbc:{scheme}"
        if url_lower.startswith(prefix):
            rest = url[len(prefix):].lstrip(":/@; ")
            if scheme == "sqlserver":
                host = rest.split(":")[0] if ":" in rest else rest.split(";")[0]
                port = "1433"
                db = ""
                for part in rest.split(";"):
                    part = part.strip()
                    if "=" in part:
                        k, v = part.split("=", 1)
                        if k.lower() in ("databasename", "database"):
                            db = v
                return f"{host}:{port}/{db}"
            host = rest.split(":")[0]
            port = "1521" if "oracle" in scheme else "3306"
            tail = rest[len(host):].lstrip(":")
            return f"{host}:{port}/"
    return url


def _auto_label(url: str, username: str) -> str:
    driver_map = {
        "mysql": "MySQL",
        "postgresql": "PostgreSQL",
        "oracle": "Oracle",
        "sqlserver": "SQL Server",
        "sqlite": "SQLite",
        "h2": "H2",
    }
    url_lower = url.lower()
    driver_name = "DB"
    for keyword, name in driver_map.items():
        if keyword in url_lower:
            driver_name = name
            break
    host = "unknown"
    for sep in ("://", ":@", ":@"):
        if sep in url:
            part = url.split(sep, 1)[1]
            host = part.split(":")[0].split(";")[0].split("/")[0]
            break
    return f"{driver_name}@{host}"


class ConnectionsStore:
    """Persists connection records to a JSON file in the user temp directory.

    The file is stored at ``os.environ['TEMP']/.database-skill-connections.json``.
    This allows the skill to remember previously used databases across sessions.
    """

    def __init__(self) -> None:
        self._path = _store_path()

    def load_all(self) -> List[ConnectionRecord]:
        """Load all saved connections."""
        try:
            if not os.path.exists(self._path):
                return []
            with open(self._path, "r") as f:
                data = json.load(f)
            return [ConnectionRecord.from_dict(item) for item in data]
        except Exception as exc:
            logger.debug("Failed to load connections: %s", exc)
            return []

    def save(self, record: ConnectionRecord) -> None:
        """Save (or update) a connection record.

        Uses ``identity()`` (username@host:port/database) as the unique key.
        If a record for the same database already exists, it is replaced.
        """
        records = self.load_all()
        key = record.identity()
        records = [r for r in records if r.identity() != key]
        records.append(record)
        self._save_all(records)

    def find_by_url(self, url: str) -> Optional[ConnectionRecord]:
        for r in self.load_all():
            if r.url == url:
                return r
        return None

    def list_labels(self) -> List[str]:
        return [r.label for r in self.load_all()]

    def get_by_index(self, index: int) -> Optional[ConnectionRecord]:
        records = self.load_all()
        if 0 <= index < len(records):
            return records[index]
        return None

    def remove(self, url: str) -> None:
        records = [r for r in self.load_all() if r.url != url]
        self._save_all(records)

    def clear(self) -> None:
        self._save_all([])

    def _save_all(self, records: List[ConnectionRecord]) -> None:
        try:
            with open(self._path, "w") as f:
                json.dump([r.to_dict() for r in records], f, indent=2)
        except Exception as exc:
            logger.debug("Failed to save connections: %s", exc)
