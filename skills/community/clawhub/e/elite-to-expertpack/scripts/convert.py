#!/usr/bin/env python3
"""
Elite Longterm Memory → ExpertPack Converter

Converts an Elite Longterm Memory 5-layer system into a structured ExpertPack.
Handles: SESSION-STATE.md, MEMORY.md, memory/*.md journals, memory/topics/*.md,
and Git-Notes JSONL cold store.

Usage:
    python3 convert.py --workspace /path/to/workspace --output ~/expertpacks/my-agent
    python3 convert.py --workspace . --output ./export --name "My Agent" --type agent
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# --- Secret patterns to strip ---
SECRET_PATTERNS = [
    re.compile(r'sk-[a-zA-Z0-9]{20,}'),
    re.compile(r'ghp_[a-zA-Z0-9]{36,}'),
    re.compile(r'xoxb-[a-zA-Z0-9\-]+'),
    re.compile(r'(?:api[_-]?key|token|secret|password|bearer)\s*[:=]\s*\S+', re.IGNORECASE),
]

# --- Parsing ---

def strip_secrets(text: str) -> tuple[str, list[str]]:
    """Strip secret patterns from text. Returns (cleaned_text, warnings)."""
    warnings = []
    for pat in SECRET_PATTERNS:
        matches = pat.findall(text)
        if matches:
            warnings.append(f"Stripped {len(matches)} potential secret(s) matching {pat.pattern[:40]}...")
            text = pat.sub("[REDACTED]", text)
    return text, warnings


def parse_session_state(filepath: Path) -> dict:
    """Parse SESSION-STATE.md into structured sections."""
    if not filepath.exists():
        return {}

    content = filepath.read_text(errors="replace")
    content, _ = strip_secrets(content)

    sections = {}
    current_section = None
    current_lines = []

    for line in content.split("\n"):
        if line.startswith("## "):
            if current_section and current_lines:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = line[3:].strip().lower()
            current_lines = []
        elif current_section:
            current_lines.append(line)

    if current_section and current_lines:
        sections[current_section] = "\n".join(current_lines).strip()

    return sections


def parse_memory_md(filepath: Path) -> dict:
    """Parse MEMORY.md into structured sections."""
    if not filepath.exists():
        return {}

    content = filepath.read_text(errors="replace")
    content, _ = strip_secrets(content)

    sections = {}
    current_section = None
    current_lines = []

    for line in content.split("\n"):
        if line.startswith("## "):
            if current_section and current_lines:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = line[3:].strip()
            current_lines = []
        elif line.startswith("# ") and not current_section:
            # Skip the title
            continue
        elif current_section:
            current_lines.append(line)

    if current_section and current_lines:
        sections[current_section] = "\n".join(current_lines).strip()

    return sections


def parse_journal(filepath: Path) -> dict:
    """Parse a daily journal file. Returns {date, sections, raw_content}."""
    content = filepath.read_text(errors="replace")
    content, _ = strip_secrets(content)

    # Extract date from filename
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.name)
    date = date_match.group(1) if date_match else filepath.stem

    sections = {}
    current_section = None
    current_lines = []

    for line in content.split("\n"):
        if line.startswith("## ") or line.startswith("### "):
            if current_section and current_lines:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = line.lstrip("#").strip()
            current_lines = []
        elif current_section:
            current_lines.append(line)

    if current_section and current_lines:
        sections[current_section] = "\n".join(current_lines).strip()

    return {"date": date, "sections": sections, "raw": content}


def parse_git_notes(filepath: Path) -> list[dict]:
    """Parse Git-Notes JSONL cold store."""
    if not filepath.exists():
        return []

    entries = []
    with open(filepath) as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                text = entry.get("content", "")
                text, _ = strip_secrets(text)
                entry["content"] = text
                entries.append(entry)
            except json.JSONDecodeError:
                print(f"  Warning: Skipping malformed JSONL line {i} in {filepath}", file=sys.stderr)

    return entries


def parse_topic_files(topic_dir: Path) -> dict[str, str]:
    """Parse memory/topics/*.md files. Returns {topic_name: content}."""
    topics = {}
    if not topic_dir.exists():
        return topics

    for f in sorted(topic_dir.glob("*.md")):
        content = f.read_text(errors="replace")
        content, _ = strip_secrets(content)
        topic_name = f.stem.replace("-", " ").replace("_", " ").title()
        topics[topic_name] = content

    return topics


# --- Classification ---

def classify_memory_section(name: str, content: str) -> str:
    """Classify a MEMORY.md section into an EP directory."""
    name_lower = name.lower()

    # Rules, guidelines, safety → mind/values
    if any(w in name_lower for w in ["rule", "guideline", "safety", "principle", "operational", "critical"]):
        return "mind"

    # People, contacts, relationships
    if any(w in name_lower for w in ["contact", "people", "team", "relationship", "about"]):
        return "relationships"

    # Projects, missions, goals
    if any(w in name_lower for w in ["project", "mission", "goal", "primary", "work"]):
        return "facts"

    # Links, references, quick
    if any(w in name_lower for w in ["link", "reference", "quick", "resource"]):
        return "operational"

    # Default
    return "facts"


def classify_git_note(entry: dict) -> str:
    """Classify a Git-Notes entry into an EP directory."""
    note_type = entry.get("type", "").lower()

    type_map = {
        "decision": "mind",
        "learning": "summaries",
        "context": "facts",
        "fact": "facts",
        "preference": "mind",
        "observation": "summaries",
    }

    return type_map.get(note_type, "facts")


def classify_journal_section(name: str) -> str:
    """Classify a journal section."""
    name_lower = name.lower()

    if any(w in name_lower for w in ["lesson", "learned", "insight", "reflection"]):
        return "summaries"
    if any(w in name_lower for w in ["decision", "chose", "decided"]):
        return "mind"
    if any(w in name_lower for w in ["project", "work", "progress", "update"]):
        return "facts"
    if any(w in name_lower for w in ["issue", "bug", "fix", "error", "troubleshoot"]):
        return "operational"

    return "summaries"


# --- EP Generation ---

def generate_manifest(output_dir: Path, name: str, pack_type: str, subtype: str,
                      stats: dict) -> None:
    """Generate manifest.yaml."""
    manifest = {
        "name": name,
        "slug": re.sub(r'[^a-z0-9-]', '-', name.lower()).strip('-'),
        "type": pack_type,
        "version": "1.0.0",
        "schema_version": "2.3",
        "description": f"ExpertPack converted from Elite Longterm Memory. "
                       f"{stats['total_items']} knowledge items from {stats['layers_found']} layers.",
        "entry_point": "overview.md",
        "author": "elite-to-expertpack converter",
        "created": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }

    if subtype:
        manifest["subtype"] = subtype

    # Context tiers
    always_files = ["overview.md"]
    searchable_dirs = []

    for d in ["mind", "facts", "summaries", "operational", "relationships"]:
        if (output_dir / d).exists():
            searchable_dirs.append(f"{d}/")

    manifest["context"] = {
        "always": always_files,
        "searchable": searchable_dirs,
    }

    with open(output_dir / "manifest.yaml", "w") as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, width=120)


def generate_overview(output_dir: Path, name: str, stats: dict, warnings: list[str]) -> None:
    """Generate overview.md."""
    content = f"""# {name}

> **Lead summary:** Agent knowledge pack converted from Elite Longterm Memory. Contains {stats['total_items']} knowledge items distilled from {stats['layers_found']} memory layers.

## Source Layers

| Layer | Status | Items |
|-------|--------|-------|
| Hot RAM (SESSION-STATE.md) | {"✅ Converted" if stats.get('session_state') else "⬜ Not found"} | {stats.get('session_state', 0)} |
| Curated Archive (MEMORY.md) | {"✅ Converted" if stats.get('memory_md') else "⬜ Not found"} | {stats.get('memory_md', 0)} |
| Daily Journals (memory/*.md) | {"✅ Converted" if stats.get('journals') else "⬜ Not found"} | {stats.get('journals', 0)} |
| Topic Files (memory/topics/*.md) | {"✅ Converted" if stats.get('topics') else "⬜ Not found"} | {stats.get('topics', 0)} |
| Cold Store (Git-Notes JSONL) | {"✅ Converted" if stats.get('git_notes') else "⬜ Not found"} | {stats.get('git_notes', 0)} |
| Warm Store (LanceDB) | ⬜ Skipped | — |
| Cloud (SuperMemory/Mem0) | ⬜ Skipped | — |

## Notes

- LanceDB vectors require export via the Elite Memory API before conversion. Not directly readable as files.
- SuperMemory and Mem0 cloud stores are external APIs — export separately if needed.
- Secrets were automatically stripped during conversion.
"""

    if warnings:
        content += "\n## Warnings\n\n"
        for w in warnings:
            content += f"- {w}\n"

    content += f"\n---\n*Converted: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*\n"

    with open(output_dir / "overview.md", "w") as f:
        f.write(content)


def write_content_file(output_dir: Path, directory: str, filename: str,
                       title: str, lead: str, body: str) -> Path:
    """Write a content file to the EP structure."""
    dir_path = output_dir / directory
    dir_path.mkdir(parents=True, exist_ok=True)

    filepath = dir_path / filename
    content = f"# {title}\n\n> **Lead summary:** {lead}\n\n{body}\n"

    # Enforce ~3KB limit — truncate if needed
    if len(content.encode()) > 3500:
        content = content[:3400] + "\n\n*[Truncated — see source files for full content]*\n"

    with open(filepath, "w") as f:
        f.write(content)

    return filepath


def write_index(output_dir: Path, directory: str, entries: list[tuple[str, str]]) -> None:
    """Write _index.md for a directory."""
    dir_path = output_dir / directory
    if not dir_path.exists():
        return

    content = f"# {directory.replace('/', '').title()}\n\n"
    for filename, desc in entries:
        name = filename.replace(".md", "").replace("-", " ").title()
        content += f"- [{name}]({filename}) — {desc}\n"

    with open(dir_path / "_index.md", "w") as f:
        f.write(content)


# --- Main Conversion ---

def convert(workspace: Path, output: Path, name: str, pack_type: str,
            git_notes_path: Path | None = None) -> None:
    """Run the full conversion."""

    print(f"\n{'='*60}")
    print(f"Elite Longterm Memory → ExpertPack Converter")
    print(f"Workspace: {workspace}")
    print(f"Output: {output}")
    print(f"{'='*60}\n")

    output.mkdir(parents=True, exist_ok=True)
    all_warnings = []
    stats = {"layers_found": 0, "total_items": 0}
    index_entries = {}  # dir -> [(filename, description)]
    written_facts = set()  # for deduplication

    # --- Layer 1: SESSION-STATE.md ---
    session_file = workspace / "SESSION-STATE.md"
    sections = parse_session_state(session_file)
    if sections:
        stats["layers_found"] += 1
        stats["session_state"] = len(sections)
        stats["total_items"] += len(sections)
        print(f"✅ Hot RAM: {len(sections)} sections from SESSION-STATE.md")

        body_parts = []
        for sec_name, sec_content in sections.items():
            if sec_content.strip():
                body_parts.append(f"## {sec_name.title()}\n\n{sec_content}")

        if body_parts:
            write_content_file(
                output, "operational", "session-state.md",
                "Active Session State",
                "Current operational state from the agent's hot RAM layer.",
                "\n\n".join(body_parts)
            )
            index_entries.setdefault("operational", []).append(
                ("session-state.md", "Active working context from SESSION-STATE.md")
            )
    else:
        print(f"⬜ Hot RAM: SESSION-STATE.md not found")

    # --- Layer 2: MEMORY.md ---
    memory_file = workspace / "MEMORY.md"
    mem_sections = parse_memory_md(memory_file)
    if mem_sections:
        stats["layers_found"] += 1
        stats["memory_md"] = len(mem_sections)
        stats["total_items"] += len(mem_sections)
        print(f"✅ Curated Archive: {len(mem_sections)} sections from MEMORY.md")

        # Group sections by EP directory
        grouped = {}
        for sec_name, sec_content in mem_sections.items():
            if not sec_content.strip():
                continue
            ep_dir = classify_memory_section(sec_name, sec_content)
            grouped.setdefault(ep_dir, []).append((sec_name, sec_content))

        for ep_dir, items in grouped.items():
            body_parts = []
            for sec_name, sec_content in items:
                body_parts.append(f"## {sec_name}\n\n{sec_content}")
                # Track for dedup
                for line in sec_content.split("\n"):
                    line_clean = line.strip().lower()[:80]
                    if len(line_clean) > 20:
                        written_facts.add(line_clean)

            slug = ep_dir
            filename = f"curated-{slug}.md"
            write_content_file(
                output, ep_dir, filename,
                f"Curated {slug.title()} Knowledge",
                f"Distilled from MEMORY.md curated archive ({len(items)} sections).",
                "\n\n".join(body_parts)
            )
            index_entries.setdefault(ep_dir, []).append(
                (filename, f"Curated knowledge from MEMORY.md ({len(items)} sections)")
            )
    else:
        print(f"⬜ Curated Archive: MEMORY.md not found")

    # --- Layer 3: Daily Journals ---
    memory_dir = workspace / "memory"
    journals = []
    if memory_dir.exists():
        for f in sorted(memory_dir.glob("*.md")):
            if re.match(r'\d{4}-\d{2}-\d{2}\.md', f.name):
                journals.append(f)

    if journals:
        stats["layers_found"] += 1
        stats["journals"] = len(journals)
        print(f"✅ Daily Journals: {len(journals)} files")

        # Distill journals — group content by classification
        journal_grouped = {}
        for jf in journals:
            parsed = parse_journal(jf)
            for sec_name, sec_content in parsed["sections"].items():
                if not sec_content.strip():
                    continue
                # Dedup check
                content_key = sec_content.strip().lower()[:80]
                if content_key in written_facts:
                    continue
                written_facts.add(content_key)

                ep_dir = classify_journal_section(sec_name)
                journal_grouped.setdefault(ep_dir, []).append(
                    (parsed["date"], sec_name, sec_content)
                )

        item_count = 0
        for ep_dir, items in journal_grouped.items():
            body_parts = []
            for date, sec_name, sec_content in items:
                body_parts.append(f"## {sec_name} ({date})\n\n{sec_content}")
                item_count += 1

            filename = f"journal-{ep_dir}.md"
            write_content_file(
                output, ep_dir if ep_dir != "summaries" else "summaries", filename,
                f"Journal {ep_dir.title()}",
                f"Distilled from {len(journals)} daily journal entries.",
                "\n\n".join(body_parts)
            )
            index_entries.setdefault(ep_dir, []).append(
                (filename, f"Distilled from {len(journals)} daily journals")
            )

        stats["total_items"] += item_count
    else:
        print(f"⬜ Daily Journals: none found")

    # --- Layer 4: Topic Files ---
    topics_dir = memory_dir / "topics" if memory_dir.exists() else None
    topics = parse_topic_files(topics_dir) if topics_dir else {}
    if topics:
        stats["layers_found"] += 1
        stats["topics"] = len(topics)
        stats["total_items"] += len(topics)
        print(f"✅ Topic Files: {len(topics)} files")

        for topic_name, content in topics.items():
            slug = re.sub(r'[^a-z0-9-]', '-', topic_name.lower()).strip('-')
            filename = f"{slug}.md"

            # Try to extract a lead from the first paragraph
            lines = content.strip().split("\n")
            lead_line = ""
            for line in lines:
                clean = line.strip().lstrip("#").strip()
                if len(clean) > 20:
                    lead_line = clean[:150]
                    break

            write_content_file(
                output, "facts", filename,
                topic_name,
                lead_line or f"Topic knowledge about {topic_name}.",
                content
            )
            index_entries.setdefault("facts", []).append(
                (filename, f"Topic: {topic_name}")
            )
    else:
        print(f"⬜ Topic Files: none found")

    # --- Layer 5: Git-Notes JSONL ---
    git_notes_file = git_notes_path
    if not git_notes_file:
        # Try common locations
        for candidate in [
            workspace / ".git-notes" / "memories.jsonl",
            workspace / "git-notes.jsonl",
            workspace / "memory" / "git-notes.jsonl",
            workspace / "memories.jsonl",
        ]:
            if candidate.exists():
                git_notes_file = candidate
                break

    git_entries = parse_git_notes(git_notes_file) if git_notes_file else []
    if git_entries:
        stats["layers_found"] += 1
        stats["git_notes"] = len(git_entries)
        stats["total_items"] += len(git_entries)
        print(f"✅ Cold Store: {len(git_entries)} entries from Git-Notes")

        # Group by classification
        gn_grouped = {}
        for entry in git_entries:
            content = entry.get("content", "").strip()
            if not content:
                continue
            # Dedup
            content_key = content.lower()[:80]
            if content_key in written_facts:
                continue
            written_facts.add(content_key)

            ep_dir = classify_git_note(entry)
            gn_grouped.setdefault(ep_dir, []).append(entry)

        for ep_dir, items in gn_grouped.items():
            body_parts = []
            for entry in items:
                note_type = entry.get("type", "note").title()
                content = entry.get("content", "")
                tags = entry.get("tags", [])
                importance = entry.get("importance", "")
                timestamp = entry.get("timestamp", "")

                header = f"## {note_type}"
                if timestamp:
                    header += f" ({timestamp[:10]})"

                meta = ""
                if tags:
                    tag_str = ", ".join(tags) if isinstance(tags, list) else str(tags)
                    meta += f"\n*Tags: {tag_str}*"
                if importance:
                    meta += f" | *Importance: {importance}*"

                body_parts.append(f"{header}\n{meta}\n\n{content}")

            filename = f"git-notes-{ep_dir}.md"
            write_content_file(
                output, ep_dir, filename,
                f"Git-Notes {ep_dir.title()}",
                f"Structured knowledge from Git-Notes cold store ({len(items)} entries).",
                "\n\n".join(body_parts)
            )
            index_entries.setdefault(ep_dir, []).append(
                (filename, f"From Git-Notes cold store ({len(items)} entries)")
            )
    else:
        print(f"⬜ Cold Store: Git-Notes not found")

    # --- Check for SOUL.md / IDENTITY.md / USER.md ---
    # These help with pack type detection and relationship extraction

    soul_file = workspace / "SOUL.md"
    identity_file = workspace / "IDENTITY.md"
    user_file = workspace / "USER.md"

    detected_subtype = ""
    if pack_type == "auto":
        if soul_file.exists() or identity_file.exists():
            pack_type = "person"
            detected_subtype = "agent"
            print(f"\n  Auto-detected pack type: person (subtype: agent)")
        else:
            pack_type = "person"
            detected_subtype = "agent"
            print(f"\n  Default pack type: person (subtype: agent)")
    elif pack_type == "agent":
        pack_type = "person"
        detected_subtype = "agent"

    # Extract user info for relationships
    if user_file.exists():
        user_content = user_file.read_text(errors="replace")
        user_content, _ = strip_secrets(user_content)

        write_content_file(
            output, "relationships", "primary-user.md",
            "Primary User",
            "Information about the agent's primary user.",
            user_content
        )
        index_entries.setdefault("relationships", []).append(
            ("primary-user.md", "Primary user profile")
        )
        stats["total_items"] += 1

    # --- Generate _index.md files ---
    for ep_dir, entries in index_entries.items():
        write_index(output, ep_dir, entries)

    # --- Generate relations.yaml if we have cross-references ---
    entities = []
    relations = []

    # Scan generated files for entity references
    for ep_dir in ["mind", "facts", "summaries", "operational", "relationships"]:
        dir_path = output / ep_dir
        if not dir_path.exists():
            continue
        for f in dir_path.glob("*.md"):
            if f.name == "_index.md":
                continue
            entity_id = f.stem
            entity_type = {
                "mind": "concept",
                "facts": "concept",
                "summaries": "concept",
                "operational": "tool",
                "relationships": "person",
            }.get(ep_dir, "concept")

            entities.append({
                "id": entity_id,
                "type": entity_type,
                "label": f.stem.replace("-", " ").title(),
                "file": f"{ep_dir}/{f.name}",
            })

    if len(entities) > 1:
        relations_data = {"entities": entities, "relations": relations}
        with open(output / "relations.yaml", "w") as f:
            yaml.dump(relations_data, f, default_flow_style=False, sort_keys=False, width=120)

    # --- Collect all warnings ---
    for ep_dir in ["mind", "facts", "summaries", "operational", "relationships"]:
        dir_path = output / ep_dir
        if not dir_path.exists():
            continue
        for f in dir_path.glob("*.md"):
            content = f.read_text(errors="replace")
            _, file_warnings = strip_secrets(content)
            all_warnings.extend(file_warnings)

    # --- Generate manifest and overview ---
    generate_manifest(output, name, pack_type, detected_subtype, stats)
    generate_overview(output, name, stats, all_warnings)

    # --- Summary ---
    file_count = sum(1 for _ in output.rglob("*.md")) + sum(1 for _ in output.rglob("*.yaml"))
    total_size = sum(f.stat().st_size for f in output.rglob("*") if f.is_file())

    print(f"\n{'='*60}")
    print(f"Conversion Complete")
    print(f"{'='*60}")
    print(f"Pack: {name}")
    print(f"Type: {pack_type}" + (f" (subtype: {detected_subtype})" if detected_subtype else ""))
    print(f"Layers converted: {stats['layers_found']}")
    print(f"Total items: {stats['total_items']}")
    print(f"Files generated: {file_count}")
    print(f"Total size: {total_size / 1024:.1f} KB")
    print(f"Output: {output}")

    if all_warnings:
        print(f"\n⚠️  {len(all_warnings)} warnings:")
        for w in all_warnings[:5]:
            print(f"  - {w}")

    print(f"\nNext steps:")
    print(f"  1. Review overview.md and manifest.yaml")
    print(f"  2. Run chunker: python3 chunk.py --pack {output} --output {output}/.chunks")
    print(f"  3. Measure EK: python3 eval-ek.py {output}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Elite Longterm Memory into an ExpertPack"
    )
    parser.add_argument("--workspace", "-w", type=Path, required=True,
                        help="Path to the OpenClaw workspace")
    parser.add_argument("--output", "-o", type=Path, required=True,
                        help="Output directory for the ExpertPack")
    parser.add_argument("--name", "-n", type=str, default="Agent Knowledge",
                        help="Pack name (default: 'Agent Knowledge')")
    parser.add_argument("--type", "-t", type=str, default="auto",
                        choices=["auto", "person", "agent", "product", "process"],
                        help="Pack type (default: auto-detect)")
    parser.add_argument("--git-notes", type=Path, default=None,
                        help="Path to Git-Notes JSONL file (auto-detected if omitted)")

    args = parser.parse_args()

    if not args.workspace.exists():
        print(f"Error: Workspace not found: {args.workspace}", file=sys.stderr)
        sys.exit(1)

    convert(
        workspace=args.workspace,
        output=args.output,
        name=args.name,
        pack_type=args.type,
        git_notes_path=args.git_notes,
    )


if __name__ == "__main__":
    main()
