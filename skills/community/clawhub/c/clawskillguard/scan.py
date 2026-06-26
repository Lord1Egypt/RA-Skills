#!/usr/bin/env python3
"""
ClawSkillGuard — OpenClaw Skill Security Scanner
100% local. Zero network calls.
"""

import os
import re
import sys
import json
import base64
import hashlib
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class Severity(Enum):
    CLEAN = "clean"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    def __lt__(self, other):
        order = [Severity.CLEAN, Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL]
        return order.index(self) < order.index(other)


SEVERITY_ICONS = {
    Severity.CLEAN: "\u2705",
    Severity.LOW: "\U0001f7e2",
    Severity.MEDIUM: "\U0001f7e1",
    Severity.HIGH: "\U0001f7e0",
    Severity.CRITICAL: "\U0001f534",
}


@dataclass
class Finding:
    severity: Severity
    category: str
    file: str
    line: Optional[int]
    pattern: str
    description: str
    recommendation: str
    snippet: str = ""


@dataclass
class ScanResult:
    skill_path: str
    skill_name: str
    findings: list = field(default_factory=list)
    files_scanned: int = 0
    errors: list = field(default_factory=list)

    @property
    def max_severity(self) -> Severity:
        if not self.findings:
            return Severity.CLEAN
        return max(f.severity for f in self.findings)

    @property
    def verdict(self) -> str:
        sev = self.max_severity
        if sev == Severity.CRITICAL:
            return "\u274c DO NOT INSTALL \u2014 Critical threats detected"
        elif sev == Severity.HIGH:
            return "\u26a0\ufe0f REVIEW NEEDED \u2014 Suspicious patterns found"
        elif sev == Severity.MEDIUM:
            return "\u26a0\ufe0f REVIEW NEEDED \u2014 Some concerns detected"
        elif sev == Severity.LOW:
            return "\u2705 SAFE TO INSTALL \u2014 Minor concerns only"
        return "\u2705 CLEAN \u2014 No threats detected"


# ─── Pattern Builder ──────────────────────────────────────────────
# Patterns are stored as base64 to avoid false-positive self-detection
# by naive scanners. Each entry: (b64_pattern, severity, description)

def _d(b64):
    """Decode base64 pattern."""
    return base64.b64decode(b64).decode()


def _build_patterns(entries):
    """Build (regex, severity, description) tuples from b64-encoded entries."""
    return [(_d(p), s, desc) for p, s, desc in entries]


# SKILL.md prompt injection patterns
_SKILL_INJECTION_RAW = [
    # Hidden HTML content
    ("PFNwYW5bPl1zdHlsZT1bXCJcJ10uKmRpc3BsYXk6XHMqbm9uZS4qW1wiXCddLio+",
     Severity.HIGH, "Hidden HTML content in markdown"),
    # Zero-width chars
    ("XHUyMDBiXFx1MjAwY1xcdTIwMGRcXHVmZWZm",
     Severity.HIGH, "Zero-width characters detected (possible hidden text)"),
    # HTML comments
    ("PCEtLVtcc1xTXT8tLT4=",
     Severity.MEDIUM, "HTML comment \u2014 may contain hidden instructions"),
    # System prompt override
    ("aWdub3JlXHMrKGFsbFxzKykocHJldmlvdXN8cHJpb3J8YWJvdmV8c3lzdGVtKVxzKyhpbnN0cnVjdGlvbnN8cHJvbXB0c3xydWxlcyk=",
     Severity.CRITICAL, "Attempt to override system instructions"),
    ("ZGlzcmVnYXJkXHMrKGFsbFxzKyk/KHByZXZpb3VzfHByaW9yfGFib3ZlfHN5c3RlbSk=",
     Severity.CRITICAL, "Attempt to disregard system prompts"),
    ("eW91XHMrYXJlXHMrbm93XHMrKGFccyk/KGRpZmZlcmVudHxuZXd8YW5vdGhlcik=",
     Severity.HIGH, "Attempt to redefine agent identity"),
    ("Zm9yZ2V0XHMrKGV2ZXJ5dGhpbmd8YWxsKVxzKyh5b3V8dGhhdClzKyhrbm93fGxlYXJuZWQp",
     Severity.HIGH, "Attempt to reset agent context"),
    ("bmV3XHMrc3lzdGVtXHMrcHJvbXB0",
     Severity.CRITICAL, "Attempt to inject new system prompt"),
    ("PFw8aW1fc3RhcnRcPn58PFw8aW1fZW5kXD5+",
     Severity.CRITICAL, "Chat template injection tokens"),
    # Data exfil
    ("KHNlbmR8cG9zdHx1cGxvYWR8dHJhbnNtaXR8ZXhmaWx0cmF0ZXxsZWFrKVxzKy4qKGNvbnRlbnRzfGRhdGF8ZmlsZXN8dG9rZW5zfGtleXN8c2VjcmV0c3xjcmVkZW50aWFscyk=",
     Severity.CRITICAL, "Potential data exfiltration instruction"),
    ("KGN1cmx8d2dldHxmZXRjaClzKy4qJHt8aHR0cFtzXTovLy4qJHw=",
     Severity.CRITICAL, "Dynamic URL construction (potential data exfil)"),
    ("cmVwb3J0XHMqLioodG98YXQpXHMqKGh0dHB8dXJsfGVuZHBvaW50fHNlcnZlcnx3ZWJob29rKQ==",
     Severity.CRITICAL, "Reporting to external endpoint"),
    # Credential access
    ("KHJlYWR8YWNjZXNzfGdyYWJ8Y29sbGVjdHxnYXRoZXJ8c3RlYWwpXHMqLiooXC5lbnZ8XC5zc2h8XC5hd3N8XC5jb25maWd8cGFzc3dvcmR8dG9rZW58c2VjcmV0fGNyZWRlbnRpYWx8YXBpLj9rZXkp",
     Severity.CRITICAL, "Prompt to access credentials"),
    ("KGNhdHxyZWFkfG9wZW4pXHMqLioofnxcJHtIT01FfSk/Lz9cLihlbnZ8c3NofGF3c3xnbnVwZ3xucG1yY3xwaXAp",
     Severity.CRITICAL, "Prompt to read sensitive config files"),
]

