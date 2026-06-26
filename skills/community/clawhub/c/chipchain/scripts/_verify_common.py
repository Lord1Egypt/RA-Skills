"""
Shared utilities for chipchain verification scripts.

Provides common regex patterns, file extraction, report generation,
and runtime dependency management.
"""

import re
import os
import sys
import json
from pathlib import Path
from datetime import datetime


# ── Regex patterns ──────────────────────────────────────────────

# CAS Registry Number: digits-digits-digit (e.g., 7664-39-3)
CAS_PATTERN = re.compile(r'\b(\d{2,7}-\d{2}-\d)\b')



# ── Project structure ───────────────────────────────────────────

def find_skill_dir() -> Path:
    """Return the project root (parent of scripts/)."""
    return Path(__file__).resolve().parent.parent


# ── Extraction ──────────────────────────────────────────────────

def extract_from_markdown(filepath: str | Path, pattern: re.Pattern) -> list[dict]:
    """Extract all regex matches from a markdown file.

    Returns list of dicts with keys: value, file, line, context.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        return []

    results = []
    seen = set()
    lines = filepath.read_text(encoding="utf-8").split("\n")

    for i, line in enumerate(lines):
        # Skip markdown headers and blockquotes
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith(">"):
            continue

        for match in pattern.finditer(line):
            value = match.group(1) if match.lastindex else match.group(0)
            if value in seen:
                continue
            seen.add(value)
            results.append({
                "value": value,
                "file": filepath.name,
                "line": i + 1,
                "context": stripped[:120],
            })

    return results


# ── Report output ───────────────────────────────────────────────

def write_report(path: str | Path, title: str, sections: list[dict]) -> None:
    """Write a markdown verification report.

    Each section is a dict with keys: heading, content (str).
    """
    path = Path(path)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"**Generated:** {now}\n\n")
        for section in sections:
            f.write(f"## {section['heading']}\n\n")
            f.write(section["content"])
            f.write("\n\n")


def write_json(path: str | Path, results: list | dict) -> None:
    """Write verification results as JSON."""
    path = Path(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


# ── Dependency management ───────────────────────────────────────

def ensure_package(name: str, pip_name: str | None = None) -> None:
    """Import a package, auto-installing via pip if missing.

    Args:
        name: Python import name (e.g., 'pykrx')
        pip_name: pip package name if different from import name
    """
    try:
        __import__(name)
    except ImportError:
        import subprocess
        pip_name = pip_name or name
        print(f"Installing {pip_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
        __import__(name)
