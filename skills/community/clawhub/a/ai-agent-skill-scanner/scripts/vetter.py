#!/usr/bin/env python3
"""AI Agent Skill Scanner v2.1 — Security scanner for AI agent skills.

Loads detection signatures from signatures.json and performs fast
line-by-line text matching. Skips node_modules, __pycache__, and
other noise directories.
"""

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

# Directories and file types to skip (reduces false positives)
SKIP_DIRS = {"node_modules", "__pycache__", ".git", ".venv", ".env", "venv", "dist", "build", ".next"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".woff", ".woff2", ".ttf", ".eot",
            ".pyc", ".pyo", ".so", ".o", ".a", ".class", ".jar",
            ".mp3", ".mp4", ".avi", ".mov", ".wav",
            ".zip", ".tar", ".gz", ".bz2", ".rar", ".7z"}
SKIP_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "composer.lock"}
# Files within a skill directory that should NOT scan their own tool files
SELF_SKIP_FILES = {"signatures.json", "vetter.py", "safe-install.sh"}


@dataclass
class Finding:
    severity: str
    rule_id: str
    file: str
    line: int
    message: str
    matched: str

    def to_dict(self) -> dict:
        return {
            "severity": self.severity,
            "rule_id": self.rule_id,
            "file": self.file,
            "line": self.line,
            "message": self.message,
            "matched_fragment": self.matched,
        }


@dataclass
class Report:
    findings: List[Finding] = field(default_factory=list)
    scanned_files: int = 0
    skipped_files: int = 0
    duration_ms: float = 0.0

    def to_dict(self) -> dict:
        return {
            "summary": {
                "scanned_files": self.scanned_files,
                "skipped_files": self.skipped_files,
                "duration_ms": round(self.duration_ms, 2),
                "total_findings": len(self.findings),
            },
            "findings": [f.to_dict() for f in self.findings],
        }


def load_signatures(path: Path) -> List[Dict]:
    data = json.load(open(path))
    return data["signatures"]


def should_skip(path: Path) -> bool:
    """Return True if file should not be scanned."""
    # Skip by file extension
    if path.suffix.lower() in SKIP_EXT:
        return True
    # Skip known noise files
    if path.name in SKIP_FILES:
        return True
    # Check parent directories for skip dirs
    for part in path.parts:
        if part in SKIP_DIRS:
            return True
    # Skip self-scan of scanner's own files
    if path.name in SELF_SKIP_FILES and "skill-vetter-plus" in path.parts:
        return True
    return False


def scan_file(path: Path, signatures: List[Dict]) -> List[Finding]:
    findings: List[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    lines = text.splitlines()
    for lineno, line in enumerate(lines, start=1):
        line_lower = line.lower().strip()

        for sig in signatures:
            # Special handling for pipe-to-shell: only flag if curl/wget X | sh/bash pattern
            if sig["id"] == "pipe-to-shell":
                if "curl" in line or "wget" in line:
                    stripped = line.strip()
                    # Check for pipe to shell pattern
                    if "| sh" in stripped or "| bash" in stripped or "| /bin/sh" in stripped or "| /bin/bash" in stripped:
                        pass  # This is a real finding
                    else:
                        continue  # curl/wget without pipe to shell is benign
                else:
                    continue

            for frag in sig["fragments"]:
                frag_lower = frag.lower()
                if frag in line or (frag_lower in line_lower and len(frag) > 2):
                    findings.append(
                        Finding(
                            severity=sig["severity"],
                            rule_id=sig["id"],
                            file=str(path),
                            line=lineno,
                            message=sig["message"],
                            matched=frag,
                        )
                    )
                    break
    return findings


def scan_skill(skill_dir: Path, signatures: List[Dict]) -> Report:
    start = time.monotonic()
    report = Report()

    for root, dirs, files in os.walk(skill_dir):
        # Prune skip dirs in-place so os.walk doesn't descend into them
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            path = Path(root) / fname
            if should_skip(path):
                report.skipped_files += 1
                continue
            report.scanned_files += 1
            findings = scan_file(path, signatures)
            report.findings.extend(findings)

    report.duration_ms = (time.monotonic() - start) * 1000
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="AI Agent Skill Scanner — Security scanner for agent skills")
    parser.add_argument("path", type=Path, help="Skill directory to scan")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    parser.add_argument("--signatures", type=Path, default=None, help="Custom signatures.json path")
    parser.add_argument("--verbose", action="store_true", help="Include skipped file count")
    args = parser.parse_args()

    sig_path = args.signatures or Path(__file__).parent.parent / "signatures.json"
    if not sig_path.exists():
        print(f"Error: signatures not found at {sig_path}", file=sys.stderr)
        return 2
    signatures = load_signatures(sig_path)

    report = scan_skill(args.path, signatures)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(f"Scanned {report.scanned_files} files in {report.duration_ms:.0f}ms", end="")
        if args.verbose:
            print(f" (skipped {report.skipped_files})", end="")
        print()
        if report.findings:
            print(f"Found {len(report.findings)} issue(s):")
            for f in report.findings:
                print(f"  [{f.severity.upper()}] {f.rule_id} at {f.file}:{f.line}")
                print(f"    → {f.message} (matched: '{f.matched}')")
        else:
            print("No issues found.")
    return 0 if len(report.findings) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())