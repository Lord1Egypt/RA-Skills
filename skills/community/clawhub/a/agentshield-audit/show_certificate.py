#!/usr/bin/env python3
"""
Display local AgentShield certificate.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

CERT_FILE = Path.home() / ".openclaw" / "workspace" / ".agentshield" / "certificate.json"
KEY_FILE = Path.home() / ".openclaw" / "workspace" / ".agentshield" / "agent.key"


def load_certificate():
    """Load certificate from disk."""
    if not CERT_FILE.exists():
        return None
    
    with open(CERT_FILE, 'r') as f:
        return json.load(f)


def load_keys():
    """Load keys from disk."""
    if not KEY_FILE.exists():
        return None
    
    with open(KEY_FILE, 'r') as f:
        return json.load(f)


def format_time_remaining(expires_at_str: str) -> str:
    """Calculate time remaining until expiration."""
    try:
        expires = datetime.fromisoformat(expires_at_str.replace('Z', '+00:00'))
        now = datetime.utcnow()
        if expires.tzinfo:
            expires = expires.replace(tzinfo=None)
        
        delta = expires - now
        days = delta.days
        
        if days < 0:
            return "EXPIRED"
        elif days == 0:
            hours = delta.seconds // 3600
            return f"{hours} hours"
        elif days == 1:
            return "1 day"
        else:
            return f"{days} days"
    except:
        return "Unknown"


def get_tier_badge(tier: str) -> str:
    """Get visual badge for tier."""
    badges = {
        'HARDENED': '🛡️  HARDENED',
        'PROTECTED': '🔒 PROTECTED',
        'BASIC': '🔓 BASIC',
        'UNVERIFIED': '❌ UNVERIFIED'
    }
    return badges.get(tier, tier)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Show AgentShield certificate")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--raw", action="store_true", help="Show raw certificate data")
    args = parser.parse_args()
    
    cert = load_certificate()
    keys = load_keys()
    
    if not cert:
        print("❌ No certificate found")
        print(f"   Run: python scripts/initiate_audit.py --name \"YourAgentName\"")
        sys.exit(1)
    
    if args.json:
        print(json.dumps(cert, indent=2))
        return
    
    if args.raw:
        print(json.dumps(cert, indent=2))
        return
    
    # Extract from payload if present
    payload = cert.get('payload', cert)
    
    # Pretty display
    print("=" * 60)
    print("       🛡️  AGENTSHIELD SECURITY CERTIFICATE")
    print("=" * 60)
    print()
    print(f"   Agent ID:     {payload.get('sub', cert.get('agent_id', 'Unknown'))}")
    print(f"   Agent Name:   {payload.get('agent_name', 'Unknown')}")
    print()
    print(f"   {get_tier_badge(payload.get('tier', 'UNKNOWN'))}")
    print(f"   Score:        {payload.get('score', 'N/A')}/100")
    print()
    issued = payload.get('iat')
    expires = payload.get('exp')
    if issued:
        issued_str = datetime.fromtimestamp(issued).isoformat()
    else:
        issued_str = cert.get('issued_at', 'Unknown')
    if expires:
        expires_str = datetime.fromtimestamp(expires).isoformat()
    else:
        expires_str = cert.get('expires_at', 'Unknown')
    print(f"   Issued:       {issued_str}")
    print(f"   Expires:      {expires_str}")
    
    expires = cert.get('expires_at')
    if expires:
        remaining = format_time_remaining(expires)
        if remaining == "EXPIRED":
            print(f"   Status:       ⚠️  EXPIRED - Please renew")
        else:
            print(f"   Valid for:    {remaining}")
    
    print()
    
    if keys:
        pubkey_short = keys.get('public_key', '')[:20] + "..."
        print(f"   Public Key:   {pubkey_short}")
    
    # Verification URL
    agent_id = cert.get('agent_id')
    if agent_id:
        print()
        print(f"   Verification: https://agentshield.live/verify/{agent_id}")
    
    print()
    print("=" * 60)
    print("   Other agents can verify this certificate at:")
    print("   https://agentshield.live/api/verify/")
    print("=" * 60)


if __name__ == "__main__":
    main()
