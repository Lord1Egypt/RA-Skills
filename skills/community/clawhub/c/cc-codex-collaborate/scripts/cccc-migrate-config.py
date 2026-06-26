#!/usr/bin/env python3
"""
Migrate config.json to new version.
- Preserves user settings
- Adds new template fields
- Updates skill metadata
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
        # else: keep base value
    return result


def main():
    parser = argparse.ArgumentParser(description="Migrate config.json")
    parser.add_argument('--config', default='docs/cccc/config.json')
    parser.add_argument('--template', required=True)
    parser.add_argument('--version', required=True)
    parser.add_argument('--backup-dir', default='docs/cccc/backups')
    args = parser.parse_args()

    config_path = Path(args.config)
    template_path = Path(args.template)
    backup_dir = Path(args.backup_dir)

    if not config_path.exists():
        print(f"ERROR: config.json not found: {config_path}", file=__import__('sys').stderr)
        print("Run /cc-codex-collaborate setup first.", file=__import__('sys').stderr)
        __import__('sys').exit(1)

    if not template_path.exists():
        print(f"ERROR: template not found: {template_path}", file=__import__('sys').stderr)
        __import__('sys').exit(1)

    # Load existing config
    try:
        existing = json.loads(config_path.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in config.json: {e}", file=__import__('sys').stderr)
        __import__('sys').exit(1)

    # Load template
    try:
        template = json.loads(template_path.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in template: {e}", file=__import__('sys').stderr)
        __import__('sys').exit(1)

    # Check for deprecated fields
    deprecated_fields = []
    deprecated_file = backup_dir / 'deprecated-config-fields.txt'

    # Known deprecated fields that might exist in old configs
    known_deprecated = ['thresholds']  # thresholds moved to review section

    for field in known_deprecated:
        if field in existing:
            deprecated_fields.append(field)

    if deprecated_fields:
        deprecated_file.write_text('\n'.join(deprecated_fields) + '\n')
        print(f"Deprecated fields found: {deprecated_fields}")
        print(f"  Saved to: {deprecated_file}")

    # Deep merge: preserve user settings, add new template fields
    merged = deep_merge(existing, template)

    # Update skill metadata
    merged.setdefault('skill', {})
    merged['skill']['name'] = 'cc-codex-collaborate'
    merged['skill']['installed_version'] = args.version
    merged['skill']['workspace_schema_version'] = template.get('skill', {}).get('workspace_schema_version', 1)
    merged['skill']['last_updated_at'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Update top-level version for compatibility
    merged['version'] = args.version

    # Write merged config
    config_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + '\n')
    print(f"Updated: {config_path}")

    # Summary
    print(f"Installed version: {args.version}")
    print(f"Schema version: {merged['skill']['workspace_schema_version']}")


if __name__ == '__main__':
    main()