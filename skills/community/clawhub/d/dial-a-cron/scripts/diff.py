#!/usr/bin/env python3
"""
Dial-a-Cron — Diff Engine (Phase 2)
Detects what changed since the last run.
Supports: file hash, HTTP endpoint, command output.

Usage:
    from diff import DiffEngine
    engine = DiffEngine("helga-sync-rook", prev_hash="abc123")
    result = engine.run([
        {"type": "file", "path": "memory/2026-04-01.md", "label": "Daily log"},
        {"type": "http", "url": "http://192.168.1.225:8200/collections", "label": "Helga2"},
        {"type": "command", "cmd": "git log --oneline -3", "label": "Recent commits"},
    ])
    if result.has_changes:
        print(result.summary)
    else:
        print("No changes — skipping LLM")
"""

import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from urllib.request import urlopen
from urllib.error import URLError


@dataclass
class DiffResult:
    has_changes: bool
    changes: list[dict] = field(default_factory=list)
    new_hash: str = ""
    summary: str = ""

    def to_prompt_block(self) -> str:
        """Format changes for injection into LLM prompt."""
        if not self.has_changes:
            return "No changes detected since last run."
        lines = ["## Changes Since Last Run\n"]
        for c in self.changes:
            label = c.get("label", c.get("type", "unknown"))
            change = c.get("change", "changed")
            lines.append(f"- **{label}:** {change}")
        return "\n".join(lines)


def _hash(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()[:12]


def _diff_file(spec: dict, prev_hashes: dict) -> Optional[dict]:
    """Diff a file by hash."""
    path = Path(spec["path"])
    label = spec.get("label", str(path))
    if not path.exists():
        return {"type": "file", "label": label, "change": "FILE MISSING"}
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        h = _hash(content)
        prev = prev_hashes.get(str(path))
        if h != prev:
            size_kb = len(content) / 1024
            return {"type": "file", "label": label, "change": f"modified ({size_kb:.1f}KB)", "hash": h, "path": str(path)}
        return None
    except Exception as e:
        return {"type": "file", "label": label, "change": f"read error: {e}"}


def _diff_http(spec: dict, prev_hashes: dict) -> Optional[dict]:
    """Diff an HTTP endpoint by response hash."""
    url = spec["url"]
    label = spec.get("label", url)
    jq_path = spec.get("jq")  # dot-notation path for JSON extraction
    try:
        with urlopen(url, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="replace")
        # Optional JSON extraction
        if jq_path:
            try:
                data = json.loads(body)
                # Simple dot-notation traversal
                val = data
                for key in jq_path.strip(".").split("."):
                    if isinstance(val, list):
                        val = [item.get(key) if isinstance(item, dict) else item for item in val]
                    elif isinstance(val, dict):
                        val = val.get(key)
                    else:
                        break
                body = json.dumps(val)
            except Exception:
                pass
        h = _hash(body)
        prev = prev_hashes.get(url)
        if h != prev:
            return {"type": "http", "label": label, "change": f"response changed", "hash": h, "url": url, "snippet": body[:200]}
        return None
    except URLError as e:
        return {"type": "http", "label": label, "change": f"unreachable: {e}"}
    except Exception as e:
        return {"type": "http", "label": label, "change": f"error: {e}"}


def _diff_command(spec: dict, prev_hashes: dict) -> Optional[dict]:
    """Diff command stdout by hash."""
    cmd = spec["cmd"]
    label = spec.get("label", cmd[:40])
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=15
        )
        output = result.stdout.strip()
        h = _hash(output)
        prev = prev_hashes.get(cmd)
        if h != prev:
            return {"type": "command", "label": label, "change": f"output changed", "hash": h, "cmd": cmd, "snippet": output[:200]}
        return None
    except subprocess.TimeoutExpired:
        return {"type": "command", "label": label, "change": "command timed out"}
    except Exception as e:
        return {"type": "command", "label": label, "change": f"error: {e}"}


class DiffEngine:
    def __init__(self, job_id: str, prev_hashes: dict = None):
        self.job_id = job_id
        self.prev_hashes = prev_hashes or {}

    def run(self, specs: list[dict]) -> DiffResult:
        """Run all diffs and return result."""
        changes = []
        new_hashes = {}

        for spec in specs:
            diff_type = spec.get("type", "file")
            result = None

            if diff_type == "file":
                result = _diff_file(spec, self.prev_hashes)
                if result and "hash" in result:
                    new_hashes[spec["path"]] = result["hash"]
                elif not result:
                    # Unchanged — preserve hash
                    key = spec["path"]
                    if key in self.prev_hashes:
                        new_hashes[key] = self.prev_hashes[key]

            elif diff_type == "http":
                result = _diff_http(spec, self.prev_hashes)
                if result and "hash" in result:
                    new_hashes[spec["url"]] = result["hash"]
                elif not result:
                    key = spec["url"]
                    if key in self.prev_hashes:
                        new_hashes[key] = self.prev_hashes[key]

            elif diff_type == "command":
                result = _diff_command(spec, self.prev_hashes)
                if result and "hash" in result:
                    new_hashes[spec["cmd"]] = result["hash"]
                elif not result:
                    key = spec["cmd"]
                    if key in self.prev_hashes:
                        new_hashes[key] = self.prev_hashes[key]

            if result:
                changes.append(result)

        combined_hash = _hash(json.dumps(new_hashes, sort_keys=True))
        has_changes = len(changes) > 0
        summary = f"{len(changes)} change(s)" if has_changes else "no changes"

        return DiffResult(
            has_changes=has_changes,
            changes=changes,
            new_hash=combined_hash,
            summary=summary,
        )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test diff engine")
    parser.add_argument("--file", help="Test file diff")
    parser.add_argument("--url", help="Test HTTP diff")
    parser.add_argument("--cmd", help="Test command diff")
    args = parser.parse_args()

    specs = []
    if args.file:
        specs.append({"type": "file", "path": args.file, "label": "Test file"})
    if args.url:
        specs.append({"type": "http", "url": args.url, "label": "Test URL"})
    if args.cmd:
        specs.append({"type": "command", "cmd": args.cmd, "label": "Test cmd"})

    if not specs:
        print("Usage: python diff.py --file path/to/file --url http://... --cmd 'command'")
        sys.exit(1)

    engine = DiffEngine("test")
    result = engine.run(specs)
    print(f"Has changes: {result.has_changes}")
    print(f"Summary: {result.summary}")
    print(result.to_prompt_block())
