#!/usr/bin/env python3
"""Code Complexity Analyzer — measure cyclomatic, cognitive, and structural complexity.

Analyzes Python, JavaScript/TypeScript, and Go source files. Reports per-function
complexity metrics with CI-friendly thresholds. Pure Python stdlib.
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Optional


# --- Data Classes ---

@dataclass
class FunctionMetrics:
    name: str
    file: str
    line: int
    end_line: int = 0
    cyclomatic: int = 1  # starts at 1
    cognitive: int = 0
    lines: int = 0
    params: int = 0
    nesting_max: int = 0

    @property
    def risk(self) -> str:
        if self.cyclomatic > 20 or self.cognitive > 25:
            return "high"
        if self.cyclomatic > 10 or self.cognitive > 15:
            return "moderate"
        if self.cyclomatic > 5 or self.cognitive > 8:
            return "low"
        return "simple"


@dataclass
class FileMetrics:
    path: str
    language: str
    total_lines: int = 0
    code_lines: int = 0
    functions: list = field(default_factory=list)

    @property
    def avg_cyclomatic(self) -> float:
        if not self.functions:
            return 0
        return sum(f.cyclomatic for f in self.functions) / len(self.functions)

    @property
    def max_cyclomatic(self) -> int:
        if not self.functions:
            return 0
        return max(f.cyclomatic for f in self.functions)

    @property
    def avg_cognitive(self) -> float:
        if not self.functions:
            return 0
        return sum(f.cognitive for f in self.functions) / len(self.functions)


# --- Language Detection ---

LANG_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".mjs": "javascript",
    ".cjs": "javascript",
}


def detect_language(filepath: str) -> Optional[str]:
    ext = os.path.splitext(filepath)[1].lower()
    return LANG_MAP.get(ext)


# --- Python Analyzer ---

# Python branching keywords that increase cyclomatic complexity
PY_BRANCH_PATTERNS = [
    r'\bif\b', r'\belif\b', r'\bfor\b', r'\bwhile\b',
    r'\band\b', r'\bor\b', r'\bexcept\b',
    r'\bcase\b',  # match/case (Python 3.10+)
]

# Python cognitive complexity increments
PY_COGNITIVE_NESTING = [r'\bif\b', r'\belif\b', r'\bfor\b', r'\bwhile\b', r'\btry\b']
PY_COGNITIVE_INCREMENT = [r'\band\b', r'\bor\b', r'\bbreak\b', r'\bcontinue\b', r'\bexcept\b']


def analyze_python(content: str, filepath: str) -> FileMetrics:
    lines = content.split("\n")
    metrics = FileMetrics(path=filepath, language="python", total_lines=len(lines))

    # Count code lines (non-empty, non-comment)
    in_docstring = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('"""') or stripped.startswith("'''"):
            if stripped.count('"""') >= 2 or stripped.count("'''") >= 2:
                pass  # single-line docstring
            else:
                in_docstring = not in_docstring
            continue
        if in_docstring:
            continue
        if stripped and not stripped.startswith("#"):
            metrics.code_lines += 1

    # Find functions/methods
    func_pattern = re.compile(r'^(\s*)(def|async\s+def)\s+(\w+)\s*\(([^)]*)\)')
    func_starts = []

    for i, line in enumerate(lines):
        m = func_pattern.match(line)
        if m:
            indent = len(m.group(1))
            name = m.group(3)
            params_str = m.group(4).strip()
            params = [p.strip() for p in params_str.split(",") if p.strip()] if params_str else []
            # Remove 'self' and 'cls' from param count
            params = [p for p in params if p.split(":")[0].split("=")[0].strip() not in ("self", "cls")]
            func_starts.append((i, indent, name, len(params)))

    # Analyze each function
    for idx, (start_line, func_indent, func_name, param_count) in enumerate(func_starts):
        # Find function end
        if idx + 1 < len(func_starts):
            # Next function at same or lower indent level
            end_line = func_starts[idx + 1][0] - 1
        else:
            end_line = len(lines) - 1

        # Trim trailing blank lines
        while end_line > start_line and not lines[end_line].strip():
            end_line -= 1

        func_lines = lines[start_line:end_line + 1]
        func = FunctionMetrics(
            name=func_name,
            file=filepath,
            line=start_line + 1,
            end_line=end_line + 1,
            lines=len(func_lines),
            params=param_count,
        )

        # Calculate cyclomatic complexity
        nesting = 0
        max_nesting = 0

        for line in func_lines[1:]:  # skip def line
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            # Calculate nesting level
            line_indent = len(line) - len(line.lstrip())
            rel_indent = max(0, (line_indent - func_indent - 4) // 4)  # relative to function body
            if rel_indent > max_nesting:
                max_nesting = rel_indent

            for pattern in PY_BRANCH_PATTERNS:
                if re.search(pattern, stripped):
                    func.cyclomatic += 1

            # Cognitive complexity
            for pattern in PY_COGNITIVE_NESTING:
                if re.search(pattern, stripped):
                    func.cognitive += 1 + rel_indent  # increment + nesting penalty

            for pattern in PY_COGNITIVE_INCREMENT:
                if re.search(pattern, stripped):
                    func.cognitive += 1

        func.nesting_max = max_nesting
        metrics.functions.append(func)

    return metrics


# --- JavaScript/TypeScript Analyzer ---

JS_BRANCH_PATTERNS = [
    r'\bif\s*\(', r'\belse\s+if\s*\(', r'\bfor\s*\(', r'\bwhile\s*\(',
    r'\bcase\b', r'\bcatch\s*\(', r'&&', r'\|\|', r'\?\?', r'\?[^?:]',  # ternary
]

JS_COGNITIVE_NESTING = [r'\bif\s*\(', r'\belse\s+if\s*\(', r'\bfor\s*\(', r'\bwhile\s*\(', r'\btry\b', r'\bswitch\s*\(']
JS_COGNITIVE_INCREMENT = [r'&&', r'\|\|', r'\?\?', r'\bbreak\b', r'\bcontinue\b', r'\bcatch\s*\(']


def analyze_js(content: str, filepath: str) -> FileMetrics:
    lines = content.split("\n")
    lang = "typescript" if filepath.endswith((".ts", ".tsx")) else "javascript"
    metrics = FileMetrics(path=filepath, language=lang, total_lines=len(lines))

    # Count code lines
    in_block_comment = False
    for line in lines:
        stripped = line.strip()
        if "/*" in stripped:
            in_block_comment = True
        if "*/" in stripped:
            in_block_comment = False
            continue
        if in_block_comment:
            continue
        if stripped and not stripped.startswith("//"):
            metrics.code_lines += 1

    # Find functions
    func_patterns = [
        # function declarations
        re.compile(r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)'),
        # arrow functions assigned to variables
        re.compile(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(([^)]*)\)\s*=>'),
        # method definitions in classes
        re.compile(r'^\s+(?:async\s+)?(\w+)\s*\(([^)]*)\)\s*[:{]'),
    ]

    func_starts = []
    for i, line in enumerate(lines):
        for pattern in func_patterns:
            m = pattern.search(line)
            if m:
                name = m.group(1)
                params_str = m.group(2).strip()
                params = [p.strip() for p in params_str.split(",") if p.strip()] if params_str else []
                indent = len(line) - len(line.lstrip())
                func_starts.append((i, indent, name, len(params)))
                break

    # Analyze functions using brace counting
    for idx, (start_line, func_indent, func_name, param_count) in enumerate(func_starts):
        # Find function body via brace matching
        brace_count = 0
        found_open = False
        end_line = start_line

        for i in range(start_line, len(lines)):
            for ch in lines[i]:
                if ch == '{':
                    brace_count += 1
                    found_open = True
                elif ch == '}':
                    brace_count -= 1

            if found_open and brace_count <= 0:
                end_line = i
                break
        else:
            end_line = len(lines) - 1

        func_lines = lines[start_line:end_line + 1]
        func = FunctionMetrics(
            name=func_name,
            file=filepath,
            line=start_line + 1,
            end_line=end_line + 1,
            lines=len(func_lines),
            params=param_count,
        )

        max_nesting = 0
        for line in func_lines[1:]:
            stripped = line.strip()
            if not stripped or stripped.startswith("//"):
                continue

            line_indent = len(line) - len(line.lstrip())
            rel_indent = max(0, (line_indent - func_indent - 2) // 2)
            if rel_indent > max_nesting:
                max_nesting = rel_indent

            for pattern in JS_BRANCH_PATTERNS:
                if re.search(pattern, stripped):
                    func.cyclomatic += 1

            for pattern in JS_COGNITIVE_NESTING:
                if re.search(pattern, stripped):
                    func.cognitive += 1 + rel_indent

            for pattern in JS_COGNITIVE_INCREMENT:
                if re.search(pattern, stripped):
                    func.cognitive += 1

        func.nesting_max = max_nesting
        metrics.functions.append(func)

    return metrics


# --- Go Analyzer ---

GO_BRANCH_PATTERNS = [
    r'\bif\b', r'\belse\s+if\b', r'\bfor\b', r'\bcase\b',
    r'&&', r'\|\|',
]


def analyze_go(content: str, filepath: str) -> FileMetrics:
    lines = content.split("\n")
    metrics = FileMetrics(path=filepath, language="go", total_lines=len(lines))

    # Count code lines
    in_block_comment = False
    for line in lines:
        stripped = line.strip()
        if "/*" in stripped:
            in_block_comment = True
        if "*/" in stripped:
            in_block_comment = False
            continue
        if in_block_comment:
            continue
        if stripped and not stripped.startswith("//"):
            metrics.code_lines += 1

    # Find functions
    func_pattern = re.compile(r'^func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\(([^)]*)\)')
    func_starts = []

    for i, line in enumerate(lines):
        m = func_pattern.match(line)
        if m:
            name = m.group(1)
            params_str = m.group(2).strip()
            params = [p.strip() for p in params_str.split(",") if p.strip()] if params_str else []
            func_starts.append((i, 0, name, len(params)))

    for idx, (start_line, func_indent, func_name, param_count) in enumerate(func_starts):
        brace_count = 0
        found_open = False
        end_line = start_line

        for i in range(start_line, len(lines)):
            for ch in lines[i]:
                if ch == '{':
                    brace_count += 1
                    found_open = True
                elif ch == '}':
                    brace_count -= 1
            if found_open and brace_count <= 0:
                end_line = i
                break
        else:
            end_line = len(lines) - 1

        func_lines = lines[start_line:end_line + 1]
        func = FunctionMetrics(
            name=func_name,
            file=filepath,
            line=start_line + 1,
            end_line=end_line + 1,
            lines=len(func_lines),
            params=param_count,
        )

        max_nesting = 0
        for line in func_lines[1:]:
            stripped = line.strip()
            if not stripped or stripped.startswith("//"):
                continue

            line_indent = len(line) - len(line.lstrip())
            rel_indent = max(0, line_indent // 4)
            if rel_indent > max_nesting:
                max_nesting = rel_indent

            for pattern in GO_BRANCH_PATTERNS:
                if re.search(pattern, stripped):
                    func.cyclomatic += 1

            # Cognitive
            for pattern in [r'\bif\b', r'\bfor\b', r'\bswitch\b', r'\bselect\b']:
                if re.search(pattern, stripped):
                    func.cognitive += 1 + rel_indent

            for pattern in [r'&&', r'\|\|', r'\bbreak\b', r'\bcontinue\b', r'\bgoto\b']:
                if re.search(pattern, stripped):
                    func.cognitive += 1

        func.nesting_max = max_nesting
        metrics.functions.append(func)

    return metrics


# --- File Analysis Dispatcher ---

ANALYZERS = {
    "python": analyze_python,
    "javascript": analyze_js,
    "typescript": analyze_js,
    "go": analyze_go,
}


def analyze_file(filepath: str) -> Optional[FileMetrics]:
    lang = detect_language(filepath)
    if not lang:
        return None

    analyzer = ANALYZERS.get(lang)
    if not analyzer:
        return None

    with open(filepath, "r", errors="replace") as f:
        content = f.read()

    return analyzer(content, filepath)


def find_files(paths: list, exclude_patterns: list = None) -> list:
    """Find analyzable files from given paths."""
    exclude = exclude_patterns or ["node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build"]
    files = []

    for path in paths:
        if os.path.isfile(path):
            if detect_language(path):
                files.append(path)
        elif os.path.isdir(path):
            for root, dirs, filenames in os.walk(path):
                # Prune excluded dirs
                dirs[:] = [d for d in dirs if d not in exclude and not d.startswith(".")]
                for fname in filenames:
                    fpath = os.path.join(root, fname)
                    if detect_language(fpath):
                        files.append(fpath)

    return sorted(files)


# --- Output Formatters ---

def format_text(all_metrics: list, thresholds: dict, verbose: bool = False) -> str:
    out = []
    violations = []
    total_funcs = 0
    total_complex = 0

    for fm in all_metrics:
        file_violations = []
        for func in fm.functions:
            total_funcs += 1
            exceeded = []
            if func.cyclomatic > thresholds.get("cyclomatic", 10):
                exceeded.append(f"cyclomatic={func.cyclomatic}")
            if func.cognitive > thresholds.get("cognitive", 15):
                exceeded.append(f"cognitive={func.cognitive}")
            if func.lines > thresholds.get("lines", 50):
                exceeded.append(f"lines={func.lines}")
            if func.params > thresholds.get("params", 5):
                exceeded.append(f"params={func.params}")
            if func.nesting_max > thresholds.get("nesting", 4):
                exceeded.append(f"nesting={func.nesting_max}")

            if exceeded:
                total_complex += 1
                file_violations.append((func, exceeded))

        if file_violations or verbose:
            out.append(f"\n📄 {fm.path} ({fm.language}, {fm.code_lines} LOC, {len(fm.functions)} functions)")

            if verbose:
                for func in fm.functions:
                    risk_icon = {"simple": "🟢", "low": "🟡", "moderate": "🟠", "high": "🔴"}[func.risk]
                    out.append(f"  {risk_icon} {func.name}:{func.line} — CC={func.cyclomatic} COG={func.cognitive} lines={func.lines} params={func.params} nest={func.nesting_max}")

            for func, exceeded in file_violations:
                out.append(f"  🔴 {func.name}:{func.line} — {', '.join(exceeded)}")
                violations.append(func)

    # Summary
    out.append(f"\n{'─' * 60}")
    out.append(f"Files: {len(all_metrics)} | Functions: {total_funcs} | Violations: {total_complex}")

    if total_funcs:
        avg_cc = sum(f.cyclomatic for fm in all_metrics for f in fm.functions) / total_funcs
        avg_cog = sum(f.cognitive for fm in all_metrics for f in fm.functions) / total_funcs
        out.append(f"Avg cyclomatic: {avg_cc:.1f} | Avg cognitive: {avg_cog:.1f}")

    if violations:
        out.append(f"Result: FAIL ({total_complex} functions exceed thresholds)")
    else:
        out.append("Result: PASS")

    return "\n".join(out)


def format_json(all_metrics: list, thresholds: dict) -> str:
    data = {
        "files": [],
        "summary": {
            "total_files": len(all_metrics),
            "total_functions": 0,
            "violations": 0,
            "avg_cyclomatic": 0,
            "avg_cognitive": 0,
            "thresholds": thresholds,
        }
    }

    all_cc = []
    all_cog = []

    for fm in all_metrics:
        file_data = {
            "path": fm.path,
            "language": fm.language,
            "total_lines": fm.total_lines,
            "code_lines": fm.code_lines,
            "functions": [],
        }

        for func in fm.functions:
            exceeded = []
            if func.cyclomatic > thresholds.get("cyclomatic", 10):
                exceeded.append("cyclomatic")
            if func.cognitive > thresholds.get("cognitive", 15):
                exceeded.append("cognitive")
            if func.lines > thresholds.get("lines", 50):
                exceeded.append("lines")
            if func.params > thresholds.get("params", 5):
                exceeded.append("params")
            if func.nesting_max > thresholds.get("nesting", 4):
                exceeded.append("nesting")

            file_data["functions"].append({
                "name": func.name,
                "line": func.line,
                "cyclomatic": func.cyclomatic,
                "cognitive": func.cognitive,
                "lines": func.lines,
                "params": func.params,
                "nesting_max": func.nesting_max,
                "risk": func.risk,
                "exceeded": exceeded,
            })

            data["summary"]["total_functions"] += 1
            if exceeded:
                data["summary"]["violations"] += 1
            all_cc.append(func.cyclomatic)
            all_cog.append(func.cognitive)

        data["files"].append(file_data)

    if all_cc:
        data["summary"]["avg_cyclomatic"] = round(sum(all_cc) / len(all_cc), 1)
        data["summary"]["avg_cognitive"] = round(sum(all_cog) / len(all_cog), 1)

    data["summary"]["result"] = "fail" if data["summary"]["violations"] > 0 else "pass"

    return json.dumps(data, indent=2)


def format_markdown(all_metrics: list, thresholds: dict) -> str:
    out = ["# Code Complexity Report\n"]

    total_funcs = sum(len(fm.functions) for fm in all_metrics)
    violations = 0
    all_cc = []
    all_cog = []

    for fm in all_metrics:
        for func in fm.functions:
            all_cc.append(func.cyclomatic)
            all_cog.append(func.cognitive)
            if (func.cyclomatic > thresholds.get("cyclomatic", 10) or
                func.cognitive > thresholds.get("cognitive", 15)):
                violations += 1

    avg_cc = sum(all_cc) / len(all_cc) if all_cc else 0
    avg_cog = sum(all_cog) / len(all_cog) if all_cog else 0

    out.append(f"**Files:** {len(all_metrics)} | **Functions:** {total_funcs} | **Violations:** {violations}")
    out.append(f"**Avg Cyclomatic:** {avg_cc:.1f} | **Avg Cognitive:** {avg_cog:.1f}\n")

    out.append(f"**Thresholds:** CC≤{thresholds.get('cyclomatic', 10)}, COG≤{thresholds.get('cognitive', 15)}, Lines≤{thresholds.get('lines', 50)}, Params≤{thresholds.get('params', 5)}, Nesting≤{thresholds.get('nesting', 4)}\n")

    # Top complex functions
    all_funcs = [(func, fm.path) for fm in all_metrics for func in fm.functions]
    all_funcs.sort(key=lambda x: x[0].cyclomatic + x[0].cognitive, reverse=True)

    if all_funcs:
        out.append("## Hotspots (Top 10)\n")
        out.append("| Risk | Function | File:Line | CC | COG | Lines | Params |")
        out.append("|------|----------|-----------|---:|----:|------:|-------:|")
        for func, fpath in all_funcs[:10]:
            risk_icon = {"simple": "🟢", "low": "🟡", "moderate": "🟠", "high": "🔴"}[func.risk]
            out.append(f"| {risk_icon} | {func.name} | {fpath}:{func.line} | {func.cyclomatic} | {func.cognitive} | {func.lines} | {func.params} |")
        out.append("")

    # Violations
    violation_funcs = [(f, p) for f, p in all_funcs if f.cyclomatic > thresholds.get("cyclomatic", 10) or f.cognitive > thresholds.get("cognitive", 15)]
    if violation_funcs:
        out.append("## Violations\n")
        for func, fpath in violation_funcs:
            reasons = []
            if func.cyclomatic > thresholds.get("cyclomatic", 10):
                reasons.append(f"CC={func.cyclomatic}")
            if func.cognitive > thresholds.get("cognitive", 15):
                reasons.append(f"COG={func.cognitive}")
            out.append(f"- **{func.name}** ({fpath}:{func.line}) — {', '.join(reasons)}")

    return "\n".join(out)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="Analyze code complexity (cyclomatic, cognitive, structural)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s src/                              # Analyze directory
  %(prog)s app.py utils.py                   # Analyze specific files
  %(prog)s src/ --format json                # JSON output for CI
  %(prog)s src/ --cc 15 --cog 20             # Custom thresholds
  %(prog)s src/ --verbose                    # Show all functions
  %(prog)s src/ --format markdown            # Markdown report

Supported: Python (.py), JavaScript/TypeScript (.js/.jsx/.ts/.tsx), Go (.go)
        """
    )

    parser.add_argument("paths", nargs="+", help="Files or directories to analyze")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all functions")
    parser.add_argument("--cc", type=int, default=10, help="Cyclomatic complexity threshold (default: 10)")
    parser.add_argument("--cog", type=int, default=15, help="Cognitive complexity threshold (default: 15)")
    parser.add_argument("--max-lines", type=int, default=50, help="Function length threshold (default: 50)")
    parser.add_argument("--max-params", type=int, default=5, help="Parameter count threshold (default: 5)")
    parser.add_argument("--max-nesting", type=int, default=4, help="Nesting depth threshold (default: 4)")
    parser.add_argument("--exclude", nargs="*", default=[], help="Additional directories to exclude")

    args = parser.parse_args()

    thresholds = {
        "cyclomatic": args.cc,
        "cognitive": args.cog,
        "lines": args.max_lines,
        "params": args.max_params,
        "nesting": args.max_nesting,
    }

    exclude = ["node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build"] + args.exclude
    files = find_files(args.paths, exclude)

    if not files:
        print("No analyzable files found.", file=sys.stderr)
        sys.exit(2)

    all_metrics = []
    for fpath in files:
        fm = analyze_file(fpath)
        if fm:
            all_metrics.append(fm)

    if not all_metrics:
        print("No analyzable files found.", file=sys.stderr)
        sys.exit(2)

    if args.format == "json":
        print(format_json(all_metrics, thresholds))
    elif args.format == "markdown":
        print(format_markdown(all_metrics, thresholds))
    else:
        print(format_text(all_metrics, thresholds, args.verbose))

    # Exit code based on violations
    has_violations = any(
        func.cyclomatic > thresholds["cyclomatic"] or func.cognitive > thresholds["cognitive"]
        for fm in all_metrics for func in fm.functions
    )

    sys.exit(1 if has_violations else 0)


if __name__ == "__main__":
    main()
