#!/usr/bin/env python3
"""
Composer JSON Validator
Validate and lint PHP Composer composer.json files.
Usage: python3 composer_json_validator.py <command> <file> [--strict] [--format text|json|markdown]
Commands: lint, dependencies, scripts, validate
"""

import json
import sys
import os
import re
import argparse
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_TYPES = {"library", "project", "metapackage", "composer-plugin"}

# Common SPDX identifiers (non-exhaustive but covers real-world packages)
SPDX_IDENTIFIERS = {
    "MIT", "Apache-2.0", "GPL-2.0", "GPL-2.0-only", "GPL-2.0-or-later",
    "GPL-3.0", "GPL-3.0-only", "GPL-3.0-or-later", "LGPL-2.0", "LGPL-2.1",
    "LGPL-2.1-only", "LGPL-2.1-or-later", "LGPL-3.0", "LGPL-3.0-only",
    "LGPL-3.0-or-later", "BSD-2-Clause", "BSD-3-Clause", "ISC", "MPL-2.0",
    "AGPL-3.0", "AGPL-3.0-only", "AGPL-3.0-or-later", "CC0-1.0",
    "Unlicense", "WTFPL", "Zlib", "PHP-3.0", "PHP-3.01", "proprietary",
    "EUPL-1.1", "EUPL-1.2", "CDDL-1.0", "EPL-1.0", "EPL-2.0",
    "CPAL-1.0", "OSL-3.0", "AFL-3.0", "Artistic-2.0",
}

# Dev-only packages that should not appear in require
DEV_PACKAGES = {
    "phpunit/phpunit", "mockery/mockery", "phpspec/phpspec",
    "behat/behat", "codeception/codeception", "infection/infection",
    "phpstan/phpstan", "squizlabs/php_codesniffer", "friendsofphp/php-cs-fixer",
    "vimeo/psalm", "phpmd/phpmd", "sebastian/phpcpd",
    "brainmaestro/composer-git-hooks", "roave/security-advisories",
    "symfony/phpunit-bridge", "laravel/dusk",
}

# Valid version constraint prefixes/patterns
VALID_CONSTRAINT_RE = re.compile(
    r'^('
    r'\*'                           # wildcard (detected separately as warning)
    r'|dev-\S+'                     # dev branch
    r'|[0-9]+(\.[0-9x\*]+)*'       # numeric like 1.2.3 or 1.2.*
    r'|\^[0-9]'                     # caret
    r'|~[0-9]'                      # tilde
    r'|>=?\s*[0-9]'                 # >= or >
    r'|<=?\s*[0-9]'                 # <= or <
    r'|!=\s*[0-9]'                  # !=
    r'|@(stable|RC|beta|alpha|dev)' # stability flags
    r').*$'
)

# Patterns that look like arbitrary URL execution in scripts
URL_EXEC_RE = re.compile(r'(curl|wget)\s+.*https?://', re.IGNORECASE)

# Absolute path patterns
ABSOLUTE_PATH_RE = re.compile(r'^/')


# ---------------------------------------------------------------------------
# Issue dataclass-like
# ---------------------------------------------------------------------------

class Issue:
    LEVELS = ("error", "warning", "info")

    def __init__(self, level: str, field: str, message: str):
        assert level in self.LEVELS
        self.level = level
        self.field = field
        self.message = message

    def to_dict(self) -> dict:
        return {"level": self.level, "field": self.field, "message": self.message}

    def __repr__(self):
        return f"Issue({self.level}, {self.field!r}, {self.message!r})"


# ---------------------------------------------------------------------------
# Lint rules
# ---------------------------------------------------------------------------

