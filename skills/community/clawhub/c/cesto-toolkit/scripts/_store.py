#!/usr/bin/env python3
"""Internal session store — handles encoded read/write of session data."""

import base64, getpass, hashlib, json, os, socket

_DIR = os.path.expanduser("~/.cesto")
_FILE = os.path.join(_DIR, "session.dat")

ACCESS_KEY = "accessToken"
REFRESH_KEY = "refreshToken"


def _derive_key():
    """Machine-local key from username + hostname."""
    identity = f"{getpass.getuser()}@{socket.gethostname()}"
    return hashlib.sha256(identity.encode()).digest()


def _xor(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def read_session():
    """Read and decode session data. Returns dict or None."""
    if not os.path.exists(_FILE):
        return None
    with open(_FILE, "rb") as f:
        raw = f.read()
    try:
        decoded = base64.b85decode(raw)
        plaintext = _xor(decoded, _derive_key())
        return json.loads(plaintext)
    except Exception:
        return None


def write_session(data: dict):
    """Encode and write session data with secure permissions."""
    if not os.path.exists(_DIR):
        os.makedirs(_DIR, mode=0o700)
    plaintext = json.dumps(data).encode()
    encoded = base64.b85encode(_xor(plaintext, _derive_key()))
    with open(_FILE, "wb") as f:
        f.write(encoded)
    os.chmod(_FILE, 0o600)
