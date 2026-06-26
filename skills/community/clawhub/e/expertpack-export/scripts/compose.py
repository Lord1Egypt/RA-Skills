#!/usr/bin/env python3
"""
ExpertPack Export — Composite Generator

Reads the scan manifest and generates a composite manifest + overview
that wires all exported packs together.

Usage:
    python3 compose.py --scan /tmp/ep-scan.json --export-dir /path/to/export/
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def compose(scan_path: str, export_dir: str):
    """Generate composite manifest and overview."""
    with open(scan_path) as f:
        scan = json.load(f)

    export = Path(export_dir)
    packs = scan.get("packs", {})

    if not packs:
        print("Error: No packs found in scan manifest", file=sys.stderr)
        sys.exit(1)

    # Determine composite slug from agent pack or workspace
    agent_packs = [s for s, p in packs.items() if p.get("subtype") == "agent"]
    agent_slug = agent_packs[0] if agent_packs else "agent"
    composite_slug = f"{agent_slug}-full"

    composite_dir = export / "composites" / composite_slug
    composite_dir.mkdir(parents=True, exist_ok=True)

    # Build pack entries
    pack_entries = []
    priority_order = []

    # Agent pack first (voice role)
    for slug, pack in packs.items():
        if pack.get("subtype") == "agent":
            pack_entries.append({
                "path": f"../../packs/{slug}",
                "role": "voice",
            })
            priority_order.append(slug)

    # Then person packs, then product, then process (knowledge role)
    type_order = ["person", "product", "process"]
    for pack_type in type_order:
        for slug, pack in packs.items():
            if pack["type"] == pack_type and pack.get("subtype") != "agent":
                pack_entries.append({
                    "path": f"../../packs/{slug}",
                    "role": "knowledge",
                })
                priority_order.append(slug)

    # Write composite manifest
    manifest_lines = [
        f'name: "{agent_slug.replace("-", " ").title()} — Full Instance Export"',
        f'slug: "{composite_slug}"',
        'type: "composite"',
        'version: "1.0.0"',
        'schema_version: "1.1"',
        f'description: "Complete knowledge export of the {agent_slug.replace("-", " ").title()} instance"',
        'entry_point: "overview.md"',
        '',
        'packs:',
    ]

    for entry in pack_entries:
        manifest_lines.append(f'  - path: "{entry["path"]}"')
        manifest_lines.append(f'    role: "{entry["role"]}"')

    manifest_lines.extend([
        '',
        'conflicts:',
        f'  priority: [{", ".join(priority_order)}]',
        '  strategy: "flag"',
    ])

    (composite_dir / "manifest.yaml").write_text("\n".join(manifest_lines) + "\n")

    # Write composite overview
    overview_lines = [
        f"# {agent_slug.replace('-', ' ').title()} — Full Export",
        "",
        f"Composite ExpertPack exported from an OpenClaw instance on {datetime.utcnow().strftime('%Y-%m-%d')}.",
        "",
        "## Constituent Packs",
        "",
    ]

    for entry in pack_entries:
        slug = entry["path"].split("/")[-1]
        pack_info = packs.get(slug, {})
        pack_type = pack_info.get("type", "unknown")
        subtype = f" ({pack_info['subtype']})" if pack_info.get("subtype") else ""
        overview_lines.append(f"- **{slug}** — {pack_type}{subtype}, role: {entry['role']}")
        if pack_info.get("description"):
            overview_lines.append(f"  - {pack_info['description']}")

    overview_lines.extend([
        "",
        "## Import",
        "",
        "See each pack's MIGRATION.md (agent pack) or overview.md for hydration instructions.",
        "Configure credentials separately — no secrets are included in this export.",
    ])

    (composite_dir / "overview.md").write_text("\n".join(overview_lines) + "\n")

    print(f"Composite '{composite_slug}' generated at {composite_dir}")
    print(f"  {len(pack_entries)} packs wired:")
    for e in pack_entries:
        print(f"    [{e['role']}] {e['path']}")


def main():
    parser = argparse.ArgumentParser(description="Generate EP composite from scan")
    parser.add_argument("--scan", required=True, help="Path to scan manifest JSON")
    parser.add_argument("--export-dir", required=True, help="Export root directory")
    args = parser.parse_args()

    compose(args.scan, args.export_dir)


if __name__ == "__main__":
    main()
