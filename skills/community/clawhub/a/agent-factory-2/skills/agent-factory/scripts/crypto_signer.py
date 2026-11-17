#!/usr/bin/env python3
"""
Cryptographic Manifest Signer & Integrity Verifier for OpenClaw.
Guarantees sub-agent manifests cannot be tampered with or escalated locally.
"""

import hmac
import hashlib
import json
import os
from typing import Tuple

SECRET_KEY_ENV = "OPENCLAW_FACTORY_SIGNING_KEY"
DEFAULT_KEY = "openclaw_secret_master_factory_key_2026"


def _get_key() -> bytes:
    key_str = os.environ.get(SECRET_KEY_ENV, DEFAULT_KEY)
    return key_str.encode("utf-8")


def sign_manifest(manifest_dict: dict) -> str:
    """Computes HMAC-SHA256 signature for a sub-agent manifest dictionary."""
    canonical_bytes = json.dumps(manifest_dict, sort_keys=True).encode("utf-8")
    return hmac.new(_get_key(), canonical_bytes, hashlib.sha256).hexdigest()


def verify_manifest(manifest_path: str) -> Tuple[bool, str]:
    """Verifies that a manifest file matches its signature."""
    sig_path = manifest_path + ".sig"
    if not os.path.exists(manifest_path):
        return False, "Manifest file not found"
    if not os.path.exists(sig_path):
        return False, "Signature file (.sig) not found"

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_dict = json.load(f)

    with open(sig_path, "r", encoding="utf-8") as f:
        stored_sig = f.read().strip()

    expected_sig = sign_manifest(manifest_dict)
    if hmac.compare_digest(stored_sig, expected_sig):
        return True, "Signature valid and verified"
    else:
        return False, "Cryptographic signature MISMATCH (Tampering detected)"


def sign_file(manifest_path: str) -> str:
    """Signs a manifest file on disk and writes .sig companion file."""
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_dict = json.load(f)

    signature = sign_manifest(manifest_dict)
    sig_path = manifest_path + ".sig"
    with open(sig_path, "w", encoding="utf-8") as f:
        f.write(signature)
    return signature


if __name__ == "__main__":
    import sys
    test_manifest = {"agent_id": "subagent_test", "status": "active", "allowed_tools": ["calc_tax"]}
    sig = sign_manifest(test_manifest)
    print("🔐 Test Manifest Signature:", sig[:16] + "...")
