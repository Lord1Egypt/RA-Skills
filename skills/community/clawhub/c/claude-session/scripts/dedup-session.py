#!/usr/bin/env python3
"""Remove duplicate messages from a session JSONL file

Usage:
    python dedup-session.py <session_file>
    python dedup-session.py <session_file> --dry-run
"""

import json
import hashlib
import sys
from pathlib import Path


def get_content_richness(data: dict) -> int:
    """Calculate content richness score for a message (higher is better)"""
    if not data:
        return 0

    msg_type = data.get('type', '')
    if msg_type not in ('assistant', 'user'):
        return len(json.dumps(data))

    content = data.get('message', {}).get('content', [])
    if not isinstance(content, list):
        return 0

    score = 0
    for item in content:
        if not isinstance(item, dict):
            continue
        item_type = item.get('type', '')
        # High score for tool_use/tool_result
        if item_type in ('tool_use', 'tool_result'):
            score += 1000
        # Score text content by length
        elif item_type == 'text':
            score += len(item.get('text', ''))
        # Low score for thinking (not valuable without other content)
        elif item_type == 'thinking':
            score += 1

    return score


def get_dedup_key(data: dict) -> str:
    """Generate key for duplicate detection

    Messages with the same message.id are treated as the same message regardless of streaming stage:
    - Intermediate streaming results (text only) and final results (with tool_use) share the same key
    - get_content_richness() selects the richest version
    """
    msg_type = data.get('type', '')

    # assistant/user messages: keyed by message.id only
    if msg_type in ('assistant', 'user'):
        msg = data.get('message', {})
        if isinstance(msg, dict) and msg.get('id'):
            return f"msg:{msg['id']}"

    # progress: keyed by tool_use_id + content hash
    if msg_type == 'progress':
        tool_use_id = data.get('tool_use_id', '')
        content = json.dumps(data.get('content', {}), sort_keys=True)
        content_hash = hashlib.md5(content.encode()).hexdigest()[:16]
        return f"progress:{tool_use_id}:{content_hash}"

    # others: keyed by uuid
    uuid = data.get('uuid')
    if uuid:
        return f"uuid:{uuid}"

    return f"line:{json.dumps(data, sort_keys=True)}"


