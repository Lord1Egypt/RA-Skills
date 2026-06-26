"""ArmorClaw — Main API class."""
import getpass
from .store   import (init_vault, is_initialized, mark_initialized,
                      get_lock_config, set_secret, get_secret,
                      delete_secret, list_secrets, get_access_log,
                      skill_usage_report)
from .auth    import validate_password, LockConfig, get_machine_fingerprint, get_current_ip
from .crypto  import decrypt
from .session import ArmorClawSession
from .importer import import_env_file, handle_env_after_import, scan_for_env_files


class ArmorClaw:
    """
    Main ArmorClaw interface.

    Usage:
        ck = ArmorClaw()

        # First run — initialize vault
        if not ck.is_setup:
            ck.setup()

        # Unlock
        ck.unlock("your-master-password")

        # Use
        key = ck.get("OPENAI_KEY")
        ck.set("NEW_KEY", "value123!")
    """

    def __init__(self):
        init_vault()
        self._session: ArmorClawSession | None = None

    @property
    def is_setup(self) -> bool:
        return is_initialized()

    @property
    def is_unlocked(self) -> bool:
        return self._session is not None and not self._session.is_locked

    def setup(self, password: str | None = None, mode: str = "password",
              register_machine: bool = False, register_ip: bool = False,
              ip_type: str = "local") -> dict:
        """
        Initialize the vault for the first time.
        Returns: {"ok": True} or {"ok": False, "errors": [...]}
        """
        if self.is_setup:
            return {"ok": False, "error": "Vault already initialized"}

        if not password:
            return {"ok": False, "error": "Password required"}

        errors = validate_password(password)
        if errors:
            return {"ok": False, "errors": errors}

        lock_cfg = LockConfig()
        lock_cfg.mode    = mode
        lock_cfg.ip_type = ip_type
        if register_machine:
            lock_cfg.registered_fingerprint = get_machine_fingerprint()
        if register_ip:
            lock_cfg.registered_ip = get_current_ip(mode=ip_type)

        mark_initialized(lock_cfg)
        self._session = ArmorClawSession(password, lock_cfg)
        return {"ok": True, "mode": mode}

    def unlock(self, password: str | None = None) -> dict:
        """
        Unlock the vault. Checks machine/IP if configured.
        Returns {"ok": True} or {"ok": False, "error": ...}
        """
        if not self.is_setup:
            return {"ok": False, "error": "Vault not initialized. Run setup() first."}

        lock_cfg = get_lock_config()

        # Machine/IP checks
        ok, reason = lock_cfg.check_access()
        if not ok:
            return {"ok": False, "error": reason, "access_denied": True}

        # Verify password by attempting to decrypt a test entry
        # (we just try to get any existing key — if wrong pw, crypto will raise)
        pwd = password or getpass.getpass("ArmorClaw master password: ")

        try:
            secrets = list_secrets()
            if secrets:
                # Try decrypting the first secret to verify password
                from .store import _conn
                with _conn() as c:
                    row = c.execute("SELECT ciphertext FROM secrets LIMIT 1").fetchone()
                if row:
                    decrypt(row[0], pwd)  # raises ValueError if wrong
        except ValueError:
            return {"ok": False, "error": "Wrong password"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

        self._session = ArmorClawSession(pwd, lock_cfg)
        return {"ok": True}

    def lock(self):
        """Lock the vault session."""
        if self._session:
            self._session.lock()
        self._session = None

    def _require_unlocked(self):
        if not self.is_unlocked:
            raise PermissionError("Vault is locked. Call unlock() first.")

    def get(self, name: str, skill: str = "") -> str | None:
        """Get a secret by name."""
        self._require_unlocked()
        return self._session.get(name, skill=skill)

    def set(self, name: str, value: str, tags: list | None = None, skill: str = ""):
        """Store a secret."""
        self._require_unlocked()
        return self._session.set(name, value, tags=tags, skill=skill)

    def delete(self, name: str) -> bool:
        """Delete a secret."""
        self._require_unlocked()
        return self._session.delete(name)

    def list(self) -> list[dict]:
        """List all secret names (no values)."""
        self._require_unlocked()
        return self._session.list()

    def import_env(self, env_path: str,
                   after: str = "ask") -> dict:
        """
        Import keys from a .env file.
        after: 'delete' | 'backup' | 'keep' | 'ask'
        """
        self._require_unlocked()
        result = import_env_file(env_path, self._session._password)
        if result.get("error"):
            return result

        if after != "ask":
            cleanup = handle_env_after_import(env_path, after)
            result["cleanup"] = cleanup

        return result

    def scan_envs(self, paths: list[str] | None = None) -> list[str]:
        """Scan for .env files in common locations."""
        return scan_for_env_files(paths)

    def access_log(self, name: str | None = None, limit: int = 50) -> list[dict]:
        """Get access log entries."""
        self._require_unlocked()
        return get_access_log(name, limit)

    def skill_report(self) -> dict:
        """Get per-skill usage report."""
        self._require_unlocked()
        return skill_usage_report()

    def env_inject(self, skill: str = "") -> dict:
        """
        Return all secrets as a plain dict for injecting into os.environ.
        Use with caution — only call this in trusted contexts.
        """
        self._require_unlocked()
        result = {}
        for item in list_secrets():
            val = self._session.get(item["name"], skill=skill)
            if val:
                result[item["name"]] = val
        return result
