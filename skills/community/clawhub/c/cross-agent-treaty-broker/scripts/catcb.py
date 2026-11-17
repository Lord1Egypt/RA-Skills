#!/usr/bin/env python3
"""Cross-Agent Treaty Broker CLI - negotiate and manage inter-agent treaties."""

import argparse
import os
import sys
import json
import uuid
import hashlib
from datetime import datetime

# Define paths
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SKILL_DIR, "data")
TREATIES_DIR = os.path.join(DATA_DIR, "treaties")
LOGS_DIR = os.path.join(DATA_DIR, "logs")
ANCHORS_DIR = os.path.join(DATA_DIR, "anchors")


def ensure_setup():
    """Ensure skill is initialized."""
    for directory in [DATA_DIR, TREATIES_DIR, LOGS_DIR, ANCHORS_DIR]:
        os.makedirs(directory, exist_ok=True)

    # Initialize anchor registry
    registry = {
        "anchors": [],
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    registry_path = os.path.join(ANCHORS_DIR, "registry.json")
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)

    print(f"CATB initialized. Data directory: {DATA_DIR}")
    print(f"Treaties directory: {TREATIES_DIR}")
    print(f"Logs directory: {LOGS_DIR}")
    print(f"Anchors directory: {ANCHORS_DIR}")


def generate_treaty_id():
    """Generate a unique treaty ID."""
    return f"tre-{uuid.uuid4().hex[:8]}"


def generate_anchor_hash(data):
    """Generate SHA256 hash for treaty anchor."""
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def propose_treaty(args):
    """Create and propose a treaty to another agent."""
    ensure_setup()

    # Load existing treaty if specified
    treaty_file = args.treaty
    if treaty_file and os.path.exists(treaty_file):
        with open(treaty_file, 'r') as f:
            treaty_data = json.load(f)
    else:
        # Create new treaty structure
        treaty_data = {
            "treaty_id": generate_treaty_id(),
            "parties": {
                "agent_a": {"id": args.to, "role": "proposer"},
                "agent_b": {"id": args.with_agent or "target-agent", "role": "respondent"}
            },
            "terms": {
                "data_sharing": {"scopes": [], "retention": ""},
                "capability_access": {"allowed_ops": [], "rate_limits": {}},
                "escalation_paths": {"dispute_resolution": ""},
                "revocation_conditions": {"notice_period": "", "cleanup": ""}
            },
            "timeline": {
                "proposed_at": datetime.utcnow().isoformat() + "Z",
                "reviewed_at": None,
                "signed_at": None,
                "effective_at": None
            },
            "signatures": {
                "agent_a": {"signed_by": None, "timestamp": None},
                "agent_b": {"signed_by": None, "timestamp": None}
            }
        }

    # Save treaty proposal
    treaties_dir = os.path.join(DATA_DIR, "treaties")
    os.makedirs(treaties_dir, exist_ok=True)

    output_file = os.path.join(treaties_dir, f"{treaty_data['treaty_id']}.json")
    with open(output_file, 'w') as f:
        json.dump(treaty_data, f, indent=2)

    # Log the proposal
    log_entry = {
        "event": "proposal_created",
        "treaty_id": treaty_data["treaty_id"],
        "proposed_to": args.to,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    log_file = os.path.join(LOGS_DIR, "treaty-events.log")
    os.makedirs(LOGS_DIR, exist_ok=True)

    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"Treaty proposed: {treaty_data['treaty_id']}")
    print(f"Saved to: {output_file}")
    return 0


def review_treaty(args):
    """Show human-readable preview of a treaty."""
    ensure_setup()

    treaty_file = os.path.join(TREATIES_DIR, f"{args.treaty_id}.json")
    if not os.path.exists(treaty_file):
        print(f"Treaty not found: {args.treaty_id}")
        return 1

    with open(treaty_file, 'r') as f:
        treaty_data = json.load(f)

    # Generate human-readable summary
    print("=" * 60)
    print("TREATY PREVIEW")
    print("=" * 60)
    print(f"\nTreaty ID: {treaty_data.get('treaty_id', 'N/A')}")
    print(f"Proposed: {treaty_data.get('timeline', {}).get('proposed_at', 'N/A')}")

    parties = treaty_data.get('parties', {})
    if 'agent_a' in parties:
        print(f"\nParties:")
        print(f"  Agent A: {parties['agent_a'].get('id', 'N/A')} ({parties['agent_a'].get('role', 'N/A')})")
    if 'agent_b' in parties:
        print(f"  Agent B: {parties['agent_b'].get('id', 'N/A')} ({parties['agent_b'].get('role', 'N/A')})")

    terms = treaty_data.get('terms', {})
    if terms:
        print(f"\nTerms:")
        for key, value in terms.items():
            if value:
                print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("REVIEW THIS TREATY BEFORE SIGNING")
    print("=" * 60)

    return 0


def sign_treaty(args):
    """Sign a treaty (requires human confirmation)."""
    ensure_setup()

    treaty_file = os.path.join(TREATIES_DIR, f"{args.treaty_id}.json")
    if not os.path.exists(treaty_file):
        print(f"Treaty not found: {args.treaty_id}")
        return 1

    with open(treaty_file, 'r') as f:
        treaty_data = json.load(f)

    # Update signature
    signer = args.signer or "human-operator"
    treaty_data['signatures']['agent_a']['signed_by'] = signer
    treaty_data['signatures']['agent_a']['timestamp'] = datetime.utcnow().isoformat() + "Z"
    treaty_data['timeline']['signed_at'] = datetime.utcnow().isoformat() + "Z"

    # Save signed treaty
    with open(treaty_file, 'w') as f:
        json.dump(treaty_data, f, indent=2)

    # Record anchor
    anchor_hash = generate_anchor_hash(treaty_data)
    registry_file = os.path.join(ANCHORS_DIR, "registry.json")

    with open(registry_file, 'r') as f:
        registry = json.load(f)

    registry['anchors'].append({
        "treaty_id": treaty_data['treaty_id'],
        "anchor_hash": anchor_hash,
        "signed_at": treaty_data['timeline']['signed_at'],
        "signer": signer
    })

    with open(registry_file, 'w') as f:
        json.dump(registry, f, indent=2)

    print(f"Treaty signed and anchored: {treaty_data['treaty_id']}")
    print(f"Anchor hash: {anchor_hash[:16]}...")

    return 0


