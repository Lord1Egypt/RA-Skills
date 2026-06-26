#!/usr/bin/env python3
"""Format sync operation results for Notion/Sheets bidirectional sync.

Usage: Claude calls MCP sync tools, saves JSON responses to temp files, then runs:
  python sync-flow.py --storage notion \
    --manifest manifest.json \
    --sync-result result.json

Can also be used pre-sync to analyze the manifest and show what will be synced:
  python sync-flow.py --storage notion --manifest manifest.json --dry-run

Outputs formatted sync report markdown to stdout.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


MAX_JSON_SIZE = 10 * 1024 * 1024  # 10MB


def load_json(path):
    if not path or not Path(path).exists():
        return None
    file_path = Path(path)
    if file_path.stat().st_size > MAX_JSON_SIZE:
        print(f"Error: {path} exceeds 10MB size limit", file=sys.stderr)
        return None
    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error loading {path}: {e}", file=sys.stderr)
        return None


def analyze_manifest(manifest, storage_type):
    """Analyze sync manifest and return summary of changes."""
    if not manifest:
        return {"total": 0, "by_type": {}, "conflicts": []}

    changes = manifest if isinstance(manifest, list) else manifest.get("changes", [])
    by_type = {}
    conflicts = []

    for item in changes:
        entity_type = item.get("entity_type", "unknown")
        direction = item.get("direction", "unknown")
        by_type.setdefault(entity_type, {"push": 0, "pull": 0, "conflict": 0})

        if item.get("conflict"):
            by_type[entity_type]["conflict"] += 1
            conflicts.append(item)
        elif direction == "push":
            by_type[entity_type]["push"] += 1
        elif direction == "pull":
            by_type[entity_type]["pull"] += 1

    return {
        "total": len(changes),
        "by_type": by_type,
        "conflicts": conflicts,
    }


def format_dry_run(manifest_analysis, storage_type):
    """Format a pre-sync analysis showing what will be synced."""
    now = datetime.now()
    lines = [
        f"# Sync Preview — {storage_type.title()}",
        f"*Generated at {now.strftime('%Y-%m-%d %H:%M')}*\n",
    ]

    if manifest_analysis["total"] == 0:
        lines.append("**No changes detected.** Everything is in sync.")
        return "\n".join(lines)

    lines.append(f"**{manifest_analysis['total']} changes detected**\n")

    # Changes by entity type
    lines.append("## Changes by Type\n")
    lines.append("| Type | Push (→ {}) | Pull (← {}) | Conflicts |".format(
        storage_type.title(), storage_type.title()))
    lines.append("|------|-------------|-------------|-----------|")
    for entity_type, counts in manifest_analysis["by_type"].items():
        lines.append(
            f"| {entity_type} | {counts['push']} | {counts['pull']} | {counts['conflict']} |"
        )
    lines.append("")

    # Conflicts detail
    if manifest_analysis["conflicts"]:
        lines.append("## Conflicts Requiring Resolution\n")
        for c in manifest_analysis["conflicts"]:
            name = c.get("title", c.get("name", c.get("external_id", "Unknown")))
            entity_type = c.get("entity_type", "unknown")
            local_time = c.get("local_updated_at", "?")
            remote_time = c.get("remote_updated_at", "?")
            lines.append(f"- **{name}** ({entity_type})")
            lines.append(f"  - Local updated: {local_time}")
            lines.append(f"  - {storage_type.title()} updated: {remote_time}")
            lines.append(f"  - Action needed: Boss decides which version to keep")
        lines.append("")

    lines.extend([
        "## Next Steps\n",
        "1. Review changes above",
        "2. Resolve any conflicts (boss picks the winning version)",
        "3. Execute sync to apply changes",
        "",
        "---",
        f"*Read `references/scenarios.md` Scenario 12 for the full sync flow.*",
    ])
    return "\n".join(lines)


def format_sync_result(result, storage_type):
    """Format post-sync result report."""
    now = datetime.now()
    lines = [
        f"# Sync Report — {storage_type.title()}",
        f"*Completed at {now.strftime('%Y-%m-%d %H:%M')}*\n",
    ]

    if not result:
        lines.append("No sync result data available.")
        return "\n".join(lines)

    pushed = result.get("items_pushed", 0)
    pulled = result.get("items_pulled", 0)
    conflicts = result.get("conflicts", 0)
    errors = result.get("errors", [])

    status = "✅ Success" if not errors else "⚠️ Completed with errors"
    lines.extend([
        f"**Status**: {status}\n",
        "## Summary\n",
        f"- **Pushed** (→ {storage_type.title()}): {pushed} items",
        f"- **Pulled** (← {storage_type.title()}): {pulled} items",
        f"- **Conflicts**: {conflicts}",
        f"- **Errors**: {len(errors)}",
        "",
    ])

    if errors:
        lines.append("## Errors\n")
        for e in errors:
            lines.append(f"- ❌ {e}")
        lines.append("")

    if conflicts > 0:
        lines.extend([
            "## Conflict Resolution\n",
            f"{conflicts} conflicts were detected. Last-write-wins was applied for gaps > 5min.",
            "Check the sync log for details on which version was kept.\n",
        ])

    lines.extend([
        "---",
        f"*Read `references/scenarios.md` Scenario 12 for the full sync flow.*",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Format sync results from MCP data")
    parser.add_argument("--storage", default="notion", choices=["notion", "sheets"],
                        help="Storage type (notion or sheets)")
    parser.add_argument("--manifest", help="Path to sync manifest JSON")
    parser.add_argument("--sync-result", help="Path to sync result JSON")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only analyze manifest, don't expect sync result")
    args = parser.parse_args()

    manifest = load_json(args.manifest)

    if args.dry_run or not args.sync_result:
        analysis = analyze_manifest(manifest, args.storage)
        print(format_dry_run(analysis, args.storage))
    else:
        result = load_json(args.sync_result)
        print(format_sync_result(result, args.storage))


if __name__ == "__main__":
    main()