def dedup_session(session_file: Path, dry_run: bool = False) -> dict:
    """Remove duplicates from session file and repair chain

    Strategy: dedup -> chain repair (aggressive)
    1. Load all messages
    2. Keep only first occurrence in each duplicate group (regardless of references)
    3. Repair parentUuid chain broken by removals, linking to previous message uuid

    Returns:
        dict: {
            'original_lines': int,
            'unique_lines': int,
            'duplicates_by_type': dict,
            'fixed_chains': int,
            'output_file': str (only when dry_run=False)
        }
    """
    # Pass 1: load all messages
    messages = []

    with open(session_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                messages.append((line, data))
            except json.JSONDecodeError:
                messages.append((line, None))

    # Pass 2: group by duplicate key (dedup_key -> [(line, data), ...])
    dedup_groups = {}
    for line, data in messages:
        if data is None:
            key = f"raw:{line}"
        else:
            key = get_dedup_key(data)

        if key not in dedup_groups:
            dedup_groups[key] = []
        dedup_groups[key].append((line, data))

    # Pass 3: select richest message from each group (prefer tool_use, then content length)
    best_messages = {}  # key -> (line, data)
    for key, group in dedup_groups.items():
        # Sort by richness score, pick the highest
        best = max(group, key=lambda x: get_content_richness(x[1]))
        best_messages[key] = best

    # Preserve original order while building unique_lines (use best message)
    unique_lines = []
    unique_data = []
    duplicates_by_type = {}
    seen_keys = set()

    for line, data in messages:
        if data is None:
            key = f"raw:{line}"
        else:
            key = get_dedup_key(data)

        if key not in seen_keys:
            # Use best message at the first occurrence position
            best_line, best_data = best_messages[key]
            unique_lines.append(best_line)
            unique_data.append(best_data)
            seen_keys.add(key)
        else:
            # Count removed duplicates
            msg_type = data.get('type', 'unknown') if data else 'unknown'
            duplicates_by_type[msg_type] = duplicates_by_type.get(msg_type, 0) + 1

    # Pass 4: collect all tool_use ids from remaining messages
    remaining_tool_use_ids = set()
    for data in unique_data:
        if data and data.get('type') == 'assistant':
            content = data.get('message', {}).get('content', [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'tool_use':
                        remaining_tool_use_ids.add(item.get('id'))

    # Pass 5: remove orphan tool_results (tool_use_id not in remaining tool_use ids)
    orphan_removed = 0
    filtered_lines = []
    filtered_data = []
    for line, data in zip(unique_lines, unique_data):
        if data and data.get('type') == 'user':
            content = data.get('message', {}).get('content', [])
            if isinstance(content, list):
                # Check if this is a user message with tool_results
                tool_results = [item for item in content if isinstance(item, dict) and item.get('type') == 'tool_result']
                if tool_results:
                    # Check if all tool_results are orphans
                    all_orphan = all(
                        item.get('tool_use_id') not in remaining_tool_use_ids
                        for item in tool_results
                    )
                    if all_orphan:
                        # Remove only orphan tool_results, keep other content (text, etc.)
                        non_orphan_content = [
                            item for item in data.get('message', {}).get('content', [])
                            if item.get('type') != 'tool_result'
                            or item.get('tool_use_id') in remaining_tool_use_ids
                        ]
                        if non_orphan_content:
                            data['message']['content'] = non_orphan_content
                            filtered_lines.append(json.dumps(data))
                            filtered_data.append(data)
                        else:
                            orphan_removed += 1
                        duplicates_by_type['user (orphan tool_result)'] = duplicates_by_type.get('user (orphan tool_result)', 0) + 1
                        continue
        filtered_lines.append(line)
        filtered_data.append(data)

    unique_lines = filtered_lines
    unique_data = filtered_data

    # Pass 6: rebuild chain (sequential linking)
    # Force all messages to point to the previous message as parent
    fixed_chains = 0
    final_lines = []

    prev_uuid = None
    for i, (line, data) in enumerate(zip(unique_lines, unique_data)):
        if data is None:
            final_lines.append(line)
            continue

        # Messages without uuid (e.g. file-history-snapshot) are kept as-is
        if not data.get('uuid'):
            final_lines.append(line)
            continue

        current_parent = data.get('parentUuid')
        expected_parent = prev_uuid  # uuid of the previous message

        # First message must have parentUuid == null
        if i == 0 or prev_uuid is None:
            if current_parent is not None:
                data['parentUuid'] = None
                final_lines.append(json.dumps(data, ensure_ascii=False))
                fixed_chains += 1
            else:
                final_lines.append(line)
        # Subsequent messages must point to the previous message
        elif current_parent != expected_parent:
            data['parentUuid'] = expected_parent
            final_lines.append(json.dumps(data, ensure_ascii=False))
            fixed_chains += 1
        else:
            final_lines.append(line)

        prev_uuid = data.get('uuid')

    result = {
        'original_lines': len(messages),
        'unique_lines': len(final_lines),
        'duplicates_by_type': duplicates_by_type,
        'fixed_chains': fixed_chains,
    }

    if not dry_run:
        # Generate .dedup output filename correctly even for .jsonl.bak etc.
        output_file = Path(str(session_file) + '.dedup')
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in final_lines:
                f.write(line + '\n')
        result['output_file'] = str(output_file)

    return result


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    session_file = Path(sys.argv[1])
    dry_run = '--dry-run' in sys.argv

    if not session_file.exists():
        print(f"Error: {session_file} not found")
        sys.exit(1)

    result = dedup_session(session_file, dry_run)

    print(f"Original lines: {result['original_lines']}")
    print(f"Resulting lines: {result['unique_lines']}")
    print(f"Duplicates removed: {result['original_lines'] - result['unique_lines']}")

    if result.get('fixed_chains', 0) > 0:
        print(f"Chains repaired: {result['fixed_chains']}")

    if result['duplicates_by_type']:
        print("\nRemoved by type:")
        for t, c in sorted(result['duplicates_by_type'].items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")

    if not dry_run and 'output_file' in result:
        print(f"\nSaved: {result['output_file']}")


if __name__ == '__main__':
    main()
