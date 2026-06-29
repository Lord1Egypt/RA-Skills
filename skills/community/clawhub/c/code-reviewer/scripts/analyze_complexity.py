#!/usr/bin/env python3
"""
Code Complexity Analyzer

Analyzes source files for cyclomatic complexity, function length, and nesting depth.
Supports: Python, JavaScript, TypeScript, Java, Go, C/C++, PHP, Ruby

Usage:
    python analyze_complexity.py <file-or-directory> [--format json|text]

Output:
    Prints analysis results. With --format json, outputs machine-readable JSON
    suitable for piping to generate_report.py.
"""

import argparse
import ast
import json
import os
import re
import sys
from pathlib import Path

# Severity thresholds
MAX_FUNCTION_LENGTH = 50      # lines
MAX_CYCLOMATIC_COMPLEXITY = 10
MAX_NESTING_DEPTH = 4
MAX_PARAMETER_COUNT = 5


def analyze_python_file(filepath):
    """Analyze a Python file using the ast module."""
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            source = f.read()
        tree = ast.parse(source, filename=filepath)
    except SyntaxError as e:
        return [{
            "type": "syntax_error",
            "severity": "Medium",
            "file": filepath,
            "line": e.lineno or 0,
            "message": f"Syntax error: {e.msg}"
        }]
    except Exception as e:
        return [{
            "type": "parse_error",
            "severity": "Low",
            "file": filepath,
            "line": 0,
            "message": f"Could not parse: {e}"
        }]

    lines = source.splitlines()

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_name = node.name
            start_line = node.lineno
            end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
            func_length = end_line - start_line + 1

            # Cyclomatic complexity: count decision points + 1
            complexity = 1
            for child in ast.walk(node):
                if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                    complexity += 1
                elif isinstance(child, ast.BoolOp):
                    complexity += len(child.values) - 1
                elif isinstance(child, (ast.ExceptHandler,)):
                    complexity += 1
                elif isinstance(child, (ast.With, ast.AsyncWith)):
                    complexity += 1
                elif isinstance(child, ast.comprehension):
                    complexity += 1
                    if child.ifs:
                        complexity += len(child.ifs)

            # Nesting depth
            max_depth = _calculate_nesting_depth_python(node)

            # Parameter count
            param_count = len(node.args.args) + len(node.args.posonlyargs) + len(node.args.kwonlyargs)
            if node.args.vararg:
                param_count += 1
            if node.args.kwarg:
                param_count += 1

            if func_length > MAX_FUNCTION_LENGTH:
                findings.append({
                    "type": "long_function",
                    "severity": "Medium" if func_length > MAX_FUNCTION_LENGTH * 2 else "Low",
                    "file": filepath,
                    "line": start_line,
                    "function": func_name,
                    "message": f"Function '{func_name}' is {func_length} lines long (max {MAX_FUNCTION_LENGTH})"
                })

            if complexity > MAX_CYCLOMATIC_COMPLEXITY:
                findings.append({
                    "type": "high_complexity",
                    "severity": "High" if complexity > 20 else "Medium",
                    "file": filepath,
                    "line": start_line,
                    "function": func_name,
                    "message": f"Function '{func_name}' has cyclomatic complexity {complexity} (max {MAX_CYCLOMATIC_COMPLEXITY})"
                })

            if max_depth > MAX_NESTING_DEPTH:
                findings.append({
                    "type": "deep_nesting",
                    "severity": "Medium",
                    "file": filepath,
                    "line": start_line,
                    "function": func_name,
                    "message": f"Function '{func_name}' has nesting depth {max_depth} (max {MAX_NESTING_DEPTH})"
                })

            if param_count > MAX_PARAMETER_COUNT:
                findings.append({
                    "type": "too_many_params",
                    "severity": "Low",
                    "file": filepath,
                    "line": start_line,
                    "function": func_name,
                    "message": f"Function '{func_name}' has {param_count} parameters (max {MAX_PARAMETER_COUNT})"
                })

    return findings


def _calculate_nesting_depth_python(node, depth=0):
    """Calculate maximum nesting depth of a Python AST node."""
    if not hasattr(node, 'body'):
        return depth
    max_d = depth
    for child in node.body:
        if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try,
                              ast.AsyncFor, ast.AsyncWith)):
            d = _calculate_nesting_depth_python(child, depth + 1)
            max_d = max(max_d, d)
        elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Don't count nested function definitions
            pass
    return max_d


# --- Brace-based language analysis (JS/TS/Java/Go/C/C++/PHP) ---

BRACE_LANGUAGES = {
    '.js': 'javascript', '.jsx': 'javascript',
    '.ts': 'typescript', '.tsx': 'typescript',
    '.java': 'java', '.go': 'go',
    '.c': 'c', '.h': 'c', '.cpp': 'cpp', '.cc': 'cpp', '.hpp': 'cpp',
    '.php': 'php', '.rb': 'ruby',
    '.kt': 'kotlin', '.swift': 'swift', '.rs': 'rust', '.cs': 'csharp',
    '.scala': 'scala',
}

FUNCTION_PATTERN = re.compile(
    r'(?:function\s+(\w+)|'
    r'(?:public|private|protected|static|async|export|def|func|fn)\s+)*'
    r'(\w+)\s*\([^)]*\)\s*(?:\{|=>|:)',
    re.MULTILINE
)

GO_FUNC_PATTERN = re.compile(r'func\s+(?:\([^)]*\)\s+)?(\w+)\s*\(', re.MULTILINE)


