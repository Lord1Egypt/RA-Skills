#!/usr/bin/env python3
"""
Agent Audit — OpenClaw Skill Scanner Wrapper

Scans OpenClaw skill directories for security vulnerabilities.
Wraps the agent-audit CLI with OpenClaw-specific discovery and reporting.

Usage:
    python3 scan-skill.py <skill-directory>
    python3 scan-skill.py --all
    python3 scan-skill.py --list

Exit codes:
    0 = No findings above INFO
    1 = WARN findings only
    2 = BLOCK findings exist
    3 = Scanner error
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


# ─── Constants ───────────────────────────────────────────────────────────

OPENCLAW_WORKSPACE_SKILLS = Path.home() / ".openclaw" / "workspace" / "skills"
OPENCLAW_MANAGED_SKILLS = Path.home() / ".openclaw" / "skills"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"

TIER_BLOCK = "BLOCK"
TIER_WARN = "WARN"
TIER_INFO = "INFO"

EMOJI_BLOCK = "🔴"
EMOJI_WARN = "🟡"
EMOJI_INFO = "🔵"
EMOJI_CLEAN = "✅"
EMOJI_SHIELD = "🛡️"
EMOJI_STOP = "⛔"


# ─── Helpers ─────────────────────────────────────────────────────────────

def check_agent_audit_installed() -> bool:
    """Check if agent-audit is available on PATH."""
    try:
        result = subprocess.run(
            ["agent-audit", "--version"],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def install_agent_audit() -> bool:
    """Attempt to install agent-audit via pip."""
    print("📦 agent-audit not found. Installing...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "agent-audit", "--quiet"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print("✅ agent-audit installed successfully.")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out.")
        return False


def discover_skills() -> list[Path]:
    """Discover all skill directories in OpenClaw skill locations."""
    skills = []
    for base_dir in [OPENCLAW_WORKSPACE_SKILLS, OPENCLAW_MANAGED_SKILLS]:
        if base_dir.exists():
            for item in sorted(base_dir.iterdir()):
                skill_md = item / "SKILL.md"
                if item.is_dir() and skill_md.exists():
                    skills.append(item)
    return skills


def run_scan(skill_dir: Path) -> Optional[dict]:
    """Run agent-audit scan on a skill directory and return parsed JSON."""
    try:
        result = subprocess.run(
            ["agent-audit", "scan", str(skill_dir), "--format", "json"],
            capture_output=True, text=True, timeout=60
        )
        if result.stdout.strip():
            return json.loads(result.stdout)
        return {"findings": [], "summary": {"total": 0}}
    except json.JSONDecodeError:
        print(f"  ⚠️  Could not parse scan output for {skill_dir.name}")
        return None
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  Scan timed out for {skill_dir.name}")
        return None
    except FileNotFoundError:
        print("❌ agent-audit command not found.")
        return None


def classify_finding(finding: dict) -> str:
    """Classify a finding into BLOCK/WARN/INFO based on confidence."""
    conf = finding.get("confidence", 0.0)
    if conf >= 0.92:
        return TIER_BLOCK
    elif conf >= 0.60:
        return TIER_WARN
    elif conf >= 0.30:
        return TIER_INFO
    return "SUPPRESSED"


def format_report(skill_name: str, scan_result: dict) -> str:
    """Format scan results into a human-readable report."""
    findings = scan_result.get("findings", [])
    
    blocks = []
    warns = []
    infos = []
    
    for f in findings:
        tier = classify_finding(f)
        entry = {
            "rule_id": f.get("rule_id", "UNKNOWN"),
            "message": f.get("message", "No description"),
            "file": f.get("file_path", ""),
            "line": f.get("line_number", 0),
            "confidence": f.get("confidence", 0.0),
        }
        if tier == TIER_BLOCK:
            blocks.append(entry)
        elif tier == TIER_WARN:
            warns.append(entry)
        elif tier == TIER_INFO:
            infos.append(entry)
    
    lines = [
        f"{EMOJI_SHIELD} Agent Audit Security Report: {skill_name}",
        "━" * 48,
        f"📊 Summary: {len(blocks)} BLOCK | {len(warns)} WARN | {len(infos)} INFO",
        "",
    ]
    
    if blocks:
        lines.append(f"{EMOJI_BLOCK} BLOCK Findings:")
        for b in blocks:
            loc = f"{b['file']}:{b['line']}" if b['file'] else "N/A"
            lines.append(f"  • [{b['rule_id']}] {b['message']} ({loc})")
        lines.append("")
    
    if warns:
        lines.append(f"{EMOJI_WARN} WARN Findings:")
        for w in warns:
            loc = f"{w['file']}:{w['line']}" if w['file'] else "N/A"
            lines.append(f"  • [{w['rule_id']}] {w['message']} ({loc})")
        lines.append("")
    
    if infos:
        lines.append(f"{EMOJI_INFO} INFO Findings:")
        for i in infos:
            loc = f"{i['file']}:{i['line']}" if i['file'] else "N/A"
            lines.append(f"  • [{i['rule_id']}] {i['message']} ({loc})")
        lines.append("")
    
    lines.append("━" * 48)
    
    if blocks:
        lines.append(f"Verdict: {EMOJI_STOP} DO NOT ENABLE — {len(blocks)} critical finding(s)")
    elif warns:
        lines.append(f"Verdict: ⚠️  PROCEED WITH CAUTION — {len(warns)} warning(s)")
    else:
        lines.append(f"Verdict: {EMOJI_CLEAN} SAFE — no issues found")
    
    return "\n".join(lines)


# ─── Main ────────────────────────────────────────────────────────────────

def scan_single(skill_dir: Path) -> int:
    """Scan a single skill directory. Returns exit code."""
    if not skill_dir.exists():
        print(f"❌ Directory not found: {skill_dir}")
        return 3
    
    skill_name = skill_dir.name
    print(f"\n{EMOJI_SHIELD} Scanning skill: {skill_name}")
    print(f"  📂 {skill_dir}\n")
    
    result = run_scan(skill_dir)
    if result is None:
        return 3
    
    report = format_report(skill_name, result)
    print(report)
    
    findings = result.get("findings", [])
    has_block = any(classify_finding(f) == TIER_BLOCK for f in findings)
    has_warn = any(classify_finding(f) == TIER_WARN for f in findings)
    
    if has_block:
        return 2
    elif has_warn:
        return 1
    return 0


def scan_all() -> int:
    """Scan all discovered skills. Returns worst exit code."""
    skills = discover_skills()
    if not skills:
        print("ℹ️  No skills found in OpenClaw skill directories.")
        print(f"  Checked: {OPENCLAW_WORKSPACE_SKILLS}")
        print(f"  Checked: {OPENCLAW_MANAGED_SKILLS}")
        return 0
    
    print(f"{EMOJI_SHIELD} Scanning {len(skills)} skill(s)...\n")
    
    worst_exit = 0
    results = []
    
    for skill_dir in skills:
        exit_code = scan_single(skill_dir)
        worst_exit = max(worst_exit, exit_code)
        results.append((skill_dir.name, exit_code))
        print()
    
    # Summary
    print("\n" + "═" * 48)
    print(f"{EMOJI_SHIELD} Batch Scan Complete: {len(skills)} skill(s)")
    print("═" * 48)
    
    for name, code in results:
        if code == 2:
            print(f"  {EMOJI_STOP} {name}")
        elif code == 1:
            print(f"  ⚠️  {name}")
        elif code == 0:
            print(f"  {EMOJI_CLEAN} {name}")
        else:
            print(f"  ❓ {name} (scan error)")
    
    return worst_exit


def list_skills():
    """List all discovered skills without scanning."""
    skills = discover_skills()
    if not skills:
        print("ℹ️  No skills found.")
        return
    
    print(f"Found {len(skills)} skill(s):\n")
    for s in skills:
        print(f"  📂 {s.name} — {s}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 scan-skill.py <skill-directory>")
        print("  python3 scan-skill.py --all")
        print("  python3 scan-skill.py --list")
        sys.exit(3)
    
    # Ensure agent-audit is available
    if not check_agent_audit_installed():
        if not install_agent_audit():
            print("\n❌ Cannot proceed without agent-audit.")
            print("   Install manually: pip install agent-audit")
            sys.exit(3)
    
    arg = sys.argv[1]
    
    if arg == "--all":
        sys.exit(scan_all())
    elif arg == "--list":
        list_skills()
    elif arg == "--help" or arg == "-h":
        print(__doc__)
    else:
        skill_dir = Path(arg).expanduser().resolve()
        sys.exit(scan_single(skill_dir))


if __name__ == "__main__":
    main()
