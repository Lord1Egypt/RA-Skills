#!/usr/bin/env python3
"""Solana smart contract audit script.

Runs ``anchor build``, ``cargo-audit``, and custom static analysis on
Solana programs (Anchor or native), then outputs a unified JSON audit report.
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
        "anchor": {"install_hint": "cargo install --git https://github.com/coral-xyz/anchor avm && avm install latest && avm use latest"},
        "solana": {"install_hint": "sh -c \"$(curl -sSfL https://release.anza.xyz/stable/install)\""},
        "cargo-audit": {"install_hint": "cargo install cargo-audit"},
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


def _is_anchor_project(project_path: str) -> bool:
    return (Path(project_path) / "Anchor.toml").exists()


def _find_program_dirs(project_path: str) -> list[str]:
    """Find Rust program directories."""
    dirs = []
    # Anchor: programs/*/
    programs_dir = Path(project_path) / "programs"
    if programs_dir.is_dir():
        for d in programs_dir.iterdir():
            if d.is_dir() and (d / "Cargo.toml").exists():
                dirs.append(str(d))
    # Native: check if root has Cargo.toml with solana-program dep
    root_cargo = Path(project_path) / "Cargo.toml"
    if root_cargo.exists() and not dirs:
        try:
            content = root_cargo.read_text()
            if "solana-program" in content or "anchor-lang" in content:
                dirs.append(project_path)
        except Exception:
            pass
    return dirs


# ---------------------------------------------------------------------------
# Anchor / Solana build
# ---------------------------------------------------------------------------

def _run_anchor_build(project_path: str, findings: list, errors: list, versions: dict):
    """Run ``anchor build``."""
    if not _which("anchor"):
        errors.append({
            "tool": "anchor",
            "error": "tool_not_found",
            "message": "anchor CLI is not installed or not in PATH",
            "install_hint": "cargo install --git https://github.com/coral-xyz/anchor avm && avm install latest && avm use latest",
        })
        return

    versions["anchor"] = _tool_version("anchor")

    try:
        r = _run(["anchor", "build"], cwd=project_path, timeout=600)
        combined = (r.stdout or "") + "\n" + (r.stderr or "")

        if r.returncode != 0:
            for line in combined.split("\n"):
                line = line.strip()
                if not line:
                    continue
                if "error" in line.lower() and "warning" not in line.lower():
                    findings.append({
                        "severity": "high",
                        "title": "Compilation error",
                        "location": _extract_rust_location(line),
                        "description": line,
                        "recommendation": "Fix the compilation error before proceeding.",
                        "tool": "anchor-build",
                    })

        # Capture warnings
        for line in combined.split("\n"):
            line = line.strip()
            if "warning:" in line.lower() and "generated" not in line.lower():
                findings.append({
                    "severity": "low",
                    "title": "Build warning",
                    "location": _extract_rust_location(line),
                    "description": line,
                    "recommendation": "Review and address compiler warnings.",
                    "tool": "anchor-build",
                })

    except subprocess.TimeoutExpired:
        errors.append({
            "tool": "anchor-build",
            "error": "execution_failed",
            "message": "anchor build timed out after 600s",
        })
    except Exception as exc:
        errors.append({
            "tool": "anchor-build",
            "error": "execution_failed",
            "message": str(exc),
        })


def _run_cargo_build(project_path: str, findings: list, errors: list, versions: dict):
    """Fallback: run cargo build-sbf for native Solana programs."""
    # Try cargo-build-sbf or cargo-build-bpf
    for cmd_name in ["cargo-build-sbf", "cargo-build-bpf"]:
        if _which(cmd_name):
            versions[cmd_name] = _tool_version(cmd_name)
            try:
                r = _run([cmd_name], cwd=project_path, timeout=600)
                if r.returncode != 0:
                    for line in (r.stderr or "").split("\n"):
                        if "error" in line.lower():
                            findings.append({
                                "severity": "high",
                                "title": "Compilation error",
                                "location": _extract_rust_location(line),
                                "description": line.strip(),
                                "recommendation": "Fix the compilation error.",
                                "tool": cmd_name,
                            })
            except Exception as exc:
                errors.append({
                    "tool": cmd_name,
                    "error": "execution_failed",
                    "message": str(exc),
                })
            return

    if not _which("solana"):
        errors.append({
            "tool": "solana",
            "error": "tool_not_found",
            "message": "solana CLI is not installed or not in PATH",
            "install_hint": "sh -c \"$(curl -sSfL https://release.anza.xyz/stable/install)\"",
        })


def _run_cargo_audit(project_path: str, findings: list, errors: list, versions: dict):
    """Run ``cargo audit`` for dependency vulnerabilities."""
    if not _which("cargo-audit"):
        errors.append({
            "tool": "cargo-audit",
            "error": "tool_not_found",
            "message": "cargo-audit is not installed",
            "install_hint": "cargo install cargo-audit",
        })
        return

    versions["cargo-audit"] = _tool_version("cargo-audit")

    # Find directories with Cargo.lock
    audit_dirs = []
    if (Path(project_path) / "Cargo.lock").exists():
        audit_dirs.append(project_path)
    else:
        for program_dir in _find_program_dirs(project_path):
            if (Path(program_dir) / "Cargo.lock").exists():
                audit_dirs.append(program_dir)

    for audit_dir in audit_dirs:
        try:
            r = _run(["cargo", "audit", "--json"], cwd=audit_dir, timeout=120)
            output = r.stdout or ""
            json_start = output.find("{")
            if json_start != -1:
                try:
                    data = json.loads(output[json_start:])
                    for vuln in data.get("vulnerabilities", {}).get("list", []):
                        advisory = vuln.get("advisory", {})
                        severity = "medium"
                        cvss = advisory.get("cvss")
                        if cvss and isinstance(cvss, str):
                            # Parse CVSS score
                            try:
                                score_part = cvss.split("/")[0].replace("CVSS:3.1/AV:", "")
                            except Exception:
                                pass
                        if advisory.get("informational"):
                            severity = "info"
                        elif "critical" in (advisory.get("title", "") + str(advisory.get("categories", []))).lower():
                            severity = "critical"

                        findings.append({
                            "severity": severity,
                            "title": f"Dependency vulnerability: {advisory.get('id', 'UNKNOWN')}",
                            "location": f"Cargo.lock ({advisory.get('package', 'unknown')})",
                            "description": advisory.get("title", "")
                                           + ". " + advisory.get("description", "")[:300],
                            "recommendation": f"Update {advisory.get('package', '')} or apply patch. See: {advisory.get('url', '')}",
                            "tool": "cargo-audit",
                        })
                except json.JSONDecodeError:
                    pass
        except subprocess.TimeoutExpired:
            errors.append({
                "tool": "cargo-audit",
                "error": "execution_failed",
                "message": f"cargo audit timed out in {audit_dir}",
            })
        except Exception as exc:
            errors.append({
                "tool": "cargo-audit",
                "error": "execution_failed",
                "message": str(exc),
            })


# ---------------------------------------------------------------------------
# Custom static analysis for Solana programs
# ---------------------------------------------------------------------------

def _static_analysis(project_path: str, findings: list):
    """Pattern-based static analysis on Rust source files for Solana-specific issues."""
    rs_files = []
    for program_dir in _find_program_dirs(project_path):
        rs_files.extend(Path(program_dir).rglob("*.rs"))

    # Also check root src/
    src_dir = Path(project_path) / "src"
    if src_dir.exists():
        rs_files.extend(src_dir.rglob("*.rs"))

    rs_files = [f for f in rs_files if "target/" not in str(f) and "build/" not in str(f)]

    # Determine if Anchor project
    is_anchor = _is_anchor_project(project_path)

    for rs_file in rs_files:
        try:
            content = rs_file.read_text(errors="replace")
            rel_path = os.path.relpath(str(rs_file), project_path)
            lines = content.split("\n")

            if is_anchor:
                _check_anchor_patterns(rel_path, content, lines, findings)
            else:
                _check_native_patterns(rel_path, content, lines, findings)

            # Common checks
            _check_common_solana_patterns(rel_path, content, lines, findings)

        except Exception:
            continue


def _check_anchor_patterns(rel_path: str, content: str, lines: list, findings: list):
    """Anchor-specific security checks."""
    for i, line in enumerate(lines, 1):
        # Missing account validation constraints
        if re.search(r"pub\s+\w+\s*:\s*Account<", line) or re.search(r"pub\s+\w+\s*:\s*UncheckedAccount", line):
            if "UncheckedAccount" in line:
                # Check if there's a CHECK comment
                context = "\n".join(lines[max(0, i - 3):i])
                if "CHECK" not in context and "check" not in context.lower():
                    findings.append({
                        "severity": "high",
                        "title": "UncheckedAccount without CHECK comment",
                        "location": f"{rel_path}:{i}",
                        "description": "UncheckedAccount used without a /// CHECK: comment explaining why it's safe.",
                        "recommendation": "Add a /// CHECK: comment or use a validated account type instead.",
                        "tool": "static-analysis",
                    })

        # Missing signer constraint
        if re.search(r"pub\s+(\w+)\s*:\s*Signer", line):
            pass  # Signer type is self-checking in Anchor

        # Missing has_one / constraint
        if re.search(r"#\[account\(", line):
            if "mut" in line and "constraint" not in line and "has_one" not in line and "seeds" not in line:
                findings.append({
                    "severity": "medium",
                    "title": "Mutable account without constraint",
                    "location": f"{rel_path}:{i}",
                    "description": "Account is marked as mutable but has no constraint or has_one validation.",
                    "recommendation": "Add appropriate constraints (has_one, constraint, seeds) to validate account relationships.",
                    "tool": "static-analysis",
                })

        # Unchecked arithmetic (non-checked_* operations in Anchor)
        if re.search(r"\.checked_(add|sub|mul|div)\(", line):
            pass  # Good practice
        elif re.search(r"[^a-zA-Z_](amount|balance|supply|total|price|fee|reward)\s*[+\-*/]=?\s*", line):
            # Potential unchecked arithmetic on financial values
            if "checked_" not in line and "saturating_" not in line:
                findings.append({
                    "severity": "medium",
                    "title": "Potentially unchecked arithmetic",
                    "location": f"{rel_path}:{i}",
                    "description": "Arithmetic operation on what appears to be a financial value without checked/saturating math.",
                    "recommendation": "Use checked_add/checked_sub/checked_mul/checked_div or overflow-checks = true in Cargo.toml.",
                    "tool": "static-analysis",
                })


def _check_native_patterns(rel_path: str, content: str, lines: list, findings: list):
    """Native Solana program-specific checks."""
    has_owner_check = "owner" in content.lower() and ("check" in content.lower() or "assert" in content.lower())
    has_signer_check = "is_signer" in content

    for i, line in enumerate(lines, 1):
        # Missing owner check
        if re.search(r"fn\s+process_instruction\s*\(", line):
            if not has_owner_check:
                findings.append({
                    "severity": "high",
                    "title": "Potentially missing owner check",
                    "location": f"{rel_path}:{i}",
                    "description": "Program instruction processor does not appear to verify account ownership.",
                    "recommendation": "Verify that accounts are owned by the expected program using account.owner == program_id.",
                    "tool": "static-analysis",
                })
            if not has_signer_check:
                findings.append({
                    "severity": "high",
                    "title": "Potentially missing signer check",
                    "location": f"{rel_path}:{i}",
                    "description": "Program instruction processor does not appear to verify signers.",
                    "recommendation": "Verify that required accounts have is_signer == true.",
                    "tool": "static-analysis",
                })

        # Unsafe deserialization
        if re.search(r"try_from_slice\s*\(", line) and "borsh" not in content.lower():
            findings.append({
                "severity": "medium",
                "title": "Raw byte deserialization",
                "location": f"{rel_path}:{i}",
                "description": "Using try_from_slice without borsh serialization framework may be error-prone.",
                "recommendation": "Consider using borsh or anchor for safe serialization/deserialization.",
                "tool": "static-analysis",
            })


def _check_common_solana_patterns(rel_path: str, content: str, lines: list, findings: list):
    """Security checks common to both Anchor and native programs."""
    for i, line in enumerate(lines, 1):
        # PDA without proper seeds
        if re.search(r"find_program_address\s*\(", line) or re.search(r"create_program_address\s*\(", line):
            findings.append({
                "severity": "info",
                "title": "PDA derivation",
                "location": f"{rel_path}:{i}",
                "description": "Program-derived address is being computed. Ensure seeds are unique and collision-resistant.",
                "recommendation": "Use unique, descriptive seeds for PDAs. Include discriminators to prevent seed collisions.",
                "tool": "static-analysis",
            })

        # CPI (Cross-Program Invocation)
        if re.search(r"invoke\s*\(", line) or re.search(r"invoke_signed\s*\(", line):
            findings.append({
                "severity": "medium",
                "title": "Cross-Program Invocation (CPI)",
                "location": f"{rel_path}:{i}",
                "description": "CPI detected. Ensure the target program is verified and the invocation is safe.",
                "recommendation": "Verify the target program ID before CPI. Be cautious with invoke_signed to prevent privilege escalation.",
                "tool": "static-analysis",
            })

        # Account close/drain
        if re.search(r"close\s*\(", line) and "ctx" in line:
            findings.append({
                "severity": "info",
                "title": "Account close operation",
                "location": f"{rel_path}:{i}",
                "description": "Account is being closed. Ensure lamports are properly transferred.",
                "recommendation": "Verify account data is zeroed after closing to prevent revival attacks.",
                "tool": "static-analysis",
            })

        # Unsafe unwrap
        if re.search(r"\.unwrap\(\)", line):
            findings.append({
                "severity": "low",
                "title": "unwrap() usage",
                "location": f"{rel_path}:{i}",
                "description": "Using unwrap() can cause the program to panic on None/Err.",
                "recommendation": "Use proper error handling with ? operator or match/if-let instead of unwrap().",
                "tool": "static-analysis",
            })

        # Msg! with sensitive data
        if re.search(r'msg!\s*\(.*".*key.*"', line, re.IGNORECASE) or \
           re.search(r'msg!\s*\(.*".*secret.*"', line, re.IGNORECASE):
            findings.append({
                "severity": "medium",
                "title": "Potentially logging sensitive data",
                "location": f"{rel_path}:{i}",
                "description": "msg! macro may be logging sensitive information (keys/secrets).",
                "recommendation": "Remove or sanitize sensitive data from log messages.",
                "tool": "static-analysis",
            })


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _extract_rust_location(line: str) -> str:
    m = re.search(r"-->\s*([\w/.]+:\d+:\d+)", line)
    if m:
        return m.group(1)
    m = re.search(r"([\w/.]+\.rs:\d+)", line)
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
    parser = argparse.ArgumentParser(description="Solana contract audit")
    parser.add_argument("--path", help="Path to Solana project root")
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

    # Determine project type
    is_anchor = _is_anchor_project(project_path)
    program_dirs = _find_program_dirs(project_path)

    if not program_dirs and not is_anchor:
        print(json.dumps({
            "error": "not_a_solana_project",
            "message": f"No Solana program found in {project_path}. Expected Anchor.toml or Cargo.toml with solana-program dependency.",
        }))
        sys.exit(1)

    findings: list[dict] = []
    errors: list[dict] = []
    versions: dict[str, str] = {}

    # Build
    if is_anchor:
        _run_anchor_build(project_path, findings, errors, versions)
    else:
        _run_cargo_build(project_path, findings, errors, versions)

    # Dependency audit
    _run_cargo_audit(project_path, findings, errors, versions)

    # Static analysis
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
        "chain": "solana",
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
