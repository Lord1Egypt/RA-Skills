#!/usr/bin/env python3
"""Full session JSONL file repair script

Usage:
    python repair-session.py <session_file>
    python repair-session.py <session_file> --dry-run
"""

import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# dedup-session.py has a hyphen in the filename, so load with importlib
_scripts_dir = Path(__file__).parent
_spec = importlib.util.spec_from_file_location("dedup_session", _scripts_dir / "dedup-session.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
dedup_session = _mod.dedup_session


def load_lines(session_file: Path) -> List[Tuple[str, Optional[dict]]]:
    """Load JSONL file as a list of (raw_line, parsed_data) tuples"""
    messages = []
    with open(session_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                messages.append((line, data))
            except json.JSONDecodeError:
                messages.append((line, None))
    return messages


def remove_400_errors(messages: List[Tuple[str, Optional[dict]]]) -> Tuple[List[Tuple[str, Optional[dict]]], int]:
    """Remove 400 error lines and the preceding user message

    Condition: isApiErrorMessage==True or error=="invalid_request"
    Also removes the preceding user message when an error is removed
    """
    removed = 0
    result = []

    for line, data in messages:
        if data is None:
            result.append((line, data))
            continue

        is_error = (
            data.get('isApiErrorMessage') is True
            or data.get('error') == 'invalid_request'
        )

        if is_error:
            # Remove preceding user message
            if result and result[-1][1] is not None and result[-1][1].get('type') == 'user':
                result.pop()
                removed += 1
            removed += 1
        else:
            result.append((line, data))

    return result, removed


def remove_orphan_tool_results(messages: List[Tuple[str, Optional[dict]]]) -> Tuple[List[Tuple[str, Optional[dict]]], int]:
    """Detect and remove orphan tool_results

    Collect all assistant tool_use ids -> delete user messages whose
    tool_result.tool_use_id does not match any remaining tool_use
    """
    # Collect all tool_use ids
    tool_use_ids = set()
    for _, data in messages:
        if data and data.get('type') == 'assistant':
            content = data.get('message', {}).get('content', [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'tool_use':
                        tool_use_ids.add(item.get('id'))

    removed = 0
    result = []

    for line, data in messages:
        if data and data.get('type') == 'user':
            content = data.get('message', {}).get('content', [])
            if isinstance(content, list):
                tool_results = [
                    item for item in content
                    if isinstance(item, dict) and item.get('type') == 'tool_result'
                ]
                if tool_results:
                    all_orphan = all(
                        item.get('tool_use_id') not in tool_use_ids
                        for item in tool_results
                    )
                    if all_orphan:
                        # Remove only orphan tool_results, keep other content
                        non_orphan_content = [
                            item for item in data.get('message', {}).get('content', [])
                            if item.get('type') != 'tool_result'
                            or item.get('tool_use_id') in tool_use_ids
                        ]
                        if non_orphan_content:
                            data['message']['content'] = non_orphan_content
                            result.append((json.dumps(data), data))
                        else:
                            removed += 1
                        continue
        result.append((line, data))

    return result, removed


# Types to exclude from chain repair
_SKIP_CHAIN_TYPES = {'file-history-snapshot', 'queue-operation', 'last-prompt'}


def repair_chains(messages: List[Tuple[str, Optional[dict]]]) -> Tuple[List[Tuple[str, Optional[dict]]], int]:
    """Repair broken chains

    For messages where isSidechain==false and type is not in the exclusion list,
    set parentUuid to the previous message's uuid if parentUuid is missing
    """
    fixed = 0
    result = []
    prev_uuid = None

    for line, data in messages:
        if data is None or not data.get('uuid'):
            result.append((line, data))
            continue

        msg_type = data.get('type', '')
        is_sidechain = data.get('isSidechain', False)

        if not is_sidechain and msg_type not in _SKIP_CHAIN_TYPES:
            if 'parentUuid' not in data and prev_uuid is not None:
                data = dict(data)
                data['parentUuid'] = prev_uuid
                line = json.dumps(data, ensure_ascii=False)
                fixed += 1

        prev_uuid = data.get('uuid')
        result.append((line, data))

    return result, fixed


def validate(messages: List[Tuple[str, Optional[dict]]]) -> dict:
    """Validate: duplicate message.id==0, orphan tool_results, broken chains, JSON validity"""
    # Check for duplicate message.id (id==0)
    msg_id_zero_count = 0
    tool_use_ids = set()
    orphan_tool_results = 0
    broken_chains = 0
    invalid_json = 0
    prev_uuid = None

    for line, data in messages:
        if data is None:
            invalid_json += 1
            continue

        # Check message.id == 0 duplicates
        msg = data.get('message', {})
        if isinstance(msg, dict) and msg.get('id') == 0:
            msg_id_zero_count += 1

        # Collect tool_use ids
        if data.get('type') == 'assistant':
            content = data.get('message', {}).get('content', [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'tool_use':
                        tool_use_ids.add(item.get('id'))

        # Check for orphan tool_results
        if data.get('type') == 'user':
            content = data.get('message', {}).get('content', [])
            if isinstance(content, list):
                tool_results = [
                    item for item in content
                    if isinstance(item, dict) and item.get('type') == 'tool_result'
                ]
                if tool_results:
                    orphans = [
                        item for item in tool_results
                        if item.get('tool_use_id') not in tool_use_ids
                    ]
                    orphan_tool_results += len(orphans)

        # Check for broken chains
        if data.get('uuid') and not data.get('isSidechain'):
            msg_type = data.get('type', '')
            if msg_type not in _SKIP_CHAIN_TYPES:
                if prev_uuid is not None and 'parentUuid' not in data:
                    broken_chains += 1

        prev_uuid = data.get('uuid')

    return {
        'duplicate_message_id_zero': msg_id_zero_count,
        'orphan_tool_results': orphan_tool_results,
        'broken_chains': broken_chains,
        'invalid_json': invalid_json,
    }


def repair_session(session_file: Path, dry_run: bool = False) -> dict:
    """Run full session file repair"""
    session_file = Path(session_file)

    if not session_file.exists():
        print(f"Error: {session_file} not found")
        sys.exit(1)

    original_lines = load_lines(session_file)
    original_count = len(original_lines)

    # Step 1: backup
    if not dry_run:
        bak_file = Path(str(session_file) + '.bak')
        shutil.copy2(session_file, bak_file)
        print(f"[1/6] Backup: {bak_file}")
    else:
        print(f"[1/6] Backup: (dry-run, skipped)")

    # Step 2: dedup
    dedup_result = dedup_session(session_file, dry_run=dry_run)
    dedup_removed = dedup_result['original_lines'] - dedup_result['unique_lines']
    dedup_fixed_chains = dedup_result.get('fixed_chains', 0)

    if not dry_run and 'output_file' in dedup_result:
        dedup_file = Path(dedup_result['output_file'])
        os.replace(dedup_file, session_file)
        print(f"[2/6] dedup: {dedup_removed} duplicates removed, {dedup_fixed_chains} chains repaired -> applied")
    else:
        print(f"[2/6] dedup: {dedup_removed} duplicates removed, {dedup_fixed_chains} chains repaired (dry-run)")

    # Reload file after dedup
    if not dry_run:
        messages = load_lines(session_file)
    else:
        # dry-run: analyze original as-is
        messages = original_lines

    # Step 3: remove 400 errors
    messages, error_removed = remove_400_errors(messages)
    print(f"[3/6] 400 error removal: {error_removed} (error lines + preceding user messages)")

    # Step 4: remove orphan tool_results
    messages, orphan_removed = remove_orphan_tool_results(messages)
    print(f"[4/6] Orphan tool_result removal: {orphan_removed}")

    # Step 5: repair broken chains
    messages, chain_fixed = repair_chains(messages)
    print(f"[5/6] Broken chain repair: {chain_fixed}")

    # Step 6: validate
    validation = validate(messages)
    print(f"[6/6] Validation:")
    print(f"  duplicate message.id=0: {validation['duplicate_message_id_zero']}")
    print(f"  orphan tool_results: {validation['orphan_tool_results']}")
    print(f"  broken chains: {validation['broken_chains']}")
    print(f"  JSON parse errors: {validation['invalid_json']}")

    final_count = len(messages)

    # Save results
    if not dry_run and (error_removed > 0 or orphan_removed > 0 or chain_fixed > 0):
        with open(session_file, 'w') as f:
            for line, _ in messages:
                f.write(line + '\n')

    return {
        'original_lines': original_count,
        'final_lines': final_count,
        'dedup_removed': dedup_removed,
        'dedup_fixed_chains': dedup_fixed_chains,
        'error_removed': error_removed,
        'orphan_removed': orphan_removed,
        'chain_fixed': chain_fixed,
        'validation': validation,
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    session_file = Path(sys.argv[1])
    dry_run = '--dry-run' in sys.argv

    if not session_file.exists():
        print(f"Error: {session_file} not found")
        sys.exit(1)

    mode = "(dry-run)" if dry_run else ""
    print(f"=== repair-session {mode}: {session_file} ===\n")

    result = repair_session(session_file, dry_run=dry_run)

    print(f"\n=== Results ===")
    print(f"Original lines: {result['original_lines']}")
    print(f"Final lines: {result['final_lines']}")
    print(f"Total removed/repaired:")
    print(f"  dedup removed: {result['dedup_removed']}")
    print(f"  dedup chain repairs: {result['dedup_fixed_chains']}")
    print(f"  400 errors removed: {result['error_removed']}")
    print(f"  orphan tool_results removed: {result['orphan_removed']}")
    print(f"  chains repaired: {result['chain_fixed']}")

    v = result['validation']
    ok = all(v[k] == 0 for k in v)
    status = "PASS" if ok else "FAIL"
    print(f"\nValidation: {status}")


if __name__ == '__main__':
    main()
