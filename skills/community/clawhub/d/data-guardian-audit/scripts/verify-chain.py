#!/usr/bin/env python3
"""
Guardian Audit — Chain Integrity Verifier

Verifies that the audit log's hash chain is intact.
Usage:
    python3 verify-chain.py /path/to/audit.log
"""

import argparse
import hashlib
import json
import sys

def compute_hash(entry):
    """Recompute SHA-256 of entry content (excluding entry_hash field)."""
    # Clone entry without entry_hash
    content = {k: v for k, v in entry.items() if k != 'entry_hash'}
    canonical = json.dumps(content, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()

def verify_chain(path):
    """Verify hash chain integrity."""
    issues = []
    entry_count = 0
    previous_hash = "genesis"
    
    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                issues.append(f"Line {line_num}: Invalid JSON: {e}")
                continue
            
            entry_count += 1
            seq = entry.get('sequence', '?')
            
            # Check previous_hash linkage
            if entry.get('previous_hash') != previous_hash:
                issues.append(
                    f"Line {line_num} (seq {seq}): Hash chain broken. "
                    f"Expected previous_hash={previous_hash[:16]}..., got {entry.get('previous_hash', 'MISSING')[:16]}..."
                )
            
            # Check entry_hash integrity
            expected_hash = compute_hash(entry)
            if entry.get('entry_hash') != expected_hash:
                issues.append(
                    f"Line {line_num} (seq {seq}): Entry hash mismatch. "
                    f"Expected {expected_hash[:16]}..., got {entry.get('entry_hash', 'MISSING')[:16]}..."
                )
            
            # Check sequence continuity
            if entry_count > 1:
                if entry.get('sequence') != entry_count:
                    issues.append(
                        f"Line {line_num}: Sequence gap. Expected {entry_count}, got {entry.get('sequence', 'MISSING')}"
                    )
            
            previous_hash = entry.get('entry_hash', 'missing')
    
    return entry_count, issues, previous_hash

def main():
    parser = argparse.ArgumentParser(description='Verify Guardian Audit chain integrity')
    parser.add_argument('log_path', help='Path to audit.log')
    args = parser.parse_args()
    
    try:
        count, issues, last_hash = verify_chain(args.log_path)
    except FileNotFoundError:
        print(f"ERROR: Log file not found: {args.log_path}")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 1
    
    if issues:
        print(f"CHAIN BROKEN: {len(issues)} issue(s) found in {count} entries")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    else:
        print(f"Chain valid: {count} entries, 0 breaks")
        print(f"Last hash: {last_hash[:16]}... (verified)")
        print(f"Integrity: PASS")
        return 0

if __name__ == '__main__':
    sys.exit(main())
