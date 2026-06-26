"""
config.py - Configuration Management Module

Reads DBDoctor configuration from environment variables:
  - DBDOCTOR_URL: API base URL (always required)
  - DBDOCTOR_USER: Login username (password mode)
  - DBDOCTOR_PASSWORD: Login password (password mode)
  - DBDOCTOR_EMAIL: Login email (email verification code mode)

Login mode detection:
  - If DBDOCTOR_EMAIL is set → email mode (verification code login)
  - Otherwise → password mode (username/password login)

Priority: System / platform-injected environment variables > .env file (legacy fallback)
"""

import os
import base64
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Login mode constants
LOGIN_MODE_PASSWORD = "password"
LOGIN_MODE_EMAIL = "email"

# Required env vars by mode
_REQUIRED_COMMON = ("DBDOCTOR_URL",)
_REQUIRED_PASSWORD_MODE = ("DBDOCTOR_USER", "DBDOCTOR_PASSWORD")

# Storage encryption key (for decrypting legacy ENC: prefixed values in .env)
_STORAGE_KEY = b"dbdoctor-tools!!dbdoctor-tools!!"  # 32 bytes for AES-256

# Prefix to identify encrypted values
_ENC_PREFIX = "ENC:"


def _decrypt_from_storage(value: str) -> str:
    """Decrypt an ENC: prefixed value from legacy .env file. Returns plaintext as-is."""
    if not value.startswith(_ENC_PREFIX):
        return value
    encrypted = base64.b64decode(value[len(_ENC_PREFIX):])
    cipher = AES.new(_STORAGE_KEY, AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
    return decrypted.decode("utf-8")


class ConfigError(Exception):
    """Configuration error exception"""
    pass


def _try_load_dotenv():
    """Try to load .env file (legacy fallback)"""
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            return True
    except ImportError:
        pass
    return False


def _detect_login_mode() -> str:
    """Detect login mode based on environment variables.
    If DBDOCTOR_EMAIL is set (non-empty), use email mode; otherwise password mode.
    """
    email = os.environ.get("DBDOCTOR_EMAIL", "").strip()
    if email:
        return LOGIN_MODE_EMAIL
    return LOGIN_MODE_PASSWORD


def _check_env_vars_for_mode(mode: str):
    """Check if required environment variables are set for the given mode.
    Returns (complete: bool, missing: list[str]).
    """
    required = list(_REQUIRED_COMMON)
    if mode == LOGIN_MODE_PASSWORD:
        required.extend(_REQUIRED_PASSWORD_MODE)
    # Email mode only needs DBDOCTOR_URL (+ DBDOCTOR_EMAIL which is already verified)
    missing = [k for k in required if not os.environ.get(k)]
    return len(missing) == 0, missing


class Config:
    """DBDoctor Configuration Management"""

    def __init__(self):
        # Try to load legacy .env file first (may populate env vars)
        _try_load_dotenv()

        # Detect login mode
        self.login_mode = _detect_login_mode()

        # Validate required env vars for the detected mode
        env_complete, missing = _check_env_vars_for_mode(self.login_mode)

        if not env_complete:
            raise ConfigError(
                f"Missing required environment variables: {', '.join(missing)}\n\n"
                f"Please configure using one of the following methods:\n\n"
                f"Mode 1 - Password login (one-click launch version):\n"
                f"   clawdbot skills config dbdoctor-tools DBDOCTOR_URL \"http://[host]:[port]\"\n"
                f"   clawdbot skills config dbdoctor-tools DBDOCTOR_USER \"[username]\"\n"
                f"   clawdbot skills config dbdoctor-tools DBDOCTOR_PASSWORD \"[password]\"\n\n"
                f"Mode 2 - Email verification code login (free version):\n"
                f"   clawdbot skills config dbdoctor-tools DBDOCTOR_URL \"http://[host]:[port]\"\n"
                f"   clawdbot skills config dbdoctor-tools DBDOCTOR_EMAIL \"[email]\""
            )

        self.base_url = os.environ["DBDOCTOR_URL"]
        # Role hardcoded as dev
        self.role = "dev"

        if self.login_mode == LOGIN_MODE_PASSWORD:
            self.username = os.environ["DBDOCTOR_USER"]
            # Support legacy ENC: prefixed passwords from old .env files
            self.password = _decrypt_from_storage(os.environ["DBDOCTOR_PASSWORD"])
            self.email = None
            # Username is used as UserId
            self.user_id = self.username
        else:
            self.username = None
            self.password = None
            self.email = os.environ["DBDOCTOR_EMAIL"].strip()
            self.user_id = self.email


# Global configuration singleton
config = Config()
