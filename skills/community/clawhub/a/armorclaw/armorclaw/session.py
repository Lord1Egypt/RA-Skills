"""ArmorClaw — Unlocked session (holds decrypted password in memory only)."""
import time
from .store import get_secret, set_secret, list_secrets, delete_secret
from .auth  import LockConfig

DEFAULT_TIMEOUT = 900  # 15 minutes


class ArmorClawSession:
    """
    An unlocked vault session. Password is held in memory only.
    Auto-locks after timeout.
    """
    def __init__(self, password: str, lock_config: LockConfig,
                 timeout: int = DEFAULT_TIMEOUT):
        self._password    = password
        self._lock_config = lock_config
        self._unlocked_at = time.time()
        self._timeout     = timeout

    @property
    def is_locked(self) -> bool:
        return time.time() - self._unlocked_at > self._timeout

    def _check(self):
        if self.is_locked:
            self._password = None
            raise PermissionError("Vault session expired. Please unlock again.")

    def get(self, name: str, skill: str = "") -> str | None:
        self._check()
        return get_secret(name, self._password, skill=skill)

    def set(self, name: str, value: str, tags: list | None = None, skill: str = ""):
        self._check()
        return set_secret(name, value, self._password, tags=tags, skill=skill)

    def delete(self, name: str, skill: str = "") -> bool:
        self._check()
        return delete_secret(name, skill=skill)

    def list(self) -> list[dict]:
        self._check()
        return list_secrets()

    def lock(self):
        self._password = None
        self._unlocked_at = 0

    def touch(self):
        """Reset the session timeout."""
        self._unlocked_at = time.time()
