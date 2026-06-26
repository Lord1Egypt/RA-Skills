#!/usr/bin/env python3
"""
AgentShield Trust Handshake Helper

Simplified helper script for initiating trust handshakes with other agents.
"""

import argparse
import json
import sys
from pathlib import Path
import requests

# Configuration
AGENTSHIELD_API = "https://agentshield.live"


def load_my_agent_id():
    """Load agent ID from local certificate."""
    cert_path = Path.home() / ".openclaw" / "workspace" / ".agentshield" / "certificate.json"
    
    if not cert_path.exists():
        print("❌ No certificate found!")
        print("   Run 'python3 initiate_audit.py' first to get certified.")
        return None
    
    with open(cert_path) as f:
        cert = json.load(f)
    
    return cert['payload']['sub']  # Agent ID


def initiate_handshake(my_agent_id: str, target_agent_id: str, ttl_seconds: int = 600):
    """Initiate a trust handshake with another agent."""
    
    print(f"🤝 Initiating Trust Handshake")
    print(f"   Requester: {my_agent_id}")
    print(f"   Target: {target_agent_id}")
    print()
    
    url = f"{AGENTSHIELD_API}/api/trust-handshake/initiate"
    
    payload = {
        "requester_id": my_agent_id,
        "target_id": target_agent_id,
        "ttl_seconds": ttl_seconds
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)  # Increased for cold starts
        response.raise_for_status()
        
        data = response.json()
        
        print("✅ Handshake Initiated Successfully!")
        print()
        print(f"Handshake ID: {data['handshake_id']}")
        print(f"Status: {data['status']}")
        print(f"Expires: {data['expires_at']}")
        print()
        print("📋 Next Steps:")
        print("1. Both agents must sign their respective challenges")
        print("2. Call /api/trust-handshake/complete with signatures")
        print("3. Receive shared session key for encrypted communication")
        print()
        print("Challenges:")
        print(f"  Yours: {data['requester']['challenge'][:50]}...")
        print(f"  Theirs: {data['target']['challenge'][:50]}...")
        
        return data
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"   Response: {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Initiate a trust handshake with another AgentShield-certified agent"
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target agent ID (e.g., agent_xxxxx)"
    )
    parser.add_argument(
        "--ttl",
        type=int,
        default=600,
        help="Handshake TTL in seconds (default: 600 = 10 minutes)"
    )
    
    args = parser.parse_args()
    
    # Load my agent ID
    my_agent_id = load_my_agent_id()
    if not my_agent_id:
        sys.exit(1)
    
    # Initiate handshake
    result = initiate_handshake(my_agent_id, args.target, args.ttl)
    
    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