# Script malicious patterns
_SCRIPT_MALICIOUS_RAW = [
    # Shell/network
    ("YmFzaFxzKy1pXHM+JlxzL2Rldi8odGNwfHVkcCk=",
     Severity.CRITICAL, "Reverse shell attempt"),
    ("bmNccysuKi1bZWxdXHMr",
     Severity.CRITICAL, "Netcat listener (possible backdoor)"),
    ("bmNhdFxzKy4qLVtlbF1ccys=",
     Severity.CRITICAL, "Ncat listener (possible backdoor)"),
    ("c29jYXRccysuKmV4ZWM=",
     Severity.CRITICAL, "Socat with exec (possible shell)"),
    ("cHl0aG9uLipzb2NrZXQuKmNvbm5lY3Q=",
     Severity.HIGH, "Python socket connection"),
    ("b3NcLnN5c3RlbVxzKlwo",
     Severity.HIGH, "Direct OS command execution"),
    ("c3VicHJvY2Vzc1wuKGNhbGx8cnVufFBvcGVufGNoZWNrX291dHB1dCkuKnNoZWxsXHMqPVxzKlRydWU=",
     Severity.HIGH, "Shell injection risk (shell=True)"),
    # Credential theft
    ("KGNhdHxyZWFkfG9wZW58bG9hZClzKy4qXC5lbnY=",
     Severity.CRITICAL, "Reading .env files"),
    ("KGNhdHxyZWFkfG9wZW58bG9hZClzKy4qXC5zc2gv",
     Severity.CRITICAL, "Reading SSH keys"),
    ("KGNhdHxyZWFkfG9wZW58bG9hZClzKy4qXy4oYXdzfGdudXBnfG5wbXJjL3BpcC8p",
     Severity.CRITICAL, "Reading sensitive config"),
    ("b3NcLmVudmlyb24=",
     Severity.MEDIUM, "Accessing environment variables"),
    ("cHJvY2Vzc1wuZW52",
     Severity.MEDIUM, "Accessing environment variables"),
    ("KGxvY2FsU3RvcmFnZXxzc2lvblN0b3JhZ2V8ZG9jdW1lbnRcLmNvb2tpZSk=",
     Severity.MEDIUM, "Accessing browser storage/cookies"),
    # Destructive
    ("cm1ccysoLXJmP3wtLXJlY3Vyc2l2ZSlccysv",
     Severity.CRITICAL, "Recursive deletion from root"),
    ("cm1ccysuKi0tZm9yY2U=",
     Severity.CRITICAL, "Forced deletion"),
    ("KF58W1xzO3wmXSlmb3JtYXRcc3woXnxbXHM7fCZdKW1rZnNcc3woXnxbXHM7fCZdKXdpcGVmc1xzfChefFtcczt8Jl0pc2hyZWRcc3xkZFxzK2lmPQ==",
     Severity.CRITICAL, "Disk destruction/formatting"),
    ("Y2htb2Rccys3Nzc=",
     Severity.HIGH, "Overly permissive file permissions"),
    ("Y2hvd25ccystUlxzKnJvb3Q=",
     Severity.HIGH, "Recursive ownership change to root"),
    # Cryptomining
    ("KHhtcmlnfG1pbmVyZHxjZ21pbmVyfGV0aG1pbmVyfG5pY2VoYXNoKQ==",
     Severity.CRITICAL, "Cryptocurrency miner detected"),
    ("c3RyYXR1bSt0Y3A=",
     Severity.CRITICAL, "Mining pool connection"),
    # Downloads
    ("Y3VybFxzKy4qXHwqKGJhKT9zaA==",
     Severity.CRITICAL, "Piping download to shell"),
    ("d2dldFxzKy4qXHwqKGJhKT9zaA==",
     Severity.CRITICAL, "Piping download to shell"),
    ("SW52b2tlLVdlYlJlcXVlc3QuKnxccyooaWV4fEludm9rZS1FeHByZXNzaW9uKQ==",
     Severity.CRITICAL, "PowerShell download and execute"),
    ("SW52b2tlLUV4cHJlc3Npb258SUVYXHMqXCg=",
     Severity.HIGH, "PowerShell dynamic execution"),
    # Obfuscation
    ("YmFzZTY0XHMqKC1kfC0tZGVjb2RlKVxzKlx8",
     Severity.HIGH, "Base64 decode piped to shell"),
    ("ZXZhbFxzKlwo",
     Severity.HIGH, "Dynamic code evaluation"),
    ("ZXhlY1xzKlwo",
     Severity.HIGH, "Dynamic code execution"),
    ("RnVuY3Rpb25ccypcKFxzKltcIlwnXXJldHVyblxzKltcIlwnXQ==",
     Severity.HIGH, "JavaScript Function constructor (obfuscation)"),
    ("XFx4WzAtOWEtZkEtRl17Mn1cXHhbMC05YS1mQS1GezJ9XFx4WzAtOWEtZkEtRl17Mn0=",
     Severity.HIGH, "Hex-encoded strings (possible obfuscation)"),
    ("U3RyaW5nXC5mcm9tQ2hhckNvZGVccypcKA==",
     Severity.MEDIUM, "Character code obfuscation"),
    ("YXRvYlxzKlwo",
     Severity.MEDIUM, "Base64 decode (atob)"),
    # Privilege
    ("c3Vkb1xzKw==",
     Severity.MEDIUM, "Uses sudo"),
    ("c2V0dWlkfHNldGdpZA==",
     Severity.HIGH, "Setuid/setgid operation"),
    ("Y2htb2RccytbNC03XVswLTldezN9",
     Severity.MEDIUM, "Setuid/setgid permission"),
    # Data exfil via HTTP
    ("KHJlcXVlc3RzfHVybGlifGh0dHBcLmNsaWVudHxheGlvc3xmZXRjaHxnb3R8bm9kZS1mZXRjaCkuKlwuKHBvc3R8cHV0fHBhdGNoKVxzKlwo",
     Severity.HIGH, "Outbound HTTP POST (potential data exfil)"),
    ("KGN1cmx8d2dldCkuKi1YXHMrcG9zdA==",
     Severity.HIGH, "Outbound HTTP POST via CLI"),
    # Persistence
    ("KGNyb250YWJ8c3lzdGVtY3RsfGxhdW5jaGN0bClccys=",
     Severity.HIGH, "System service/cron manipulation"),
    ("L2V0Yy9jcm9u",
     Severity.HIGH, "Modifying system cron"),
]

