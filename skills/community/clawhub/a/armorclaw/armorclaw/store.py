"""ArmorClaw — Encrypted SQLite vault store."""
import sqlite3, json, time
from pathlib import Path
from datetime import datetime
from .crypto import encrypt, decrypt
from .auth   import LockConfig, get_machine_fingerprint, get_current_ip

VAULT_DIR  = Path.home() / ".armorclaw"
VAULT_DB   = VAULT_DIR / "vault.db"
CONFIG_FILE = VAULT_DIR / "config.json"


def _conn():
    VAULT_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    c = sqlite3.connect(str(VAULT_DB), timeout=5)
    c.execute("PRAGMA journal_mode=WAL")
    return c


def init_vault():
    """Create vault tables if they don't exist."""
    VAULT_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    VAULT_DB.touch(mode=0o600) if not VAULT_DB.exists() else None
    with _conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS secrets (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL UNIQUE,
            ciphertext  TEXT NOT NULL,
            tags        TEXT NOT NULL DEFAULT '[]',
            created_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS access_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            secret_name TEXT NOT NULL,
            skill       TEXT NOT NULL DEFAULT '',
            accessed_at TEXT NOT NULL,
            ip          TEXT NOT NULL DEFAULT '',
            action      TEXT NOT NULL DEFAULT 'read'
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS vault_meta (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )""")
        c.execute("CREATE INDEX IF NOT EXISTS idx_secrets_name ON secrets(name)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_log_name ON access_log(secret_name)")


def is_initialized() -> bool:
    if not VAULT_DB.exists():
        return False
    with _conn() as c:
        row = c.execute("SELECT value FROM vault_meta WHERE key='initialized'").fetchone()
        return row is not None and row[0] == "1"


def mark_initialized(lock_config: LockConfig):
    with _conn() as c:
        c.execute("INSERT OR REPLACE INTO vault_meta(key,value) VALUES ('initialized','1')")
        c.execute("INSERT OR REPLACE INTO vault_meta(key,value) VALUES ('lock_config',?)",
                  (json.dumps(lock_config.to_dict()),))
        c.execute("INSERT OR REPLACE INTO vault_meta(key,value) VALUES ('created_at',?)",
                  (datetime.utcnow().isoformat(),))


def get_lock_config() -> LockConfig:
    with _conn() as c:
        row = c.execute("SELECT value FROM vault_meta WHERE key='lock_config'").fetchone()
    if row:
        return LockConfig(json.loads(row[0]))
    return LockConfig()


def set_secret(name: str, value: str, password: str, tags: list | None = None, skill: str = "") -> bool:
    """Encrypt and store a secret. Returns True on success."""
    ct  = encrypt(value, password)
    now = datetime.utcnow().isoformat()
    with _conn() as c:
        c.execute("""
            INSERT INTO secrets(name, ciphertext, tags, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                ciphertext=excluded.ciphertext,
                tags=excluded.tags,
                updated_at=excluded.updated_at
        """, (name, ct, json.dumps(tags or []), now, now))
        _log_access(c, name, skill, "write")
    return True


def get_secret(name: str, password: str, skill: str = "") -> str | None:
    """Decrypt and return a secret value."""
    with _conn() as c:
        row = c.execute("SELECT ciphertext FROM secrets WHERE name=?", (name,)).fetchone()
        if not row:
            return None
        value = decrypt(row[0], password)
        _log_access(c, name, skill, "read")
    return value


def delete_secret(name: str, skill: str = "") -> bool:
    with _conn() as c:
        result = c.execute("DELETE FROM secrets WHERE name=?", (name,))
        if result.rowcount:
            _log_access(c, name, skill, "delete")
            return True
    return False


def list_secrets() -> list[dict]:
    with _conn() as c:
        rows = c.execute(
            "SELECT name, tags, created_at, updated_at FROM secrets ORDER BY name"
        ).fetchall()
    return [{"name": r[0], "tags": json.loads(r[1]), "created": r[2], "updated": r[3]}
            for r in rows]


def get_access_log(name: str | None = None, limit: int = 50) -> list[dict]:
    with _conn() as c:
        if name:
            rows = c.execute(
                "SELECT * FROM access_log WHERE secret_name=? ORDER BY id DESC LIMIT ?",
                (name, limit)
            ).fetchall()
        else:
            rows = c.execute(
                "SELECT * FROM access_log ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        cols = [d[0] for d in c.execute("SELECT * FROM access_log LIMIT 0").description]
    return [dict(zip(cols, r)) for r in rows]


def skill_usage_report() -> dict:
    """Returns {skill: {secret: count}} usage breakdown."""
    with _conn() as c:
        rows = c.execute(
            "SELECT skill, secret_name, COUNT(*) FROM access_log "
            "WHERE action='read' GROUP BY skill, secret_name"
        ).fetchall()
    report = {}
    for skill, secret, count in rows:
        skill = skill or "unknown"
        report.setdefault(skill, {})[secret] = count
    return report


def _log_access(conn, name: str, skill: str, action: str):
    conn.execute(
        "INSERT INTO access_log(secret_name, skill, accessed_at, ip, action) VALUES(?,?,?,?,?)",
        (name, skill or "", datetime.utcnow().isoformat(), get_current_ip(), action),
    )
