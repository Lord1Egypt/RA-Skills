#!/usr/bin/env python3
"""Code complexity and quality metrics analyzer.

Analyzes Python, JavaScript/TypeScript, Go, and other source files for:
- Lines of code (total, blank, comment, code)
- Cyclomatic complexity (Python)
- Function/class counts
- File-level metrics summary
- Largest files ranking
"""

import argparse
import ast
import json
import os
import re
import sys
from collections import defaultdict


# Language detection by extension
LANG_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".java": "Java",
    ".c": "C",
    ".h": "C",
    ".cpp": "C++",
    ".hpp": "C++",
    ".cs": "C#",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".php": "PHP",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".lua": "Lua",
    ".r": "R",
    ".scala": "Scala",
}

COMMENT_PATTERNS = {
    "Python": (r"^\s*#", None),
    "JavaScript": (r"^\s*//", (r"/\*", r"\*/")),
    "TypeScript": (r"^\s*//", (r"/\*", r"\*/")),
    "Go": (r"^\s*//", (r"/\*", r"\*/")),
    "Rust": (r"^\s*//", (r"/\*", r"\*/")),
    "Ruby": (r"^\s*#", (r"=begin", r"=end")),
    "Java": (r"^\s*//", (r"/\*", r"\*/")),
    "C": (r"^\s*//", (r"/\*", r"\*/")),
    "C++": (r"^\s*//", (r"/\*", r"\*/")),
    "C#": (r"^\s*//", (r"/\*", r"\*/")),
    "Swift": (r"^\s*//", (r"/\*", r"\*/")),
    "Kotlin": (r"^\s*//", (r"/\*", r"\*/")),
    "PHP": (r"^\s*(?://|#)", (r"/\*", r"\*/")),
    "Shell": (r"^\s*#", None),
    "Lua": (r"^\s*--", (r"--\[\[", r"\]\]")),
    "R": (r"^\s*#", None),
    "Scala": (r"^\s*//", (r"/\*", r"\*/")),
}

# Patterns for counting functions/classes
FUNC_PATTERNS = {
    "Python": r"^\s*def\s+\w+",
    "JavaScript": r"(?:function\s+\w+|(?:const|let|var)\s+\w+\s*=\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))",
    "TypeScript": r"(?:function\s+\w+|(?:const|let|var)\s+\w+\s*=\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))",
    "Go": r"^func\s+",
    "Rust": r"^\s*(?:pub\s+)?fn\s+",
    "Ruby": r"^\s*def\s+",
    "Java": r"(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+\w+\s*\(",
    "Swift": r"^\s*(?:func|init)\s+",
}

CLASS_PATTERNS = {
    "Python": r"^\s*class\s+\w+",
    "JavaScript": r"^\s*class\s+\w+",
    "TypeScript": r"^\s*(?:export\s+)?class\s+\w+",
    "Java": r"(?:public|private|protected|\s)*class\s+\w+",
    "Ruby": r"^\s*class\s+\w+",
    "Rust": r"^\s*(?:pub\s+)?struct\s+\w+",
    "Go": r"^\s*type\s+\w+\s+struct",
    "Swift": r"^\s*class\s+\w+",
    "C#": r"(?:public|private|protected|internal|\s)*class\s+\w+",
}


def count_lines(filepath, lang):
    """Count total, blank, comment, and code lines."""
    try:
        with open(filepath, "r", errors="ignore") as f:
            lines = f.readlines()
    except OSError:
        return {"total": 0, "blank": 0, "comment": 0, "code": 0}

    total = len(lines)
    blank = 0
    comment = 0
    in_block = False

    comment_info = COMMENT_PATTERNS.get(lang, (r"^\s*#", None))
    single_re = comment_info[0]
    block_info = comment_info[1] if len(comment_info) > 1 else None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            blank += 1
            continue

        if in_block:
            comment += 1
            if block_info and re.search(block_info[1], stripped):
                in_block = False
            continue

        if block_info and re.search(block_info[0], stripped):
            comment += 1
            if not re.search(block_info[1], stripped):
                in_block = True
            continue

        if single_re and re.match(single_re, stripped):
            comment += 1
            continue

    code = total - blank - comment
    return {"total": total, "blank": blank, "comment": comment, "code": code}


def count_functions_classes(filepath, lang):
    """Count functions and classes in a file."""
    try:
        with open(filepath, "r", errors="ignore") as f:
            content = f.read()
    except OSError:
        return 0, 0

    func_pattern = FUNC_PATTERNS.get(lang)
    class_pattern = CLASS_PATTERNS.get(lang)

    funcs = len(re.findall(func_pattern, content, re.MULTILINE)) if func_pattern else 0
    classes = len(re.findall(class_pattern, content, re.MULTILINE)) if class_pattern else 0
    return funcs, classes


def python_cyclomatic_complexity(filepath):
    """Calculate cyclomatic complexity for Python files using AST."""
    try:
        with open(filepath, "r") as f:
            source = f.read()
        tree = ast.parse(source)
    except (SyntaxError, OSError):
        return []

    results = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            complexity = 1  # Base
            for child in ast.walk(node):
                if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                    complexity += 1
                elif isinstance(child, ast.BoolOp):
                    complexity += len(child.values) - 1
                elif isinstance(child, ast.comprehension):
                    complexity += 1 + len(child.ifs)
                elif isinstance(child, ast.Assert):
                    complexity += 1
            results.append({
                "name": node.name,
                "line": node.lineno,
                "complexity": complexity,
            })
    return results


