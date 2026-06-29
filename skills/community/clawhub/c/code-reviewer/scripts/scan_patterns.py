#!/usr/bin/env python3
"""
Code Pattern Scanner

Scans source files for common anti-patterns, security issues, and code smells
using regex-based pattern matching.

Usage:
    python scan_patterns.py <file-or-directory> [--format json|text]

Supported: Python, JavaScript/TypeScript, Java, Go, PHP, C/C++, Ruby
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# --- Pattern Definitions ---

SECURITY_PATTERNS = [
    # SQL Injection
    {
        "id": "SQLI001",
        "name": "SQL string concatenation",
        "pattern": r'(?:query|execute|exec|raw)\s*\(\s*(?:f["\']|["\'].*?\+|.*format\()',
        "severity": "Critical",
        "category": "Security",
        "languages": ["all"],
        "message": "Potential SQL injection: SQL query constructed with string concatenation",
    },
    # Command Injection
    {
        "id": "CMD001",
        "name": "Command execution with potential injection",
        "pattern": r'(?:os\.system|os\.popen|subprocess\.(?:call|run|Popen)\s*\(\s*shell\s*=\s*True|exec\s*\(\s*`|child_process\.exec)\s*\(.*(?:req\.|request\.|input|param|args|argv)',
        "severity": "Critical",
        "category": "Security",
        "languages": ["all"],
        "message": "Potential command injection: shell command with user input",
    },
    # Hardcoded secrets
    {
        "id": "SEC001",
        "name": "Hardcoded secret/password",
        "pattern": r'(?i)(?:password|passwd|secret|api[_-]?key|auth[_-]?token|access[_-]?key|private[_-]?key)\s*[:=]\s*["\'][^"\']{8,}["\']',
        "severity": "High",
        "category": "Security",
        "languages": ["all"],
        "message": "Hardcoded credential detected in source code",
    },
    # AWS key
    {
        "id": "SEC002",
        "name": "AWS Access Key",
        "pattern": r'AKIA[0-9A-Z]{16}',
        "severity": "Critical",
        "category": "Security",
        "languages": ["all"],
        "message": "AWS Access Key ID detected in source code",
    },
    # Private key
    {
        "id": "SEC003",
        "name": "Private key block",
        "pattern": r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
        "severity": "Critical",
        "category": "Security",
        "languages": ["all"],
        "message": "Private key found in source code",
    },
    # Eval
    {
        "id": "SEC004",
        "name": "Use of eval()",
        "pattern": r'\beval\s*\(',
        "severity": "High",
        "category": "Security",
        "languages": ["javascript", "python", "php"],
        "message": "Use of eval() can lead to code injection",
    },
    # Weak hashing
    {
        "id": "SEC005",
        "name": "Weak hash algorithm for password",
        "pattern": r'(?i)(?:md5|sha1)\s*\(',
        "severity": "Medium",
        "category": "Security",
        "languages": ["all"],
        "message": "Weak hash algorithm (MD5/SHA1) detected - use bcrypt/argon2 for passwords",
    },
    # Insecure random
    {
        "id": "SEC006",
        "name": "Insecure random for security context",
        "pattern": r'\bMath\.random\s*\(\)',
        "severity": "Medium",
        "category": "Security",
        "languages": ["javascript"],
        "message": "Math.random() is not cryptographically secure - use crypto.getRandomValues()",
    },
    # Dangerous innerHTML
    {
        "id": "SEC007",
        "name": "innerHTML with dynamic content",
        "pattern": r'\.innerHTML\s*=\s*(?!["\']<)',
        "severity": "High",
        "category": "Security",
        "languages": ["javascript"],
        "message": "Potential XSS: innerHTML assigned with dynamic content",
    },
    # dangerouslySetInnerHTML
    {
        "id": "SEC008",
        "name": "dangerouslySetInnerHTML",
        "pattern": r'dangerouslySetInnerHTML',
        "severity": "High",
        "category": "Security",
        "languages": ["javascript"],
        "message": "dangerouslySetInnerHTML used - ensure content is sanitized",
    },
    # Pickle deserialization
    {
        "id": "SEC009",
        "name": "Pickle deserialization",
        "pattern": r'pickle\.loads?\s*\(',
        "severity": "High",
        "category": "Security",
        "languages": ["python"],
        "message": "pickle.loads on untrusted data can lead to RCE",
    },
    # YAML unsafe load
    {
        "id": "SEC010",
        "name": "Unsafe YAML load",
        "pattern": r'yaml\.load\s*\((?!.*SafeLoader)',
        "severity": "High",
        "category": "Security",
        "languages": ["python"],
        "message": "yaml.load without SafeLoader can execute arbitrary code",
    },
    # Debug mode
    {
        "id": "SEC011",
        "name": "Debug mode enabled",
        "pattern": r'(?i)DEBUG\s*=\s*True',
        "severity": "Medium",
        "category": "Security",
        "languages": ["python"],
        "message": "Debug mode enabled - ensure this is not in production config",
    },
    # CORS wildcard
    {
        "id": "SEC012",
        "name": "Wildcard CORS",
        "pattern": r"Access-Control-Allow-Origin.*\*",
        "severity": "Medium",
        "category": "Security",
        "languages": ["all"],
        "message": "Wildcard CORS origin - restrict to trusted domains",
    },
    # Hardcoded DB connection string
    {
        "id": "SEC013",
        "name": "Database connection string with credentials",
        "pattern": r'(?:mongodb|postgresql|postgres|mysql|redis)://[^\s\'"]*:[^\s\'"/]+@',
        "severity": "High",
        "category": "Security",
        "languages": ["all"],
        "message": "Database connection string with embedded credentials detected",
    },
]

QUALITY_PATTERNS = [
    # TODO/FIXME/HACK
    {
        "id": "TODO001",
        "name": "TODO comment",
        "pattern": r'(?i)\b(TODO|FIXME|HACK|XXX|BUG)\b',
        "severity": "Low",
        "category": "Code Quality",
        "languages": ["all"],
        "message": "Technical debt marker found - consider creating a tracked issue",
    },
    # Empty catch block
    {
        "id": "QUAL001",
        "name": "Empty catch block",
        "pattern": r'catch\s*\([^)]*\)\s*\{\s*\}',
        "severity": "Medium",
        "category": "Error Handling",
        "languages": ["javascript", "java", "csharp"],
        "message": "Empty catch block - errors are silently swallowed",
    },
    # Empty except block (Python)
    {
        "id": "QUAL002",
        "name": "Empty except block",
        "pattern": r'except.*:\s*\n\s*pass',
        "severity": "Medium",
        "category": "Error Handling",
        "languages": ["python"],
        "message": "Empty except block - errors are silently swallowed",
    },
    # Bare except (Python)
    {
        "id": "QUAL003",
        "name": "Bare except clause",
        "pattern": r'\bexcept\s*:',
        "severity": "Medium",
        "category": "Error Handling",
        "languages": ["python"],
        "message": "Bare except catches all exceptions including SystemExit/KeyboardInterrupt",
    },
    # console.log in production code
    {
        "id": "QUAL004",
        "name": "Debug console.log",
        "pattern": r'console\.log\s*\(',
        "severity": "Low",
        "category": "Code Quality",
        "languages": ["javascript"],
        "message": "console.log found - remove before production or use proper logger",
    },
    # print() in production Python
    {
        "id": "QUAL005",
        "name": "Debug print statement",
        "pattern": r'\bprint\s*\(',
        "severity": "Low",
        "category": "Code Quality",
        "languages": ["python"],
        "message": "print() found - use logging module for production code",
    },
    # var keyword (should be let/const)
    {
        "id": "QUAL006",
        "name": "Use of var keyword",
        "pattern": r'\bvar\s+\w+',
        "severity": "Low",
        "category": "Code Quality",
        "languages": ["javascript"],
        "message": "Use 'const' or 'let' instead of 'var'",
    },
    # == instead of ===
    {
        "id": "QUAL007",
        "name": "Loose equality operator",
        "pattern": r'[^=!]==[^=]',
        "severity": "Low",
        "category": "Code Quality",
        "languages": ["javascript"],
        "message": "Use strict equality (===) instead of loose equality (==)",
    },
    # Mutable default argument (Python)
    {
        "id": "QUAL008",
        "name": "Mutable default argument",
        "pattern": r'def\s+\w+\s*\([^)]*=\s*(?:\[\]|\{\}|set\(\))',
        "severity": "Medium",
        "category": "Code Quality",
        "languages": ["python"],
        "message": "Mutable default argument - shared across all calls, use None instead",
    },
    # Any type in TypeScript
    {
        "id": "QUAL009",
        "name": "TypeScript 'any' type",
        "pattern": r':\s*any\b',
        "severity": "Low",
        "category": "Code Quality",
        "languages": ["typescript"],
        "message": "Avoid 'any' type - use 'unknown' or proper types",
    },
    # Suppressed error
    {
        "id": "QUAL010",
        "name": "Suppressed error",
        "pattern": r'(?:,\s*_\s*=\s*\w+\(|\bignore\s*=\s*True|#\s*noqa|#\s*type:\s*ignore|//\s*@ts-ignore|//\s*eslint-disable)',
        "severity": "Low",
        "category": "Error Handling",
        "languages": ["all"],
        "message": "Error or linting rule suppressed - ensure this is intentional",
    },
    # Magic number
    {
        "id": "QUAL011",
        "name": "Potential magic number",
        "pattern": r'(?<![.\w])(?<!["\'])\b\d{3,}\b(?!\w)',
        "severity": "Low",
        "category": "Code Quality",
        "languages": ["all"],
        "message": "Large numeric literal - consider extracting to a named constant",
    },
]

ALL_PATTERNS = SECURITY_PATTERNS + QUALITY_PATTERNS

# Language detection by extension
EXT_TO_LANG = {
    '.py': 'python',
    '.js': 'javascript', '.jsx': 'javascript', '.mjs': 'javascript',
    '.ts': 'typescript', '.tsx': 'typescript',
    '.java': 'java', '.kt': 'kotlin', '.scala': 'scala',
    '.go': 'go',
    '.c': 'c', '.h': 'c', '.cpp': 'cpp', '.cc': 'cpp', '.hpp': 'cpp',
    '.cs': 'csharp',
    '.php': 'php',
    '.rb': 'ruby',
    '.rs': 'rust',
    '.swift': 'swift',
}

SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist',
             'build', '.next', '.nuxt', 'target', 'vendor', '.idea', '.vscode',
             'coverage', '.cache', '.workbuddy'}
SKIP_EXTENSIONS = {'.min.js', '.min.css', '.map', '.lock', '.png', '.jpg', '.jpeg',
                   '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.eot',
                   '.pdf', '.zip', '.tar', '.gz', '.bin', '.exe', '.dll', '.so',
                   '.dylib', '.pyc', '.class', '.o', '.a'}


def scan_file(filepath, language=None):
    """Scan a single file for pattern matches."""
    findings = []

    if language is None:
        ext = Path(filepath).suffix.lower()
        language = EXT_TO_LANG.get(ext, 'unknown')

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except Exception:
        return []

    source = ''.join(lines)

    for pattern_def in ALL_PATTERNS:
        pattern_langs = pattern_def['languages']
        if 'all' not in pattern_langs and language not in pattern_langs:
            continue

        try:
            for match in re.finditer(pattern_def['pattern'], source, re.MULTILINE):
                line_num = source[:match.start()].count('\n') + 1
                line_content = lines[line_num - 1].strip() if line_num <= len(lines) else ''

                findings.append({
                    "type": pattern_def['id'],
                    "severity": pattern_def['severity'],
                    "category": pattern_def['category'],
                    "file": filepath,
                    "line": line_num,
                    "rule": pattern_def['name'],
                    "message": pattern_def['message'],
                    "snippet": line_content[:120],
                })
        except re.error:
            continue

    return findings


def scan_path(path):
    """Scan a file or directory."""
    all_findings = []
    path = Path(path)

    if path.is_file():
        ext = path.suffix.lower()
        if ext not in SKIP_EXTENSIONS and ext in EXT_TO_LANG:
            all_findings.extend(scan_file(str(path)))
    elif path.is_dir():
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                ext = Path(f).suffix.lower()
                if ext in SKIP_EXTENSIONS or ext not in EXT_TO_LANG:
                    continue
                if any(f.endswith(se) for se in SKIP_EXTENSIONS):
                    continue
                filepath = os.path.join(root, f)
                all_findings.extend(scan_file(filepath))

    return all_findings


def main():
    parser = argparse.ArgumentParser(description='Scan code for anti-patterns and security issues')
    parser.add_argument('path', help='File or directory to scan')
    parser.add_argument('--format', choices=['json', 'text'], default='text',
                        help='Output format')
    args = parser.parse_args()

    findings = scan_path(args.path)

    if args.format == 'json':
        print(json.dumps(findings, indent=2, ensure_ascii=False))
    else:
        if not findings:
            print("No pattern issues found.")
            return

        # Group by category then severity
        categories = {}
        for f in findings:
            cat = f['category']
            sev = f['severity']
            if cat not in categories:
                categories[cat] = {}
            if sev not in categories[cat]:
                categories[cat][sev] = []
            categories[cat][sev].append(f)

        for cat in sorted(categories.keys()):
            print(f"\n{'='*60}")
            print(f"  {cat}")
            print(f"{'='*60}")
            for sev in ['Critical', 'High', 'Medium', 'Low']:
                items = categories[cat].get(sev, [])
                if items:
                    print(f"\n  [{sev}] ({len(items)} issues)")
                    for item in items:
                        print(f"    {item['file']}:{item['line']}")
                        print(f"      [{item['type']}] {item['message']}")
                        if item.get('snippet'):
                            print(f"      > {item['snippet']}")

    print(f"\nTotal: {len(findings)} issues found")


if __name__ == '__main__':
    main()
