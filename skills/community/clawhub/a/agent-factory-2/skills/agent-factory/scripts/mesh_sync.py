#!/usr/bin/env python3
"""
ClawHub P2P & Mesh Federation Sync for OpenClaw.
Exports and imports validated sub-agent packages to/from ClawHub format (.tar.gz / bundle)
with cryptographic signature validation across instances.
"""

import json
import os
import tarfile
import shutil
import time
from typing import Dict, Any, List, Optional
from crypto_signer import verify_manifest, sign_file

AGENTS_DIR = os.path.join(os.path.dirname(__file__), "..", "agents")
EXPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "exports")


def export_agent_bundle(agent_id: str, version: str = "v1.0.0") -> str:
    """Exports a validated sub-agent into a deployable ClawHub bundle archive."""
    agent_path = os.path.join(AGENTS_DIR, agent_id, version)
    if not os.path.exists(agent_path):
        raise FileNotFoundError(f"Agent {agent_id} ({version}) introuvable.")

    manifest_file = os.path.join(agent_path, "manifest.json")
    # Ensure signed
    sign_file(manifest_file)

    os.makedirs(EXPORTS_DIR, exist_ok=True)
    bundle_name = f"{agent_id}-{version}.clawbundle.tar.gz"
    bundle_path = os.path.join(EXPORTS_DIR, bundle_name)

    with tarfile.open(bundle_path, "w:gz") as tar:
        tar.add(agent_path, arcname=f"{agent_id}/{version}")

    return bundle_path


def import_agent_bundle(bundle_path: str) -> Dict[str, Any]:
    """Imports a ClawHub sub-agent bundle and verifies its cryptographic signature."""
    if not os.path.exists(bundle_path):
        raise FileNotFoundError(f"Archive bundle {bundle_path} introuvable.")

    with tarfile.open(bundle_path, "r:gz") as tar:
        tar.extractall(path=AGENTS_DIR)

    # Find extracted manifest and verify
    bundle_basename = os.path.basename(bundle_path).replace(".clawbundle.tar.gz", "")
    parts = bundle_basename.split("-")
    agent_id = parts[0]
    version = parts[1] if len(parts) > 1 else "v1.0.0"

    manifest_path = os.path.join(AGENTS_DIR, agent_id, version, "manifest.json")
    is_valid, msg = verify_manifest(manifest_path)

    return {
        "status": "imported",
        "agent_id": agent_id,
        "version": version,
        "signature_valid": is_valid,
        "integrity_message": msg
    }


def list_federated_mesh() -> List[Dict[str, Any]]:
    """Returns local active agents and exported bundles."""
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    bundles = os.listdir(EXPORTS_DIR)
    return [{
        "bundle": b,
        "size_bytes": os.path.getsize(os.path.join(EXPORTS_DIR, b)),
        "exported_at": os.path.getmtime(os.path.join(EXPORTS_DIR, b))
    } for b in bundles if b.endswith(".clawbundle.tar.gz")]


if __name__ == "__main__":
    print("🌐 ClawHub P2P Mesh Sync Engine Ready.")
    bundles = list_federated_mesh()
    print(f"📦 Bundles exportés disponibles: {len(bundles)}")