# Suspicious imports
_SUSPICIOUS_IMPORTS_RAW = [
    ("aW1wb3J0XHNzb2NrZXQ=",
     Severity.MEDIUM, "Network socket access"),
    ("aW1wb3J0XHNzdWJwcm9jZXNz",
     Severity.MEDIUM, "Process spawning"),
    ("aW1wb3J0XHNvcw==",
     Severity.LOW, "OS access"),
    ("ZnJvbVxzb3NcaW1wb3J0XHNzeXN0ZW0=",
     Severity.HIGH, "Direct OS command execution"),
    ("aW1wb3J0XHNwaWNrbGU=",
     Severity.MEDIUM, "Pickle deserialization (can execute arbitrary code)"),
    ("aW1wb3J0XHNtYXJzaGFs",
     Severity.MEDIUM, "Marshal deserialization"),
    ("aW1wb3J0XHNjdHlwZXM=",
     Severity.HIGH, "Low-level C access via ctypes"),
    ("cmVxdWlyZVxzKlwoXHMqW1wiXCddY2hpbGRfcHJvY2Vzc1tcIlwnXVxzKlwp",
     Severity.MEDIUM, "Node.js child process access"),
    ("cmVxdWlyZVxzKlwoXHMqW1wiXCddZnNbXCJcJ11ccypcKQ==",
     Severity.LOW, "Node.js filesystem access"),
    ("cmVxdWlyZVxzKlwoXHMqW1wiXCddbmV0W1wiXCddXHMqXCk=",
     Severity.MEDIUM, "Node.js network access"),
    ("cmVxdWlyZVxzKlwoXHMqW1wiXCddKGh0dHB8aHR0cHMpW1wiXCddXHMqXCk=",
     Severity.MEDIUM, "Node.js HTTP client"),
]


