#!/usr/bin/env python3
"""Generate unique canary tokens with distinctive fingerprints."""

import json
import os
import secrets
import string
import hashlib
from datetime import datetime, timezone

CANARY_DIR = os.path.expanduser("~/.openclaw/agent-canary")
MANIFEST_PATH = os.path.join(CANARY_DIR, "manifest.json")

# Token generators: (id_prefix, token_type, generator_function)
def gen_aws_key():
    """AKIA + 16 uppercase alphanumeric."""
    chars = string.ascii_uppercase + string.digits
    return "AKIACANARY" + "".join(secrets.choice(chars) for _ in range(7))

def gen_github_token():
    """ghp_CANARY_ + 36 chars."""
    chars = string.ascii_letters + string.digits
    return "ghp_CANARY_" + "".join(secrets.choice(chars) for _ in range(36))

def gen_stripe_key():
    """sk_live_CANARY_ + 24 chars."""
    chars = string.ascii_letters + string.digits
    return "sk_live_CANARY_" + "".join(secrets.choice(chars) for _ in range(24))

def gen_api_key():
    """sk-CANARY- + 32 chars."""
    chars = string.ascii_letters + string.digits
    return "sk-CANARY-" + "".join(secrets.choice(chars) for _ in range(32))

def gen_db_password():
    """CANARY_PASS_ + 16 chars."""
    chars = string.ascii_letters + string.digits
    return "CANARY_PASS_" + "".join(secrets.choice(chars) for _ in range(16))

def gen_token_id():
    """8-char hex ID for tracking."""
    return secrets.token_hex(4).upper()

TOKEN_TYPES = [
    ("aws", gen_aws_key),
    ("github", gen_github_token),
    ("stripe", gen_stripe_key),
    ("api_key", gen_api_key),
    ("db_password", gen_db_password),
]

def generate_all_tokens():
    """Generate one of each token type with unique IDs."""
    tokens = []
    for ttype, genfn in TOKEN_TYPES:
        tid = gen_token_id()
        tval = genfn()
        tokens.append({
            "id": tid,
            "type": ttype,
            "value": tval,
            "greppable": tval,  # exact string to grep for
        })
    return tokens

def file_hash(path):
    """SHA-256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def save_manifest(planted_files, tokens):
    """Save manifest with all token info and file hashes."""
    os.makedirs(CANARY_DIR, exist_ok=True)
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_check": None,
        "tokens": tokens,
        "files": planted_files,
    }
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    os.chmod(MANIFEST_PATH, 0o600)
    return manifest

def load_manifest():
    """Load manifest or return None."""
    if not os.path.exists(MANIFEST_PATH):
        return None
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    tokens = generate_all_tokens()
    print("=== Generated Canary Tokens ===")
    for t in tokens:
        print(f"  [{t['id']}] {t['type']}: {t['value']}")
