#!/usr/bin/env python3
"""
ExpertPack Export — Knowledge Distiller

Reads source files from the scan manifest and produces structured EP-compliant
output files for a single pack.

This script handles the STRUCTURAL work: creating directories, writing manifests,
and scaffolding files. The actual CONTENT distillation (compressing journals into
lessons, extracting operational knowledge from memory files) is done by the AI agent
that calls this script — the agent reads source files, distills the knowledge, and
writes the content to the scaffolded files.

Usage:
    python3 distill.py --scan /tmp/ep-scan.json --pack agent:slug --output /path/to/pack/
    python3 distill.py --scan /tmp/ep-scan.json --pack person:slug --output /path/to/pack/
    python3 distill.py --scan /tmp/ep-scan.json --pack product:slug --output /path/to/pack/
    python3 distill.py --scan /tmp/ep-scan.json --pack process:slug --output /path/to/pack/
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime


# Secret patterns to strip from content
SECRET_PATTERNS = [
    (re.compile(r'((?:api[_-]?key|token|secret|password|bearer)\s*[:=]\s*)\S+', re.IGNORECASE),
     r'\1<REDACTED>'),
    (re.compile(r'(sk-)[a-zA-Z0-9]{20,}'), r'\1<REDACTED>'),
    (re.compile(r'(ghp_)[a-zA-Z0-9]{36,}'), r'\1<REDACTED>'),
    (re.compile(r'(xoxb-)[a-zA-Z0-9\-]+'), r'\1<REDACTED>'),
]


def strip_secrets(text: str) -> str:
    """Replace known secret patterns with <REDACTED>."""
    for pattern, replacement in SECRET_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def scaffold_agent_pack(output_dir: Path, slug: str, scan: dict):
    """Create directory structure and manifest for an agent pack."""
    dirs = [
        "operational",
        "mind",
        "relationships",
        "facts",
        "presentation",
        "summaries",
        "meta",
    ]
    for d in dirs:
        (output_dir / d).mkdir(parents=True, exist_ok=True)

    # Write manifest
    manifest = {
        "name": slug.replace("-", " ").title(),
        "slug": slug,
        "type": "person",
        "subtype": "agent",
        "version": "1.0.0",
        "schema_version": "1.6",
        "description": f"Agent identity and operational knowledge for {slug}",
        "entry_point": "overview.md",
        "subject": {
            "name": slug.replace("-", " ").title(),
            "platform": "OpenClaw",
            "created": datetime.utcnow().strftime("%Y-%m-%d"),
        },
        "context": {
            "always": [
                "overview.md",
                "presentation/speech_patterns.md",
                "operational/safety.md",
                "mind/values.md",
            ],
            "searchable": [
                "mind/",
                "relationships/",
                "facts/",
                "operational/",
                "summaries/",
                "presentation/modes.md",
            ],
            "on_demand": [
                "meta/",
            ],
        },
        "sources": [
            {
                "type": "platform-export",
                "description": "Auto-generated from OpenClaw instance state",
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
            }
        ],
    }

    _write_yaml(output_dir / "manifest.yaml", manifest)

    # Write stub files that the agent will fill with distilled content
    stubs = {
        "overview.md": "# {name}\n\n> Agent identity and personality. To be distilled from SOUL.md + IDENTITY.md.\n",
        "MIGRATION.md": "# Migration Guide\n\n> Hydration instructions. To be filled after distillation.\n",
        "operational/tools.md": "# Tools\n\n> Distilled from TOOLS.md. No secrets.\n",
        "operational/infrastructure.md": "# Infrastructure\n\n> Distilled from TOOLS.md + memory files.\n",
        "operational/integrations.md": "# Integrations\n\n> Messaging channels, APIs, external services.\n",
        "operational/routines.md": "# Routines\n\n> Distilled from HEARTBEAT.md + cron jobs.\n",
        "operational/safety.md": "# Safety Contracts\n\n> Distilled from AGENTS.md safety rules.\n",
        "mind/values.md": "# Values & Operational Principles\n\n> Prescriptive rules from AGENTS.md.\n",
        "mind/skills.md": "# Capabilities\n\n> What this agent can do.\n",
        "mind/relational.md": "# Interaction Rules\n\n> How this agent communicates in different contexts.\n",
        "mind/preferences.md": "# Learned Preferences\n\n> Formatting, behavior, platform-specific rules.\n",
        "mind/reasoning.md": "# Reasoning Patterns\n\n> How this agent approaches decisions.\n",
        "mind/tensions.md": "# Known Limitations\n\n> Failure modes, weaknesses, things to improve.\n",
        "relationships/people.md": "# Relationships\n\n> Primary user, contacts, peer agents.\n",
        "facts/personal.md": "# Agent Identity\n\n> Name, creation date, platform, avatar.\n",
        "facts/timeline.md": "# Timeline\n\n> Significant events in this agent's history.\n",
        "presentation/speech_patterns.md": "# Communication Style\n\n> Tone, humor, formality, emoji usage.\n",
        "presentation/modes.md": "# Modes\n\n> Context-dependent voices.\n",
        "summaries/lessons.md": "# Lessons Learned\n\n> Patterns, post-mortems, accumulated wisdom.\n",
        "meta/privacy.md": "# Privacy\n\n## Public\n- Identity, capabilities, communication style\n\n## Private\n- User details, infrastructure specifics, relationship details\n",
    }

    for relpath, template in stubs.items():
        fpath = output_dir / relpath
        content = template.replace("{name}", slug.replace("-", " ").title())
        fpath.write_text(content)

    return manifest


def scaffold_person_pack(output_dir: Path, slug: str, scan: dict):
    """Create directory structure and manifest for a person pack."""
    dirs = ["facts", "relationships", "mind", "presentation", "meta"]
    for d in dirs:
        (output_dir / d).mkdir(parents=True, exist_ok=True)

    manifest = {
        "name": slug.replace("-", " ").title(),
        "slug": slug,
        "type": "person",
        "version": "1.0.0",
        "schema_version": "1.5",
        "description": f"Knowledge about {slug.replace('-', ' ').title()}",
        "entry_point": "overview.md",
        "subject": {
            "full_name": slug.replace("-", " ").title(),
            "alive": True,
        },
        "context": {
            "always": ["overview.md", "facts/personal.md"],
            "searchable": ["facts/", "relationships/", "mind/"],
            "on_demand": ["meta/"],
        },
        "sources": [
            {
                "type": "platform-export",
                "description": "Distilled from OpenClaw workspace knowledge",
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
            }
        ],
    }

    _write_yaml(output_dir / "manifest.yaml", manifest)

    stubs = {
        "overview.md": "# {name}\n\n> Person overview. To be distilled from USER.md + MEMORY.md.\n",
        "facts/personal.md": "# Personal Facts\n\n> Bio, timezone, role, background.\n",
        "relationships/people.md": "# Relationships\n\n> Key people in this person's life/work.\n",
        "mind/preferences.md": "# Preferences\n\n> Communication style, work patterns, interests.\n",
        "meta/privacy.md": "# Privacy\n\n## Public\n- Name, role, professional info\n\n## Private\n- Personal details, family, beliefs\n",
    }

    for relpath, template in stubs.items():
        fpath = output_dir / relpath
        content = template.replace("{name}", slug.replace("-", " ").title())
        fpath.write_text(content)

    return manifest


def scaffold_product_pack(output_dir: Path, slug: str, scan: dict):
    """Create directory structure and manifest for a product pack."""
    dirs = ["concepts", "workflows", "commercial", "troubleshooting", "faq"]
    for d in dirs:
        (output_dir / d).mkdir(parents=True, exist_ok=True)

    manifest = {
        "name": slug.replace("-", " ").title(),
        "slug": slug,
        "type": "product",
        "version": "1.0.0",
        "schema_version": "1.4",
        "description": f"Product knowledge for {slug.replace('-', ' ').title()}",
        "entry_point": "overview.md",
        "context": {
            "always": ["overview.md"],
            "searchable": ["concepts/", "workflows/", "commercial/", "faq/"],
            "on_demand": ["troubleshooting/"],
        },
        "sources": [
            {
                "type": "platform-export",
                "description": "Distilled from OpenClaw workspace knowledge",
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
            }
        ],
    }

    _write_yaml(output_dir / "manifest.yaml", manifest)

    stubs = {
        "overview.md": f"# {slug.replace('-', ' ').title()}\n\n> Product overview. To be distilled.\n",
    }

    for relpath, content in stubs.items():
        (output_dir / relpath).write_text(content)

    return manifest


def scaffold_process_pack(output_dir: Path, slug: str, scan: dict):
    """Create directory structure and manifest for a process pack."""
    dirs = ["phases", "decisions", "checklists", "gotchas"]
    for d in dirs:
        (output_dir / d).mkdir(parents=True, exist_ok=True)

    manifest = {
        "name": slug.replace("-", " ").title(),
        "slug": slug,
        "type": "process",
        "version": "1.0.0",
        "schema_version": "1.2",
        "description": f"Process documentation for {slug.replace('-', ' ').title()}",
        "entry_point": "overview.md",
        "context": {
            "always": ["overview.md"],
            "searchable": ["phases/", "decisions/", "checklists/"],
            "on_demand": ["gotchas/"],
        },
        "sources": [
            {
                "type": "platform-export",
                "description": "Distilled from OpenClaw workspace knowledge",
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
            }
        ],
    }

    _write_yaml(output_dir / "manifest.yaml", manifest)

    stubs = {
        "overview.md": f"# {slug.replace('-', ' ').title()}\n\n> Process overview. To be distilled.\n",
    }

    for relpath, content in stubs.items():
        (output_dir / relpath).write_text(content)

    return manifest


def _write_yaml(path: Path, data: dict):
    """Write a dict as YAML (simple serializer — avoids PyYAML dependency)."""
    def _serialize(obj, indent=0):
        lines = []
        prefix = "  " * indent
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    lines.append(f"{prefix}{k}:")
                    lines.extend(_serialize(v, indent + 1))
                elif isinstance(v, bool):
                    lines.append(f"{prefix}{k}: {'true' if v else 'false'}")
                elif v is None:
                    lines.append(f"{prefix}{k}: null")
                else:
                    lines.append(f'{prefix}{k}: "{v}"')
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, dict):
                    first = True
                    for k, v in item.items():
                        if first:
                            lines.append(f"{prefix}- {k}: \"{v}\"" if isinstance(v, str) else f"{prefix}- {k}: {v}")
                            first = False
                        else:
                            lines.append(f"{prefix}  {k}: \"{v}\"" if isinstance(v, str) else f"{prefix}  {k}: {v}")
                elif isinstance(item, str):
                    lines.append(f'{prefix}- "{item}"')
                else:
                    lines.append(f"{prefix}- {item}")
        return lines

    content = "\n".join(_serialize(data)) + "\n"
    path.write_text(content)


def main():
    parser = argparse.ArgumentParser(description="Scaffold and distill an EP pack")
    parser.add_argument("--scan", required=True, help="Path to scan manifest JSON")
    parser.add_argument("--pack", required=True, help="Pack to distill: type:slug (e.g., agent:easybot)")
    parser.add_argument("--output", "-o", required=True, help="Output directory for the pack")
    args = parser.parse_args()

    with open(args.scan) as f:
        scan = json.load(f)

    pack_type, pack_slug = args.pack.split(":", 1)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    scaffolders = {
        "agent": scaffold_agent_pack,
        "person": scaffold_person_pack,
        "product": scaffold_product_pack,
        "process": scaffold_process_pack,
    }

    if pack_type not in scaffolders:
        print(f"Error: unknown pack type '{pack_type}'. Use: {', '.join(scaffolders.keys())}", file=sys.stderr)
        sys.exit(1)

    manifest = scaffolders[pack_type](output_dir, pack_slug, scan)
    print(f"Scaffolded {pack_type} pack '{pack_slug}' at {output_dir}")

    # List source files for this pack from the scan
    source_files = [f for f in scan.get("files", []) if f.get("pack") == pack_slug]
    print(f"Source files to distill: {len(source_files)}")
    for sf in source_files:
        flag = " ⚠️ SECRETS" if sf.get("has_secret_patterns") else ""
        flag += " 🔍 NEEDS ANALYSIS" if sf.get("needs_content_analysis") else ""
        print(f"  [{sf['confidence']:.1f}] {sf['path']} → {sf['section']}{flag}")

    print(f"\nNext: Agent reads source files and writes distilled content to {output_dir}/")


if __name__ == "__main__":
    main()