def analyze_brace_file(filepath):
    """Analyze a brace-based language file using regex heuristics."""
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except Exception as e:
        return [{"type": "read_error", "severity": "Low", "file": filepath,
                 "line": 0, "message": f"Could not read: {e}"}]

    source = ''.join(lines)

    # Find function definitions
    ext = Path(filepath).suffix
    if ext == '.go':
        matches = list(GO_FUNC_PATTERN.finditer(source))
    else:
        matches = list(FUNCTION_PATTERN.finditer(source))

    for match in matches:
        func_name = match.group(1) or match.group(2) or 'anonymous'
        start_line = source[:match.start()].count('\n') + 1

        # Find function body by tracking braces
        brace_pos = source.find('{', match.end())
        if brace_pos == -1:
            continue

        depth = 1
        pos = brace_pos + 1
        while depth > 0 and pos < len(source):
            if source[pos] == '{':
                depth += 1
            elif source[pos] == '}':
                depth -= 1
            pos += 1

        end_line = source[:pos].count('\n') + 1
        func_length = end_line - start_line + 1

        # Count decision points in function body
        func_body = source[brace_pos:pos]
        complexity = 1
        complexity += len(re.findall(r'\bif\b', func_body))
        complexity += len(re.findall(r'\belse\s+if\b', func_body))
        complexity += len(re.findall(r'\bfor\b', func_body))
        complexity += len(re.findall(r'\bwhile\b', func_body))
        complexity += len(re.findall(r'\bcase\b', func_body))
        complexity += len(re.findall(r'&&', func_body))
        complexity += len(re.findall(r'\|\|', func_body))
        complexity += len(re.findall(r'\bcatch\b', func_body))

        # Nesting depth
        max_depth = _calculate_brace_depth(func_body)

        if func_length > MAX_FUNCTION_LENGTH:
            findings.append({
                "type": "long_function",
                "severity": "Medium" if func_length > MAX_FUNCTION_LENGTH * 2 else "Low",
                "file": filepath,
                "line": start_line,
                "function": func_name,
                "message": f"Function '{func_name}' is {func_length} lines long (max {MAX_FUNCTION_LENGTH})"
            })

        if complexity > MAX_CYCLOMATIC_COMPLEXITY:
            findings.append({
                "type": "high_complexity",
                "severity": "High" if complexity > 20 else "Medium",
                "file": filepath,
                "line": start_line,
                "function": func_name,
                "message": f"Function '{func_name}' has estimated cyclomatic complexity {complexity} (max {MAX_CYCLOMATIC_COMPLEXITY})"
            })

        if max_depth > MAX_NESTING_DEPTH:
            findings.append({
                "type": "deep_nesting",
                "severity": "Medium",
                "file": filepath,
                "line": start_line,
                "function": func_name,
                "message": f"Function '{func_name}' has nesting depth {max_depth} (max {MAX_NESTING_DEPTH})"
            })

    return findings


def _calculate_brace_depth(code):
    """Calculate maximum brace nesting depth."""
    max_depth = 0
    depth = 0
    in_string = False
    string_char = None
    in_comment = False
    in_line_comment = False

    i = 0
    while i < len(code):
        c = code[i]
        next_c = code[i + 1] if i + 1 < len(code) else ''

        if in_line_comment:
            if c == '\n':
                in_line_comment = False
        elif in_comment:
            if c == '*' and next_c == '/':
                in_comment = False
                i += 1
        elif in_string:
            if c == '\\':
                i += 1
            elif c == string_char:
                in_string = False
        else:
            if c == '/' and next_c == '/':
                in_line_comment = True
            elif c == '/' and next_c == '*':
                in_comment = True
                i += 1
            elif c in ('"', "'", '`'):
                in_string = True
                string_char = c
            elif c == '{':
                depth += 1
                max_depth = max(max_depth, depth)
            elif c == '}':
                depth -= 1
        i += 1

    return max_depth


def analyze_file(filepath):
    """Analyze a single file, dispatching to the appropriate analyzer."""
    ext = Path(filepath).suffix.lower()

    if ext == '.py':
        return analyze_python_file(filepath)
    elif ext in BRACE_LANGUAGES:
        return analyze_brace_file(filepath)
    else:
        return []


def analyze_path(path):
    """Analyze a file or directory."""
    all_findings = []
    path = Path(path)

    if path.is_file():
        all_findings.extend(analyze_file(str(path)))
    elif path.is_dir():
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv',
                     'dist', 'build', '.next', '.nuxt', 'target', 'vendor',
                     '.idea', '.vscode', 'coverage', '.cache'}
        skip_exts = {'.min.js', '.min.css', '.map', '.lock', '.png', '.jpg',
                     '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2',
                     '.ttf', '.eot', '.pdf', '.zip', '.tar', '.gz'}

        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for f in files:
                filepath = os.path.join(root, f)
                ext = Path(f).suffix.lower()
                if any(f.endswith(se) for se in skip_exts):
                    continue
                all_findings.extend(analyze_file(filepath))

    return all_findings


def main():
    parser = argparse.ArgumentParser(description='Analyze code complexity')
    parser.add_argument('path', help='File or directory to analyze')
    parser.add_argument('--format', choices=['json', 'text'], default='text',
                        help='Output format')
    args = parser.parse_args()

    findings = analyze_path(args.path)

    if args.format == 'json':
        print(json.dumps(findings, indent=2, ensure_ascii=False))
    else:
        if not findings:
            print("No complexity issues found.")
            return

        # Group by severity
        for severity in ['Critical', 'High', 'Medium', 'Low']:
            items = [f for f in findings if f['severity'] == severity]
            if items:
                print(f"\n{'='*60}")
                print(f"  {severity} ({len(items)} issues)")
                print(f"{'='*60}")
                for item in items:
                    print(f"  [{item['type']}] {item['file']}:{item['line']}")
                    print(f"    {item['message']}")
                    print()

    print(f"\nTotal: {len(findings)} issues found")


if __name__ == '__main__':
    main()