def find_source_files(path, exclude_dirs=None):
    """Recursively find source files."""
    exclude_dirs = exclude_dirs or {
        "node_modules", ".git", "__pycache__", ".venv", "venv",
        "vendor", "dist", "build", ".next", ".nuxt", "target",
        ".tox", ".mypy_cache", ".pytest_cache", "coverage",
    }
    files = []
    for root, dirs, filenames in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext in LANG_MAP:
                files.append(os.path.join(root, fname))
    return files


def analyze_file(filepath, base_path):
    """Analyze a single file."""
    ext = os.path.splitext(filepath)[1].lower()
    lang = LANG_MAP.get(ext, "Unknown")
    line_counts = count_lines(filepath, lang)
    funcs, classes = count_functions_classes(filepath, lang)

    result = {
        "file": os.path.relpath(filepath, base_path),
        "language": lang,
        "lines": line_counts,
        "functions": funcs,
        "classes": classes,
    }

    # Cyclomatic complexity for Python
    if lang == "Python":
        cc = python_cyclomatic_complexity(filepath)
        if cc:
            result["cyclomatic_complexity"] = cc
            result["avg_complexity"] = round(sum(c["complexity"] for c in cc) / len(cc), 1) if cc else 0
            result["max_complexity"] = max(c["complexity"] for c in cc) if cc else 0

    return result


def format_report(results, project_path, show_complexity=True):
    """Format results as a human-readable report."""
    lines = []
    lines.append(f"=== Code Metrics Report ===")
    lines.append(f"Project: {project_path}")
    lines.append(f"Files analyzed: {len(results)}")
    lines.append("")

    # Aggregate by language
    lang_stats = defaultdict(lambda: {"files": 0, "total": 0, "code": 0, "blank": 0, "comment": 0, "funcs": 0, "classes": 0})
    for r in results:
        lang = r["language"]
        lang_stats[lang]["files"] += 1
        lang_stats[lang]["total"] += r["lines"]["total"]
        lang_stats[lang]["code"] += r["lines"]["code"]
        lang_stats[lang]["blank"] += r["lines"]["blank"]
        lang_stats[lang]["comment"] += r["lines"]["comment"]
        lang_stats[lang]["funcs"] += r["functions"]
        lang_stats[lang]["classes"] += r["classes"]

    lines.append("--- By Language ---")
    lines.append(f"{'Language':<15} {'Files':>6} {'Code':>8} {'Comment':>8} {'Blank':>6} {'Total':>8} {'Funcs':>6} {'Classes':>7}")
    lines.append("-" * 78)
    grand = {"files": 0, "code": 0, "comment": 0, "blank": 0, "total": 0, "funcs": 0, "classes": 0}
    for lang in sorted(lang_stats, key=lambda l: lang_stats[l]["code"], reverse=True):
        s = lang_stats[lang]
        lines.append(f"{lang:<15} {s['files']:>6} {s['code']:>8,} {s['comment']:>8,} {s['blank']:>6,} {s['total']:>8,} {s['funcs']:>6} {s['classes']:>7}")
        for k in grand:
            grand[k] += s[k]
    lines.append("-" * 78)
    lines.append(f"{'TOTAL':<15} {grand['files']:>6} {grand['code']:>8,} {grand['comment']:>8,} {grand['blank']:>6,} {grand['total']:>8,} {grand['funcs']:>6} {grand['classes']:>7}")
    lines.append("")

    # Comment ratio
    if grand["code"] > 0:
        ratio = grand["comment"] / grand["code"] * 100
        lines.append(f"Comment-to-code ratio: {ratio:.1f}%")
        lines.append("")

    # Largest files
    by_loc = sorted(results, key=lambda r: r["lines"]["code"], reverse=True)[:10]
    lines.append("--- Largest Files (by code lines) ---")
    for i, r in enumerate(by_loc, 1):
        lines.append(f"  {i:>3}. {r['file']:<50} {r['lines']['code']:>6} lines ({r['language']})")
    lines.append("")

    # Python complexity
    if show_complexity:
        complex_funcs = []
        for r in results:
            for cc in r.get("cyclomatic_complexity", []):
                if cc["complexity"] >= 5:
                    complex_funcs.append({
                        "file": r["file"],
                        "name": cc["name"],
                        "line": cc["line"],
                        "complexity": cc["complexity"],
                    })
        if complex_funcs:
            complex_funcs.sort(key=lambda x: x["complexity"], reverse=True)
            lines.append("--- High Complexity Functions (≥5) ---")
            for cf in complex_funcs[:15]:
                risk = "🔴" if cf["complexity"] >= 15 else "🟡" if cf["complexity"] >= 10 else "🟢"
                lines.append(f"  {risk} {cf['file']}:{cf['line']} {cf['name']}() — complexity {cf['complexity']}")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze code metrics: LOC, complexity, function/class counts by language."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to project directory (default: current dir)",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-complexity", action="store_true", help="Skip cyclomatic complexity analysis")
    parser.add_argument("--top", type=int, default=10, help="Number of largest files to show")
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        help="Additional directories to exclude",
    )
    args = parser.parse_args()

    project_path = os.path.abspath(args.path)
    if not os.path.isdir(project_path):
        print(f"Error: '{project_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    source_files = find_source_files(project_path)
    if not source_files:
        print(f"No source files found in: {project_path}", file=sys.stderr)
        sys.exit(1)

    results = [analyze_file(f, project_path) for f in source_files]

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_report(results, project_path, show_complexity=not args.no_complexity))


if __name__ == "__main__":
    main()
