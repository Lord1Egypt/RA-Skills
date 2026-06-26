"""Discord token extraction from local browser and Discord client data."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


# Discord token regex patterns
# Tokens can be:
#   - Regular user token: base64(user_id).timestamp.hmac
#   - MFA token: mfa.base64_encoded_string
_TOKEN_PATTERNS = [
    re.compile(r'[\w-]{24,}\.[\w-]{6}\.[\w-]{27,}'),
    re.compile(r'mfa\.[\w-]{84}'),
]


def _get_search_paths() -> list[tuple[str, Path]]:
    """Return list of (source_name, leveldb_path) to search for tokens."""
    home = Path.home()

    if sys.platform == "darwin":
        paths = [
            ("Discord App", home / "Library/Application Support/discord/Local Storage/leveldb"),
            ("Discord PTB", home / "Library/Application Support/discordptb/Local Storage/leveldb"),
            ("Discord Canary", home / "Library/Application Support/discordcanary/Local Storage/leveldb"),
            ("Chrome", home / "Library/Application Support/Google/Chrome/Default/Local Storage/leveldb"),
            ("Brave", home / "Library/Application Support/BraveSoftware/Brave-Browser/Default/Local Storage/leveldb"),
            ("Edge", home / "Library/Application Support/Microsoft Edge/Default/Local Storage/leveldb"),
            ("Firefox", home / "Library/Application Support/Firefox/Profiles"),
        ]
    elif os.name == "nt":
        appdata = Path(os.environ.get("APPDATA", ""))
        local_appdata = Path(os.environ.get("LOCALAPPDATA", ""))
        paths = [
            ("Discord App", appdata / "discord/Local Storage/leveldb"),
            ("Discord PTB", appdata / "discordptb/Local Storage/leveldb"),
            ("Discord Canary", appdata / "discordcanary/Local Storage/leveldb"),
            ("Chrome", local_appdata / "Google/Chrome/User Data/Default/Local Storage/leveldb"),
            ("Brave", local_appdata / "BraveSoftware/Brave-Browser/User Data/Default/Local Storage/leveldb"),
            ("Edge", local_appdata / "Microsoft/Edge/User Data/Default/Local Storage/leveldb"),
        ]
    else:  # Linux
        config = Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
        paths = [
            ("Discord App", config / "discord/Local Storage/leveldb"),
            ("Discord PTB", config / "discordptb/Local Storage/leveldb"),
            ("Discord Canary", config / "discordcanary/Local Storage/leveldb"),
            ("Chrome", config / "google-chrome/Default/Local Storage/leveldb"),
            ("Brave", config / "BraveSoftware/Brave-Browser/Default/Local Storage/leveldb"),
        ]

    return [(name, p) for name, p in paths if p.exists()]


def _extract_tokens_from_file(filepath: Path) -> list[str]:
    """Extract Discord tokens from a single file by regex scanning."""
    tokens: list[str] = []
    try:
        data = filepath.read_bytes().decode("utf-8", errors="ignore")
        for pattern in _TOKEN_PATTERNS:
            tokens.extend(pattern.findall(data))
    except (OSError, PermissionError):
        pass
    return tokens


def find_tokens() -> list[dict]:
    """Scan known browser/Discord client paths for tokens.

    Returns list of {source, token} dicts, deduplicated by token.
    """
    search_paths = _get_search_paths()
    found: dict[str, str] = {}  # token -> source

    for source_name, db_path in search_paths:
        if not db_path.is_dir():
            continue

        # Scan .ldb and .log files
        for ext in ("*.ldb", "*.log"):
            for filepath in db_path.glob(ext):
                for token in _extract_tokens_from_file(filepath):
                    if token not in found:
                        found[token] = source_name

    return [{"source": source, "token": token} for token, source in found.items()]


def save_token_to_env(token: str, env_path: Path | None = None) -> Path:
    """Save token to .env file."""
    if env_path is None:
        env_path = Path.cwd() / ".env"

    lines = []
    token_found = False

    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("DISCORD_TOKEN="):
                lines.append(f"DISCORD_TOKEN={token}")
                token_found = True
            else:
                lines.append(line)

    if not token_found:
        lines.append(f"DISCORD_TOKEN={token}")

    env_path.write_text("\n".join(lines) + "\n")
    return env_path
