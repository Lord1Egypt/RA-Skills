# FILE_META
# INPUT:  phone number + SMS code (interactive)
# OUTPUT: API key stored in .env
# POS:    skill lib — called by submit.py, query.py
# MISSION: Handle phone+SMS authentication flow and API key management.

"""Authentication flow for ClawTraces: phone + SMS verification code → API key.

This is the **end-user** side (SECRET key, public API at api.shixiann.com),
explicitly separated from the operations admin auth at `scripts/_admin_auth.py`
(admin key, SSH tunnel to ECS). The two modules serve different roles and
are intentionally not unified — see their respective READMEs.
"""

from __future__ import annotations

import json
import os
import ssl
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

try:
    from .paths import get_env_file_path
except ImportError:
    try:
        from lib.paths import get_env_file_path
    except ImportError:
        from paths import get_env_file_path

ENV_FILE_PATH = get_env_file_path()

# ── SSL context (fixes macOS certificate issues) ──────────────────────

_ssl_context: ssl.SSLContext | None = None

# Bundled Mozilla CA certificate bundle — works on any Python version
# without requiring certifi, pip, or valid system certificates.
_BUNDLED_CACERT = os.path.join(os.path.dirname(__file__), "cacert.pem")


def get_ssl_context() -> ssl.SSLContext:
    """Return an SSL context that works on any Python/macOS version.

    Priority:
    1. Bundled cacert.pem (ships with the skill, zero dependencies)
    2. certifi package (if user happens to have it installed)
    3. System default (last resort)
    """
    global _ssl_context
    if _ssl_context is not None:
        return _ssl_context

    # 1. Bundled CA cert — always available, no dependencies
    if os.path.isfile(_BUNDLED_CACERT):
        _ssl_context = ssl.create_default_context(cafile=_BUNDLED_CACERT)
        return _ssl_context

    # 2. certifi package
    try:
        import certifi
        _ssl_context = ssl.create_default_context(cafile=certifi.where())
        return _ssl_context
    except ImportError:
        pass

    # 3. System default (may fail on old macOS Python)
    _ssl_context = ssl.create_default_context()
    return _ssl_context


def _format_connection_error(reason) -> str:
    """Format URLError.reason into a user-friendly message."""
    reason_str = str(reason)
    if "CERTIFICATE_VERIFY_FAILED" in reason_str:
        return (
            "SSL 证书验证失败。这通常是 macOS Python 环境的已知问题。\n"
            "请尝试以下任一方法修复：\n"
            "  1. pip install --upgrade certifi\n"
            "  2. 如果是 Python 官方安装器：运行 /Applications/Python 3.x/Install Certificates.command\n"
            "  3. brew install ca-certificates （Homebrew 用户）"
        )
    return f"Connection failed: {reason_str}"
KEY_ENV_VAR = "CLAWTRACES_SECRET_KEY"
SERVER_URL_ENV_VAR = "CLAWTRACES_SERVER_URL"
DEFAULT_SERVER_URL = "https://api.shixiann.com"


