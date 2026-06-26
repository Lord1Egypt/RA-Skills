#!/usr/bin/env python3
"""Commit message linter — validate git commit messages against configurable rules.

Supports Conventional Commits spec, custom type/scope whitelists, length limits,
and more. Reads from stdin, file, or git log. CI-friendly exit codes.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Optional


# --- Default Configuration ---

DEFAULT_CONFIG = {
    "header_max_length": 72,
    "header_min_length": 10,
    "body_max_line_length": 100,
    "require_conventional": True,
    "types": [
        "feat", "fix", "docs", "style", "refactor", "perf",
        "test", "build", "ci", "chore", "revert"
    ],
    "scopes": [],  # empty = any scope allowed
    "require_scope": False,
    "require_body": False,
    "require_breaking_change_description": True,
    "no_trailing_period": True,
    "header_case": "lower",  # lower, upper, sentence, any
    "no_leading_whitespace": True,
    "no_trailing_whitespace": True,
    "no_empty_lines_between_header_and_body": False,
    "max_body_lines": 0,  # 0 = unlimited
    "forbidden_patterns": [],  # regex patterns to reject
    "required_patterns": [],  # regex patterns that must match
    "ignore_patterns": [
        r"^Merge (branch|pull request|remote-tracking)",
        r"^Revert \"",
        r"^Initial commit$",
        r"^v?\d+\.\d+\.\d+"
    ]
}

# --- Data Classes ---

@dataclass
class LintIssue:
    level: str  # "error" or "warning"
    rule: str
    message: str
    line: int = 0

@dataclass
class LintResult:
    commit_hash: str
    header: str
    issues: list = field(default_factory=list)

    @property
    def has_errors(self):
        return any(i.level == "error" for i in self.issues)

    @property
    def has_warnings(self):
        return any(i.level == "warning" for i in self.issues)


# --- Config Loading ---

def load_config(config_path: Optional[str] = None) -> dict:
    """Load config from file, merging with defaults."""
    config = dict(DEFAULT_CONFIG)

    # Auto-discover config files
    search_paths = [
        config_path,
        ".commitlintrc.json",
        ".commitlintrc",
        "commitlint.config.json",
    ]

    for path in search_paths:
        if path and os.path.isfile(path):
            with open(path, "r") as f:
                user_config = json.load(f)
            config.update(user_config)
            break

    return config


# --- Conventional Commit Parsing ---

CONVENTIONAL_RE = re.compile(
    r'^(?P<type>[a-zA-Z]+)'
    r'(?:\((?P<scope>[^)]+)\))?'
    r'(?P<breaking>!)?'
    r':\s+'
    r'(?P<description>.+)$'
)


def parse_conventional(header: str) -> Optional[dict]:
    """Parse a Conventional Commits header. Returns None if not conventional."""
    m = CONVENTIONAL_RE.match(header)
    if not m:
        return None
    return {
        "type": m.group("type"),
        "scope": m.group("scope"),
        "breaking": m.group("breaking") == "!",
        "description": m.group("description"),
    }


# --- Lint Rules ---

def lint_message(message: str, config: dict, commit_hash: str = "") -> LintResult:
    """Lint a single commit message against config rules."""
    lines = message.split("\n")
    header = lines[0] if lines else ""
    body_lines = lines[2:] if len(lines) > 2 else []  # skip blank line after header

    result = LintResult(commit_hash=commit_hash or "stdin", header=header)

    # Check ignore patterns
    for pattern in config.get("ignore_patterns", []):
        if re.match(pattern, header):
            return result  # skip this commit

    # --- Header Rules ---

    # Empty header
    if not header.strip():
        result.issues.append(LintIssue("error", "header-empty", "Commit message header is empty"))
        return result

    # Leading whitespace
    if config.get("no_leading_whitespace") and header != header.lstrip():
        result.issues.append(LintIssue("error", "header-leading-whitespace", "Header has leading whitespace"))

    # Trailing whitespace
    if config.get("no_trailing_whitespace") and header != header.rstrip():
        result.issues.append(LintIssue("warning", "header-trailing-whitespace", "Header has trailing whitespace"))

    # Header length
    max_len = config.get("header_max_length", 72)
    if max_len and len(header) > max_len:
        result.issues.append(LintIssue("error", "header-max-length",
            f"Header is {len(header)} chars, max {max_len}"))

    min_len = config.get("header_min_length", 10)
    if min_len and len(header) < min_len:
        result.issues.append(LintIssue("warning", "header-min-length",
            f"Header is {len(header)} chars, min {min_len}"))

    # Trailing period
    if config.get("no_trailing_period") and header.rstrip().endswith("."):
        result.issues.append(LintIssue("warning", "header-no-period",
            "Header should not end with a period"))

    # --- Conventional Commits ---

    if config.get("require_conventional"):
        parsed = parse_conventional(header)

        if not parsed:
            result.issues.append(LintIssue("error", "conventional-format",
                "Header must follow Conventional Commits: <type>[scope]: <description>"))
        else:
            # Type validation
            allowed_types = config.get("types", [])
            if allowed_types and parsed["type"] not in allowed_types:
                result.issues.append(LintIssue("error", "type-enum",
                    f"Type '{parsed['type']}' not in allowed: {', '.join(allowed_types)}"))

            # Scope validation
            if config.get("require_scope") and not parsed["scope"]:
                result.issues.append(LintIssue("error", "scope-required",
                    "Scope is required"))

            allowed_scopes = config.get("scopes", [])
            if allowed_scopes and parsed["scope"] and parsed["scope"] not in allowed_scopes:
                result.issues.append(LintIssue("error", "scope-enum",
                    f"Scope '{parsed['scope']}' not in allowed: {', '.join(allowed_scopes)}"))

            # Description case
            desc = parsed["description"]
            case_rule = config.get("header_case", "any")
            if case_rule == "lower" and desc and desc[0].isupper():
                result.issues.append(LintIssue("warning", "description-case",
                    "Description should start with lowercase"))
            elif case_rule == "upper" and desc and desc[0].islower():
                result.issues.append(LintIssue("warning", "description-case",
                    "Description should start with uppercase"))
            elif case_rule == "sentence" and desc and desc[0].islower():
                result.issues.append(LintIssue("warning", "description-case",
                    "Description should start with uppercase (sentence case)"))

            # Empty description
            if not desc or not desc.strip():
                result.issues.append(LintIssue("error", "description-empty",
                    "Description is empty after type/scope"))

            # Breaking change in body
            if parsed["breaking"] and config.get("require_breaking_change_description"):
                body_text = "\n".join(body_lines)
                if "BREAKING CHANGE:" not in body_text and "BREAKING-CHANGE:" not in body_text:
                    result.issues.append(LintIssue("warning", "breaking-change-description",
                        "Breaking change (!) should have BREAKING CHANGE: description in body"))

    # --- Body Rules ---

    # Blank line between header and body
    if len(lines) > 1:
        if config.get("no_empty_lines_between_header_and_body"):
            pass  # allow no blank line
        elif lines[1].strip():
            result.issues.append(LintIssue("error", "body-separator",
                "There must be a blank line between header and body"))

    # Require body
    if config.get("require_body") and not body_lines:
        result.issues.append(LintIssue("warning", "body-required",
            "Commit body is required"))

    # Body line length
    body_max = config.get("body_max_line_length", 100)
    if body_max:
        for i, line in enumerate(body_lines):
            if len(line) > body_max:
                result.issues.append(LintIssue("warning", "body-line-length",
                    f"Body line {i+3} is {len(line)} chars, max {body_max}"))
                break  # report only first

    # Max body lines
    max_body = config.get("max_body_lines", 0)
    if max_body and len(body_lines) > max_body:
        result.issues.append(LintIssue("warning", "body-max-lines",
            f"Body has {len(body_lines)} lines, max {max_body}"))

    # --- Pattern Rules ---

    full_message = message
    for pattern in config.get("forbidden_patterns", []):
        if re.search(pattern, full_message):
            result.issues.append(LintIssue("error", "forbidden-pattern",
                f"Message matches forbidden pattern: {pattern}"))

    for pattern in config.get("required_patterns", []):
        if not re.search(pattern, full_message):
            result.issues.append(LintIssue("warning", "required-pattern",
                f"Message must match pattern: {pattern}"))

    # --- Trailing whitespace in body ---
    if config.get("no_trailing_whitespace"):
        for i, line in enumerate(body_lines):
            if line != line.rstrip():
                result.issues.append(LintIssue("warning", "body-trailing-whitespace",
                    f"Body line {i+3} has trailing whitespace"))
                break

    return result


# --- Git Integration ---

def get_commits_from_git(rev_range: str = "HEAD~1..HEAD") -> list:
    """Get commit messages from git log."""
    try:
        output = subprocess.check_output(
            ["git", "log", "--format=%H%n%B%n---COMMIT-END---", rev_range],
            stderr=subprocess.PIPE, text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running git log: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    except FileNotFoundError:
        print("Error: git not found", file=sys.stderr)
        sys.exit(2)

    commits = []
    current_hash = ""
    current_lines = []

    for line in output.split("\n"):
        if line == "---COMMIT-END---":
            if current_hash:
                msg = "\n".join(current_lines).strip()
                commits.append((current_hash, msg))
            current_hash = ""
            current_lines = []
        elif not current_hash:
            current_hash = line.strip()
        else:
            current_lines.append(line)

    return commits


# --- Output Formatters ---

def format_text(results: list, verbose: bool = False) -> str:
    """Format results as human-readable text."""
    out = []
    errors = 0
    warnings = 0

    for r in results:
        if not r.issues:
            if verbose:
                out.append(f"✅ {r.commit_hash[:8]} {r.header}")
            continue

        out.append(f"\n{'❌' if r.has_errors else '⚠️'} {r.commit_hash[:8]} {r.header}")
        for issue in r.issues:
            icon = "  ✖" if issue.level == "error" else "  ⚠"
            out.append(f"{icon} [{issue.rule}] {issue.message}")
            if issue.level == "error":
                errors += 1
            else:
                warnings += 1

    out.append(f"\n{'─' * 50}")
    out.append(f"Commits: {len(results)} | Errors: {errors} | Warnings: {warnings}")

    if errors:
        out.append("Result: FAIL")
    elif warnings:
        out.append("Result: PASS (with warnings)")
    else:
        out.append("Result: PASS")

    return "\n".join(out)


def format_json(results: list) -> str:
    """Format results as JSON."""
    data = {
        "commits": [],
        "summary": {
            "total": len(results),
            "errors": 0,
            "warnings": 0,
            "passed": 0,
            "failed": 0,
        }
    }

    for r in results:
        commit = {
            "hash": r.commit_hash,
            "header": r.header,
            "issues": [
                {"level": i.level, "rule": i.rule, "message": i.message}
                for i in r.issues
            ],
            "status": "fail" if r.has_errors else ("warn" if r.has_warnings else "pass")
        }
        data["commits"].append(commit)

        if r.has_errors:
            data["summary"]["failed"] += 1
        else:
            data["summary"]["passed"] += 1

        data["summary"]["errors"] += sum(1 for i in r.issues if i.level == "error")
        data["summary"]["warnings"] += sum(1 for i in r.issues if i.level == "warning")

    data["summary"]["result"] = "fail" if data["summary"]["failed"] > 0 else "pass"

    return json.dumps(data, indent=2)


def format_markdown(results: list) -> str:
    """Format results as markdown."""
    out = ["# Commit Message Lint Report\n"]

    errors = sum(1 for r in results if r.has_errors)
    warnings = sum(1 for r in results if r.has_warnings and not r.has_errors)
    passed = len(results) - errors - warnings

    out.append(f"**Commits:** {len(results)} | **Errors:** {errors} | **Warnings:** {warnings} | **Clean:** {passed}\n")

    if errors:
        out.append("## ❌ Failed\n")
        for r in results:
            if r.has_errors:
                out.append(f"### `{r.commit_hash[:8]}` {r.header}\n")
                for issue in r.issues:
                    icon = "❌" if issue.level == "error" else "⚠️"
                    out.append(f"- {icon} **{issue.rule}**: {issue.message}")
                out.append("")

    if warnings:
        out.append("## ⚠️ Warnings\n")
        for r in results:
            if r.has_warnings and not r.has_errors:
                out.append(f"### `{r.commit_hash[:8]}` {r.header}\n")
                for issue in r.issues:
                    out.append(f"- ⚠️ **{issue.rule}**: {issue.message}")
                out.append("")

    return "\n".join(out)


# --- Init Config ---

def init_config(path: str = ".commitlintrc.json"):
    """Generate a default config file."""
    config = dict(DEFAULT_CONFIG)
    config.pop("ignore_patterns")  # keep defaults internally

    with open(path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Created {path} with default configuration")
    print("Edit this file to customize commit message rules.")


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="Lint git commit messages against configurable rules",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Lint last commit
  %(prog)s --range HEAD~5..HEAD      # Lint last 5 commits
  %(prog)s --range main..feature     # Lint branch commits
  %(prog)s --message "feat: add X"   # Lint a single message
  %(prog)s --stdin                   # Read message from stdin
  %(prog)s --format json             # JSON output for CI
  %(prog)s init                      # Generate config file
        """
    )

    sub = parser.add_subparsers(dest="command")
    sub.add_parser("init", help="Generate default .commitlintrc.json")

    parser.add_argument("--range", "-r", default="HEAD~1..HEAD",
        help="Git rev range to lint (default: HEAD~1..HEAD)")
    parser.add_argument("--message", "-m",
        help="Lint a single message string")
    parser.add_argument("--stdin", action="store_true",
        help="Read commit message from stdin")
    parser.add_argument("--file", "-f",
        help="Read commit message from file")
    parser.add_argument("--config", "-c",
        help="Path to config file")
    parser.add_argument("--format", choices=["text", "json", "markdown"],
        default="text", help="Output format (default: text)")
    parser.add_argument("--verbose", "-v", action="store_true",
        help="Show passing commits too")
    parser.add_argument("--strict", action="store_true",
        help="Treat warnings as errors")

    args = parser.parse_args()

    # Handle init command
    if args.command == "init":
        init_config()
        return

    # Load config
    config = load_config(args.config)

    # Get messages to lint
    results = []

    if args.message:
        results.append(lint_message(args.message, config))
    elif args.stdin:
        message = sys.stdin.read().strip()
        results.append(lint_message(message, config))
    elif args.file:
        with open(args.file, "r") as f:
            message = f.read().strip()
        results.append(lint_message(message, config))
    else:
        commits = get_commits_from_git(args.range)
        for commit_hash, message in commits:
            results.append(lint_message(message, config, commit_hash))

    # Format output
    if args.format == "json":
        print(format_json(results))
    elif args.format == "markdown":
        print(format_markdown(results))
    else:
        print(format_text(results, args.verbose))

    # Exit code
    has_errors = any(r.has_errors for r in results)
    has_warnings = any(r.has_warnings for r in results)

    if has_errors:
        sys.exit(1)
    elif args.strict and has_warnings:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
