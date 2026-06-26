#!/usr/bin/env python3
"""Sui Move smart contract audit script.

Runs ``sui move build --lint`` and custom static analysis on Move source files,
then outputs a unified JSON audit report.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _which(binary: str) -> str | None:
    for d in os.environ.get("PATH", "").split(os.pathsep):
        p = os.path.join(d, binary)
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


def _run(cmd: list[str], cwd: str, timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def _tool_version(binary: str) -> str:
    try:
        r = _run([binary, "--version"], cwd=".")
        return (r.stdout or r.stderr).strip().split("\n")[0]
    except Exception:
        return "unknown"


def check_tools_only() -> dict:
    tools = {
        "sui": {"install_hint": "cargo install --locked --git https://github.com/MystenLabs/sui.git sui"},
    }
    result = {}
    for name, info in tools.items():
        path = _which(name)
        result[name] = {
            "installed": path is not None,
            "path": path,
            "version": _tool_version(name) if path else None,
            "install_hint": info["install_hint"],
        }
    return result


# ---------------------------------------------------------------------------
# Sui Move build + lint
# ---------------------------------------------------------------------------

def _run_sui_build(project_path: str, findings: list, errors: list, versions: dict):
    """Run ``sui move build --lint``."""
    if not _which("sui"):
        errors.append({
            "tool": "sui",
            "error": "tool_not_found",
            "message": "sui CLI is not installed or not in PATH",
            "install_hint": "cargo install --locked --git https://github.com/MystenLabs/sui.git sui",
        })
        return

    versions["sui"] = _tool_version("sui")

    # Try build with lint
    try:
        r = _run(["sui", "move", "build", "--lint"], cwd=project_path, timeout=300)
        combined = (r.stdout or "") + "\n" + (r.stderr or "")

        for line in combined.split("\n"):
            line = line.strip()
            if not line:
                continue

            # Parse warnings and errors
            if "warning" in line.lower():
                loc = _extract_move_location(line, project_path)
                findings.append({
                    "severity": "low",
                    "title": "Build warning",
                    "location": loc,
                    "description": line,
                    "recommendation": "Review and fix the compiler warning.",
                    "tool": "sui-move-build",
                })
            elif "error" in line.lower() and "───" not in line:
                loc = _extract_move_location(line, project_path)
                findings.append({
                    "severity": "high",
                    "title": "Compilation error",
                    "location": loc,
                    "description": line,
                    "recommendation": "Fix the compilation error before proceeding.",
                    "tool": "sui-move-build",
                })

        # Lint-specific output (sui move build --lint outputs lint warnings)
        for line in combined.split("\n"):
            if "Lint" in line or "lint" in line.lower():
                if "warning" in line.lower() or "error" in line.lower():
                    loc = _extract_move_location(line, project_path)
                    findings.append({
                        "severity": "medium",
                        "title": "Lint issue",
                        "location": loc,
                        "description": line,
                        "recommendation": "Address the lint warning for code quality.",
                        "tool": "sui-move-lint",
                    })

    except subprocess.TimeoutExpired:
        errors.append({
            "tool": "sui-move-build",
            "error": "execution_failed",
            "message": "sui move build timed out after 300s",
        })
    except Exception as exc:
        errors.append({
            "tool": "sui-move-build",
            "error": "execution_failed",
            "message": str(exc),
        })


# ---------------------------------------------------------------------------
# Custom static analysis for Move source files
# ---------------------------------------------------------------------------

def _static_analysis(project_path: str, findings: list):
    """Pattern-based static analysis on .move source files."""
    move_files = list(Path(project_path).rglob("*.move"))
    move_files = [f for f in move_files if "build/" not in str(f) and "cache" not in str(f)]

    for move_file in move_files:
        try:
            content = move_file.read_text(errors="replace")
            rel_path = os.path.relpath(str(move_file), project_path)
            lines = content.split("\n")

            _check_init_function(rel_path, content, lines, findings)
            _check_object_ownership(rel_path, content, lines, findings)
            _check_ability_usage(rel_path, content, lines, findings)
            _check_shared_object_patterns(rel_path, content, lines, findings)
            _check_transfer_patterns(rel_path, content, lines, findings)
            _check_clock_usage(rel_path, content, lines, findings)
            _check_public_entry_functions(rel_path, content, lines, findings)
            _check_coin_handling(rel_path, content, lines, findings)

        except Exception:
            continue


def _check_init_function(rel_path: str, content: str, lines: list, findings: list):
    """Check init function patterns."""
    has_init = False
    for i, line in enumerate(lines, 1):
        if re.search(r"\bfun\s+init\s*\(", line):
            has_init = True
            # Check if init takes OTW (one-time witness)
            if "OTW" not in content and "witness" not in line.lower():
                findings.append({
                    "severity": "medium",
                    "title": "init() without one-time witness",
                    "location": f"{rel_path}:{i}",
                    "description": "Module init function does not appear to use a one-time witness pattern. "
                                   "This may indicate missing initialization guarantees.",
                    "recommendation": "Consider using a one-time witness (OTW) pattern for module initialization to prevent re-initialization.",
                    "tool": "static-analysis",
                })

    # Check for modules without init
    if "module" in content and not has_init:
        findings.append({
            "severity": "info",
            "title": "Module without init function",
            "location": rel_path,
            "description": "Module does not define an init function. This is fine if no initialization is needed.",
            "recommendation": "If the module needs one-time setup, add an init function.",
            "tool": "static-analysis",
        })


def _check_object_ownership(rel_path: str, content: str, lines: list, findings: list):
    """Check for potential object ownership issues."""
    for i, line in enumerate(lines, 1):
        # Transfer to tx_context::sender without checks
        if re.search(r"transfer::transfer\s*\(.*,\s*tx_context::sender\s*\(", line) or \
           re.search(r"transfer::public_transfer\s*\(.*,\s*tx_context::sender\s*\(", line):
            findings.append({
                "severity": "info",
                "title": "Object transferred to sender",
                "location": f"{rel_path}:{i}",
                "description": "Object is transferred to the transaction sender. Ensure this is the intended recipient.",
                "recommendation": "Verify that transferring to tx sender is the correct behavior.",
                "tool": "static-analysis",
            })

        # Shared objects
        if re.search(r"transfer::share_object\s*\(", line) or \
           re.search(r"transfer::public_share_object\s*\(", line):
            findings.append({
                "severity": "medium",
                "title": "Shared object creation",
                "location": f"{rel_path}:{i}",
                "description": "Creating a shared object. Shared objects can be accessed by anyone and may lead to race conditions.",
                "recommendation": "Ensure proper access control on shared object operations. Consider if owned objects would be more appropriate.",
                "tool": "static-analysis",
            })


def _check_ability_usage(rel_path: str, content: str, lines: list, findings: list):
    """Check for potentially dangerous ability combinations."""
    for i, line in enumerate(lines, 1):
        # Struct with key + store but no drop
        m = re.search(r"struct\s+\w+\s+has\s+([\w\s,]+)", line)
        if m:
            abilities = [a.strip() for a in m.group(1).split(",")]
            if "key" in abilities and "store" in abilities and "drop" not in abilities:
                findings.append({
                    "severity": "info",
                    "title": "Object with key+store without drop",
                    "location": f"{rel_path}:{i}",
                    "description": "Struct has key+store but no drop ability. Objects cannot be destroyed except via explicit unpacking.",
                    "recommendation": "Ensure there is a way to destroy this object (public destroy/burn function) or add drop if appropriate.",
                    "tool": "static-analysis",
                })

            # copy ability on objects
            if "copy" in abilities and "key" in abilities:
                findings.append({
                    "severity": "medium",
                    "title": "Object with copy ability",
                    "location": f"{rel_path}:{i}",
                    "description": "Object has both key and copy abilities. This allows duplicating the object, which may lead to double-spend.",
                    "recommendation": "Remove copy ability from objects unless duplication is intentional.",
                    "tool": "static-analysis",
                })


def _check_shared_object_patterns(rel_path: str, content: str, lines: list, findings: list):
    """Check for potentially unsafe shared object access patterns."""
    for i, line in enumerate(lines, 1):
        # Mutable borrow of shared object without access control
        if re.search(r"&mut\s+\w+.*shared", line, re.IGNORECASE):
            findings.append({
                "severity": "medium",
                "title": "Mutable access to shared object",
                "location": f"{rel_path}:{i}",
                "description": "Mutable borrow of what appears to be a shared object. Ensure access is properly controlled.",
                "recommendation": "Add appropriate access control checks before mutating shared objects.",
                "tool": "static-analysis",
            })


def _check_transfer_patterns(rel_path: str, content: str, lines: list, findings: list):
    """Check for unsafe transfer patterns."""
    for i, line in enumerate(lines, 1):
        # Freezing objects
        if re.search(r"transfer::freeze_object\s*\(", line) or \
           re.search(r"transfer::public_freeze_object\s*\(", line):
            findings.append({
                "severity": "info",
                "title": "Object freeze",
                "location": f"{rel_path}:{i}",
                "description": "Object is being frozen (made immutable). This is irreversible.",
                "recommendation": "Ensure freezing is intentional; the object can never be modified again.",
                "tool": "static-analysis",
            })


def _check_clock_usage(rel_path: str, content: str, lines: list, findings: list):
    """Check for timestamp/clock dependency."""
    for i, line in enumerate(lines, 1):
        if re.search(r"clock::timestamp_ms\s*\(", line) or \
           re.search(r"Clock", line) and "use" not in line.lower():
            if "clock" in line.lower() and "::" in line:
                findings.append({
                    "severity": "low",
                    "title": "Clock/timestamp dependency",
                    "location": f"{rel_path}:{i}",
                    "description": "Contract uses on-chain clock for time-dependent logic. Validators have some influence over timestamps.",
                    "recommendation": "Be cautious with time-dependent logic. Use reasonable time windows rather than exact timestamps.",
                    "tool": "static-analysis",
                })


def _check_public_entry_functions(rel_path: str, content: str, lines: list, findings: list):
    """Check public entry functions for potential issues."""
    for i, line in enumerate(lines, 1):
        if re.search(r"public\s+entry\s+fun\s+", line):
            # Check if function name suggests admin/privileged operation
            func_name = re.search(r"fun\s+(\w+)", line)
            if func_name:
                name = func_name.group(1).lower()
                admin_keywords = ["admin", "owner", "mint", "burn", "pause", "upgrade", "set_", "update_", "withdraw"]
                if any(kw in name for kw in admin_keywords):
                    # Check if there's an admin cap check nearby (within next 10 lines)
                    context = "\n".join(lines[i - 1:min(i + 10, len(lines))])
                    if "AdminCap" not in context and "admin_cap" not in context.lower() and "OwnerCap" not in context:
                        findings.append({
                            "severity": "high",
                            "title": f"Admin function '{func_name.group(1)}' may lack access control",
                            "location": f"{rel_path}:{i}",
                            "description": f"Public entry function '{func_name.group(1)}' appears to be an admin/privileged operation "
                                           "but does not seem to require an admin capability.",
                            "recommendation": "Add an admin capability (AdminCap) parameter to restrict access to privileged functions.",
                            "tool": "static-analysis",
                        })


def _check_coin_handling(rel_path: str, content: str, lines: list, findings: list):
    """Check for potential coin/token handling issues."""
    for i, line in enumerate(lines, 1):
        # Coin splitting/merging without balance checks
        if re.search(r"coin::split\s*\(", line):
            findings.append({
                "severity": "info",
                "title": "Coin split operation",
                "location": f"{rel_path}:{i}",
                "description": "Coin is being split. Ensure the split amount does not exceed the coin value.",
                "recommendation": "Verify that the split amount is valid and handle insufficient balance gracefully.",
                "tool": "static-analysis",
            })

        # Direct coin value extraction
        if re.search(r"coin::into_balance\s*\(", line):
            findings.append({
                "severity": "info",
                "title": "Coin to Balance conversion",
                "location": f"{rel_path}:{i}",
                "description": "Coin is converted to Balance. Ensure the resulting balance is properly managed.",
                "recommendation": "Verify that balance is stored or transferred properly after conversion.",
                "tool": "static-analysis",
            })


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _extract_move_location(line: str, project_path: str) -> str:
    """Try to extract file:line from a Move compiler message."""
    m = re.search(r"┌──\s*([\w/.]+:\d+:\d+)", line)
    if m:
        return m.group(1)
    m = re.search(r"([\w/.]+\.move:\d+)", line)
    if m:
        return m.group(1)
    return ""


def _build_summary(findings: list) -> dict:
    summary = {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        sev = f.get("severity", "info")
        summary[sev] = summary.get(sev, 0) + 1
        summary["total"] += 1
    return summary


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Sui Move contract audit")
    parser.add_argument("--path", help="Path to Sui Move project root")
    parser.add_argument("--check-tools", action="store_true", help="Only check tool availability")
    args = parser.parse_args()

    if args.check_tools:
        print(json.dumps(check_tools_only(), indent=2))
        return

    if not args.path:
        parser.error("--path is required when not using --check-tools")

    project_path = os.path.abspath(args.path)
    if not os.path.isdir(project_path):
        print(json.dumps({
            "error": "invalid_path",
            "message": f"Project path does not exist: {project_path}",
        }))
        sys.exit(1)

    # Check for Move.toml
    if not (Path(project_path) / "Move.toml").exists():
        print(json.dumps({
            "error": "not_a_move_project",
            "message": f"No Move.toml found in {project_path}. Is this a Sui Move project?",
        }))
        sys.exit(1)

    findings: list[dict] = []
    errors: list[dict] = []
    versions: dict[str, str] = {}

    _run_sui_build(project_path, findings, errors, versions)
    _static_analysis(project_path, findings)

    # Deduplicate
    seen = set()
    unique_findings = []
    for f in findings:
        key = (f["title"], f["location"])
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    unique_findings.sort(key=lambda f: SEVERITY_ORDER.get(f.get("severity", "info"), 99))

    result = {
        "chain": "sui_move",
        "project_path": project_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool_versions": versions,
        "findings": unique_findings,
        "summary": _build_summary(unique_findings),
        "errors": errors,
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