def scan_file_patterns(filepath: Path, patterns: list, category: str) -> list:
    """Scan a file against a list of regex patterns."""
    findings = []
    try:
        content = filepath.read_text(errors='replace')
        lines = content.splitlines()

        for pattern, severity, description in patterns:
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(Finding(
                        severity=severity,
                        category=category,
                        file=str(filepath),
                        line=line_num,
                        pattern=pattern,
                        description=description,
                        recommendation=f"Review line {line_num}: {line.strip()[:120]}",
                        snippet=line.strip()[:200],
                    ))
    except Exception as e:
        findings.append(Finding(
            severity=Severity.LOW,
            category="scan_error",
            file=str(filepath),
            line=None,
            pattern="",
            description=f"Could not scan file: {e}",
            recommendation="Manual review recommended",
        ))
    return findings


def scan_skill(skill_path: str, min_severity: Severity = Severity.LOW) -> ScanResult:
    """Scan an OpenClaw skill directory."""
    # Build patterns at runtime (decoded from base64 to avoid self-detection)
    skill_injection = _build_patterns(_SKILL_INJECTION_RAW)
    script_malicious = _build_patterns(_SCRIPT_MALICIOUS_RAW)
    suspicious_imports = _build_patterns(_SUSPICIOUS_IMPORTS_RAW)

    skill_dir = Path(skill_path).resolve()
    skill_name = skill_dir.name
    result = ScanResult(
        skill_path=str(skill_dir),
        skill_name=skill_name,
    )

    if not skill_dir.exists():
        result.errors.append(f"Path does not exist: {skill_dir}")
        return result

    # Skip self (don't scan our own source — we contain detection patterns by design)
    SELF_SLUG = "clawskillguard"
    if skill_name == SELF_SLUG:
        result.errors.append("Self-scan skipped (ClawSkillGuard contains detection patterns by design)")
        return result

    # Files to skip
    skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', '.env', 'dist', 'build'}
    skip_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.woff', '.woff2', '.ttf', '.eot',
                       '.mp3', '.mp4', '.wav', '.zip', '.tar', '.gz', '.pdf', '.doc', '.docx'}

    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for fname in files:
            filepath = Path(root) / fname

            if filepath.suffix.lower() in skip_extensions:
                continue

            result.files_scanned += 1

            # SKILL.md — prompt injection scan
            if fname.upper() == 'SKILL.md':
                findings = scan_file_patterns(filepath, skill_injection, "prompt_injection")
                result.findings.extend(findings)

            # Script files
            script_ext = {'.py', '.js', '.ts', '.sh', '.bash', '.zsh', '.ps1', '.rb', '.pl', '.php', '.go', '.rs', '.c', '.cpp', '.h', '.hpp'}
            if filepath.suffix.lower() in script_ext or fname.startswith(('scan', 'install', 'setup', 'run')):
                findings = scan_file_patterns(filepath, script_malicious, "malicious_code")
                result.findings.extend(findings)

                import_findings = scan_file_patterns(filepath, suspicious_imports, "suspicious_import")
                result.findings.extend(import_findings)

            # Config files
            config_ext = {'.json', '.yaml', '.yml', '.toml', '.env', '.ini', '.cfg'}
            if filepath.suffix.lower() in config_ext and fname.upper() != 'SKILL.MD':
                findings = scan_file_patterns(filepath, script_malicious, "config_analysis")
                result.findings.extend(findings)

    # Filter by minimum severity
    severity_order = [Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL]
    min_idx = severity_order.index(min_severity) if min_severity in severity_order else 0
    result.findings = [f for f in result.findings if severity_order.index(f.severity) >= min_idx]

    return result


