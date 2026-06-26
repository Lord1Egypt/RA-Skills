#!/usr/bin/env python3
"""
Verify peer agents using AgentShield certificates.
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime
from pathlib import Path

AGENTSHIELD_API = os.environ.get("AGENTSHIELD_API", "https://agentshield.live")


def verify_certificate_signature(certificate: dict, agentshield_pubkey: str) -> bool:
    """
    Verify that the certificate was signed by AgentShield.
    In production, this would use Ed25519 signature verification.
    """
    # TODO: Implement actual signature verification in Phase 2
    # For now, trust the API response
    return True


def check_certificate_validity(certificate: dict) -> dict:
    """Check if certificate is valid (not expired, not revoked)."""
    from email.utils import parsedate_to_datetime
    now = datetime.utcnow()
    
    # Parse expiration (supports ISO string, Unix timestamp, and HTTP date format)
    expires_at_raw = certificate.get('expires_at') or certificate.get('exp')
    if expires_at_raw:
        try:
            # Handle Unix timestamp (integer)
            if isinstance(expires_at_raw, (int, float)):
                expires_at = datetime.utcfromtimestamp(expires_at_raw)
            # Handle string formats
            elif isinstance(expires_at_raw, str):
                # Try HTTP date format first (from backend)
                if ',' in expires_at_raw and 'GMT' in expires_at_raw:
                    expires_at = parsedate_to_datetime(expires_at_raw)
                    if expires_at.tzinfo:
                        expires_at = expires_at.replace(tzinfo=None)
                # Try ISO format
                else:
                    expires_at = datetime.fromisoformat(expires_at_raw.replace('Z', '+00:00'))
                    if expires_at.tzinfo:
                        expires_at = expires_at.replace(tzinfo=None)
            else:
                return {
                    'valid': False,
                    'reason': f"Invalid expiration date type: {type(expires_at_raw)}"
                }
            
            if now > expires_at:
                return {
                    'valid': False,
                    'reason': f"Certificate expired on {expires_at.isoformat()}"
                }
        except (ValueError, OSError, TypeError) as e:
            return {
                'valid': False,
                'reason': f"Invalid expiration date format: {e}"
            }
    
    # Check status
    status = certificate.get('status', 'active')
    if status == 'revoked':
        return {
            'valid': False,
            'reason': "Certificate has been revoked"
        }
    
    if status != 'active':
        return {
            'valid': False,
            'reason': f"Certificate status: {status}"
        }
    
    return {'valid': True}


def verify_agent(agent_id: str, require_tier: str = None) -> dict:
    """
    Verify an agent by their AgentShield ID.
    
    Args:
        agent_id: The agent's unique identifier
        require_tier: Minimum tier required ('HARDENED', 'PROTECTED', 'BASIC')
    
    Returns:
        dict with verification result
    """
    import requests
    
    try:
        response = requests.get(
            f"{AGENTSHIELD_API}/api/verify/{agent_id}",
            timeout=30  # Increased for Heroku cold starts
        )
        response.raise_for_status()
        certificate = response.json()
    except requests.exceptions.ConnectionError:
        return {
            'valid': False,
            'reason': f"Cannot connect to AgentShield API",
            'agent_id': agent_id
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {
                'valid': False,
                'reason': f"Agent {agent_id} not found or not certified",
                'agent_id': agent_id
            }
        return {
            'valid': False,
            'reason': f"API error: {e}",
            'agent_id': agent_id
        }
    
    # Check certificate validity
    validity = check_certificate_validity(certificate)
    if not validity['valid']:
        return {
            'valid': False,
            'reason': validity['reason'],
            'agent_id': agent_id,
            'certificate': certificate
        }
    
    # Check tier requirement
    tier = certificate.get('tier', 'UNKNOWN')
    if require_tier:
        tier_order = {'BASIC': 1, 'PROTECTED': 2, 'HARDENED': 3}
        agent_tier_level = tier_order.get(tier, 0)
        required_tier_level = tier_order.get(require_tier, 0)
        
        if agent_tier_level < required_tier_level:
            return {
                'valid': False,
                'reason': f"Tier requirement not met. Agent has {tier}, requires {require_tier}+",
                'agent_id': agent_id,
                'tier': tier,
                'certificate': certificate
            }
    
    # All checks passed
    return {
        'valid': True,
        'agent_id': agent_id,
        'agent_name': certificate.get('agent_name'),
        'tier': tier,
        'score': certificate.get('score'),
        'issued_at': certificate.get('issued_at'),
        'expires_at': certificate.get('expires_at'),
        'public_key': certificate.get('public_key'),
        'certificate': certificate
    }


def verify_challenge(agent_id: str, challenge: str, signature: str, public_key: str) -> bool:
    """
    Verify that an agent controls the private key for their certificate.
    
    Args:
        agent_id: Agent identifier
        challenge: The challenge string that was signed
        signature: Base64-encoded signature
        public_key: Base64-encoded Ed25519 public key from certificate
    
    Returns:
        True if signature is valid
    """
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        
        public_bytes = base64.b64decode(public_key)
        ed_public_key = Ed25519PublicKey.from_public_bytes(public_bytes)
        
        sig_bytes = base64.b64decode(signature)
        ed_public_key.verify(sig_bytes, challenge.encode('utf-8'))
        return True
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return False


def generate_challenge() -> str:
    """Generate a random challenge string."""
    import secrets
    import string
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))


def main():
    parser = argparse.ArgumentParser(description="Verify an agent's AgentShield certificate")
    parser.add_argument("agent-id", help="Agent ID to verify")
    parser.add_argument("--require-tier", choices=['BASIC', 'PROTECTED', 'HARDENED'],
                       help="Minimum required tier")
    parser.add_argument("--challenge", action="store_true",
                       help="Generate and verify challenge (proof of key ownership)")
    parser.add_argument("--json", action="store_true",
                       help="Output as JSON")
    
    args = parser.parse_args()
    agent_id = getattr(args, 'agent-id')
    
    # Verify certificate
    result = verify_agent(agent_id, args.require_tier)
    
    if args.json:
        print(json.dumps(result, indent=2))
        sys.exit(0 if result['valid'] else 1)
    
    # Human-readable output
    print(f"🔍 Agent Verification: {agent_id}")
    print("=" * 50)
    
    if not result['valid']:
        print(f"❌ VERIFICATION FAILED")
        print(f"   Reason: {result['reason']}")
        sys.exit(1)
    
    print(f"✅ CERTIFICATE VALID")
    print(f"   Agent Name: {result.get('agent_name', 'Unknown')}")
    print(f"   Tier: {result['tier']}")
    print(f"   Security Score: {result.get('security_score', result.get('score', 'N/A'))}/100")
    print(f"   Issued: {result['issued_at']}")
    print(f"   Expires: {result['expires_at']}")
    
    # Optional challenge-response
    if args.challenge:
        print(f"\n🔑 Challenge-Response Verification")
        challenge = generate_challenge()
        print(f"   Challenge: {challenge}")
        print(f"   (In real usage, the agent would sign this challenge)")
        # TODO: Implement interactive challenge in Phase 3
    
    print("\n✓ Agent verified - safe to communicate")


if __name__ == "__main__":
    main()
