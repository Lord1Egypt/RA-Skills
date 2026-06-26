#!/usr/bin/env python3
"""
Migrate state.json to new version.
- Preserves runtime state
- Adds new template fields
- Updates migration metadata
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def deep_merge(base: dict, template: dict) -> dict:
    """Deep merge template into base, preserving base values."""
    result = dict(base)
    for key, value in template.items():
        if key not in result:
            result[key] = value
        elif isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        # else: keep base value (runtime state)
    return result


# Fields that must be preserved (runtime state)
PRESERVE_FIELDS = {
    'status', 'pause_reason', 'current_milestone_id',
    'completed_milestones', 'blocked_milestones', 'known_risks',
    'stop_hook_continuations', 'review_round_current', 'fix_attempts_current',
    'codex_plan_review_status', 'codex_final_review_status',
    'last_codex_plan_review_file', 'last_codex_milestone_review_file',
    'last_codex_final_review_file', 'codex_unavailable_reason',
    'current_milestone_codex_review_status', 'current_milestone_codex_review_file',
    'task', 'enabled', 'created_at', 'updated_at'
}


def main():
    parser = argparse.ArgumentParser(description="Migrate state.json")
    parser.add_argument('--state', default='docs/cccc/state.json')
    parser.add_argument('--template', required=True)
    parser.add_argument('--from-version', default='unknown')
    parser.add_argument('--to-version', required=True)
    parser.add_argument('--backup-dir', default='docs/cccc/backups')
    args = parser.parse_args()

    state_path = Path(args.state)
    template_path = Path(args.template)
    backup_dir = Path(args.backup_dir)

    if not state_path.exists():
        print(f"ERROR: state.json not found: {state_path}", file=__import__('sys').stderr)
        print("Run /cc-codex-collaborate setup first.", file=__import__('sys').stderr)
        __import__('sys').exit(1)

    if not template_path.exists():
        print(f"ERROR: template not found: {template_path}", file=__import__('sys').stderr)
        __import__('sys').exit(1)

    # Load existing state
    try:
        existing = json.loads(state_path.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in state.json: {e}", file=__import__('sys').stderr)
        __import__('sys').exit(1)

    # Load template
    try:
        template = json.loads(template_path.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in template: {e}", file=__import__('sys').stderr)
        __import__('sys').exit(1)

    # Deep merge: preserve runtime state, add new template fields
    merged = deep_merge(existing, template)

    # Explicitly preserve runtime fields
    for field in PRESERVE_FIELDS:
        if field in existing:
            merged[field] = existing[field]

    # Update migration metadata
    merged['workspace_schema_version'] = template.get('workspace_schema_version', 1)
    merged['last_migration_at'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    merged['last_migration_from_version'] = args.from_version
    merged['last_migration_to_version'] = args.to_version
    merged['skill_version'] = args.to_version

    # Write merged state
    state_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + '\n')
    print(f"Updated: {state_path}")

    # Summary
    print(f"Migration: {args.from_version} -> {args.to_version}")
    print(f"Schema version: {merged['workspace_schema_version']}")


if __name__ == '__main__':
    main()