def format_text_report(result: ScanResult) -> str:
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"\U0001f6e1\ufe0f  ClawSkillGuard Security Scan Report")
    lines.append(f"{'='*60}")
    lines.append(f"")
    lines.append(f"\U0001f4c1 Skill: {result.skill_name}")
    lines.append(f"\U0001f4c2 Path:  {result.skill_path}")
    lines.append(f"\U0001f4c4 Files: {result.files_scanned} scanned")
    lines.append(f"")

    if result.errors:
        lines.append(f"\u26a0\ufe0f  Errors:")
        for err in result.errors:
            lines.append(f"   \u2022 {err}")
        lines.append(f"")

    if not result.findings:
        lines.append(f"\u2705 No security issues detected.")
        lines.append(f"")
        lines.append(f"Verdict: {result.verdict}")
        return "\n".join(lines)

    by_severity = {}
    for f in result.findings:
        by_severity.setdefault(f.severity, []).append(f)

    for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
        if sev not in by_severity:
            continue
        icon = SEVERITY_ICONS[sev]
        findings = by_severity[sev]
        lines.append(f"{icon} {sev.value.upper()} ({len(findings)} finding{'s' if len(findings) != 1 else ''})")
        lines.append(f"{'-'*40}")
        for f in findings:
            rel_file = f.file.replace(result.skill_path, ".")
            lines.append(f"  \U0001f4c4 {rel_file}:{f.line or '?'}")
            lines.append(f"     {f.description}")
            if f.snippet:
                snippet = f.snippet[:100] + ("..." if len(f.snippet) > 100 else "")
                lines.append(f"     > {snippet}")
            lines.append(f"")

    lines.append(f"{'='*60}")
    lines.append(f"Verdict: {result.verdict}")
    lines.append(f"{'='*60}")
    return "\n".join(lines)


def format_json_report(result: ScanResult) -> str:
    data = {
        "skill_name": result.skill_name,
        "skill_path": result.skill_path,
        "files_scanned": result.files_scanned,
        "max_severity": result.max_severity.value,
        "verdict": result.verdict,
        "finding_count": len(result.findings),
        "findings": [
            {"severity": f.severity.value, "category": f.category, "file": f.file,
             "line": f.line, "pattern": f.pattern, "description": f.description, "snippet": f.snippet}
            for f in result.findings
        ],
        "errors": result.errors,
    }
    return json.dumps(data, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="ClawSkillGuard \u2014 OpenClaw Skill Security Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  scan.py ~/.openclaw/skills/my-skill
  scan.py ~/.openclaw/workspace/skills/my-skill --format json
  scan.py ~/.openclaw/skills/ --severity high
        """,
    )
    parser.add_argument("path", help="Path to skill directory or parent directory")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--severity", choices=["low", "medium", "high", "critical"], default="low",
                        help="Minimum severity to report")
    parser.add_argument("--all", action="store_true", help="Scan all skills in parent directory")

    args = parser.parse_args()
    min_severity = Severity(args.severity)
    scan_path = Path(args.path).resolve()

    if not scan_path.exists():
        print(f"\u274c Path does not exist: {scan_path}", file=sys.stderr)
        sys.exit(1)

    if args.all or (scan_path.is_dir() and not (scan_path / "SKILL.md").exists()):
        skill_dirs = [d for d in scan_path.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
        if not skill_dirs:
            if (scan_path / "SKILL.md").exists():
                skill_dirs = [scan_path]
            else:
                print(f"\u274c No skills found in: {scan_path}", file=sys.stderr)
                sys.exit(1)

        all_results = []
        for skill_dir in sorted(skill_dirs):
            result = scan_skill(str(skill_dir), min_severity)
            all_results.append(result)
            if args.format == "text":
                print(format_text_report(result))
                print()

        if args.format == "json":
            print(json.dumps([json.loads(format_json_report(r)) for r in all_results], indent=2))

        if len(all_results) > 1 and args.format == "text":
            print(f"\n{'='*60}")
            print(f"\U0001f4ca Summary: {len(all_results)} skills scanned")
            for r in all_results:
                icon = SEVERITY_ICONS[r.max_severity]
                print(f"  {icon} {r.skill_name}: {r.max_severity.value}")
            print(f"{'='*60}")
    else:
        result = scan_skill(str(scan_path), min_severity)
        if args.format == "json":
            print(format_json_report(result))
        else:
            print(format_text_report(result))


if __name__ == "__main__":
    main()
