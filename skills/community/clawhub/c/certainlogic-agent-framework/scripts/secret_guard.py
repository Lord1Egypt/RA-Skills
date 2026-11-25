#!/usr/bin/env python3
"""
Secret Guard — git pre-commit secret scanner.

Scans staged files for API keys, tokens, private keys, and credentials.
Prevents secrets from entering git history.

Usage:
    python3 secret_guard.py --staged       # check staged files
    python3 secret_guard.py <file>         # check specific file
    python3 secret_guard.py --all          # check all tracked files
"""
import argparse
import os
import re
import sys
from pathlib import Path


SECRET_PATTERNS = [
    # API keys and tokens
    (r'(?i)(api[_-]?key|api[_-]?secret|api[_-]?token)\s*[=:]\s*["\'][^"\']{8,}', "API key/secret/token"),
    (r'(?i)(sk-[a-zA-Z0-9]{20,}|pk-[a-zA-Z0-9]{20,})', "OpenAI-style API key"),
    (r'(?i)(ghp_|gho_|ghu_|ghs_|ghr_)[a-zA-Z0-9]{36}', "GitHub token"),
    (r'(?i)xox[abpors]-[a-zA-Z0-9]{10,}', "Slack token"),
    (r'(?i)AKIA[0-9A-Z]{16}', "AWS access key"),
    # Private keys
    (r'-----BEGIN\s+(RSA|DSA|EC|OPENSSH|PGP)\s+PRIVATE\s+KEY-----', "Private key"),
    (r'(?i)(private[_-]?key|private[_-]?key[_-]?path)\s*[=:]\s*["\']?[^"\' ]+', "Private key reference"),
    # Connection strings
    (r'(?i)(mongodb|postgresql|mysql|redis)://[^@]+@', "Database connection string with credentials"),
    (r'(?i)jdbc:[a-z]+://[^@]+@', "JDBC connection string with credentials"),
    # Generic secrets
    (r'(?i)(password|passwd|pwd)\s*[=:]\s*["\'][^"\']{4,}', "Password"),
    (r'(?i)(secret|token|credential)\s*[=:]\s*["\'][^"\']{8,}', "Generic secret"),
    (r'(?i)-----BEGIN\s+CERTIFICATE-----', "Certificate (may contain sensitive info)"),
    # .env patterns
    (r'(?i)^(API_KEY|SECRET|TOKEN|PASSWORD|PRIVATE_KEY)\s*=', "Environment variable with secret name"),
]

# Paths to always skip
SKIP_PATTERNS = [
    r'\.gitignore$',
    r'\.gitattributes$',
    r'\.gitmodules$',
    r'package-lock\.json$',
    r'yarn\.lock$',
    r'\.poetry/',
    r'__pycache__/',
]


def should_skip(path):
    for p in SKIP_PATTERNS:
        if re.search(p, str(path)):
            return True
    return False


def scan_file(path):
    """Scan a single file for secrets. Returns list of (line_num, pattern_name, context)."""
    if should_skip(path):
        return []

    try:
        text = path.read_text()
    except (UnicodeDecodeError, IOError):
        return []  # Binary or unreadable

    issues = []
    for pattern, name in SECRET_PATTERNS:
        for match in re.finditer(pattern, text):
            line_num = text[:match.start()].count("\n") + 1
            # Mask the actual secret for display
            masked = match.group()[:20] + "..." if len(match.group()) > 20 else match.group()
            issues.append((line_num, name, masked))

    return issues


def scan_staged():
    """Scan staged files via git diff."""
    import subprocess
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        print(f"Git error: {result.stderr}")
        return {}

    files = [f for f in result.stdout.strip().split("\n") if f]
    results = {}
    for f in files:
        path = Path.cwd() / f
        if path.exists():
            issues = scan_file(path)
            if issues:
                results[f] = issues
    return results


def main():
    parser = argparse.ArgumentParser(description="Git pre-commit secret scanner")
    parser.add_argument("--staged", action="store_true", help="Check staged files")
    parser.add_argument("--all", action="store_true", help="Check all tracked files")
    parser.add_argument("files", nargs="*", help="Files to check")
    args = parser.parse_args()

    if args.staged:
        results = scan_staged()
    elif args.all:
        import subprocess
        result = subprocess.run(
            ["git", "ls-files"], capture_output=True, text=True, timeout=10
        )
        files = [Path.cwd() / f for f in result.stdout.strip().split("\n") if f]
        results = {}
        for f in files:
            if f.exists():
                issues = scan_file(f)
                if issues:
                    results[str(f)] = issues
    elif args.files:
        results = {}
        for f in args.files:
            path = Path(f)
            if path.exists():
                issues = scan_file(path)
                if issues:
                    results[f] = issues
    else:
        print("Usage: python3 secret_guard.py --staged | --all | <files...>")
        sys.exit(1)

    if results:
        print("SECRETS DETECTED\n")
        for f, issues in sorted(results.items()):
            print(f"  {f}:")
            for line, name, context in issues:
                print(f"    Line {line}: {name} — {context}")
        print("\nIf you are CERTAIN this is a false positive, commit with: git commit --no-verify")
        sys.exit(1)

    print("secret_guard: clean")
    sys.exit(0)


if __name__ == "__main__":
    main()