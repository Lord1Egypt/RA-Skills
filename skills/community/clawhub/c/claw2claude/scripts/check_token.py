#!/usr/bin/env python3
"""
Generic OpenClaw credential health check.

Reads all credential files under ~/.openclaw/credentials/, decodes any JWT
tokens found, and warns if a token is expired or about to expire.

No provider-specific refresh logic — refreshing is OpenClaw's responsibility.
Exit code is always 0 (warnings only, never blocks execution).
"""
import base64
import json
import sys
import time
from pathlib import Path

OPENCLAW_DIR = Path.home() / ".openclaw"
CONFIG_FILE  = OPENCLAW_DIR / "openclaw.json"
CREDS_DIR    = OPENCLAW_DIR / "credentials"
WARN_BEFORE  = 5 * 60  # Warn when fewer than 5 minutes remain


def decode_jwt_exp(token: str) -> float | None:
    """Decode the exp field from a JWT payload without verifying the signature."""
    try:
        parts = token.strip().split(".")
        if len(parts) != 3:
            return None
        # JWT uses base64url — pad to a multiple of 4
        payload_b64 = parts[1] + "=" * (-len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        return float(payload["exp"]) if "exp" in payload else None
    except Exception:
        return None


def find_credential_files() -> list[Path]:
    """Return all candidate credential files (.txt or .json) in the credentials directory."""
    candidates = []
    for f in CREDS_DIR.glob("*"):
        if f.suffix in (".txt", ".json") and f.is_file():
            candidates.append(f)
    return candidates


def extract_tokens(cred_file: Path) -> list[str]:
    """Extract token strings from a credential file."""
    try:
        text = cred_file.read_text().strip()
        # JSON format: read access_token or token field
        if text.startswith("{"):
            data = json.loads(text)
            return [v for k, v in data.items()
                    if k in ("access_token", "token") and isinstance(v, str)]
        # Plain text: treat the whole content as a token
        return [text] if text else []
    except Exception:
        return []


def check_token_in_file(cred_file: Path) -> None:
    tokens = extract_tokens(cred_file)
    for token in tokens:
        exp = decode_jwt_exp(token)
        if exp is None:
            continue  # Not a JWT — skip
        remaining = exp - time.time()
        name = cred_file.name
        if remaining <= 0:
            print(f"⚠️  [{name}] token has expired — please re-authenticate in OpenClaw", file=sys.stderr)
        elif remaining < WARN_BEFORE:
            mins = int(remaining / 60)
            print(f"⚠️  [{name}] token expires in {mins} minute(s) — "
                  f"long-running tasks may lose their OpenClaw connection", file=sys.stderr)
        else:
            mins = int(remaining / 60)
            print(f"✅ [{name}] token valid (~{mins} minutes remaining)", file=sys.stderr)


def main():
    if not CREDS_DIR.exists():
        return  # No credentials directory — nothing to check

    cred_files = find_credential_files()
    if not cred_files:
        return

    checked = 0
    for f in cred_files:
        tokens = extract_tokens(f)
        if any(decode_jwt_exp(t) is not None for t in tokens):
            check_token_in_file(f)
            checked += 1

    # No JWT tokens found — API key credentials don't expire, so nothing to warn about


if __name__ == "__main__":
    main()
    sys.exit(0)  # Always exit 0 — warnings only, never block
