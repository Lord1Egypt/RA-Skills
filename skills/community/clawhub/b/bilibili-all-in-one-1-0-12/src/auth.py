"""Authentication and credential management for Bilibili API."""

import json
import os
from typing import Optional, Dict, Any

import httpx

from .utils import DEFAULT_HEADERS, API_BASE


class BilibiliAuth:
    """Manage Bilibili authentication credentials and cookies.

    Supports login via SESSDATA cookie, QR code, and credential file.
    """

    def __init__(
        self,
        sessdata: Optional[str] = None,
        bili_jct: Optional[str] = None,
        buvid3: Optional[str] = None,
        credential_file: Optional[str] = None,
    ):
        """Initialize BilibiliAuth.

        Args:
            sessdata: SESSDATA cookie value.
            bili_jct: bili_jct cookie value (CSRF token).
            buvid3: buvid3 cookie value.
            credential_file: Path to a JSON file containing credentials.
        """
        self.sessdata = sessdata
        self.bili_jct = bili_jct
        self.buvid3 = buvid3

        if credential_file and os.path.exists(credential_file):
            self._load_from_file(credential_file)

        # Try environment variables as fallback
        if not self.sessdata:
            self.sessdata = os.environ.get("BILIBILI_SESSDATA", "")
        if not self.bili_jct:
            self.bili_jct = os.environ.get("BILIBILI_BILI_JCT", "")
        if not self.buvid3:
            self.buvid3 = os.environ.get("BILIBILI_BUVID3", "")

    def _load_from_file(self, filepath: str) -> None:
        """Load credentials from a JSON file.

        Args:
            filepath: Path to the credential JSON file.
        """
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

    def save_to_file(self, filepath: str) -> None:
        """Save current credentials to a JSON file.

        WARNING: This persists sensitive session cookies to disk. Only call this
        method when explicitly requested by the user. The file is created with
        restrictive permissions (owner read/write only, 0600) to minimize
        exposure risk.

        Args:
            filepath: Path to save the credential file.
        """
        cred = {
            "sessdata": self.sessdata,
            "bili_jct": self.bili_jct,
            "buvid3": self.buvid3,
        }
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

        # Open with restrictive permissions (0600 = owner read/write only)
        fd = os.open(filepath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(cred, f, indent=2)
        except Exception:
            os.close(fd)
            raise
