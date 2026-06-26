"""Authentication and credential management for Bilibili API."""

import json
import logging
import os
import stat
import time
from typing import Optional, Dict, Any

import httpx

from .utils import DEFAULT_HEADERS, API_BASE

_logger = logging.getLogger("bilibili.auth")

# Default path for persisted credentials (relative to project root)
DEFAULT_CREDENTIAL_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ".credentials.json",
)

# Maximum age (in seconds) of a persisted credential file before it is
# automatically treated as stale and ignored. Default: 30 days.
# This limits the blast-radius of a stolen on-disk credential and mitigates
# "Memory and Context Poisoning" where an old saved session could be silently
# reused long after the user intended.
CREDENTIAL_MAX_AGE_SECONDS = 30 * 24 * 60 * 60


def _assert_safe_credential_path(filepath: str) -> None:
    """Refuse to write credentials into world/group-accessible locations.

    Guards against "Memory and Context Poisoning": if the project directory
    is shared (e.g. /tmp, a world-writable CI workspace, or a network share),
    another process could read or replace the saved credentials.
    """
    directory = os.path.dirname(os.path.abspath(filepath)) or "."
    try:
        st = os.stat(directory)
    except OSError:
        # Directory doesn't exist yet — caller will create it with os.makedirs.
        return
    mode = st.st_mode
    # Disallow if the directory is group-writable or world-writable
    if mode & (stat.S_IWGRP | stat.S_IWOTH):
        raise PermissionError(
            f"Refusing to persist credentials into {directory!r}: "
            "directory is group- or world-writable. "
            "Move the project to a private directory (chmod 700) first."
        )


