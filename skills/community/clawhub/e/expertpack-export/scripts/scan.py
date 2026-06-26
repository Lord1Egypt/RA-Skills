#!/usr/bin/env python3
"""
ExpertPack Export — Workspace Scanner

Scans an OpenClaw workspace and produces a JSON manifest describing:
- All discovered files and their categories
- Proposed pack assignments (agent, person, product, process)
- Knowledge domains detected
- Confidence scores for ambiguous items

Usage:
    python3 scan.py --workspace /path/to/workspace --output /tmp/ep-scan.json
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime


# --- File classification rules ---

# Files that define the agent itself
AGENT_FILES = {
    "SOUL.md": {"section": "overview", "confidence": 1.0},
    "IDENTITY.md": {"section": "facts/personal", "confidence": 1.0},
    "AGENTS.md": {"section": "mind/values+safety", "confidence": 1.0},
    "TOOLS.md": {"section": "operational/tools+infrastructure", "confidence": 1.0},
    "HEARTBEAT.md": {"section": "operational/routines", "confidence": 1.0},
}

# Files that describe the user (person pack)
USER_FILES = {
    "USER.md": {"section": "overview+facts", "confidence": 1.0},
}

# Memory files — need content analysis to classify
MEMORY_PATTERNS = {
    "MEMORY.md": {"default_pack": "agent", "section": "mixed", "confidence": 0.7},
    "memory/session-state.md": {"default_pack": "agent", "section": "operational/routines", "confidence": 0.6},
    "memory/archive.md": {"default_pack": "mixed", "section": "mixed", "confidence": 0.5},
    "memory/droplet-architecture.md": {"default_pack": "agent", "section": "operational/infrastructure", "confidence": 0.9},
}

# Secret patterns to flag
SECRET_PATTERNS = [
    re.compile(r'(?:api[_-]?key|token|secret|password|bearer)\s*[:=]\s*\S+', re.IGNORECASE),
    re.compile(r'sk-[a-zA-Z0-9]{20,}'),
    re.compile(r'ghp_[a-zA-Z0-9]{36,}'),
    re.compile(r'xoxb-[a-zA-Z0-9\-]+'),
]


def scan_workspace(workspace: str) -> dict:
    """Scan workspace and produce classification manifest."""
    ws = Path(workspace)
    if not ws.exists():
        print(f"Error: workspace {workspace} does not exist", file=sys.stderr)
        sys.exit(1)

    manifest = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "workspace": str(ws.resolve()),
        "packs": {},
        "files": [],
        "warnings": [],
    }

    # Track proposed packs
    packs = {}

    # --- Pass 1: Scan root-level OC files ---
    agent_slug = None
    user_slug = None

    # Detect agent identity
    identity_file = ws / "IDENTITY.md"
    if identity_file.exists():
        content = identity_file.read_text(errors="replace")
        name_match = re.search(r'\*\*Name:\*\*\s*(.+)', content)
        if name_match:
            agent_slug = name_match.group(1).strip().lower().replace(" ", "-")
    if not agent_slug:
        agent_slug = "agent"

    # Detect user identity
    user_file = ws / "USER.md"
    if user_file.exists():
        content = user_file.read_text(errors="replace")
        name_match = re.search(r'\*\*Name:\*\*\s*(.+)', content)
        if name_match:
            raw_name = name_match.group(1).strip()
            user_slug = raw_name.lower().replace(" ", "-")
    if not user_slug:
        user_slug = "user"

    # Register agent pack
    packs[agent_slug] = {
        "type": "person",
        "subtype": "agent",
        "slug": agent_slug,
        "sources": [],
        "description": f"AI agent identity and operational knowledge",
    }

    # Register person pack for user
    packs[user_slug] = {
        "type": "person",
        "subtype": None,
        "slug": user_slug,
        "sources": [],
        "description": f"Knowledge about the primary user",
    }

    # --- Pass 2: Classify root workspace files ---
    for fname, meta in AGENT_FILES.items():
        fpath = ws / fname
        if fpath.exists():
            entry = _make_file_entry(fpath, ws, agent_slug, meta["section"], meta["confidence"])
            _check_secrets(fpath, entry, manifest)
            manifest["files"].append(entry)
            packs[agent_slug]["sources"].append(str(fpath.relative_to(ws)))

    for fname, meta in USER_FILES.items():
        fpath = ws / fname
        if fpath.exists():
            entry = _make_file_entry(fpath, ws, user_slug, meta["section"], meta["confidence"])
            _check_secrets(fpath, entry, manifest)
            manifest["files"].append(entry)
            packs[user_slug]["sources"].append(str(fpath.relative_to(ws)))

    # --- Pass 3: Memory files ---
    for pattern, meta in MEMORY_PATTERNS.items():
        fpath = ws / pattern
        if fpath.exists():
            pack_assignment = agent_slug if meta["default_pack"] != "mixed" else agent_slug
            entry = _make_file_entry(fpath, ws, pack_assignment, meta["section"], meta["confidence"])
            if meta["default_pack"] == "mixed":
                entry["needs_content_analysis"] = True
            _check_secrets(fpath, entry, manifest)
            manifest["files"].append(entry)
            packs[agent_slug]["sources"].append(str(fpath.relative_to(ws)))

    # Daily journals
    memory_dir = ws / "memory"
    if memory_dir.exists():
        for f in sorted(memory_dir.glob("*.md")):
            rel = str(f.relative_to(ws))
            if rel in [v for v in MEMORY_PATTERNS.keys()]:
                continue  # already handled
            if re.match(r'memory/\d{4}-\d{2}-\d{2}\.md', rel):
                entry = _make_file_entry(f, ws, agent_slug, "summaries/lessons", 0.6)
                entry["content_type"] = "daily_journal"
                entry["needs_content_analysis"] = True
                manifest["files"].append(entry)
                packs[agent_slug]["sources"].append(rel)
            elif re.match(r'memory/\d{4}-\d{2}-summary\.md', rel):
                entry = _make_file_entry(f, ws, agent_slug, "summaries/lessons", 0.7)
                entry["content_type"] = "monthly_summary"
                manifest["files"].append(entry)
                packs[agent_slug]["sources"].append(rel)
            else:
                # Other memory files — classify by name
                entry = _make_file_entry(f, ws, agent_slug, "mixed", 0.5)
                entry["needs_content_analysis"] = True
                manifest["files"].append(entry)
                packs[agent_slug]["sources"].append(rel)

    # --- Pass 4: Detect product/process knowledge ---
    # Look for project directories with STATUS.md or known structures
    skip_dirs = {"memory", "export", ".git", "node_modules", "logs", "scripts",
                 ".secrets", "bot-profiles", "memory/old"}

    for item in ws.iterdir():
        if not item.is_dir():
            continue
        if item.name in skip_dirs or item.name.startswith("."):
            continue

        status_file = item / "STATUS.md"
        manifest_file = item / "manifest.yaml"
        readme_file = item / "README.md"

        # Check if this looks like an ExpertPack already
        if manifest_file.exists():
            # It's already an EP — note it but don't re-export
            manifest["warnings"].append(
                f"Directory {item.name}/ appears to be an existing ExpertPack (has manifest.yaml). Skipping."
            )
            continue

        # Check for product/process indicators
        has_status = status_file.exists()
        has_concepts = (item / "concepts").exists()
        has_workflows = (item / "workflows").exists()
        has_phases = (item / "phases").exists()

        if has_concepts or has_workflows or has_status:
            # Likely a product knowledge directory
            slug = item.name.lower().replace(" ", "-")
            if slug not in packs:
                packs[slug] = {
                    "type": "product",
                    "subtype": None,
                    "slug": slug,
                    "sources": [],
                    "description": f"Product knowledge from {item.name}/",
                }
            # Scan .md files in the directory
            for md_file in item.rglob("*.md"):
                entry = _make_file_entry(md_file, ws, slug, _guess_section(md_file, item), 0.7)
                manifest["files"].append(entry)
                packs[slug]["sources"].append(str(md_file.relative_to(ws)))

        elif has_phases:
            # Likely a process directory
            slug = item.name.lower().replace(" ", "-")
            if slug not in packs:
                packs[slug] = {
                    "type": "process",
                    "subtype": None,
                    "slug": slug,
                    "sources": [],
                    "description": f"Process knowledge from {item.name}/",
                }
            for md_file in item.rglob("*.md"):
                entry = _make_file_entry(md_file, ws, slug, "phases", 0.6)
                manifest["files"].append(entry)
                packs[slug]["sources"].append(str(md_file.relative_to(ws)))

    # --- Pass 5: Scan logs for operational knowledge ---
    logs_dir = ws / "logs"
    if logs_dir.exists():
        for md_file in logs_dir.rglob("*.md"):
            entry = _make_file_entry(md_file, ws, agent_slug, "operational/routines", 0.5)
            entry["content_type"] = "log"
            entry["needs_content_analysis"] = True
            manifest["files"].append(entry)
            packs[agent_slug]["sources"].append(str(md_file.relative_to(ws)))

    # --- Pass 6: Scripts ---
    scripts_dir = ws / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.iterdir():
            if script.is_file():
                entry = _make_file_entry(script, ws, agent_slug, "operational/tools", 0.6)
                entry["content_type"] = "script"
                manifest["files"].append(entry)
                packs[agent_slug]["sources"].append(str(script.relative_to(ws)))

    manifest["packs"] = packs

    # --- Summary stats ---
    manifest["summary"] = {
        "total_files": len(manifest["files"]),
        "total_packs": len(packs),
        "pack_types": {slug: p["type"] + (f"/{p['subtype']}" if p.get("subtype") else "")
                       for slug, p in packs.items()},
        "files_needing_analysis": sum(1 for f in manifest["files"] if f.get("needs_content_analysis")),
        "secret_warnings": sum(1 for f in manifest["files"] if f.get("has_secret_patterns")),
    }

    return manifest


def _make_file_entry(fpath: Path, workspace: Path, pack_slug: str,
                     section: str, confidence: float) -> dict:
    """Create a file entry for the manifest."""
    stat = fpath.stat()
    return {
        "path": str(fpath.relative_to(workspace)),
        "pack": pack_slug,
        "section": section,
        "confidence": confidence,
        "size_bytes": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
    }


def _check_secrets(fpath: Path, entry: dict, manifest: dict):
    """Check file for potential secret patterns."""
    try:
        content = fpath.read_text(errors="replace")
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                entry["has_secret_patterns"] = True
                manifest["warnings"].append(
                    f"Potential secret found in {entry['path']} — review before export"
                )
                return
    except Exception:
        pass


def _guess_section(fpath: Path, project_root: Path) -> str:
    """Guess the EP section for a file within a project directory."""
    rel = fpath.relative_to(project_root)
    parts = rel.parts

    if len(parts) > 1:
        parent = parts[0].lower()
        section_map = {
            "concepts": "concepts",
            "workflows": "workflows",
            "interfaces": "interfaces",
            "commercial": "commercial",
            "troubleshooting": "troubleshooting",
            "faq": "faq",
            "phases": "phases",
            "decisions": "decisions",
            "checklists": "checklists",
        }
        if parent in section_map:
            return section_map[parent]

    name = fpath.stem.lower()
    if "status" in name:
        return "overview"
    if "readme" in name:
        return "overview"
    if "glossary" in name:
        return "glossary"

    return "concepts"  # default for product files


def main():
    parser = argparse.ArgumentParser(description="Scan OpenClaw workspace for EP export")
    parser.add_argument("--workspace", "-w", required=True, help="Path to workspace")
    parser.add_argument("--output", "-o", required=True, help="Output JSON path")
    args = parser.parse_args()

    manifest = scan_workspace(args.workspace)

    with open(args.output, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Scan complete: {manifest['summary']['total_files']} files, "
          f"{manifest['summary']['total_packs']} packs proposed")
    print(f"Output: {args.output}")

    if manifest["warnings"]:
        print(f"\n⚠️  {len(manifest['warnings'])} warnings:")
        for w in manifest["warnings"][:10]:
            print(f"  - {w}")
        if len(manifest["warnings"]) > 10:
            print(f"  ... and {len(manifest['warnings']) - 10} more")


if __name__ == "__main__":
    main()