def _load_env_file() -> dict[str, str]:
    """Load key=value pairs from the skill .env file."""
    env = {}
    if os.path.isfile(ENV_FILE_PATH):
        with open(ENV_FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def _save_to_env_file(key: str, value: str):
    """Save or update a key=value pair in the .env file."""
    lines = []
    found = False

    if os.path.isfile(ENV_FILE_PATH):
        with open(ENV_FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith(f"{key}="):
                    lines.append(f"{key}={value}\n")
                    found = True
                else:
                    lines.append(line)

    if not found:
        lines.append(f"{key}={value}\n")

    os.makedirs(os.path.dirname(ENV_FILE_PATH), exist_ok=True)
    with open(ENV_FILE_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)


def _remove_from_env_file(key: str):
    """Remove a key from the .env file."""
    if not os.path.isfile(ENV_FILE_PATH):
        return
    lines = []
    with open(ENV_FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip().startswith(f"{key}="):
                lines.append(line)
    with open(ENV_FILE_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)


class ConfigError(Exception):
    """Raised when required configuration is missing."""
    pass


def get_server_url() -> str:
    """Get server URL from env var, .env file, or default.

    Falls back to DEFAULT_SERVER_URL if not explicitly configured.
    """
    url = os.environ.get(SERVER_URL_ENV_VAR)
    if url:
        return url.rstrip("/")
    dotenv = _load_env_file()
    url = dotenv.get(SERVER_URL_ENV_VAR, "")
    if url:
        return url.rstrip("/")
    return DEFAULT_SERVER_URL


def get_stored_key() -> str | None:
    """Get API key from env var or .env file. Returns None if not found."""
    key = os.environ.get(KEY_ENV_VAR)
    if key:
        return key
    dotenv = _load_env_file()
    return dotenv.get(KEY_ENV_VAR)


def clear_stored_key():
    """Remove stored API key (called on 401)."""
    _remove_from_env_file(KEY_ENV_VAR)


def save_key(key: str):
    """Save API key to .env file."""
    _save_to_env_file(KEY_ENV_VAR, key)


def _api_call(server_url: str, path: str, body: dict | None = None,
              method: str = "POST", secret_key: str | None = None) -> dict:
    """Make an API call to the server. Returns parsed JSON response."""
    url = f"{server_url}{path}"
    try:
        from lib.version import default_headers, exit_if_upgrade_required
    except ImportError:
        from ..version import default_headers, exit_if_upgrade_required  # type: ignore
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "X-Client-Id": "clawtraces-skill",
        **default_headers(secret_key),
    }

    data = json.dumps(body).encode("utf-8") if body else None
    req = Request(url, data=data, headers=headers, method=method)

    try:
        with urlopen(req, timeout=30, context=get_ssl_context()) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(error_body)
        except (json.JSONDecodeError, ValueError):
            parsed = {}
        exit_if_upgrade_required(parsed)
        if "error" not in parsed:
            parsed["error"] = f"HTTP {e.code}"
        return parsed
    except URLError as e:
        return {"error": _format_connection_error(e.reason)}


def _normalize_phone(phone: str) -> str:
    """Normalize phone number to +86XXXXXXXXXXX format.

    Handles common input variants:
      13800008888      → +8613800008888
      +8613800008888   → +8613800008888
      86 138 0000 8888 → +8613800008888
      +86-138-0000-8888 → +8613800008888
    """
    import re
    # Strip whitespace, dashes, dots, parentheses
    cleaned = re.sub(r"[\s\-\.\(\)]+", "", phone.strip())

    # Remove leading + for uniform processing
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]

    # Remove leading 86 country code if present
    if cleaned.startswith("86") and len(cleaned) == 13:
        cleaned = cleaned[2:]

    # Validate: must be 11 digits starting with 1
    if not re.match(r"^1\d{10}$", cleaned):
        raise ValueError(f"Invalid phone number: {phone}. Expected 11-digit Chinese mobile number.")

    return f"+86{cleaned}"


def send_code(server_url: str, phone: str) -> dict:
    """Request SMS verification code. Normalizes phone number before sending."""
    try:
        phone = _normalize_phone(phone)
    except ValueError as e:
        return {"error": str(e)}
    return _api_call(server_url, "/auth/send-code", {"phone": phone})


def verify_code(server_url: str, phone: str, code: str) -> dict:
    """Verify SMS code and get API key. Normalizes phone number before sending."""
    try:
        phone = _normalize_phone(phone)
    except ValueError as e:
        return {"error": str(e)}
    return _api_call(server_url, "/auth/verify", {"phone": phone, "code": code, "source": "skill"})


def check_key_valid(server_url: str, key: str) -> bool:
    """Check if a stored key is still valid by calling /count."""
    result = _api_call(server_url, "/count", method="GET", secret_key=key)
    return "error" not in result


def handle_401():
    """Handle 401 response: clear key and notify."""
    clear_stored_key()
    print("API key is invalid or expired. Please re-authenticate.", file=sys.stderr)


def main():
    """Check authentication status and print result as JSON."""
    key = get_stored_key()
    if not key:
        result = {"authenticated": False, "reason": "no_key"}
        print(json.dumps(result, indent=2))
        return

    server_url = get_server_url()
    valid = check_key_valid(server_url, key)
    if valid:
        result = {"authenticated": True, "key_prefix": key[:12] + "..."}
    else:
        clear_stored_key()
        result = {"authenticated": False, "reason": "key_invalid"}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
