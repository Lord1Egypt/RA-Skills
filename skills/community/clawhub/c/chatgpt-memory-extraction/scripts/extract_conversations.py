#!/usr/bin/env python3
"""
Extract conversations from ChatGPT export JSON files into readable text files.

Usage:
    python extract_conversations.py <input_dir> <output_dir> [--year YYYY] [--quarter Q1|Q2|Q3|Q4]

Arguments:
    input_dir   Directory containing conversations-*.json files
    output_dir  Directory to write extracted text files

Options:
    --year      Filter by year (e.g., 2024)
    --quarter   Filter by quarter (Q1=Jan-Mar, Q2=Apr-Jun, Q3=Jul-Sep, Q4=Oct-Dec)
    --timezone  Timezone for date conversion (default: UTC). E.g., Asia/Tokyo

Output:
    Creates one .txt file per conversation in output_dir/{year}_Q{n}/
    Each file contains all messages in conversation-tree order with role labels.
    Also generates a conversation index file: output_dir/conversation-index.md
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone, timedelta


def get_timezone(tz_name):
    """Simple timezone support without pytz dependency."""
    tz_offsets = {
        'UTC': timedelta(hours=0),
        'Asia/Tokyo': timedelta(hours=9),
        'Asia/Shanghai': timedelta(hours=8),
        'America/New_York': timedelta(hours=-5),
        'America/Los_Angeles': timedelta(hours=-8),
        'Europe/London': timedelta(hours=0),
        'Europe/Berlin': timedelta(hours=1),
        'Europe/Paris': timedelta(hours=1),
    }
    offset = tz_offsets.get(tz_name, timedelta(hours=0))
    return timezone(offset)


def get_ordered_messages(conv):
    """Extract messages from conversation in tree order (BFS)."""
    mapping = conv.get('mapping', {})
    root_id = None
    for nid, node in mapping.items():
        if node.get('parent') is None:
            root_id = nid
            break
    if not root_id:
        return []

    messages = []
    queue = [root_id]
    visited = set()
    while queue:
        nid = queue.pop(0)
        if nid in visited:
            continue
        visited.add(nid)
        node = mapping.get(nid, {})
        msg = node.get('message')
        if msg and msg.get('content', {}).get('parts'):
            role = msg.get('author', {}).get('role', '')
            parts = msg['content']['parts']
            text_parts = [p for p in parts if isinstance(p, str)]
            text = '\n'.join(text_parts).strip()
            if text:
                messages.append({'role': role, 'text': text})
        children = node.get('children', [])
        queue.extend(children)
    return messages


def quarter_for_month(month):
    """Return quarter number (1-4) for a given month (1-12)."""
    return (month - 1) // 3 + 1


def sanitize_filename(name, max_len=60):
    """Sanitize a string to be safe for filenames."""
    cleaned = ''.join(c if c.isalnum() or c in '._- ' else '_' for c in name)
    return cleaned[:max_len]


def main():
    parser = argparse.ArgumentParser(description='Extract ChatGPT conversations to readable text files')
    parser.add_argument('input_dir', help='Directory containing conversations-*.json')
    parser.add_argument('output_dir', help='Directory to write extracted files')
    parser.add_argument('--year', type=int, help='Filter by year')
    parser.add_argument('--quarter', choices=['Q1', 'Q2', 'Q3', 'Q4'], help='Filter by quarter')
    parser.add_argument('--timezone', default='UTC', help='Timezone (default: UTC)')
    parser.add_argument('--max-chars-per-message', type=int, default=10000,
                        help='Max characters per message (default: 10000)')
    args = parser.parse_args()

    tz = get_timezone(args.timezone)
    quarter_filter = int(args.quarter[1]) if args.quarter else None

    # Load all conversations
    all_convos = []
    for fname in sorted(os.listdir(args.input_dir)):
        if not fname.startswith('conversations-') or not fname.endswith('.json'):
            continue
        fpath = os.path.join(args.input_dir, fname)
        print(f"Loading {fname}...", file=sys.stderr)
        with open(fpath, 'r') as f:
            data = json.load(f)
        for conv in data:
            ct = conv.get('create_time', 0)
            if not ct:
                continue
            dt = datetime.fromtimestamp(ct, tz=tz)
            if args.year and dt.year != args.year:
                continue
            if quarter_filter and quarter_for_month(dt.month) != quarter_filter:
                continue
            all_convos.append((dt, conv))

    all_convos.sort(key=lambda x: x[0])
    print(f"Found {len(all_convos)} conversations matching filters", file=sys.stderr)

    # Group by year and quarter
    groups = {}
    for dt, conv in all_convos:
        key = (dt.year, quarter_for_month(dt.month))
        groups.setdefault(key, []).append((dt, conv))

    # Extract each group
    index_entries = []
    for (year, q), convos in sorted(groups.items()):
        outdir = os.path.join(args.output_dir, f"{year}_Q{q}")
        os.makedirs(outdir, exist_ok=True)

        for idx, (dt, conv) in enumerate(convos):
            title = conv.get('title', 'untitled').replace('/', '_').replace('\n', ' ')
            msgs = get_ordered_messages(conv)
            user_msgs = [m for m in msgs if m['role'] == 'user']
            total_user_chars = sum(len(m['text']) for m in user_msgs)

            fname = f"{idx:03d}_{dt.strftime('%m%d')}_{sanitize_filename(title)}.txt"
            fpath = os.path.join(outdir, fname)

            with open(fpath, 'w') as f:
                f.write(f"# {title}\n")
                f.write(f"# Date: {dt.strftime('%Y-%m-%d %H:%M')} ({args.timezone})\n")
                f.write(f"# Messages: {len(msgs)} total, {len(user_msgs)} user\n")
                f.write(f"# User chars: {total_user_chars}\n")
                f.write(f"# Conversation ID: {conv.get('id', 'unknown')}\n\n")

                for m in msgs:
                    role_label = {
                        'user': '👤 USER',
                        'assistant': '🤖 ASSISTANT',
                        'system': '[SYSTEM]',
                        'tool': '[TOOL]'
                    }.get(m['role'], f"[{m['role']}]")
                    f.write(f"--- {role_label} ---\n")
                    text = m['text']
                    if len(text) > args.max_chars_per_message:
                        f.write(text[:args.max_chars_per_message])
                        f.write(f"\n... [truncated, original {len(text)} chars]")
                    else:
                        f.write(text)
                    f.write('\n\n')

            index_entries.append({
                'date': dt.strftime('%Y-%m-%d'),
                'year': year,
                'quarter': q,
                'month': dt.month,
                'title': title,
                'total_msgs': len(msgs),
                'user_msgs': len(user_msgs),
                'user_chars': total_user_chars,
                'filename': f"{year}_Q{q}/{fname}",
                'conv_id': conv.get('id', 'unknown'),
            })

    # Write conversation index
    os.makedirs(args.output_dir, exist_ok=True)
    index_path = os.path.join(args.output_dir, 'conversation-index.md')
    with open(index_path, 'w') as f:
        f.write("# Conversation Index\n\n")
        f.write(f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"> Total conversations: {len(index_entries)}\n")
        f.write(f"> Timezone: {args.timezone}\n\n")

        current_yq = None
        for entry in index_entries:
            yq = (entry['year'], entry['quarter'])
            if yq != current_yq:
                current_yq = yq
                month_range = {1: 'Jan-Mar', 2: 'Apr-Jun', 3: 'Jul-Sep', 4: 'Oct-Dec'}
                f.write(f"\n## {entry['year']} Q{entry['quarter']} ({month_range[entry['quarter']]})\n\n")
                f.write(f"| Date | User Msgs | Chars | Title |\n")
                f.write(f"|------|-----------|-------|-------|\n")
            f.write(f"| {entry['date']} | {entry['user_msgs']} | {entry['user_chars']} | {entry['title']} |\n")

    print(f"\nExtraction complete:", file=sys.stderr)
    print(f"  Conversations: {len(index_entries)}", file=sys.stderr)
    print(f"  Index: {index_path}", file=sys.stderr)


if __name__ == '__main__':
    main()
