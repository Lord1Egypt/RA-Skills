#!/usr/bin/env python3
"""
Guardian Audit — Event Logger
Appends tamper-evident entries to the audit log.

Usage:
    python3 log-event.py --event-type GUARDIAN_HALT --operation "rm -rf /tmp/old" \
        --target "/tmp/old" --category HIGH --backup-verdict UNVERIFIED \
        --decision HALT --approver guardian-auto \
        --agent-reasoning "Cleaning up old builds" \
        --guardian-notes "No backup coverage"
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

# Default log path
if sys.platform == 'win32':
    DEFAULT_LOG_DIR = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'guardian-audit')
else:
    DEFAULT_LOG_DIR = os.path.join(os.path.expanduser('~'), '.local', 'share', 'guardian-audit')

DEFAULT_LOG_PATH = os.path.join(DEFAULT_LOG_DIR, 'audit.log')

def ensure_log_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def get_last_entry(path):
    """Read last line and parse JSON. Returns None if file empty."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return None
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if not lines:
            return None
        return json.loads(lines[-1].strip())

def compute_hash(entry):
    """Compute SHA-256 of canonical JSON (sorted keys, compact)."""
    canonical = json.dumps(entry, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()

def build_entry(args, previous_entry=None):
    """Construct new entry with hash chain."""
    sequence = 1
    previous_hash = "genesis"
    
    if previous_entry:
        sequence = previous_entry.get('sequence', 0) + 1
        previous_hash = previous_entry.get('entry_hash', 'genesis')
    
    entry = {
        'timestamp': datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
        'sequence': sequence,
        'previous_hash': previous_hash,
        'event_type': args.event_type,
        'agent_id': args.agent_id or 'agent-anonymous',
        'operation': args.operation,
        'target': args.target or 'N/A',
        'category': args.category or 'N/A',
        'backup_verdict': args.backup_verdict or 'N/A',
        'backup_checks': [],  # Simplified; could accept JSON
        'decision': args.decision,
        'approver': args.approver,
        'agent_reasoning': args.agent_reasoning or '',
        'guardian_notes': args.guardian_notes or '',
        'outcome': args.outcome or 'PENDING',
    }
    
    # Compute hash
    entry['entry_hash'] = compute_hash(entry)
    return entry

def append_entry(path, entry):
    """Append entry to log as single line JSON."""
    ensure_log_dir(path)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

def main():
    parser = argparse.ArgumentParser(description='Guardian Audit Event Logger')
    parser.add_argument('--log-path', default=DEFAULT_LOG_PATH, help='Path to audit log')
    parser.add_argument('--event-type', required=True, choices=[
        'GUARDIAN_CHECK', 'GUARDIAN_HALT', 'GUARDIAN_APPROVE', 'EXECUTED',
        'ESCALATION_RESOLVED', 'MANUAL_APPROVE', 'MANUAL_DENY', 'AGENT_OVERRIDE_ATTEMPT'
    ])
    parser.add_argument('--agent-id', default=None, help='Anonymous agent identifier')
    parser.add_argument('--operation', required=True, help='The operation being logged')
    parser.add_argument('--target', default=None, help='Target file/path/endpoint')
    parser.add_argument('--category', default=None, choices=['CRITICAL', 'HIGH', 'MEDIUM', 'NON-DESTRUCTIVE', 'N/A'])
    parser.add_argument('--backup-verdict', default=None, choices=['VERIFIED', 'UNVERIFIED', 'STALE', 'PARTIAL', 'N/A'])
    parser.add_argument('--decision', required=True, choices=['PROCEED', 'HALT', 'AWAITING_HUMAN', 'DENIED', 'LOGGED'])
    parser.add_argument('--approver', required=True, help='Who made the decision')
    parser.add_argument('--agent-reasoning', default=None, help='Agent stated justification')
    parser.add_argument('--guardian-notes', default=None, help='Guardian decision notes')
    parser.add_argument('--outcome', default=None, choices=['SUCCESS', 'FAILURE', 'TIMEOUT', 'CANCELLED', 'PENDING'])
    
    args = parser.parse_args()
    
    # Read last entry for chain
    last_entry = get_last_entry(args.log_path)
    
    # Build and append
    entry = build_entry(args, last_entry)
    append_entry(args.log_path, entry)
    
    # Output
    print(json.dumps({
        'status': 'logged',
        'sequence': entry['sequence'],
        'entry_hash': entry['entry_hash'],
        'log_path': args.log_path
    }, indent=2))
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