class BilibiliAuth:
    """Manage Bilibili authentication credentials and cookies.

    Supports login via SESSDATA cookie, QR code, and credential file.
    Credentials can optionally be persisted to disk for reuse across sessions.
    """

    def __init__(
        self,
        sessdata: Optional[str] = None,
        bili_jct: Optional[str] = None,
        buvid3: Optional[str] = None,
        credential_file: Optional[str] = None,
        persist: Optional[bool] = None,
    ):
        """Initialize BilibiliAuth.

        Credential resolution order (highest priority first):
        1. Explicit parameters (sessdata, bili_jct, buvid3)
        2. credential_file (JSON file)
        3. Persisted credential file (~/.credentials.json) if persist=True
        4. Environment variables (BILIBILI_SESSDATA, etc.)

        Args:
            sessdata: SESSDATA cookie value.
            bili_jct: bili_jct cookie value (CSRF token).
            buvid3: buvid3 cookie value.
            credential_file: Path to a JSON file containing credentials.
            persist: Whether to persist credentials to disk.
                True  = auto-load from and auto-save to the default credential file.
                False = never persist (in-memory only).
                None  = check BILIBILI_PERSIST env var, default to False.
        """
        # Resolve persist flag
        if persist is None:
            persist = os.environ.get("BILIBILI_PERSIST", "").lower() in (
                "1", "true", "yes",
            )
        self._persist = persist
        self._credential_path = credential_file or DEFAULT_CREDENTIAL_FILE

        self.sessdata = sessdata
        self.bili_jct = bili_jct
        self.buvid3 = buvid3

        # Load from explicit credential file
        if credential_file and os.path.exists(credential_file):
            self._load_from_file(credential_file)
        # Auto-load from default persisted file when persist is enabled
        elif self._persist and os.path.exists(self._credential_path):
            self._load_from_file(self._credential_path)

        # Try environment variables as fallback
        if not self.sessdata:
            self.sessdata = os.environ.get("BILIBILI_SESSDATA", "")
        if not self.bili_jct:
            self.bili_jct = os.environ.get("BILIBILI_BILI_JCT", "")
        if not self.buvid3:
            self.buvid3 = os.environ.get("BILIBILI_BUVID3", "")

        # Auto-save if persist is enabled and we have valid credentials
        if self._persist and self.is_authenticated:
            self.save_to_file(self._credential_path)

    def _load_from_file(self, filepath: str) -> None:
        """Load credentials from a JSON file.

        Additionally enforces:
          * File permissions must not grant group/other read access.
          * File age must be below CREDENTIAL_MAX_AGE_SECONDS; otherwise
            the file is ignored and a warning is logged (mitigates
            "Memory and Context Poisoning" via silently reused stale sessions).

        Args:
            filepath: Path to the credential JSON file.
        """
        try:
            st = os.stat(filepath)
        except OSError as e:
            _logger.warning("Cannot stat credential file %s: %s", filepath, e)
            return

        # Reject credentials readable by group/other (Unix). On Windows these
        # bits are not meaningful, so the check is effectively a no-op there.
        if hasattr(os, "geteuid") and (st.st_mode & (stat.S_IRGRP | stat.S_IROTH)):
            _logger.warning(
                "Ignoring credential file %s: permissions %o allow other users "
                "to read it. Fix with: chmod 600 %s",
                filepath, st.st_mode & 0o777, filepath,
            )
            return

        age = time.time() - st.st_mtime
        if age > CREDENTIAL_MAX_AGE_SECONDS:
            _logger.warning(
                "Ignoring credential file %s: it is %d days old (>%d days). "
                "Re-authenticate and call auth.save_to_file() again if needed.",
                filepath, int(age / 86400), int(CREDENTIAL_MAX_AGE_SECONDS / 86400),
            )
            return

        with open(filepath, "r", encoding="utf-8") as f:
            cred = json.load(f)
        self.sessdata = cred.get("sessdata", self.sessdata)
        self.bili_jct = cred.get("bili_jct", self.bili_jct)
        self.buvid3 = cred.get("buvid3", self.buvid3)

    @property
    def is_authenticated(self) -> bool:
        """Check if valid credentials are available."""
        return bool(self.sessdata and self.bili_jct)

    @property
    def cookies(self) -> Dict[str, str]:
        """Get cookies dict for HTTP requests."""
        cookies = {}
        if self.sessdata:
            cookies["SESSDATA"] = self.sessdata
        if self.bili_jct:
            cookies["bili_jct"] = self.bili_jct
        if self.buvid3:
            cookies["buvid3"] = self.buvid3
        return cookies

    @property
    def csrf(self) -> str:
        """Get CSRF token (bili_jct)."""
        return self.bili_jct or ""

    def get_headers(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Get HTTP headers with authentication.

        Args:
            extra: Additional headers to include.

        Returns:
            Headers dictionary.
        """
        headers = DEFAULT_HEADERS.copy()
        if extra:
            headers.update(extra)
        return headers

    def get_client(self) -> httpx.AsyncClient:
        """Create an authenticated async HTTP client.

        Returns:
            httpx.AsyncClient configured with credentials.
        """
        return httpx.AsyncClient(
            headers=self.get_headers(),
            cookies=self.cookies,
            timeout=30.0,
            follow_redirects=True,
        )

    async def verify(self) -> Dict[str, Any]:
        """Verify the current credentials by calling the user info API.

        Returns:
            User info dict if credentials are valid, error dict otherwise.
        """
        if not self.is_authenticated:
            return {"success": False, "message": "No credentials provided"}

        async with self.get_client() as client:
            resp = await client.get(f"{API_BASE}/x/web-interface/nav")
            data = resp.json()

        if data.get("code") == 0:
            info = data["data"]
            return {
                "success": True,
                "uid": info.get("mid"),
                "username": info.get("uname"),
                "vip_type": info.get("vipType"),
                "level": info.get("level_info", {}).get("current_level"),
            }
        return {"success": False, "message": data.get("message", "Unknown error")}

    @property
    def persist(self) -> bool:
        """Whether credential persistence is enabled."""
        return self._persist

    @persist.setter
    def persist(self, value: bool) -> None:
        """Enable or disable credential persistence.

        When enabling, credentials are immediately saved to disk.
        When disabling, the persisted file is deleted if it exists.
        """
        self._persist = value
        if value and self.is_authenticated:
            self.save_to_file(self._credential_path)
        elif not value and os.path.exists(self._credential_path):
            os.remove(self._credential_path)

    def clear_persisted(self) -> None:
        """Delete the persisted credential file from disk."""
        if os.path.exists(self._credential_path):
            os.remove(self._credential_path)

    def save_to_file(self, filepath: Optional[str] = None) -> None:
        """Save current credentials to a JSON file.

        The file is created with restrictive permissions (owner read/write
        only, 0600) to minimize exposure risk. Additionally, the target
        directory is checked against group/world-writable modes; if the
        directory is shared, the save is refused (see
        `_assert_safe_credential_path`). These measures mitigate "Memory and
        Context Poisoning" where other processes on the host could read or
        replace the saved session.

        Args:
            filepath: Path to save the credential file.
                      Defaults to the configured credential path.
        """
        filepath = filepath or self._credential_path
        cred = {
            "sessdata": self.sessdata,
            "bili_jct": self.bili_jct,
            "buvid3": self.buvid3,
        }
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

        # Refuse to save into an unsafe directory
        _assert_safe_credential_path(filepath)

        # Open with restrictive permissions (0600 = owner read/write only)
        fd = os.open(filepath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        # os.fdopen takes ownership of fd and will close it automatically,
        # so we must NOT call os.close(fd) after os.fdopen succeeds.
        f = None
        try:
            f = os.fdopen(fd, "w", encoding="utf-8")
            json.dump(cred, f, indent=2)
        except Exception:
            # Only close fd manually if os.fdopen itself failed (f is None),
            # because os.fdopen did not take ownership yet.
            if f is None:
                os.close(fd)
            raise
        finally:
            if f is not None:
                f.close()

        # Defensive: re-apply 0600 in case umask or FS quirks altered it.
        try:
            os.chmod(filepath, 0o600)
        except OSError:
            pass

        _logger.warning(
            "Credentials persisted to %s (mode 0600). "
            "Call auth.clear_persisted() when done to remove them.",
            filepath,
        )
