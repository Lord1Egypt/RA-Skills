#!/usr/bin/env python3
"""Solidity smart contract audit script.

Runs forge build, slither, and solhint against a Solidity project and
outputs a unified JSON audit report.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def _which(binary: str) -> str | None:
    """Return the full path of *binary* if found on PATH, else None."""
    for d in os.environ.get("PATH", "").split(os.pathsep):
        p = os.path.join(d, binary)
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


def _run(cmd: list[str], cwd: str, timeout: int = 300) -> subprocess.CompletedProcess:
    """Run *cmd* and return the CompletedProcess."""
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def _tool_version(binary: str) -> str:
    """Best-effort version string."""
    try:
        r = _run([binary, "--version"], cwd=".")
        return (r.stdout or r.stderr).strip().split("\n")[0]
    except Exception:
        return "unknown"


# ---------------------------------------------------------------------------
# Audit runners
# ---------------------------------------------------------------------------

def check_tools_only() -> dict:
    """Return availability info for all required tools."""
    tools = {
        "forge": {"install_hint": "curl -L https://foundry.paradigm.xyz | bash && foundryup"},
        "slither": {"install_hint": "pip install slither-analyzer"},
        "solhint": {"install_hint": "npm install -g solhint"},
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


def _run_forge_build(project_path: str, findings: list, errors: list, versions: dict):
    """Run ``forge build`` and capture compilation errors."""
    if not _which("forge"):
        errors.append({
            "tool": "forge",
            "error": "tool_not_found",
            "message": "forge (Foundry) is not installed or not in PATH",
            "install_hint": "curl -L https://foundry.paradigm.xyz | bash && foundryup",
        })
        return

    versions["forge"] = _tool_version("forge")
    try:
        r = _run(["forge", "build", "--force"], cwd=project_path)
        if r.returncode != 0:
            # Parse compilation errors
            for line in (r.stderr or "").split("\n"):
                line = line.strip()
                if not line:
                    continue
                # Typical forge error: Error (xxxx): ... --> src/X.sol:10:5
                if "Error" in line or "error" in line.lower():
                    findings.append({
                        "severity": "high",
                        "title": "Compilation error",
                        "location": _extract_location(line),
                        "description": line,
                        "recommendation": "Fix the compilation error before proceeding.",
                        "tool": "forge",
                    })
    except subprocess.TimeoutExpired:
        errors.append({
            "tool": "forge",
            "error": "execution_failed",
            "message": "forge build timed out after 300s",
        })
    except Exception as exc:
        errors.append({
            "tool": "forge",
            "error": "execution_failed",
            "message": str(exc),
        })


def _slither_severity(impact: str) -> str:
    """Map Slither impact level to our severity."""
    mapping = {
        "High": "high",
        "Medium": "medium",
        "Low": "low",
        "Informational": "info",
        "Optimization": "info",
    }
    return mapping.get(impact, "info")


def _run_slither(project_path: str, findings: list, errors: list, versions: dict):
    """Run Slither static analysis."""
    if not _which("slither"):
        errors.append({
            "tool": "slither",
            "error": "tool_not_found",
            "message": "slither is not installed or not in PATH",
            "install_hint": "pip install slither-analyzer",
        })
        return

    versions["slither"] = _tool_version("slither")
    try:
        r = _run(
            ["slither", ".", "--json", "-"],
            cwd=project_path,
            timeout=600,
        )
        output = r.stdout or ""
        # Slither may print warnings before JSON – find the JSON blob
        json_start = output.find("{")
        if json_start == -1:
            # Fallback: try stderr
            output = r.stderr or ""
            json_start = output.find("{")

        if json_start != -1:
            try:
                data = json.loads(output[json_start:])
                for det in data.get("results", {}).get("detectors", []):
                    severity = _slither_severity(det.get("impact", "Informational"))
                    # Determine if the finding is critical (e.g. reentrancy on High)
                    check_id = det.get("check", "")
                    if severity == "high" and check_id in (
                        "reentrancy-eth", "reentrancy-no-eth",
                        "arbitrary-send-eth", "suicidal",
                        "uninitialized-state", "controlled-delegatecall",
                    ):
                        severity = "critical"

                    elements = det.get("elements", [])
                    location = ""
                    if elements:
                        src = elements[0].get("source_mapping", {})
                        filename = src.get("filename_relative", "")
                        lines = src.get("lines", [])
                        if filename and lines:
                            location = f"{filename}:{lines[0]}"

                    findings.append({
                        "severity": severity,
                        "title": det.get("check", "unknown"),
                        "location": location,
                        "description": det.get("description", "").strip(),
                        "recommendation": det.get("markdown", det.get("description", "")).strip()[:500],
                        "tool": "slither",
                    })
            except json.JSONDecodeError:
                errors.append({
                    "tool": "slither",
                    "error": "execution_failed",
                    "message": "Failed to parse slither JSON output",
                })
        elif r.returncode != 0:
            errors.append({
                "tool": "slither",
                "error": "execution_failed",
                "message": (r.stderr or r.stdout or "Unknown error")[:1000],
            })
    except subprocess.TimeoutExpired:
        errors.append({
            "tool": "slither",
            "error": "execution_failed",
            "message": "slither timed out after 600s",
        })
    except Exception as exc:
        errors.append({
            "tool": "slither",
            "error": "execution_failed",
            "message": str(exc),
        })


def _run_solhint(project_path: str, findings: list, errors: list, versions: dict):
    """Run Solhint linter."""
    if not _which("solhint"):
        errors.append({
            "tool": "solhint",
            "error": "tool_not_found",
            "message": "solhint is not installed or not in PATH",
            "install_hint": "npm install -g solhint",
        })
        return

    versions["solhint"] = _tool_version("solhint")

    # Find .sol files
    sol_files = list(Path(project_path).rglob("*.sol"))
    # Exclude common directories
    sol_files = [
        f for f in sol_files
        if "node_modules" not in str(f)
        and "lib/" not in str(f)
        and "cache" not in str(f)
    ]
    if not sol_files:
        return

    try:
        cmd = ["solhint", "--formatter", "json"] + [str(f) for f in sol_files[:50]]
        r = _run(cmd, cwd=project_path, timeout=120)
        output = r.stdout or ""
        json_start = output.find("[")
        if json_start != -1:
            try:
                results = json.loads(output[json_start:])
                for file_result in results:
                    filepath = file_result.get("filePath", "")
                    rel = os.path.relpath(filepath, project_path) if filepath else ""
                    for msg in file_result.get("messages", []):
                        sev = msg.get("severity", 1)
                        severity = "medium" if sev >= 2 else "info"
                        findings.append({
                            "severity": severity,
                            "title": msg.get("ruleId", "solhint-rule"),
                            "location": f"{rel}:{msg.get('line', '?')}:{msg.get('column', '?')}",
                            "description": msg.get("message", ""),
                            "recommendation": f"Fix solhint rule: {msg.get('ruleId', '')}",
                            "tool": "solhint",
                        })
            except json.JSONDecodeError:
                pass
    except subprocess.TimeoutExpired:
        errors.append({
            "tool": "solhint",
            "error": "execution_failed",
            "message": "solhint timed out after 120s",
        })
    except Exception as exc:
        errors.append({
            "tool": "solhint",
            "error": "execution_failed",
            "message": str(exc),
        })


# ---------------------------------------------------------------------------
# Static analysis (no external tools)
# ---------------------------------------------------------------------------

def _static_analysis(project_path: str, findings: list):
    """Lightweight pattern-based static checks on .sol source files."""
    sol_files = list(Path(project_path).rglob("*.sol"))
    sol_files = [
        f for f in sol_files
        if "node_modules" not in str(f)
        and "/lib/" not in str(f)
        and "cache" not in str(f)
    ]

    patterns = [
        (r"\btx\.origin\b", "medium", "tx.origin usage",
         "tx.origin used for authorization is vulnerable to phishing attacks",
         "Use msg.sender instead of tx.origin for authorization"),
        (r"selfdestruct\s*\(", "high", "selfdestruct usage",
         "Contract uses selfdestruct which can permanently destroy the contract",
         "Remove selfdestruct or protect with strong access control"),
        (r"delegatecall\s*\(", "medium", "delegatecall usage",
         "delegatecall can be dangerous if the target is user-controlled",
         "Ensure delegatecall target is trusted and immutable"),
        (r"block\.(timestamp|number)\b", "low", "Block variable dependency",
         "Relying on block.timestamp or block.number can be manipulated by miners",
         "Avoid using block variables for critical logic"),
        (r"assembly\s*\{", "info", "Inline assembly usage",
         "Inline assembly bypasses Solidity safety checks",
         "Review assembly code carefully for correctness"),
        (r"\.call\{value:", "medium", "Low-level call with value",
         "Low-level call with value transfer; return value may not be checked",
         "Check return value of .call and handle failure"),
        (r"pragma solidity\s*\^", "info", "Floating pragma",
         "Floating pragma allows compilation with different compiler versions",
         "Lock pragma to a specific version (e.g., pragma solidity 0.8.20;)"),
    ]

    for sol_file in sol_files:
        try:
            content = sol_file.read_text(errors="replace")
            rel_path = os.path.relpath(str(sol_file), project_path)
            for line_no, line in enumerate(content.split("\n"), 1):
                for pattern, severity, title, desc, rec in patterns:
                    if re.search(pattern, line):
                        findings.append({
                            "severity": severity,
                            "title": title,
                            "location": f"{rel_path}:{line_no}",
                            "description": desc,
                            "recommendation": rec,
                            "tool": "static-analysis",
                        })
        except Exception:
            continue


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _extract_location(line: str) -> str:
    """Try to extract a file:line location from a compiler message."""
    m = re.search(r"-->\s*([\w/.]+:\d+:\d+)", line)
    if m:
        return m.group(1)
    m = re.search(r"([\w/.]+\.sol:\d+)", line)
    if m:
        return m.group(1)
    return ""


def _build_summary(findings: list) -> dict:
    """Build summary counts."""
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
    parser = argparse.ArgumentParser(description="Solidity contract audit")
    parser.add_argument("--path", help="Path to Solidity project root")
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

    findings: list[dict] = []
    errors: list[dict] = []
    versions: dict[str, str] = {}

    # Run all checks
    _run_forge_build(project_path, findings, errors, versions)
    _run_slither(project_path, findings, errors, versions)
    _run_solhint(project_path, findings, errors, versions)
    _static_analysis(project_path, findings)

    # Deduplicate findings by (title, location)
    seen = set()
    unique_findings = []
    for f in findings:
        key = (f["title"], f["location"])
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    # Sort by severity
    unique_findings.sort(key=lambda f: SEVERITY_ORDER.get(f.get("severity", "info"), 99))

    result = {
        "chain": "solidity",
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
