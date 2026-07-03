#!/usr/bin/env python3
"""
Session Catchup Script for planning-with-files

Analyzes the previous session to find unsynced context after the last planning file
update. Designed to run on SessionStart.

Usage: python3 session-catchup.py [project-path] [plan-dir]
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple

PLANNING_FILES = ['task_plan.md', 'progress.md', 'findings.md']


def get_project_dir(project_path: str) -> Path:
    """Convert project path to storage path format."""
    sanitized = project_path.replace('/', '-')
    if not sanitized.startswith('-'):
        sanitized = '-' + sanitized
    sanitized = sanitized.replace('_', '-')
    return Path.home() / '.claude' / 'projects' / sanitized


def get_sessions_sorted(project_dir: Path) -> List[Path]:
    """Get all session files sorted by modification time (newest first)."""
    sessions = list(project_dir.glob('*.jsonl'))
    main_sessions = [s for s in sessions if not s.name.startswith('agent-')]
    return sorted(main_sessions, key=lambda p: p.stat().st_mtime, reverse=True)


def parse_session_messages(session_file: Path) -> List[Dict]:
    """Parse all messages from a session file, preserving order."""
    messages = []
    with open(session_file, 'r') as f:
        for line_num, line in enumerate(f):
            try:
                data = json.loads(line)
                data['_line_num'] = line_num
                messages.append(data)
            except json.JSONDecodeError:
                pass
    return messages


def find_last_planning_update(messages: List[Dict]) -> Tuple[int, Optional[str]]:
    """Find the last time a planning file was written/edited."""
    last_update_line = -1
    last_update_file = None

    for msg in messages:
        msg_type = msg.get('type')

        if msg_type == 'assistant':
            content = msg.get('message', {}).get('content', [])
            if isinstance(content, list):
                for item in content:
                    if item.get('type') == 'tool_use':
                        tool_name = item.get('name', '')
                        tool_input = item.get('input', {})

                        if tool_name in ('Write', 'Edit'):
                            file_path = tool_input.get('file_path', '')
                            for pf in PLANNING_FILES:
                                if file_path.endswith(pf):
                                    last_update_line = msg['_line_num']
                                    last_update_file = pf

    return last_update_line, last_update_file


def extract_messages_after(messages: List[Dict], after_line: int) -> List[Dict]:
    """Extract conversation messages after a certain line number."""
    result = []
    for msg in messages:
        if msg['_line_num'] <= after_line:
            continue
        msg_type = msg.get('type')
        if msg_type in ('human', 'assistant'):
            result.append(msg)
    return result


def summarize_unsynced(messages: List[Dict]) -> str:
    """Create a summary of unsynced messages."""
    if not messages:
        return ""

    lines = ["## Unsynced Context from Previous Session\n"]
    for msg in messages[-10:]:  # Last 10 messages
        msg_type = msg.get('type', 'unknown')
        if msg_type == 'human':
            content = msg.get('message', {}).get('content', '')
            if isinstance(content, str) and content.strip():
                lines.append(f"**User:** {content[:200]}")
        elif msg_type == 'assistant':
            content = msg.get('message', {}).get('content', [])
            if isinstance(content, list):
                for item in content:
                    if item.get('type') == 'text':
                        text = item.get('text', '')[:200]
                        if text:
                            lines.append(f"**Assistant:** {text}")

    return "\n".join(lines) if len(lines) > 1 else ""


def main():
    project_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    plan_dir = sys.argv[2] if len(sys.argv) > 2 else None

    project_dir = get_project_dir(project_path)
    if not project_dir.exists():
        return

    sessions = get_sessions_sorted(project_dir)
    if not sessions:
        return

    messages = parse_session_messages(sessions[0])
    if not messages:
        return

    last_line, last_file = find_last_planning_update(messages)
    if last_line < 0:
        return

    unsynced = extract_messages_after(messages, last_line)
    summary = summarize_unsynced(unsynced)
    if summary:
        print(summary)


if __name__ == '__main__':
    main()
