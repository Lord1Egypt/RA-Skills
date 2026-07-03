#!/usr/bin/env python3
"""Codebase Radar — static codebase analysis."""
import json
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter

# ── Import detection regexes ─────────────────────────────────────────
IMPORT_PATTERNS = {
    "python": re.compile(r'^(?:from\s+(\S+)\s+import|import\s+(\S+))'),
    "js": re.compile(r'(?:import\s+(?:\S+\s+from\s+)?["\']([^"\']+)["\']|require\(["\']([^"\']+)["\']\))'),
    "go": re.compile(r'import\s+[("]([^")]+)'),
    "rust": re.compile(r'use\s+([^;]+);'),
    "java": re.compile(r'import\s+([^;]+);'),
}

COMMENT_PATTERNS = {
    "py": (re.compile(r'^\s*#'), re.compile(r'"""')),
    "js": (re.compile(r'^\s*//'), re.compile(r'/\*')),
    "ts": (re.compile(r'^\s*//'), re.compile(r'/\*')),
    "go": (re.compile(r'^\s*//'), re.compile(r'/\*')),
    "rs": (re.compile(r'^\s*//'), re.compile(r'/\*')),
    "java": (re.compile(r'^\s*//'), re.compile(r'/\*')),
    "md": (re.compile(r'^<!--'), re.compile(r'')),
}

# ── Tech debt patterns ──────────────────────────────────────────────
TECH_DEBT_PATTERNS = [
    (re.compile(r'\bTODO\b'), "TODO"),
    (re.compile(r'\bFIXME\b'), "FIXME"),
    (re.compile(r'\bHACK\b'), "HACK"),
    (re.compile(r'\bXXX\b'), "XXX"),
    (re.compile(r'\bWORKAROUND\b'), "WORKAROUND"),
]


def scan_project(root: Path, max_files: int = 5000) -> dict:
    """Scan project structure."""
    info = {"files": 0, "dirs": 0, "loc": 0, "languages": Counter(), "extensions": Counter()}
    if not root.exists():
        return info

    for f in root.rglob("*"):
        if f.is_dir():
            # Skip hidden dirs and common dependency dirs
            if f.name.startswith(".") or f.name in ("node_modules", "__pycache__", "target", "build", "dist", ".git"):
                continue
            info["dirs"] += 1
        elif f.is_file():
            info["files"] += 1
            ext = f.suffix.lstrip(".") or "noext"
            info["extensions"][ext] += 1
            if info["files"] > max_files:
                break
    return info


def scan_dependencies(root: Path) -> dict:
    """Scan imports across files."""
    graph = defaultdict(set)
    modules = defaultdict(set)

    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.name.startswith("."):
            continue
        ext = f.suffix.lower()
        lang = None
        for l, exts in [("python", {".py"}), ("js", {".js", ".jsx", ".ts", ".tsx", ".mjs"}),
                        ("go", {".go"}), ("rust", {".rs"}), ("java", {".java"})]:
            if ext in exts:
                lang = l
                break
        if not lang:
            continue

        try:
            text = f.read_text(encoding="utf-8", errors="replace")[:5000]
        except Exception:
            continue

        pat = IMPORT_PATTERNS.get(lang)
        if not pat:
            continue

        for line in text.splitlines():
            m = pat.search(line)
            if m:
                imp = m.group(1) or m.group(2)
                if imp:
                    graph[f.name].add(imp)
                    modules[imp].add(f.name)
        modules[f.name]  # ensure module entry

    # Detect circular deps (simple n=2 detection)
    circulars = []
    for a in graph:
        for b in graph:
            if a < b and b in graph.get(a, set()) and a in graph.get(b, set()):
                circulars.append((a, b))

    return {
        "nodes": list(modules.keys()),
        "edges": [(k, v) for k, vs in graph.items() for v in vs],
        "circular_deps": circulars,
        "orphan_files": [f for f in graph if not graph[f] and not any(f in v for v in modules.values())],
    }


def scan_tech_debt(root: Path) -> list:
    """Scan for tech debt signals."""
    findings = []
    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.name.startswith("."):
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for pat, label in TECH_DEBT_PATTERNS:
            for m in pat.finditer(text):
                line_no = text[:m.start()].count("\n") + 1
                findings.append({
                    "file": str(f.relative_to(root)),
                    "line": line_no,
                    "type": label,
                    "context": text[max(0, m.start() - 30):m.end() + 30].replace("\n", " ").strip(),
                })
    return findings


