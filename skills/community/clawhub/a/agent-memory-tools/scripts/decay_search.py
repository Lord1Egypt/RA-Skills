#!/usr/bin/env python3
"""
decay_search — Temporal decay search over QMD-indexed markdown.
Recent facts score higher, permanent knowledge is protected.

Usage:
    decay_search "query" [--limit 10] [--half-life 14] [--debug]
"""
from __future__ import annotations
import os, sys
# Cross-platform PATH setup
if sys.platform == "darwin":
    os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("HOME", "") + "/.bun/bin:" + os.environ.get("PATH", "")

import argparse, json, math, re, subprocess, time
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from llm_client import load_config


CATEGORY_MAP = {
    "memory/": "episodic",
    "projects/": "project",
    "etudes/": "permanent",
    "bugs/": "permanent",
    "agents/": "permanent",
    "infra/": "permanent",
}


def classify_file(filepath: str) -> str:
    """Classify file into memory category."""
    for prefix, cat in CATEGORY_MAP.items():
        if filepath.startswith(prefix):
            return cat
    if any(k in filepath.lower() for k in ["error", "bug", "lesson", "rule"]):
        return "permanent"
    return "unknown"


def extract_date(filepath: str, text: str) -> datetime | None:
    """Extract date from filepath or content."""
    # From filename: memory/2026-03-23.md
    m = re.search(r'(\d{4}-\d{2}-\d{2})', filepath)
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y-%m-%d")
        except ValueError:
            pass
    
    # From content: dates like 23/03/2026 or 2026-03-23
    for pattern in [r'(\d{2}/\d{2}/\d{4})', r'(\d{4}-\d{2}-\d{2})']:
        m = re.search(pattern, text)
        if m:
            try:
                fmt = "%d/%m/%Y" if "/" in m.group(1) else "%Y-%m-%d"
                return datetime.strptime(m.group(1), fmt)
            except ValueError:
                continue
    return None


def decay_score(base_score: float, file_date: datetime | None, category: str,
                half_life_days: float = 14, protected: list[str] | None = None) -> float:
    """Apply temporal decay to a search score."""
    if protected is None:
        protected = ["permanent"]
    
    # No decay for protected categories
    if category in protected:
        return base_score
    
    if file_date is None:
        return base_score * 0.5  # Unknown date penalty
    
    days_old = (datetime.now() - file_date).days
    
    if days_old < 1:
        # Boost very recent (< 24h)
        return base_score * 1.2
    
    # Exponential decay
    decay = math.exp(-0.693 * days_old / half_life_days)
    return base_score * decay


def qmd_search(query: str, limit: int = 20) -> list[dict]:
    """Search via QMD CLI and parse results."""
    try:
        result = subprocess.run(
            ["qmd", "search", query, "--limit", str(limit)],
            capture_output=True, text=True, timeout=30
        )
        results = []
        current = None
        for line in result.stdout.split("\n"):
            if line.startswith("qmd://"):
                if current:
                    results.append(current)
                # Parse: qmd://workspace/path:line #hash
                path_part = line.split(" ")[0]
                path = path_part.replace("qmd://workspace/", "")
                parts = path.rsplit(":", 1)
                filepath = parts[0]
                line_num = int(parts[1]) if len(parts) > 1 else 1
                current = {"filepath": filepath, "line": line_num, "text": "", "raw_line": line}
            elif line.startswith("Score:") and current:
                m = re.search(r'(\d+)%', line)
                if m:
                    current["score"] = int(m.group(1)) / 100.0
            elif line.startswith("Title:") and current:
                current["title"] = line.replace("Title:", "").strip()
            elif current and line.strip().startswith("@@"):
                pass  # Skip diff markers
            elif current and line.strip():
                current["text"] += line.strip() + " "
        
        if current:
            results.append(current)
        return results
    except Exception as e:
        print(f"QMD error: {e}", file=sys.stderr)
        return []


def search_with_decay(query: str, limit: int = 10, half_life: float = 14,
                      cfg: dict | None = None, debug: bool = False) -> list[dict]:
    """Search with temporal decay scoring."""
    if cfg is None:
        cfg = load_config()
    
    protected = cfg["search"].get("protectedCategories", ["knowledge", "error"])
    # Map to file categories
    protected_cats = ["permanent"]  # savoir/erreur files are classified as permanent
    
    raw = qmd_search(query, limit=limit * 2)  # Fetch more, decay will filter
    
    for r in raw:
        category = classify_file(r["filepath"])
        file_date = extract_date(r["filepath"], r.get("text", ""))
        base_score = r.get("score", 0.5)
        
        r["category"] = category
        r["file_date"] = file_date.isoformat() if file_date else None
        r["base_score"] = base_score
        r["decay_score"] = decay_score(base_score, file_date, category, half_life, protected_cats)
    
    # Sort by decay score
    raw.sort(key=lambda r: r["decay_score"], reverse=True)
    
    return raw[:limit]


def main():
    parser = argparse.ArgumentParser(description="Temporal decay search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--half-life", type=float, default=14)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--preset", help="Config preset")
    args = parser.parse_args()
    
    cfg = load_config(preset=args.preset)
    results = search_with_decay(args.query, limit=args.limit, half_life=args.half_life, cfg=cfg, debug=args.debug)
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            cat = r.get("category", "?")[:9].ljust(9)
            score = r.get("decay_score", 0)
            filepath = r.get("filepath", "?")
            text = r.get("text", "")[:120].strip()
            print(f"{score:.3f} [{cat}] | {filepath} | {text}")


if __name__ == "__main__":
    main()
