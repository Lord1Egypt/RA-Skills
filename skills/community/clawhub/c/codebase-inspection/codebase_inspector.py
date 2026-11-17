#!/usr/bin/env python3
"""codebase_inspector v2.0 — Advanced codebase analysis with HTML reports, git-aware diffs, trend tracking, and CI-ready output.

Usage:
  python codebase_inspector.py <dir>                    # default text report
  python codebase_inspector.py <dir> --json              # JSON output
  python codebase_inspector.py <dir> --html report.html  # HTML visual report
  python codebase_inspector.py <dir> --badge             # SVG badge URL
  python codebase_inspector.py <dir> --snapshot          # save trend snapshot
  python codebase_inspector.py <dir> --diff <dir2>       # compare two codebases
  python codebase_inspector.py <dir> --trend             # show trend from snapshots
  python codebase_inspector.py <dir> --exclude ".git,node_modules"
  python codebase_inspector.py self-test                 # run built-in tests
"""
import json
import os
import sys
import csv
import io
import hashlib
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

NAME = "codebase-inspection"
VERSION = "2.0.0"

# ── language map ─────────────────────────────────────────────────────────

EXT_LANG = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript",
    ".jsx": "JavaScript", ".go": "Go", ".rs": "Rust", ".java": "Java",
    ".rb": "Ruby", ".php": "PHP", ".c": "C", ".h": "C", ".cpp": "C++",
    ".hpp": "C++", ".cs": "C#", ".swift": "Swift", ".kt": "Kotlin",
    ".sh": "Shell", ".bash": "Shell", ".zsh": "Shell", ".ps1": "PowerShell",
    ".md": "Markdown", ".mdx": "Markdown",
    ".json": "JSON", ".yaml": "YAML", ".yml": "YAML", ".toml": "TOML",
    ".html": "HTML", ".css": "CSS", ".scss": "SCSS", ".less": "Less",
    ".sql": "SQL", ".r": "R", ".m": "MATLAB",
    ".lua": "Lua", ".pl": "Perl", ".pm": "Perl",
    ".tex": "LaTeX", ".xml": "XML", ".svg": "SVG",
    ".dockerfile": "Docker", ".tf": "Terraform", ".hcl": "Terraform",
}

COMMENT_PREFIXES = {"#", "//", "/*", "*", "--", ";", "%", "\"", "<!--", "///", "//!"}

IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "dist",
    "build", ".next", "target", ".cache", ".idea", ".vscode",
    ".DS_Store", "coverage", ".nyc_output", "bundle", ".tox", ".eggs",
    "egg-info", "site-packages", ".pytest_cache", ".mypy_cache",
    ".serverless", ".terraform", ".svelte-kit", ".output",
}

SNAPSHOT_DIR = ".codebase-snapshots"  # stored in analyzed dir


# ── analysis engine ──────────────────────────────────────────────────────

