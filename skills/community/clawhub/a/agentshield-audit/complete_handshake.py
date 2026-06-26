#!/usr/bin/env python3
"""Complete Trust Handshake - Sign challenges and exchange session key."""
import argparse, base64, json, os, sys
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    import requests
except ImportError:
    print("❌ pip install cryptography requests")
    sys.exit(1)

API = os.getenv("AGENTSHIELD_API", "https://agentshield.live")

def load_key():
    p = Path.home() / ".openclaw" / "workspace" / ".agentshield" / "agent.key"
    if not p.exists():
        print(f"❌ No key at {p}. Run initiate_audit.py first.")
        sys.exit(1)
    return Ed25519PrivateKey.from_private_bytes(p.read_bytes())

def load_cert():
    p = Path.home() / ".openclaw" / "workspace" / ".agentshield" / "certificate.json"
    if not p.exists():
        print(f"❌ No cert at {p}. Run audit first.")
        sys.exit(1)
    return json.loads(p.read_text())["payload"]["sub"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--handshake-id", required=True)
    args = parser.parse_args()
    
    print("🔐 AgentShield Trust Handshake Completion\n")
    key = load_key()
    agent_id = load_cert()
    print(f"📜 Agent ID: {agent_id}\n")
    
    status = requests.get(f"{API}/trust-handshake/status/{args.handshake_id}").json()
    if status["status"] == "completed":
        print(f"✅ Already done! Session Key: {status['session_key']}")
        return
    
    req, tgt = status["requester"], status["target"]
    if req["agent_id"] == agent_id:
        chal, role, partner = req["challenge"], "requester", tgt["agent_id"]
    elif tgt["agent_id"] == agent_id:
        chal, role, partner = tgt["challenge"], "target", req["agent_id"]
    else:
        print(f"❌ You're not in this handshake!")
        sys.exit(1)
    
    print(f"✓ Role: {role.upper()} | Partner: {partner}\n🔏 Signing...")
    sig = base64.b64encode(key.sign(base64.b64decode(chal))).decode()
    
    res = requests.post(f"{API}/trust-handshake/complete", json={
        "handshake_id": args.handshake_id,
        "agent_id": agent_id,
        "signed_challenge": sig
    }).json()
    
    if res["status"] == "completed":
        print("="*50)
        print("✅ TRUST HANDSHAKE COMPLETE!")
        print(f"Session Key: {res['session_key']}")
        print("="*50)
    else:
        print(f"⏳ Status: {res['status']} - Waiting for partner...")

if __name__ == "__main__":
    main()
