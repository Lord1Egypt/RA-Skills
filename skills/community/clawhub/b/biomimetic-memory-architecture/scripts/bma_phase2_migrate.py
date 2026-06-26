#!/usr/bin/env python3
"""
BMA Phase 2 — Compress, migrate, and rewrite references.

Reads a Phase 1 audit report and:
  1. Compresses "retain-summary" files → active memory residue
  2. Moves source files to memory-archive/ cold storage
  3. Rewrites references in active memory files

Default: dry-run (preview only).  Use --execute to perform actual writes.
Phase 1 audit reports are process artifacts; delete them after Phase 2.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

HEADER_RE = re.compile(r"^### `(.+?)`$")
ATTR_RE = re.compile(r"^- (date|age|score|size|lines|future cold path):\s*(.+)$", re.MULTILINE)
SIGNAL_RE = re.compile(r"^- (high|low) signals:\s*`(.+?)`$", re.MULTILINE)
EXCERPT_RE = re.compile(r"^- excerpt:\s*(.+)$", re.MULTILINE)
BUCKET_RE = re.compile(r"^## (retain-summary|review-manual|cold-archive-only)$")

# Files to scan for reference rewriting
SCAN_DIRS = ["memory/projects", "memory/runbooks", "memory/workflows", "memory/contacts"]
SCAN_FILES = ["memory/preferences.md", "MEMORY.md", "TOOLS.md", "INFRA.md"]


def parse_args():
    p = argparse.ArgumentParser(description="BMA Phase 2 — compress, migrate, rewrite references")
    p.add_argument("--workspace", default=".", help="OpenClaw workspace path")
    p.add_argument("--audit-report", required=True, help="Path to Phase 1 audit report (markdown)")
    p.add_argument("--dry-run", action="store_true", default=True, help="Preview only (default)")
    p.add_argument("--execute", action="store_true", dest="execute", help="Actually perform migration")
    p.add_argument("--buckets", nargs="*", default=["retain-summary", "review-manual", "cold-archive-only"],
                   choices=["retain-summary", "cold-archive-only", "review-manual"])
    return p.parse_args()


def parse_audit_report(report_text: str) -> list[dict]:
    """Parse a Phase 1 audit report into structured entries."""
    entries = []
    current_bucket: Optional[str] = None
    current_entry: Optional[dict] = None

    # Match combined lines like: "- date: 2026-03-18 / age: 48 days / score: 112"
    COMBINED_RE = re.compile(r"^-\s*(\S+):\s*(.+)$")

    def parse_combined(val: str) -> dict[str, str]:
        parts = {}
        for segment in val.split(" / "):
            segment = segment.strip()
            m = re.match(r"^(\S+):\s*(.+)$", segment)
            if m:
                parts[m.group(1)] = m.group(2).strip()
        return parts

    for line in report_text.splitlines():
        m = BUCKET_RE.match(line.strip())
        if m:
            current_bucket = m.group(1)
            continue

        m = HEADER_RE.match(line.strip())
        if m:
            current_entry = {
                "path": m.group(1),
                "bucket": current_bucket,
                "date": None,
                "ageDays": None,
                "score": 0,
                "bytes": 0,
                "lines": 0,
                "futureColdPath": None,
                "highSignals": {},
                "lowSignals": {},
                "excerpt": "",
            }
            entries.append(current_entry)
            continue

        if not current_entry:
            continue

        stripped = line.strip()

        # Handle combined lines like "- date: 2026-03-18 / age: 48 days / score: 112"
        # Multi-word key: "future cold path" (must be checked before COMBINED_RE)
        if stripped.startswith("- future cold path:"):
            val = stripped.split(":", 1)[1].strip().strip("`")
            current_entry["futureColdPath"] = val
            continue

        m = COMBINED_RE.match(stripped)
        if m:
            attr_name = m.group(1)
            val = m.group(2)
            parts = parse_combined(val)

            if attr_name == "date":
                current_entry["date"] = parts.get("date", val).split()[0]
                if "age" in parts:
                    try:
                        current_entry["ageDays"] = int(parts["age"].split()[0])
                    except ValueError:
                        pass
                if "score" in parts:
                    try:
                        current_entry["score"] = int(parts["score"])
                    except ValueError:
                        pass
            elif attr_name == "size":
                try:
                    current_entry["bytes"] = int(parts.get("size", "0").split()[0])
                except ValueError:
                    pass
                if "lines" in parts:
                    try:
                        current_entry["lines"] = int(parts["lines"])
                    except ValueError:
                        pass
            elif attr_name == "future cold path":
                current_entry["futureColdPath"] = val.strip("`")
            continue

        m = re.match(r"^- (high|low) signals:\s*`(.+?)`$", stripped)
        if m:
            try:
                import json
                signals = json.loads(m.group(2))
            except Exception:
                signals = {}
            if m.group(1) == "high":
                current_entry["highSignals"] = signals
            else:
                current_entry["lowSignals"] = signals
            continue

        m = re.match(r"^- excerpt:\s*(.+)$", stripped)
        if m:
            current_entry["excerpt"] = m.group(1).strip()
            continue

    return entries


def generate_summary(entry: dict, workspace: Path) -> str:
    """Generate a compressed summary for a retain-summary file."""
    source_path = workspace / entry["path"]
    text = ""
    if source_path.exists():
        text = source_path.read_text(encoding="utf-8", errors="replace")

    today = dt.datetime.now().strftime("%Y-%m-%d")
    cold_path = entry.get("futureColdPath", f"memory-archive/archive/{Path(entry['path']).name}")
    stem = Path(entry["path"]).stem

    lines = [
        f"# {stem} — compressed",
        f"**Source**: `{cold_path}`  ",
        f"**Compressed**: {today}  ",
        f"**Age**: {entry.get('ageDays', '?')} days | **Score**: {entry.get('score', '?')}",
        "",
    ]

    # Extract sections by ## headers
    sections: list[tuple[str, str]] = []
    current_section = ("", "")
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            if current_section[1].strip():
                sections.append(current_section)
            current_section = (line[3:].strip(), "")
        elif current_section[0]:
            current_section = (current_section[0], current_section[1] + raw_line + "\n")
    if current_section[1].strip():
        sections.append(current_section)

    # Pull key sections: failures, decisions, runbooks
    failure_keywords = ["FAILURE", "CORRECTION", "失误", "复盘", "失败", "教训", "修复", "根因", "bug", "Bug", "错误"]
    decision_keywords = ["Decision", "决定", "确认", "选择", "方案", "架构"]

    failure_lines: list[str] = []
    decision_lines: list[str] = []

    for sec_title, sec_body in sections:
        title_lower = sec_title.lower()
        is_failure = any(kw.lower() in title_lower for kw in failure_keywords)
        is_decision = any(kw.lower() in title_lower for kw in decision_keywords)

        if is_failure:
            # Extract bullet points from failure sections
            for bline in sec_body.splitlines():
                bline = bline.strip()
                if bline.startswith("- ") and len(bline) > 3:
                    clean = bline[2:].strip()
                    if len(clean) > 10:
                        failure_lines.append(clean)
        elif is_decision:
            for bline in sec_body.splitlines():
                bline = bline.strip()
                if bline.startswith("- ") and len(bline) > 3:
                    clean = bline[2:].strip()
                    if len(clean) > 10:
                        decision_lines.append(clean)

    # Also scan for inline patterns if no section matches
    if not failure_lines:
        for pat in [r"❌\s*FAILURE[^\n]*", r"🔧\s*CORRECTION[^\n]*"]:
            for m in re.findall(pat, text):
                clean = re.sub(r"^[❌🔧]\s*(?:FAILURE|CORRECTION)[:\s]*", "", m).strip()
                if clean:
                    failure_lines.append(clean)

    if failure_lines:
        lines.append("## Failures / Corrections")
        for fl in failure_lines[:6]:
            lines.append(f"- {fl[:200]}")
        lines.append("")

    if decision_lines:
        lines.append("## Key Decisions")
        for dl in decision_lines[:6]:
            lines.append(f"- {dl[:200]}")
        lines.append("")

    # Fallback: use cleaned excerpt if no structured content found
    if not failure_lines and not decision_lines:
        excerpt = entry.get("excerpt", "")
        if excerpt:
            # Clean excerpt: remove markdown headers, collapse whitespace
            clean = re.sub(r"^#+\s*", "", excerpt)
            clean = re.sub(r"\s+", " ", clean).strip()
            lines.append("## Summary")
            lines.append(clean[:500])
            lines.append("")

    lines.append(f"---\n*BMA compressed residue — full source in cold archive.*")
    return "\n".join(lines)


def scan_for_references(workspace: Path, old_path: str, new_path: str,
                        dry_run: bool = True) -> list[tuple[str, str, str]]:
    """Scan active memory files for references to old_path, return (file, old, new) tuples."""
    refs_found = []
    candidate_files = []

    for d in SCAN_DIRS:
        scan_dir = workspace / d
        if scan_dir.exists():
            candidate_files.extend(scan_dir.rglob("*.md"))

    for f in SCAN_FILES:
        fp = workspace / f
        if fp.exists():
            candidate_files.append(fp)

    # Also scan today's daily log
    today = dt.datetime.now().strftime("%Y-%m-%d")
    daily = workspace / "memory" / f"{today}.md"
    if daily.exists():
        candidate_files.append(daily)

    old_base = Path(old_path).name
    old_rel = old_path
    if old_rel.startswith("memory/"):
        old_rel_short = old_rel[len("memory/"):]
    else:
        old_rel_short = old_rel

    for cf in candidate_files:
        try:
            content = cf.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        # Check for references: full path, relative path, or just filename
        found = False
        if old_path in content or old_rel_short in content:
            found = True

        if found:
            refs_found.append((str(cf.relative_to(workspace)), old_path, new_path))

    return refs_found


def rewrite_references(workspace: Path, refs: list[tuple[str, str, str]], dry_run: bool = True):
    """Rewrite references in active memory files."""
    for file_path, old_path, new_path in refs:
        full_path = workspace / file_path
        if dry_run:
            print(f"   [DRY RUN] Would rewrite: {file_path}: {old_path} → {new_path}")
            continue

        try:
            content = full_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            print(f"   ⚠️  Could not read: {file_path}")
            continue

        # Only replace if old_path actually appears
        if old_path in content:
            new_content = content.replace(old_path, new_path)
            if new_content != content:
                full_path.write_text(new_content, encoding="utf-8")
                print(f"   ✅ Rewrote: {file_path} ({old_path} → {new_path})")


def main():
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    report_path = Path(args.audit_report).expanduser()

    if not report_path.exists():
        raise SystemExit(f"Audit report not found: {report_path}")

    report_text = report_path.read_text(encoding="utf-8", errors="replace")
    entries = parse_audit_report(report_text)

    # Filter by requested buckets
    active_buckets = set(args.buckets)
    entries = [e for e in entries if e.get("bucket") in active_buckets and e.get("path")]

    if not entries:
        print("No entries found in requested buckets.")
        return 0

    mode = "EXECUTE" if args.execute else "DRY RUN"
    print(f"🔬 BMA Phase 2 — {mode}")
    print(f"   Report: {report_path}")
    print(f"   Buckets: {', '.join(sorted(active_buckets))}")
    print(f"   Entries: {len(entries)}")
    print()

    compressed_dir = workspace / "memory" / "archive" / "_compressed"
    cold_dir = workspace / "memory-archive" / "archive"
    total_compressed = 0
    total_migrated = 0
    total_refs_rewritten = 0

    for entry in entries:
        source_path = workspace / entry["path"]
        bucket = entry["bucket"]
        filename = Path(entry["path"]).name

        print(f"📄 {entry['path']} [{bucket}]")

        if bucket == "retain-summary":
            # 1. Generate compressed summary
            summary = generate_summary(entry, workspace)
            compressed_file = compressed_dir / f"{Path(filename).stem}.compressed.md"

            if args.execute:
                compressed_dir.mkdir(parents=True, exist_ok=True)
                compressed_file.write_text(summary, encoding="utf-8")
                print(f"   ✅ Compressed → {compressed_file.relative_to(workspace)}")
            else:
                print(f"   [DRY RUN] Would compress → {compressed_file.relative_to(workspace)}")
            total_compressed += 1

            # 2. Move source to cold archive
            cold_dest = workspace / entry.get("futureColdPath", f"memory-archive/archive/{filename}")
            if source_path.exists():
                if args.execute:
                    cold_dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source_path), str(cold_dest))
                    print(f"   ✅ Migrated → {cold_dest.relative_to(workspace)}")
                else:
                    print(f"   [DRY RUN] Would migrate → {cold_dest.relative_to(workspace)}")
                total_migrated += 1
            else:
                print(f"   ⏭️  Source already moved")

            # 3. Rewrite references
            refs = scan_for_references(workspace, entry["path"],
                                       str(compressed_file.relative_to(workspace)),
                                       dry_run=not args.execute)
            if refs:
                rewrite_references(workspace, refs, dry_run=not args.execute)
            total_refs_rewritten += len(refs)

        elif bucket == "cold-archive-only":
            # Move directly to cold archive, no summary
            cold_dest = workspace / entry.get("futureColdPath", f"memory-archive/archive/{filename}")
            if source_path.exists():
                if args.execute:
                    cold_dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source_path), str(cold_dest))
                    print(f"   ✅ Migrated → {cold_dest.relative_to(workspace)}")
                else:
                    print(f"   [DRY RUN] Would migrate → {cold_dest.relative_to(workspace)}")
                total_migrated += 1
            else:
                print(f"   ⏭️  Source already moved")

            # Rewrite references to cold path
            refs = scan_for_references(workspace, entry["path"],
                                       str(cold_dest.relative_to(workspace)),
                                       dry_run=not args.execute)
            if refs:
                rewrite_references(workspace, refs, dry_run=not args.execute)
            total_refs_rewritten += len(refs)

        elif bucket == "review-manual":
            # Conservative: move to cold archive without compression
            cold_dest = workspace / entry.get("futureColdPath", f"memory-archive/archive/{filename}")
            if source_path.exists():
                if args.execute:
                    cold_dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source_path), str(cold_dest))
                    print(f"   ✅ Migrated (review-manual) → {cold_dest.relative_to(workspace)}")
                else:
                    print(f"   [DRY RUN] Would migrate (review-manual) → {cold_dest.relative_to(workspace)}")
                total_migrated += 1
            else:
                print(f"   ⏭️  Source already moved")

            refs = scan_for_references(workspace, entry["path"],
                                       str(cold_dest.relative_to(workspace)),
                                       dry_run=not args.execute)
            if refs:
                rewrite_references(workspace, refs, dry_run=not args.execute)
            total_refs_rewritten += len(refs)

        print()

    print("━" * 60)
    print(f"📊 Summary:")
    print(f"   Compressed: {total_compressed}")
    print(f"   Migrated:   {total_migrated}")
    print(f"   Refs fixed: {total_refs_rewritten}")
    if not args.execute:
        print()
        print("   Run with --execute to apply changes.")

    # Phase 1 reports are process artifacts — suggest cleanup
    if args.execute and total_migrated > 0:
        print()
        print(f"💡 Phase 1 audit report ({report_path.name}) is a process artifact.")
        print(f"   Delete it when ready: rm {report_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