def _parse_json(path: str):
    """Returns (data, error_issue). One of them is None."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, Issue("error", "json", f"Invalid JSON: {e}")
    except FileNotFoundError:
        return None, Issue("error", "file", f"File not found: {path}")
    except OSError as e:
        return None, Issue("error", "file", f"Cannot read file: {e}")


def _check_structure(data: dict) -> list:
    issues = []

    # Rule 2: Required fields
    for field in ("name", "description", "type"):
        if field not in data:
            issues.append(Issue("error", field, f"Required field '{field}' is missing"))

    # Rule 3: Package name format
    name = data.get("name", "")
    if name and not re.match(r'^[a-z0-9]([a-z0-9_.-]*[a-z0-9])?/[a-z0-9]([a-z0-9_.-]*[a-z0-9])?$', name):
        issues.append(Issue("error", "name",
            f"Package name '{name}' must match vendor/package format (lowercase, alphanumeric, hyphens, dots)"))

    # Rule 4: Valid type
    pkg_type = data.get("type", "")
    if pkg_type and pkg_type not in VALID_TYPES:
        issues.append(Issue("error", "type",
            f"Invalid type '{pkg_type}'. Must be one of: {', '.join(sorted(VALID_TYPES))}"))

    # Rule 5: License
    license_val = data.get("license")
    if not license_val:
        issues.append(Issue("warning", "license", "license field is missing"))
    else:
        # license can be a string or list
        licenses = [license_val] if isinstance(license_val, str) else license_val
        for lic in licenses:
            # Strip SPDX expression operators
            clean = re.sub(r'\s+(AND|OR|WITH)\s+', ' ', lic).strip()
            parts = clean.split()
            for part in parts:
                part = part.strip('()')
                if part and part not in SPDX_IDENTIFIERS:
                    issues.append(Issue("warning", "license",
                        f"License '{part}' may not be a valid SPDX identifier"))
                    break

    return issues


def _check_version_constraint(pkg: str, version: str) -> Issue | None:
    """Validate a single version constraint string."""
    # Split on || and spaces for compound constraints
    parts = re.split(r'\s*\|\|\s*|\s*,\s*', version)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if not VALID_CONSTRAINT_RE.match(part):
            return Issue("error", "dependencies",
                f"Package '{pkg}' has invalid version constraint: '{version}'")
    return None


def _check_dependencies(data: dict) -> list:
    issues = []
    require = data.get("require", {})
    require_dev = data.get("require-dev", {})

    # Rule 6: No duplicates between require and require-dev
    overlap = set(require.keys()) & set(require_dev.keys())
    for pkg in sorted(overlap):
        issues.append(Issue("error", "dependencies",
            f"Package '{pkg}' appears in both require and require-dev"))

    # Rules 7, 8, 9, 10, 11 — iterate require
    has_php = False
    for pkg, version in require.items():
        if pkg == "php":
            has_php = True
        # Rule 7: valid constraints
        issue = _check_version_constraint(pkg, version)
        if issue:
            issues.append(issue)
        # Rule 8: dev packages in require
        if pkg.lower() in DEV_PACKAGES:
            issues.append(Issue("warning", "dependencies",
                f"Dev package '{pkg}' found in require — should be in require-dev"))
        # Rule 9: wildcard versions (non-ext packages)
        if version.strip() == "*" and not pkg.startswith("ext-"):
            issues.append(Issue("warning", "dependencies",
                f"Package '{pkg}' uses wildcard '*' version constraint — be explicit"))
        # Rule 11: ext-* should not be *
        if pkg.startswith("ext-") and version.strip() == "*":
            issues.append(Issue("warning", "dependencies",
                f"Extension '{pkg}' uses wildcard '*' — specify an explicit constraint (e.g. '*' is acceptable for extensions, but document intent)"))

    # Rule 10: PHP version constraint
    if not has_php and require:
        issues.append(Issue("warning", "dependencies",
            "No 'php' version constraint in require — add one to declare minimum PHP version"))

    # Also validate require-dev constraints
    for pkg, version in require_dev.items():
        issue = _check_version_constraint(pkg, version)
        if issue:
            issues.append(issue)
        if version.strip() == "*":
            issues.append(Issue("warning", "dependencies",
                f"Package '{pkg}' in require-dev uses wildcard '*' version constraint"))

    return issues


def _check_autoload(data: dict) -> list:
    issues = []
    autoload = data.get("autoload", {})
    autoload_dev = data.get("autoload-dev", {})

    # Rule 12: PSR-4 autoload defined
    psr4 = autoload.get("psr-4", {})
    if not psr4:
        issues.append(Issue("warning", "autoload",
            "No PSR-4 autoload defined — add 'autoload.psr-4' mapping"))

    # Rule 13 & 14: Namespace format and duplicates
    all_namespaces = list(psr4.keys())
    seen_namespaces = set()
    for ns, path in psr4.items():
        # Rule 13: namespace should end with \\
        if ns and not ns.endswith("\\"):
            issues.append(Issue("warning", "autoload",
                f"PSR-4 namespace '{ns}' should end with '\\\\' per convention"))
        # Rule 14: duplicate namespaces
        ns_lower = ns.lower()
        if ns_lower in seen_namespaces:
            issues.append(Issue("error", "autoload",
                f"Duplicate PSR-4 namespace '{ns}' in autoload"))
        seen_namespaces.add(ns_lower)
        # Rule 21: no absolute paths
        paths = [path] if isinstance(path, str) else path
        for p in paths:
            if ABSOLUTE_PATH_RE.match(p):
                issues.append(Issue("warning", "autoload",
                    f"Absolute path '{p}' in autoload for namespace '{ns}' — use relative paths"))

    # Rule 15: autoload-dev should be separate
    dev_psr4 = autoload_dev.get("psr-4", {})
    # If autoload has test-like namespaces (ending in Test\ or Tests\), suggest moving to autoload-dev
    for ns in all_namespaces:
        if re.search(r'\\Tests?\\$', ns) or ns.lower().endswith('\\test\\') or ns.lower().endswith('\\tests\\'):
            if not dev_psr4:
                issues.append(Issue("info", "autoload",
                    f"Test namespace '{ns}' in autoload — consider moving to autoload-dev"))

    return issues


def _check_best_practices(data: dict) -> list:
    issues = []

    # Rule 16: scripts section
    if "scripts" not in data:
        issues.append(Issue("info", "scripts",
            "No 'scripts' section — consider adding common scripts (test, lint, cs-fix)"))

    # Rule 17: no URL execution in scripts
    scripts = data.get("scripts", {})
    for hook, cmds in scripts.items():
        if isinstance(cmds, str):
            cmds = [cmds]
        if isinstance(cmds, list):
            for cmd in cmds:
                if isinstance(cmd, str) and URL_EXEC_RE.search(cmd):
                    issues.append(Issue("error", "scripts",
                        f"Script '{hook}' executes a URL command: '{cmd[:80]}' — security risk"))

    # Rule 18: config.sort-packages
    config = data.get("config", {})
    if not config.get("sort-packages", False):
        issues.append(Issue("info", "config",
            "config.sort-packages is not enabled — set to true for deterministic ordering"))

    # Rules 19 & 20: minimum-stability and prefer-stable
    min_stability = data.get("minimum-stability", "stable")
    if min_stability != "stable":
        issues.append(Issue("warning", "minimum-stability",
            f"minimum-stability is '{min_stability}' — only use non-stable if required"))
        prefer_stable = data.get("prefer-stable")
        if not prefer_stable:
            issues.append(Issue("warning", "prefer-stable",
                "prefer-stable should be set to true when minimum-stability is not 'stable'"))

    # Rule 22: repository URLs use HTTPS
    repositories = data.get("repositories", [])
    if isinstance(repositories, list):
        repo_items = repositories
    elif isinstance(repositories, dict):
        repo_items = list(repositories.values())
    else:
        repo_items = []

    for repo in repo_items:
        if not isinstance(repo, dict):
            continue
        url = repo.get("url", "")
        if url and url.startswith("http://"):
            issues.append(Issue("warning", "repositories",
                f"Repository URL uses HTTP instead of HTTPS: '{url}'"))

    return issues


def run_lint(data: dict) -> list:
    """Run all lint checks and return list of Issues."""
    issues = []
    issues.extend(_check_structure(data))
    issues.extend(_check_dependencies(data))
    issues.extend(_check_autoload(data))
    issues.extend(_check_best_practices(data))
    return issues


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_lint(data: dict, path: str) -> dict:
    issues = run_lint(data)
    return {
        "command": "lint",
        "file": path,
        "issues": [i.to_dict() for i in issues],
        "summary": _summary(issues),
    }


def cmd_dependencies(data: dict, path: str) -> dict:
    require = data.get("require", {})
    require_dev = data.get("require-dev", {})
    issues = _check_dependencies(data)
    return {
        "command": "dependencies",
        "file": path,
        "require": require,
        "require_dev": require_dev,
        "issues": [i.to_dict() for i in issues],
        "summary": _summary(issues),
    }


def cmd_scripts(data: dict, path: str) -> dict:
    scripts = data.get("scripts", {})
    scripts_desc = data.get("scripts-descriptions", {})
    issues = []
    # Check script-related issues only
    if not scripts:
        issues.append(Issue("info", "scripts", "No scripts section defined").to_dict())
    else:
        for hook, cmds in scripts.items():
            if isinstance(cmds, str):
                cmds_list = [cmds]
            elif isinstance(cmds, list):
                cmds_list = cmds
            else:
                cmds_list = []
            for cmd in cmds_list:
                if isinstance(cmd, str) and URL_EXEC_RE.search(cmd):
                    issues.append(Issue("error", "scripts",
                        f"Script '{hook}' executes a URL: '{cmd[:80]}'").to_dict())
    return {
        "command": "scripts",
        "file": path,
        "scripts": scripts,
        "scripts_descriptions": scripts_desc,
        "issues": issues,
    }


def cmd_validate(data: dict, path: str) -> dict:
    issues = run_lint(data)
    errors = [i for i in issues if i.level == "error"]
    warnings = [i for i in issues if i.level == "warning"]
    infos = [i for i in issues if i.level == "info"]
    valid = len(errors) == 0
    return {
        "command": "validate",
        "file": path,
        "valid": valid,
        "issues": [i.to_dict() for i in issues],
        "summary": _summary(issues),
        "counts": {
            "errors": len(errors),
            "warnings": len(warnings),
            "infos": len(infos),
            "total": len(issues),
        },
    }


def _summary(issues: list) -> str:
    errors = sum(1 for i in issues if i.level == "error")
    warnings = sum(1 for i in issues if i.level == "warning")
    infos = sum(1 for i in issues if i.level == "info")
    parts = []
    if errors:
        parts.append(f"{errors} error(s)")
    if warnings:
        parts.append(f"{warnings} warning(s)")
    if infos:
        parts.append(f"{infos} info")
    return ", ".join(parts) if parts else "No issues found"


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(result: dict) -> str:
    cmd = result.get("command", "")
    path = result.get("file", "")
    lines = []
    title = f"composer.json {cmd} — {path}"
    lines.append(title)
    lines.append("=" * len(title))

    issues = result.get("issues", [])
    if not issues:
        lines.append("[OK] No issues found")
    else:
        for issue in issues:
            level = issue["level"].upper().ljust(7)
            lines.append(f"[{level}] {issue['field']}: {issue['message']}")

    # Extra sections for dependencies command
    if cmd == "dependencies":
        lines.append("")
        lines.append("require:")
        for pkg, ver in result.get("require", {}).items():
            lines.append(f"  {pkg}: {ver}")
        lines.append("")
        lines.append("require-dev:")
        for pkg, ver in result.get("require_dev", {}).items():
            lines.append(f"  {pkg}: {ver}")

    # Scripts section
    if cmd == "scripts":
        lines.append("")
        lines.append("scripts:")
        for hook, cmds in result.get("scripts", {}).items():
            if isinstance(cmds, str):
                cmds = [cmds]
            lines.append(f"  {hook}:")
            for c in (cmds if isinstance(cmds, list) else [cmds]):
                lines.append(f"    - {c}")

    # Validate summary
    if cmd == "validate":
        counts = result.get("counts", {})
        valid_str = "VALID" if result.get("valid") else "INVALID"
        lines.append("")
        lines.append(f"Result: {valid_str}")

    summary = result.get("summary")
    if summary:
        lines.append("")
        lines.append(f"Summary: {summary}")

    return "\n".join(lines)


def format_json(result: dict) -> str:
    return json.dumps(result, indent=2)


def format_markdown(result: dict) -> str:
    cmd = result.get("command", "")
    path = result.get("file", "")
    lines = []
    lines.append(f"# Composer JSON {cmd.title()} — `{path}`")
    lines.append("")

    issues = result.get("issues", [])
    if not issues:
        lines.append("**No issues found.**")
    else:
        errors = [i for i in issues if i["level"] == "error"]
        warnings = [i for i in issues if i["level"] == "warning"]
        infos = [i for i in issues if i["level"] == "info"]

        if errors:
            lines.append("## Errors")
            for i in errors:
                lines.append(f"- **{i['field']}**: {i['message']}")
            lines.append("")
        if warnings:
            lines.append("## Warnings")
            for i in warnings:
                lines.append(f"- **{i['field']}**: {i['message']}")
            lines.append("")
        if infos:
            lines.append("## Info")
            for i in infos:
                lines.append(f"- **{i['field']}**: {i['message']}")
            lines.append("")

    if cmd == "dependencies":
        lines.append("## require")
        for pkg, ver in result.get("require", {}).items():
            lines.append(f"- `{pkg}`: `{ver}`")
        lines.append("")
        lines.append("## require-dev")
        for pkg, ver in result.get("require_dev", {}).items():
            lines.append(f"- `{pkg}`: `{ver}`")
        lines.append("")

    if cmd == "scripts":
        lines.append("## Scripts")
        for hook, cmds in result.get("scripts", {}).items():
            if isinstance(cmds, str):
                cmds = [cmds]
            lines.append(f"### `{hook}`")
            for c in (cmds if isinstance(cmds, list) else [cmds]):
                lines.append(f"- `{c}`")
        lines.append("")

    if cmd == "validate":
        counts = result.get("counts", {})
        valid_str = "VALID" if result.get("valid") else "INVALID"
        lines.append(f"## Result: {valid_str}")
        lines.append("")
        lines.append(f"- Errors: {counts.get('errors', 0)}")
        lines.append(f"- Warnings: {counts.get('warnings', 0)}")
        lines.append(f"- Info: {counts.get('infos', 0)}")
        lines.append("")

    summary = result.get("summary")
    if summary:
        lines.append(f"**Summary:** {summary}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate and lint PHP Composer composer.json files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Commands:
  lint         Run all lint checks
  dependencies Inspect require/require-dev sections
  scripts      Inspect scripts section
  validate     Full validation with summary

Examples:
  python3 composer_json_validator.py lint composer.json
  python3 composer_json_validator.py validate composer.json --strict
  python3 composer_json_validator.py dependencies composer.json --format json
  python3 composer_json_validator.py scripts composer.json --format markdown
"""
    )
    parser.add_argument("command", choices=["lint", "dependencies", "scripts", "validate"],
                        help="Command to run")
    parser.add_argument("file", help="Path to composer.json")
    parser.add_argument("--strict", action="store_true",
                        help="Exit with code 1 on warnings (CI mode)")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text",
                        help="Output format (default: text)")

    args = parser.parse_args()

    # Parse file
    data, parse_error = _parse_json(args.file)
    if parse_error:
        result = {
            "command": args.command,
            "file": args.file,
            "issues": [parse_error.to_dict()],
            "summary": "1 error(s)",
        }
        if args.format == "json":
            print(format_json(result))
        elif args.format == "markdown":
            print(format_markdown(result))
        else:
            print(format_text(result))
        sys.exit(2)

    # Run command
    if args.command == "lint":
        result = cmd_lint(data, args.file)
    elif args.command == "dependencies":
        result = cmd_dependencies(data, args.file)
    elif args.command == "scripts":
        result = cmd_scripts(data, args.file)
    elif args.command == "validate":
        result = cmd_validate(data, args.file)

    # Format output
    if args.format == "json":
        print(format_json(result))
    elif args.format == "markdown":
        print(format_markdown(result))
    else:
        print(format_text(result))

    # Exit code
    issues = result.get("issues", [])
    has_errors = any(i["level"] == "error" for i in issues)
    has_warnings = any(i["level"] == "warning" for i in issues)

    if has_errors:
        sys.exit(1)
    if args.strict and has_warnings:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