def analyze(path, exclude_dirs=None):
    """Walk directory and return structured analysis."""
    stats = defaultdict(lambda: {"files": 0, "lines": 0, "blank_lines": 0,
                                  "comment_lines": 0, "code_lines": 0})
    file_list = []
    ignore = IGNORE_DIRS | (set(exclude_dirs) if exclude_dirs else set())
    lang_ext_map = defaultdict(set)

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ignore and not d.startswith(".codebase-")]
        for fn in files:
            if fn.startswith(".") or fn in {".DS_Store", "package-lock.json",
                                             "yarn.lock", "Gemfile.lock", "poetry.lock"}:
                continue
            fp = Path(root, fn)
            ext = fp.suffix.lower()
            lang = EXT_LANG.get(ext, "Other")
            if ext in (".svg", ".ico", ".png", ".jpg", ".gif", ".woff", ".woff2", ".eot", ".ttf"):
                continue

            try:
                text = fp.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            lines = text.splitlines()
            nlines = len(lines)
            blanks = sum(1 for l in lines if l.strip() == "")
            comments = sum(1 for l in lines
                          if l.strip() and l.strip().startswith(tuple(COMMENT_PREFIXES)))
            code = nlines - blanks - comments

            stats[lang]["files"] += 1
            stats[lang]["lines"] += nlines
            stats[lang]["blank_lines"] += blanks
            stats[lang]["comment_lines"] += comments
            stats[lang]["code_lines"] += code
            lang_ext_map[lang].add(ext)

            try:
                rel = str(fp.relative_to(path))
            except ValueError:
                rel = str(fp)
            file_list.append({
                "file": rel,
                "lang": lang,
                "lines": nlines,
                "blank": blanks,
                "comments": comments,
                "code": code,
            })

    total_files = sum(s["files"] for s in stats.values())
    total_lines = sum(s["lines"] for s in stats.values())
    total_code = sum(s["code_lines"] for s in stats.values())
    total_blank = sum(s["blank_lines"] for s in stats.values())
    total_comments = sum(s["comment_lines"] for s in stats.values())

    langs = dict(stats)
    return {
        "tool": NAME, "version": VERSION,
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
        "directory": os.path.abspath(path),
        "total_files": total_files,
        "total_lines": total_lines,
        "total_code": total_code,
        "total_blank": total_blank,
        "total_comments": total_comments,
        "avg_lines_per_file": round(total_lines / total_files, 1) if total_files else 0,
        "comment_density": round(total_comments / total_lines * 100, 1) if total_lines else 0,
        "stats": langs,
        "largest_files": sorted(file_list, key=lambda f: f["lines"], reverse=True)[:20],
        "file_count": len(file_list),
    }


# ── output formatters ────────────────────────────────────────────────────

def print_text(result):
    """Human-readable text report."""
    print(f"Codebase: {result['directory']}")
    print(f"Analyzed: {result['analyzed_at']}")
    print()
    items = sorted(result["stats"].items(), key=lambda x: x[1]["lines"], reverse=True)
    hdr = ("Language", "Files", "Lines", "Blank", "Comments", "Code")
    print(f"{hdr[0]:<20} {hdr[1]:>6} {hdr[2]:>8} {hdr[3]:>6} {hdr[4]:>8} {hdr[5]:>8}")
    print("-" * 66)
    for lang, s in items:
        print(f"{lang:<20} {s['files']:>6} {s['lines']:>8} {s['blank_lines']:>6} "
              f"{s['comment_lines']:>8} {s['code_lines']:>8}")
    print("-" * 66)
    print(f"{'TOTAL':<20} {result['total_files']:>6} {result['total_lines']:>8} "
          f"{result['total_blank']:>6} {result['total_comments']:>8} {result['total_code']:>8}")
    print()
    print(f"Avg lines/file: {result['avg_lines_per_file']}")
    print(f"Comment density: {result['comment_density']}%")
    if result.get("largest_files"):
        print(f"\nTop 10 largest files:")
        for i, f in enumerate(result["largest_files"][:10], 1):
            print(f"  {i:>2}. {f['file']} ({f['lines']} lines, {f['lang']})")