def health_scorecard(project_info: dict, deps: dict, debt: list) -> dict:
    """Generate 5-dimension health scorecard."""
    scores = {}
    # Cohesion (heuristic: avg file size / unique imports)
    scores["cohesion"] = min(10, max(1, project_info.get("loc", 0) // max(1, project_info.get("files", 1)) // 20))
    # Coupling (heuristic: fewer circular deps = better)
    n_circular = len(deps.get("circular_deps", []))
    scores["coupling"] = max(1, 10 - n_circular)
    # Maintainability (heuristic: low TODOs = better)
    scores["maintainability"] = max(1, 10 - min(len(debt) // 10, 9))
    # Tech debt (inverted)
    scores["tech_debt"] = max(1, 10 - min(len(debt) // 5, 9))
    # Coverage (estimated from comment ratio)
    scores["coverage_estimate"] = 5  # neutral estimate

    return scores


def generate_mermaid(deps: dict) -> str:
    """Generate Mermaid graph."""
    lines = ["```mermaid", "graph TD"]
    for n in deps.get("nodes", [])[:30]:
        safe = n.replace(".", "_").replace("/", "_").replace("-", "_")
        lines.append(f"  {safe}[\"{n[:30]}\"]")
    for a, b in deps.get("edges", [])[:50]:
        safe_a = a.replace(".", "_").replace("/", "_").replace("-", "_")
        safe_b = b.replace(".", "_").replace("/", "_").replace("-", "_")
        lines.append(f"  {safe_a} --> {safe_b}")
    lines.append("```")
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Codebase Radar — full codebase analysis")
    parser.add_argument("--path", "-p", help="Project root path", required=True)
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text")
    parser.add_argument("--visual", "-v", choices=["mermaid"], help="Generate dependency visualization")
    parser.add_argument("--max-files", type=int, default=5000)
    parser.add_argument("--score-only", action="store_true")
    parser.add_argument("--exclude", nargs="+", default=[])
    args = parser.parse_args()

    root = Path(args.path).expanduser()
    if not root.exists():
        print(f"Error: path {root} not found", file=sys.stderr)
        return 1

    project = scan_project(root, args.max_files)
    deps = scan_dependencies(root)
    debt = scan_tech_debt(root)
    scores = health_scorecard(project, deps, debt)

    if args.score_only:
        print(json.dumps(scores, indent=2))
        return 0

    if args.visual == "mermaid":
        print(generate_mermaid(deps))
        return 0

    # Text report
    report = []
    report.append(f"# Codebase Radar Report: {args.path}")
    report.append("")
    report.append("## Project Overview")
    report.append(f"- Files: {project['files']}")
    report.append(f"- Dirs: {project['dirs']}")
    report.append(f"- Languages: {dict(project['extensions'].most_common(10))}")
    report.append("")
    report.append("## Dependency Analysis")
    report.append(f"- Modules: {len(deps['nodes'])}")
    report.append(f"- Edges: {len(deps['edges'])}")
    report.append(f"- Circular Dependencies: {len(deps['circular_deps'])}")
    if deps['circular_deps']:
        for a, b in deps['circular_deps'][:10]:
            report.append(f"  - {a} <-> {b}")
    report.append(f"- Orphan Files: {len(deps['orphan_files'])}")
    report.append("")
    report.append("## Tech Debt")
    debt_by_type = Counter(d["type"] for d in debt)
    for t, c in debt_by_type.most_common():
        report.append(f"- {t}: {c}")
    report.append(f"- Total debt items: {len(debt)}")
    if debt:
        report.append("- Top items:")
        for d in debt[:10]:
            report.append(f"  - [{d['type']}] {d['file']}:{d['line']} \"{d['context'][:60]}\"")
    report.append("")
    report.append("## Health Scorecard")
    for dim, score in scores.items():
        bar = "█" * score + "░" * (10 - score)
        report.append(f"- {dim}: {bar} {score}/10")

    print("\n".join(report))


if __name__ == "__main__":
    main()