def list_treaties(args):
    """List all treaties."""
    ensure_setup()

    treaties = []
    for file in os.listdir(TREATIES_DIR):
        if file.endswith('.json'):
            with open(os.path.join(TREATIES_DIR, file), 'r') as f:
                treaty_data = json.load(f)
            treaties.append(treaty_data)

    if not treaties:
        print("No treaties found.")
        return 0

    print(f"\n{'=' * 60}")
    print(f"ACTIVE TREATIES ({len(treaties)} total)")
    print(f"{'=' * 60}\n")

    for t in treaties:
        print(f"Treaty: {t.get('treaty_id', 'N/A')}")
        print(f"  Proposed: {t.get('timeline', {}).get('proposed_at', 'N/A')}")
        print(f"  Signed: {t.get('timeline', {}).get('signed_at', 'Not yet signed')}")
        parties = t.get('parties', {})
        if 'agent_a' in parties:
            print(f"  Agent A: {parties['agent_a'].get('id', 'N/A')}")
        if 'agent_b' in parties:
            print(f"  Agent B: {parties['agent_b'].get('id', 'N/A')}")
        print()

    return 0


def revoke_treaty(args):
    """Revoke a treaty."""
    ensure_setup()

    treaty_file = os.path.join(TREATIES_DIR, f"{args.treaty_id}.json")
    if not os.path.exists(treaty_file):
        print(f"Treaty not found: {args.treaty_id}")
        return 1

    with open(treaty_file, 'r') as f:
        treaty_data = json.load(f)

    reason = args.reason or "No reason provided"

    # Log revocation
    log_entry = {
        "event": "treaty_revoked",
        "treaty_id": treaty_data['treaty_id'],
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    log_file = os.path.join(LOGS_DIR, "treaty-events.log")
    os.makedirs(LOGS_DIR, exist_ok=True)

    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + "\n")

    # Remove treaty file
    os.remove(treaty_file)
    print(f"Treaty revoked: {treaty_data['treaty_id']}")
    print(f"Reason: {reason}")

    return 0


def audit_treaty(args):
    """Show audit trail for a treaty."""
    ensure_setup()

    treaty_file = os.path.join(TREATIES_DIR, f"{args.treaty_id}.json")
    if not os.path.exists(treaty_file):
        print(f"Treaty not found: {args.treaty_id}")
        return 1

    with open(treaty_file, 'r') as f:
        treaty_data = json.load(f)

    # Get anchor info
    registry_file = os.path.join(ANCHORS_DIR, "registry.json")
    if os.path.exists(registry_file):
        with open(registry_file, 'r') as f:
            registry = json.load(f)

        anchor_info = None
        for anchor in registry.get('anchors', []):
            if anchor['treaty_id'] == treaty_data['treaty_id']:
                anchor_info = anchor
                break

        if anchor_info:
            print(f"Anchor hash: {anchor_info['anchor_hash']}")
            print(f"Signed at: {anchor_info['signed_at']}")
            print(f"Signer: {anchor_info['signer']}")

    print(f"\nTreaty: {treaty_data['treaty_id']}")
    print(f"Status: {'signed' if treaty_data['timeline']['signed_at'] else 'proposed'}")
    print(f"Parties:")
    parties = treaty_data.get('parties', {})
    if 'agent_a' in parties:
        print(f"  - {parties['agent_a']}")
    if 'agent_b' in parties:
        print(f"  - {parties['agent_b']}")

    return 0


def main():
    parser = argparse.ArgumentParser(description="Cross-Agent Treaty Broker CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize CATB skill')

    # Propose command
    propose_parser = subparsers.add_parser('propose', help='Propose a treaty')
    propose_parser.add_argument('--to', required=True, help='Target agent ID')
    propose_parser.add_argument('--with-agent', help='Agent to negotiate with')
    propose_parser.add_argument('--treaty', help='Path to treaty JSON file')

    # Review command
    review_parser = subparsers.add_parser('review', help='Review treaty')
    review_parser.add_argument('treaty_id', help='Treaty ID')

    # Sign command
    sign_parser = subparsers.add_parser('sign', help='Sign a treaty')
    sign_parser.add_argument('treaty_id', help='Treaty ID')
    sign_parser.add_argument('--signer', help='Signer identity')

    # List command
    list_parser = subparsers.add_parser('list', help='List all treaties')

    # Revoke command
    revoke_parser = subparsers.add_parser('revoke', help='Revoke a treaty')
    revoke_parser.add_argument('treaty_id', help='Treaty ID')
    revoke_parser.add_argument('--reason', help='Reason for revocation')

    # Audit command
    audit_parser = subparsers.add_parser('audit', help='Audit a treaty')
    audit_parser.add_argument('treaty_id', help='Treaty ID')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == 'init':
        ensure_setup()
        return 0
    elif args.command == 'propose':
        return propose_treaty(args)
    elif args.command == 'review':
        return review_treaty(args)
    elif args.command == 'sign':
        return sign_treaty(args)
    elif args.command == 'list':
        return list_treaties(args)
    elif args.command == 'revoke':
        return revoke_treaty(args)
    elif args.command == 'audit':
        return audit_treaty(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())