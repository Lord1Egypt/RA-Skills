#!/usr/bin/env python3
"""
skill-portabilizer — Audit an agent skill for platform lock-in and cross-agent compatibility.

Usage:
    python3 audit.py <skill_dir>              # audit only, show findings
    python3 audit.py <skill_dir> --fix        # audit, auto-fix, show brief summary
    python3 audit.py <skill_dir> --json       # structured JSON output

Two-phase flow:
  1. Audit  — show all findings (auto-fixable + manual)
  2. --fix  — apply auto-fixes, show brief "what changed" confirmation
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

VERSION = "1.1.3"

# --- Patterns ---

HARDCODED_PATH_PATTERNS = [
    r'~/.openclaw/',
    r'/home/[a-zA-Z0-9_]+/',
    r'/Users/[a-zA-Z0-9_]+/',
]

PLATFORM_UA_PATTERN = re.compile(r'["\']User-Agent["\']:\s*["\'][^"\']*openclaw[^"\']*["\']', re.IGNORECASE)
SKILL_DATA_DIR_PATTERN = re.compile(r'SKILL_DATA_DIR')
XDG_FALLBACK_PATTERN = re.compile(r'~/.config/')

SETUP_SCRIPT_NAMES = {'setup.py', 'setup.sh', 'install.py', 'configure.py'}


def find_files(skill_dir, extensions=None):
    """Recursively find files in skill directory."""
    if extensions is None:
        extensions = {'.py', '.sh', '.js', '.ts', '.md', '.json', '.yaml', '.yml', '.toml'}
    found = []
    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '__pycache__', 'venv')]
        for f in files:
            if any(f.endswith(ext) for ext in extensions):
                found.append(os.path.join(root, f))
    return found


def is_pattern_definition(content, pos):
    """Check if a match is inside a pattern string literal (not actual usage)."""
    before = content[max(0, pos - 200):pos]
    indicators = ['HARDCODED_PATH_PATTERNS', 'cli_invocation_patterns', 'startswith(', '.replace(', 'r"']
    for ind in indicators:
        if ind in before[-100:]:
            return True
    return False


def read_file(path):
    """Read file contents, return None on error."""
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except (IOError, OSError):
        return None


def rel_path(skill_dir, file_path):
    """Relative path from skill dir."""
    return os.path.relpath(file_path, skill_dir)


# --- Checks ---

def check_hardcoded_paths(skill_dir, files):
    """Find hardcoded platform-specific paths. Skips references/ docs."""
    # Filter to source files only (skip reference/example docs)
    source_files = [f for f in files if '/references/' not in f]
    issues = []
    for fpath in source_files:
        content = read_file(fpath)
        if content is None:
            continue
        rel = rel_path(skill_dir, fpath)
        for pattern in HARDCODED_PATH_PATTERNS:
            for match in re.finditer(pattern, content):
                if is_pattern_definition(content, match.start()):
                    continue
                line_num = content[:match.start()].count('\n') + 1
                line_text = content.split('\n')[line_num - 1].strip()
                issues.append({
                    "check": "hardcoded_path",
                    "file": rel,
                    "line": line_num,
                    "match": match.group(),
                    "context": line_text[:120],
                    "severity": "error" if fpath.endswith(('.py', '.sh', '.js')) else "warn",
                    "auto_fixable": fpath.endswith(('.py', '.sh', '.js')),
                })
    return issues


def check_skill_data_dir(files):
    """Check if scripts use SKILL_DATA_DIR for path resolution."""
    script_files = [f for f in files if f.endswith(('.py', '.sh', '.js'))]
    has_data_dir = False
    for fpath in script_files:
        content = read_file(fpath)
        if content is None:
            continue
        if SKILL_DATA_DIR_PATTERN.search(content):
            has_data_dir = True
            break
    return {"has_support": has_data_dir}


def check_xdg_fallback(files):
    """Check if scripts have XDG fallback paths."""
    script_files = [f for f in files if f.endswith(('.py', '.sh', '.js'))]
    has_fallback = False
    for fpath in script_files:
        content = read_file(fpath)
        if content is None:
            continue
        if XDG_FALLBACK_PATTERN.search(content):
            has_fallback = True
            break
    return {"has_fallback": has_fallback}


def check_platform_cli(skill_dir, files):
    """Check for platform-specific CLI tool dependencies.
    
    Only flags actual CLI invocations (subprocess, os.system, shell calls),
    not string data keys, variable names, or regex pattern definitions.
    """
    issues = []
    script_files = [f for f in files if f.endswith(('.py', '.sh', '.js'))]
    cli_invocation_patterns = [
        r'subprocess\.(run|call|Popen|check_output).*["\']clawhub["\']',
        r'subprocess\.(run|call|Popen|check_output).*["\']openclaw["\']',
        r'os\.system.*["\']clawhub',
        r'os\.system.*["\']openclaw',
        r'"clawhub".*\]',
    ]
    for fpath in script_files:
        content = read_file(fpath)
        if content is None:
            continue
        rel = rel_path(skill_dir, fpath)
        seen_lines = set()
        for pattern in cli_invocation_patterns:
            for i, line in enumerate(content.split('\n'), 1):
                stripped = line.strip()
                if stripped.startswith('#') or stripped.startswith('//'):
                    continue
                # Skip regex pattern definitions (r'..., r"...)
                line_start = stripped[:50]
                if line_start.startswith("r'") or line_start.startswith('r"'):
                    continue
                if re.search(pattern, line):
                    if i in seen_lines:
                        continue
                    seen_lines.add(i)
                    tool = "clawhub CLI" if 'clawhub' in pattern else "openclaw CLI"
                    issues.append({
                        "check": "platform_cli",
                        "file": rel,
                        "line": i,
                        "tool": tool,
                        "context": stripped[:120],
                        "severity": "warn",
                        "auto_fixable": False,
                    })
    return issues


def check_user_agent(skill_dir, files):
    """Check for platform names in User-Agent strings."""
    issues = []
    for fpath in files:
        if not fpath.endswith(('.py', '.sh', '.js')):
            continue
        content = read_file(fpath)
        if content is None:
            continue
        match = PLATFORM_UA_PATTERN.search(content)
        if match:
            rel = rel_path(skill_dir, fpath)
            line_num = content[:match.start()].count('\n') + 1
            issues.append({
                "check": "user_agent",
                "file": rel,
                "line": line_num,
                "match": match.group(),
                "severity": "warn",
                "auto_fixable": True,
            })
    return issues


def check_skill_md_paths(skill_dir, files):
    """Check SKILL.md for hardcoded path references."""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    content = read_file(skill_md)
    if content is None:
        return []
    issues = []
    for pattern in HARDCODED_PATH_PATTERNS:
        for match in re.finditer(pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            line_text = content.split('\n')[line_num - 1].strip()
            issues.append({
                "check": "skill_md_path",
                "line": line_num,
                "match": match.group(),
                "context": line_text[:120],
                "severity": "warn",
                "auto_fixable": True,
            })
    return issues


def check_headless_setup(skill_dir, files):
    """Check if setup scripts support --no-browser for headless machines."""
    issues = []
    for fpath in files:
        fname = os.path.basename(fpath)
        if fname not in SETUP_SCRIPT_NAMES:
            continue
        content = read_file(fpath)
        if content is None:
            continue
        has_browser = any(kw in content for kw in ['run_local_server', 'webbrowser.open', 'open_browser'])
        # Check for --no-browser in actual code, not comments
        has_no_browser = any(
            '--no-browser' in line and not line.strip().startswith('#')
            for line in content.split('\n')
        ) or 'no.browser' in content
        if has_browser and not has_no_browser:
            issues.append({
                "check": "headless_setup",
                "file": rel_path(skill_dir, fpath),
                "detail": "Setup script opens a browser but lacks --no-browser flag for headless machines",
                "severity": "info",
                "auto_fixable": False,
            })
    return issues


def check_credential_env_var(files):
    """Check if credentials support env var as alternative to file.

    Broad match: if a script has file-based credential loading AND any
    os.environ.get/os.getenv calls with credential-related variable names,
    consider env vars supported.
    """
    script_files = [f for f in files if f.endswith(('.py', '.sh', '.js'))]
    has_file_creds = False
    has_env_var = False
    cred_words = ['TOKEN', 'KEY', 'SECRET', 'API', 'PASSWORD', 'USERNAME', 'AUTH', 'CREDENTIAL']
    for fpath in script_files:
        content = read_file(fpath)
        if content is None:
            continue
        # Check for env var access with credential-related names
        env_var_pattern = r'["\x27]([A-Z_]{3,}(?:' + '|'.join(cred_words) + r')[A-Z_]*)["\x27]'
        for match in re.finditer(r'os\.environ\.get\(|os\.environ\[|os\.getenv\(', content):
            after = content[match.start():match.start() + 200]
            if re.search(env_var_pattern, after):
                has_env_var = True
                break
        # Also check dotenv/load_dotenv patterns (common for env var loading)
        if 'load_dotenv' in content or 'dotenv' in content:
            has_env_var = True
        if 'CREDENTIALS_PATH' in content or 'CREDS_PATH' in content or 'credentials' in content.lower():
            has_file_creds = True
    return {
        "has_file_credentials": has_file_creds,
        "has_env_var_alternative": has_env_var,
        "needs_env_var": has_file_creds and not has_env_var,
    }


# --- Core ---

def run_audit(skill_dir):
    """Run all checks and return audit results."""
    skill_dir = os.path.abspath(skill_dir)
    if not os.path.isdir(skill_dir):
        print(f"Error: {skill_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    skill_name = os.path.basename(skill_dir)
    files = find_files(skill_dir)

    result = {
        "skill": skill_name,
        "path": skill_dir,
        "version": VERSION,
        "checks": {},
        "summary": {},
    }

    result["checks"]["hardcoded_paths"] = check_hardcoded_paths(skill_dir, files)
    result["checks"]["skill_data_dir"] = check_skill_data_dir(files)
    result["checks"]["xdg_fallback"] = check_xdg_fallback(files)
    result["checks"]["platform_cli"] = check_platform_cli(skill_dir, files)
    result["checks"]["user_agent"] = check_user_agent(skill_dir, files)
    result["checks"]["skill_md_paths"] = check_skill_md_paths(skill_dir, files)
    result["checks"]["headless_setup"] = check_headless_setup(skill_dir, files)
    result["checks"]["credential_env_vars"] = check_credential_env_var(files)

    # Tally
    all_issues = (
        result["checks"]["hardcoded_paths"] +
        result["checks"]["platform_cli"] +
        result["checks"]["user_agent"] +
        result["checks"]["skill_md_paths"] +
        result["checks"]["headless_setup"]
    )

    errors = sum(1 for i in all_issues if i.get("severity") == "error")
    warnings = sum(1 for i in all_issues if i.get("severity") == "warn")
    infos = sum(1 for i in all_issues if i.get("severity") == "info")
    auto_fixable = sum(1 for i in all_issues if i.get("auto_fixable"))
    manual = errors + warnings + infos - auto_fixable

    # Count distinct checks that passed
    has_path_issues = len(result["checks"]["hardcoded_paths"]) > 0
    check_results = [
        ("hardcoded_paths", not has_path_issues),
        ("skill_data_dir", result["checks"]["skill_data_dir"]["has_support"] or not has_path_issues),
        ("xdg_fallback", result["checks"]["xdg_fallback"]["has_fallback"] or not has_path_issues),
        ("platform_cli", len(result["checks"]["platform_cli"]) == 0),
        ("user_agent", len(result["checks"]["user_agent"]) == 0),
        ("skill_md_paths", len(result["checks"]["skill_md_paths"]) == 0),
        ("headless_setup", len(result["checks"]["headless_setup"]) == 0),
        ("credential_env_vars", not result["checks"]["credential_env_vars"].get("needs_env_var")),
    ]
    passed = sum(1 for _, ok in check_results if ok)
    cred_needs_env = result["checks"]["credential_env_vars"].get("needs_env_var")

    result["summary"] = {
        "passed": passed,
        "total_checks": 8,
        "errors": errors,
        "warnings": warnings,
        "infos": infos,
        "auto_fixable": auto_fixable,
        "manual": manual,
        "is_portable": errors == 0 and warnings == 0 and infos == 0 and not cred_needs_env,
        "verdict": "fully_portable" if (errors == 0 and warnings == 0 and infos == 0)
                  else "portable_with_warnings" if errors == 0
                  else "not_portable",
    }

    return result


def format_audit(result):
    """Format audit findings — phase 1 output."""
    s = result["summary"]
    lines = []

    if s["is_portable"]:
        lines.append(f"✅ {result['skill']} — Fully portable")
        lines.append(f"   All {s['total_checks']} checks passed")
        return "\n".join(lines)

    lines.append(f"🔍 Audit: {result['skill']}")
    lines.append("")
    lines.append(f"   {s['passed']}/{s['total_checks']} checks passed · ❌ {s['errors']} issues · 🔧 {s['auto_fixable']} auto-fixable · ⚠ {s['manual']} manual")

    # Auto-fixable findings
    auto_items = []
    for item in result["checks"]["hardcoded_paths"]:
        if item.get("auto_fixable"):
            auto_items.append(item)
    for item in result["checks"]["user_agent"]:
        if item.get("auto_fixable"):
            auto_items.append(item)
    for item in result["checks"]["skill_md_paths"]:
        if item.get("auto_fixable"):
            auto_items.append(item)

    if auto_items:
        lines.append("")
        lines.append("❌ Issues (auto-fixable with --fix)")
        for item in auto_items:
            if item["check"] in ("hardcoded_path", "skill_md_path"):
                loc = f"{item['file']}:{item['line']}" if "file" in item else f"SKILL.md:{item['line']}"
                lines.append(f"   {item['match']}")
                lines.append(f"   → {loc}")
            elif item["check"] == "user_agent":
                loc = f"{item['file']}:{item['line']}" if "file" in item else "?"
                lines.append(f"   {item['match']}")
                lines.append(f"   → {loc}")

    # Manual findings
    manual_items = []
    for item in result["checks"]["platform_cli"]:
        manual_items.append(item)
    for item in result["checks"]["headless_setup"]:
        manual_items.append(item)
    # Credential env var check
    if result["checks"]["credential_env_vars"].get("needs_env_var"):
        manual_items.append({
            "check": "credential_env_vars",
            "detail": "Credentials loaded from file only — no env var alternative",
        })
    # Missing SKILL_DATA_DIR / XDG (only flag if there are hardcoded paths to fix)
    if result["checks"]["hardcoded_paths"] and not result["checks"]["skill_data_dir"]["has_support"]:
        manual_items.append({
            "check": "skill_data_dir",
            "detail": "No SKILL_DATA_DIR support — scripts use hardcoded paths",
        })
    if result["checks"]["hardcoded_paths"] and not result["checks"]["xdg_fallback"]["has_fallback"]:
        manual_items.append({
            "check": "xdg_fallback",
            "detail": "No XDG fallback (~/.config/) path configured",
        })

    if manual_items:
        lines.append("")
        lines.append("⚠ Manual review needed")
        for item in manual_items:
            if item["check"] == "platform_cli":
                lines.append(f"   {item['tool']} in {item['file']}:{item['line']}")
                lines.append(f"   Platform-specific dependency — cannot auto-fix")
            elif item["check"] == "headless_setup":
                lines.append(f"   {item['file']}")
                lines.append(f"   {item['detail']}")
            else:
                lines.append(f"   {item['detail']}")

    lines.append("")
    lines.append(f"📌 {s['auto_fixable']} auto-fixable · {s['manual']} manual · Run with --fix to apply")

    return "\n".join(lines)


def apply_fixes(result):
    """Auto-fix what we can. Returns list of changes made."""
    skill_dir = result["path"]
    changes = []

    for item in result["checks"]["hardcoded_paths"]:
        if not item.get("auto_fixable"):
            continue
        fpath = os.path.join(skill_dir, item["file"])
        content = read_file(fpath)
        if content is None:
            continue

        old_path = item["match"]

        if old_path.startswith("~/.openclaw/credentials"):
            new_path = "$SKILL_DATA_DIR"
        elif old_path.startswith("~/.openclaw/workspace/data/"):
            rest = old_path.replace("~/.openclaw/workspace/data/", "")
            new_path = "$SKILL_DATA_DIR/" + rest
        else:
            new_path = "<portable-path>"

        if old_path in content:
            content = content.replace(old_path, new_path, 1)
            changes.append({"file": item["file"], "old": old_path, "new": new_path})

        with open(fpath, 'w') as f:
            f.write(content)

    # Fix User-Agent
    for item in result["checks"]["user_agent"]:
        if not item.get("auto_fixable"):
            continue
        fpath = os.path.join(skill_dir, item["file"])
        content = read_file(fpath)
        if content is None:
            continue

        old_ua = item["match"]
        # Strip platform name from UA
        new_ua = re.sub(r'openclaw[-_]', '', old_ua, flags=re.IGNORECASE)
        if new_ua != old_ua and old_ua in content:
            content = content.replace(old_ua, new_ua, 1)
            # Extract the UA value (after colon, between quotes)
            old_display = re.search(r':\s*["\']([^"\']+)["\']', old_ua)
            new_display = re.search(r':\s*["\']([^"\']+)["\']', new_ua)
            changes.append({
                "file": item["file"],
                "old": old_display.group(1) if old_display else old_ua,
                "new": new_display.group(1) if new_display else new_ua,
            })

        with open(fpath, 'w') as f:
            f.write(content)

    # Fix SKILL.md paths
    for item in result["checks"]["skill_md_paths"]:
        if not item.get("auto_fixable"):
            continue
        fpath = os.path.join(skill_dir, "SKILL.md")
        content = read_file(fpath)
        if content is None:
            continue

        old_path = item["match"]
        new_path = "<DATA_DIR>"
        if old_path in content:
            content = content.replace(old_path, new_path, 1)
            changes.append({"file": "SKILL.md", "old": old_path, "new": new_path})

        with open(fpath, 'w') as f:
            f.write(content)

    return changes


def format_fix_summary(result, changes):
    """Format brief fix confirmation — phase 2 output."""
    s = result["summary"]
    remaining_manual = s["manual"]

    lines = []
    lines.append(f"✅ Fixed: {len(changes)} issue{'s' if len(changes) != 1 else ''} resolved")
    lines.append("")

    for c in changes:
        lines.append(f"   {c['old']} → {c['new']}")
        lines.append(f"   in {c['file']}")

    if remaining_manual > 0:
        lines.append("")
        lines.append(f"⚠ {remaining_manual} manual item{'s' if remaining_manual != 1 else ''} still needs review")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit agent skills for cross-platform portability")
    parser.add_argument("skill_dir", help="Path to skill directory")
    parser.add_argument("--fix", action="store_true", help="Audit, auto-fix, show brief summary")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--version", action="version", version=f"skill-portabilizer {VERSION}")

    args = parser.parse_args()
    result = run_audit(args.skill_dir)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    if args.fix:
        # Phase 1: brief audit summary
        s = result["summary"]
        if s["is_portable"]:
            print(f"✅ {result['skill']} — Already fully portable. No fixes needed.")
            return

        print(f"🔍 {result['skill']} — {s['auto_fixable']} issues to fix, {s['manual']} manual")
        print("")

        # Phase 2: apply and show changes
        if s["auto_fixable"] > 0:
            changes = apply_fixes(result)
            print(format_fix_summary(result, changes))
        else:
            print("🔧 No auto-fixable issues.")
    else:
        # Audit only
        print(format_audit(result))


if __name__ == "__main__":
    main()