def print_html(result, out_path):
    """Generate a standalone HTML report with visual bars."""
    items = sorted(result["stats"].items(), key=lambda x: x[1]["lines"], reverse=True)
    max_lines = max((s["lines"] for _, s in items), default=1)
    rows = ""
    colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336",
              "#00BCD4", "#FF5722", "#607D8B", "#795548", "#CDDC39"]
    for i, (lang, s) in enumerate(items):
        pct = s["lines"] / max_lines * 100 if max_lines else 0
        c = colors[i % len(colors)]
        rows += (
            f"<tr><td><strong>{lang}</strong></td>"
            f"<td>{s['files']}</td><td>{s['lines']}</td>"
            f"<td>{s['blank_lines']}</td><td>{s['comment_lines']}</td>"
            f"<td>{s['code_lines']}</td>"
            f"<td><div style='background:{c};width:{pct:.1f}%;height:20px;"
            f"border-radius:3px;min-width:2px'></div></td></tr>\n"
        )

    top_files = ""
    for i, f in enumerate(result.get("largest_files", [])[:10], 1):
        top_files += (
            f"<tr><td>{i}</td><td>{f['file']}</td>"
            f"<td>{f['lang']}</td><td>{f['lines']}</td></tr>\n"
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Codebase Analysis — {Path(result['directory']).name}</title>
<style>
  body{{font-family:-apple-system,system-ui,sans-serif;margin:40px;background:#f8f9fa;color:#333}}
  h1{{color:#1a1a1a}} .card{{background:#fff;border-radius:8px;padding:20px;margin:20px 0;box-shadow:0 2px 4px rgba(0,0,0,.1)}}
  table{{width:100%;border-collapse:collapse}} th,td{{text-align:left;padding:8px 12px;border-bottom:1px solid #eee}}
  th{{background:#f0f0f0;font-weight:600}} .summary{{display:flex;gap:20px;flex-wrap:wrap}}
  .stat{{background:#fff;border-radius:8px;padding:15px 25px;box-shadow:0 2px 4px rgba(0,0,0,.1);text-align:center;min-width:100px}}
  .stat-value{{font-size:28px;font-weight:700;color:#1a73e8}} .stat-label{{font-size:13px;color:#666;margin-top:4px}}
  footer{{margin-top:40px;font-size:12px;color:#999}}
</style></head>
<body>
<h1>📊 Codebase Analysis: {Path(result['directory']).name}</h1>
<p>Analyzed: {result['analyzed_at']}</p>
<div class="summary">
  <div class="stat"><div class="stat-value">{result['total_files']:,}</div><div class="stat-label">Files</div></div>
  <div class="stat"><div class="stat-value">{result['total_lines']:,}</div><div class="stat-label">Lines</div></div>
  <div class="stat"><div class="stat-value">{result['avg_lines_per_file']}</div><div class="stat-label">Avg L/file</div></div>
  <div class="stat"><div class="stat-value">{result['comment_density']}%</div><div class="stat-label">Comments</div></div>
  <div class="stat"><div class="stat-value">{result['total_code']:,}</div><div class="stat-label">Code Lines</div></div>
  <div class="stat"><div class="stat-value">{result['total_blank']:,}</div><div class="stat-label">Blank</div></div>
</div>

<div class="card"><h2>Language Breakdown</h2>
<table><thead><tr><th>Language</th><th>Files</th><th>Lines</th><th>Blank</th><th>Comments</th><th>Code</th><th>Bar</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<div class="card"><h2>Top 10 Largest Files</h2>
<table><thead><tr><th>#</th><th>File</th><th>Language</th><th>Lines</th></tr></thead>
<tbody>{top_files}</tbody></table></div>

<p><em>Generated by {NAME} v{VERSION}</em>
<br><a href="https://github.com/itsPremkumar/{NAME}">GitHub</a></p>
</body></html>"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return f"HTML report: {os.path.abspath(out_path)}"


def print_svg_badge(result):
    """Generate an SVG badge URL (data URI)."""
    total = result["total_lines"]
    lang_count = len(result["stats"])
    pct = result["comment_density"]
    label = f"{total:,} lines · {lang_count} langs · {pct}% docs"
    # simple colored badge
    import urllib.parse
    badge_url = f"https://img.shields.io/badge/codebase-{urllib.parse.quote(label)}-brightgreen"
    return f"Badge: {badge_url}\nCopy into README:\n![Codebase]({badge_url})"


def print_csv(result):
    """CSV output for spreadsheet import."""
    items = sorted(result["stats"].items(), key=lambda x: x[1]["lines"], reverse=True)
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["Language", "Files", "Lines", "Blank", "Comments", "Code"])
    for lang, s in items:
        w.writerow([lang, s["files"], s["lines"], s["blank_lines"], s["comment_lines"], s["code_lines"]])
    w.writerow([])
    w.writerow(["TOTAL", result["total_files"], result["total_lines"],
                result["total_blank"], result["total_comments"], result["total_code"]])
    return out.getvalue()


# ── snapshot / trend ────────────────────────────────────────────────────

def _snapshot_path(base_dir):
    snap_dir = Path(base_dir) / SNAPSHOT_DIR
    snap_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return snap_dir / f"snapshot-{ts}.json"


def save_snapshot(result):
    """Save analysis as a trend snapshot."""
    snap = _snapshot_path(result["directory"])
    with open(snap, "w") as f:
        json.dump(result, f, indent=2)
    return f"Snapshot saved: {snap}"


def show_trend(base_dir):
    """Compare all snapshots to show trends over time."""
    snap_dir = Path(base_dir) / SNAPSHOT_DIR
    if not snap_dir.is_dir():
        return "No snapshots found. Run with --snapshot first."

    snaps = sorted(snap_dir.glob("snapshot-*.json"))
    if not snaps:
        return "No snapshots found."

    rows = []
    for s in snaps:
        with open(s) as f:
            data = json.load(f)
        rows.append({
            "ts": data.get("analyzed_at", s.stem.replace("snapshot-", "")),
            "files": data["total_files"],
            "lines": data["total_lines"],
            "code": data["total_code"],
            "density": data["comment_density"],
        })

    out = f"Trend analysis for: {base_dir}\n"
    out += f"{'Snapshot':<25} {'Files':>7} {'Lines':>9} {'Code':>9} {'Cmnt%':>6}\n"
    out += "-" * 56 + "\n"
    for r in rows:
        ts_short = r["ts"][:19] if len(r["ts"]) > 19 else r["ts"]
        out += f"{ts_short:<25} {r['files']:>7} {r['lines']:>9} {r['code']:>9} {r['density']:>6}\n"

    if len(rows) >= 2:
        a, b = rows[-1], rows[0]
        d_files = a["files"] - b["files"]
        d_lines = a["lines"] - b["lines"]
        out += f"\nSince first snapshot: "
        out += f"{'+' if d_files >= 0 else ''}{d_files} files, "
        out += f"{'+' if d_lines >= 0 else ''}{d_lines} lines"
    return out


def diff_codebases(dir_a, dir_b):
    """Compare two directories."""
    a = analyze(dir_a)
    b = analyze(dir_b)
    out = f"Diff: {dir_a} → {dir_b}\n"
    out += f"{'Metric':<25} {'Before':>10} {'After':>10} {'Δ':>8}\n"
    out += "-" * 53 + "\n"

    metrics = [
        ("Files", a["total_files"], b["total_files"]),
        ("Lines", a["total_lines"], b["total_lines"]),
        ("Code", a["total_code"], b["total_code"]),
        ("Blank", a["total_blank"], b["total_blank"]),
        ("Comments", a["total_comments"], b["total_comments"]),
    ]
    for label, before, after in metrics:
        delta = after - before
        out += f"{label:<25} {before:>10} {after:>10} {'+' if delta>=0 else ''}{delta:>7}\n"

    # Language-level changes
    all_langs = set(a["stats"]) | set(b["stats"])
    for lang in sorted(all_langs):
        sa = a["stats"].get(lang, {}).get("lines", 0)
        sb = b["stats"].get(lang, {}).get("lines", 0)
        if sa != sb:
            delta = sb - sa
            out += f"  {lang:<23} {sa:>10} {sb:>10} {'+' if delta>=0 else ''}{delta:>7}\n"
    return out


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    import argparse
    p = argparse.ArgumentParser(
        prog="codebase_inspector",
        description="Advanced codebase analysis with HTML reports, trend tracking, git-aware diffs",
        epilog="Free + MIT · github.com/itsPremkumar/codebase-inspection",
    )
    p.add_argument("--version", action="version", version=f"{NAME} v{VERSION}")
    p.add_argument("dir", nargs="?", default=None,
                   help="Directory to analyze (omit for help)")
    p.add_argument("--json", action="store_true", help="JSON output")
    p.add_argument("--html", metavar="FILE", help="Generate HTML report file")
    p.add_argument("--csv", action="store_true", help="CSV output")
    p.add_argument("--badge", action="store_true", help="Show shields.io badge URL")
    p.add_argument("--snapshot", action="store_true", help="Save snapshot for trend tracking")
    p.add_argument("--trend", action="store_true", help="Show trend from historical snapshots")
    p.add_argument("--diff", metavar="DIR2", help="Compare current dir against another")
    p.add_argument("--exclude", help="Extra dirs to exclude (comma-separated)")
    p.add_argument("--sort", action="store_true",
                   help="Sort output by lines (default for text mode)")

    if len(sys.argv) == 1:
        p.print_help()
        return 0

    # Handle self-test early
    if sys.argv[1] == "self-test":
        return self_test()

    args = p.parse_args()

    # Trend-only mode (no dir needed)
    if args.trend and args.dir:
        print(show_trend(args.dir))
        return 0

    # Diff-only mode
    if args.diff and args.dir:
        print(diff_codebases(args.dir, args.diff))
        return 0

    if not args.dir:
        p.print_help()
        return 1
    if not os.path.isdir(args.dir):
        print(f"Error: '{args.dir}' is not a directory", file=sys.stderr)
        return 1

    exclude = [x.strip() for x in args.exclude.split(",")] if args.exclude else None
    result = analyze(os.path.abspath(args.dir), exclude_dirs=exclude)

    if args.json:
        print(json.dumps(result, indent=2))
    elif args.html:
        print(print_html(result, args.html))
    elif args.csv:
        print(print_csv(result))
    elif args.badge:
        print(print_svg_badge(result))
    else:
        print_text(result)

    if args.snapshot:
        print("\n" + save_snapshot(result))

    return 0


# ── self-test ────────────────────────────────────────────────────────────

def self_test():
    """Run built-in comprehensive self-test."""
    import shutil
    import tempfile

    errors = []

    def chk(label, ok, detail=""):
        if not ok:
            errors.append(f"FAIL: {label} — {detail}")
        print(f"  {'✅' if ok else '❌'} {label}")

    print(f"{NAME} v{VERSION} self-test")

    d = tempfile.mkdtemp(prefix="cbi_test_")
    try:
        # Test 1: basic analysis
        with open(os.path.join(d, "a.py"), "w") as f:
            f.write("# comment\nx = 1\n\n\ndef f():\n    return x\n")
        with open(os.path.join(d, "b.md"), "w") as f:
            f.write("# Title\n\nsome text\n## Sub\nmore\n")
        with open(os.path.join(d, "c.js"), "w") as f:
            f.write("// script\nfunction test() {\n  return 42;\n}\n")
        with open(os.path.join(d, "d.json"), "w") as f:
            f.write('{"a": 1, "b": 2}\n')

        result = analyze(d)
        chk("Total files = 4", result["total_files"] == 4, str(result["total_files"]))
        chk("Python detected", result["stats"].get("Python", {}).get("files") == 1)
        chk("Markdown detected", result["stats"].get("Markdown", {}).get("files") == 1)
        chk("JavaScript detected", result["stats"].get("JavaScript", {}).get("files") == 1)
        chk("JSON detected", result["stats"].get("JSON", {}).get("files") == 1)
        chk("Total lines > 0", result["total_lines"] > 10)
        chk("Has avg_lines_per_file", result["avg_lines_per_file"] > 0)
        chk("Has comment_density (float)", isinstance(result["comment_density"], float))

        # Test 2: JSON output
        j = json.dumps(result)
        chk("JSON serializable", len(j) > 50)

        # Test 3: CSV output
        csv_out = print_csv(result)
        chk("CSV output has header", "Language,Files,Lines," in csv_out)

        # Test 4: Snapshot + trend
        snap = save_snapshot(result)
        chk("Snapshot saved", "Saved" in snap or "saved" in snap)

        trend = show_trend(d)
        chk("Trend works with 1 snapshot", "files" in trend.lower() or "Snapshot" in trend)

        # Test 5: File listing
        chk("Largest files not empty", len(result.get("largest_files", [])) > 0)

        # Test 6: Ignore dirs
        os.mkdir(os.path.join(d, "node_modules"))
        with open(os.path.join(d, "node_modules", "ignored.js"), "w") as f:
            f.write("ignored")
        result2 = analyze(d)
        chk("node_modules ignored", result2["total_files"] == 4)

        print()
        if errors:
            for e in errors:
                print(e)
            return 1
        print("  All checks passed ✅")
        return 0
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
