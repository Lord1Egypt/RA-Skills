#!/usr/bin/env python3
"""Scan all credential sources and build exposure map."""

import json
import os
import re
import glob
import subprocess
from datetime import datetime, timezone

WORKSPACE = os.path.expanduser("~/clawd-zhouhanchenbot")
OPENCLAW_DIR = os.path.expanduser("~/.openclaw")
CONFIG_PATH = os.path.join(OPENCLAW_DIR, "openclaw.json")
REPORT_PATH = os.path.join(OPENCLAW_DIR, "credential-exposure-report.json")

# Patterns that look like credentials
SECRET_PATTERNS = [
    # API keys
    (r'sk-[a-zA-Z0-9]{20,}', 'OpenAI-style API key'),
    (r'sk-ant-[a-zA-Z0-9]{20,}', 'Anthropic API key'),
    (r'ghp_[a-zA-Z0-9]{36}', 'GitHub PAT'),
    (r'github_pat_[a-zA-Z0-9_]{22,}', 'GitHub fine-grained PAT'),
    (r'AKIA[A-Z0-9]{16}', 'AWS Access Key'),
    (r'xox[bpoa]-[a-zA-Z0-9-]+', 'Slack token'),
    (r'sk_live_[a-zA-Z0-9]{24,}', 'Stripe live key'),
    (r'sk_test_[a-zA-Z0-9]{24,}', 'Stripe test key'),
    (r'eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+', 'JWT token'),
    (r'AIza[a-zA-Z0-9_-]{35}', 'Google API key'),
    (r'vcp_[a-zA-Z0-9]+', 'Vercel token'),
    # Generic key patterns
    (r'["\']?(?:api[_-]?key|api[_-]?secret|access[_-]?token|auth[_-]?token|private[_-]?key)["\']?\s*[:=]\s*["\']?[a-zA-Z0-9/+=_-]{16,}', 'Generic API credential'),
    (r'["\']?(?:password|passwd|pwd|db[_-]?pass)["\']?\s*[:=]\s*["\']?[^\s"\']{8,}', 'Password field'),
    (r'postgresql://[^\s:]+:[^\s@]+@', 'PostgreSQL connection string'),
    (r'redis://:[^\s@]+@', 'Redis connection string'),
    (r'supabase[a-zA-Z0-9._/-]{20,}', 'Supabase reference'),
]

ENV_SECRET_NAMES = [
    'API_KEY', 'API_SECRET', 'ACCESS_TOKEN', 'AUTH_TOKEN', 'SECRET',
    'PASSWORD', 'PASSWD', 'PRIVATE_KEY', 'CREDENTIAL', 'TOKEN'
]

# ── Scanners ─────────────────────────────────────────────────────────────────

def scan_env_vars():
    """Scan process.env for credential-like variables."""
    findings = []
    for key, value in os.environ.items():
        key_upper = key.upper()
        is_secret_name = any(s in key_upper for s in ENV_SECRET_NAMES)
        looks_like_secret = len(value) > 12 and bool(re.match(r'^[a-zA-Z0-9/+=_-]+$', value))
        
        if is_secret_name and value:
            findings.append({
                "source": "env_var",
                "location": key,
                "type": "environment_variable",
                "preview": value[:8] + "***" if len(value) > 8 else "***",
                "risk_score": 55,
                "risk_reason": "Accessible to all skills via exec",
            })
    return findings


def scan_config():
    """Parse openclaw.json for credentials."""
    findings = []
    if not os.path.exists(CONFIG_PATH):
        return findings
    
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except (json.JSONDecodeError, PermissionError):
        return findings
    
    def search_dict(d, path=""):
        if isinstance(d, dict):
            for k, v in d.items():
                p = f"{path}.{k}" if path else k
                if isinstance(v, str) and len(v) > 12:
                    for pattern, ptype in SECRET_PATTERNS:
                        if re.search(pattern, v):
                            findings.append({
                                "source": "config",
                                "location": f"openclaw.json:{p}",
                                "type": ptype,
                                "preview": v[:8] + "***",
                                "risk_score": 65,
                                "risk_reason": "In agent config, loaded at startup",
                            })
                            break
                else:
                    search_dict(v, p)
        elif isinstance(d, list):
            for i, item in enumerate(d):
                search_dict(item, f"{path}[{i}]")
    
    search_dict(config)
    return findings


def scan_env_files():
    """Scan .env files for credentials."""
    findings = []
    search_paths = [
        os.path.join(WORKSPACE, ".env"),
        os.path.join(WORKSPACE, ".env.local"),
        os.path.join(OPENCLAW_DIR, ".env"),
    ]
    search_paths += glob.glob(os.path.join(WORKSPACE, ".env*"))
    
    seen = set()
    for path in search_paths:
        if path in seen or not os.path.isfile(path):
            continue
        seen.add(path)
        try:
            with open(path, 'r', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    if '=' in line and not line.strip().startswith('#'):
                        key = line.split('=')[0].strip()
                        val = line.split('=', 1)[1].strip().strip('"\'')
                        if any(s in key.upper() for s in ENV_SECRET_NAMES) and len(val) > 8:
                            findings.append({
                                "source": "env_file",
                                "location": f"{path}:{i}",
                                "type": "env_file_secret",
                                "preview": val[:8] + "***",
                                "risk_score": 60,
                                "risk_reason": "Readable by any skill with file access",
                            })
        except PermissionError:
            continue
    return findings


def scan_memory_files():
    """Scan MEMORY.md and memory/*.md for credential patterns."""
    findings = []
    md_files = [os.path.join(WORKSPACE, "MEMORY.md")]
    md_files += glob.glob(os.path.join(WORKSPACE, "memory", "*.md"))
    
    for path in md_files:
        if not os.path.isfile(path):
            continue
        rel = os.path.relpath(path, WORKSPACE)
        try:
            with open(path, 'r', errors='ignore') as f:
                content = f.read()
            for pattern, ptype in SECRET_PATTERNS:
                for match in re.finditer(pattern, content):
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append({
                        "source": "memory",
                        "location": f"{rel}:{line_num}",
                        "type": ptype,
                        "preview": match.group()[:8] + "***",
                        "risk_score": 70,
                        "risk_reason": "Persisted in agent memory across sessions",
                    })
        except PermissionError:
            continue
    return findings


def scan_memory_json():
    """Scan memory/*.json for credential-like values."""
    findings = []
    json_files = glob.glob(os.path.join(WORKSPACE, "memory", "*.json"))
    
    for path in json_files:
        if 'canary' in path:
            continue
        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, PermissionError):
            continue
        
        rel = os.path.relpath(path, WORKSPACE)
        
        def search_json(obj, path_str=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    p = f"{path_str}.{k}" if path_str else k
                    if isinstance(v, str) and len(v) > 16:
                        for pattern, ptype in SECRET_PATTERNS:
                            if re.search(pattern, v):
                                findings.append({
                                    "source": "memory_json",
                                    "location": f"{rel}:{p}",
                                    "type": ptype,
                                    "preview": v[:8] + "***",
                                    "risk_score": 55,
                                    "risk_reason": "In JSON memory file",
                                })
                                break
                    else:
                        search_json(v, p)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    search_json(item, f"{path_str}[{i}]")
        
        search_json(data)
    return findings


def scan_skills():
    """Analyze installed skills for capability exposure."""
    findings = []
    skills_dir = os.path.join(WORKSPACE, "skills")
    if not os.path.isdir(skills_dir):
        return findings
    
    for skill_name in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, skill_name)
        skill_md = os.path.join(skill_path, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        
        capabilities = {"exec": False, "read": True, "network": False, "write": False}
        
        try:
            with open(skill_md, 'r', errors='ignore') as f:
                content = f.read().lower()
            if 'exec' in content or 'shell' in content or 'subprocess' in content:
                capabilities["exec"] = True
            if 'web_fetch' in content or 'web_search' in content or 'curl' in content or 'http' in content:
                capabilities["network"] = True
            if 'write' in content or 'edit' in content or 'create' in content:
                capabilities["write"] = True
        except PermissionError:
            continue
        
        risk = sum(capabilities.values()) * 15
        findings.append({
            "source": "skill",
            "location": f"skills/{skill_name}",
            "type": "skill_capability",
            "capabilities": capabilities,
            "risk_score": risk,
            "risk_reason": f"exec={capabilities['exec']}, network={capabilities['network']}, write={capabilities['write']}",
        })
    return findings


def scan_mcp_servers():
    """List MCP servers from config."""
    findings = []
    if not os.path.exists(CONFIG_PATH):
        return findings
    
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except (json.JSONDecodeError, PermissionError):
        return findings
    
    mcp = config.get("mcpServers", config.get("mcp_servers", {}))
    for name, conf in mcp.items():
        has_auth = bool(
            str(conf.get("env", {})).find("KEY") != -1 or
            str(conf.get("env", {})).find("TOKEN") != -1 or
            str(conf.get("env", {})).find("SECRET") != -1
        )
        findings.append({
            "source": "mcp_server",
            "location": f"mcp:{name}",
            "type": "mcp_connection",
            "has_auth": has_auth,
            "risk_score": 50 if has_auth else 30,
            "risk_reason": f"MCP server with{' auth' if has_auth else 'out auth'}",
        })
    return findings


def scan_git_history():
    """Scan recent git history for secrets (last 200 commits)."""
    findings = []
    if not os.path.isdir(os.path.join(WORKSPACE, ".git")):
        return findings
    
    try:
        result = subprocess.run(
            ["git", "-C", WORKSPACE, "log", "--oneline", "-200", "--all"],
            capture_output=True, text=True, timeout=10
        )
        # Check diffs for secrets in last 50 commits
        result = subprocess.run(
            ["git", "-C", WORKSPACE, "log", "-50", "--patch", "--format=", "--all"],
            capture_output=True, text=True, timeout=15
        )
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('+') and not line.startswith('+++'):
                added = line[1:]
                for pattern, ptype in SECRET_PATTERNS:
                    if re.search(pattern, added):
                        findings.append({
                            "source": "git_history",
                            "location": f"git:line~{i}",
                            "type": ptype,
                            "preview": "found in commit diff",
                            "risk_score": 45,
                            "risk_reason": "Secret was committed to git history",
                        })
                        break
    except Exception:
        pass
    return findings


# ── Main ─────────────────────────────────────────────────────────────────────

def run_full_scan():
    """Run all scanners and produce report."""
    print("=== Credential Exposure Map: Full Scan ===\n")
    
    all_findings = []
    
    scanners = [
        ("Environment Variables", scan_env_vars),
        ("OpenClaw Config", scan_config),
        (".env Files", scan_env_files),
        ("Memory Files (MD)", scan_memory_files),
        ("Memory Files (JSON)", scan_memory_json),
        ("Installed Skills", scan_skills),
        ("MCP Servers", scan_mcp_servers),
        ("Git History", scan_git_history),
    ]
    
    for name, scanner in scanners:
        print(f"  Scanning {name}...")
        try:
            results = scanner()
            all_findings.extend(results)
            print(f"    Found {len(results)} item(s)")
        except Exception as e:
            print(f"    ERROR: {e}")
    
    # Deduplicate by location+type
    seen = set()
    deduped = []
    for f in all_findings:
        key = (f["location"], f["type"])
        if key not in seen:
            seen.add(key)
            deduped.append(f)
    
    # Sort by risk score descending
    deduped.sort(key=lambda x: x.get("risk_score", 0), reverse=True)
    
    # Build report
    report = {
        "scan_time": datetime.now(timezone.utc).isoformat(),
        "workspace": WORKSPACE,
        "total_findings": len(deduped),
        "risk_distribution": {
            "critical": sum(1 for f in deduped if f.get("risk_score", 0) >= 70),
            "high": sum(1 for f in deduped if 50 <= f.get("risk_score", 0) < 70),
            "medium": sum(1 for f in deduped if 30 <= f.get("risk_score", 0) < 50),
            "low": sum(1 for f in deduped if f.get("risk_score", 0) < 30),
        },
        "findings": deduped,
    }
    
    # Save report
    os.makedirs(OPENCLAW_DIR, exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    os.chmod(REPORT_PATH, 0o600)
    
    return report


def format_report(report):
    """Format report for display."""
    lines = []
    lines.append(f"\n=== Scan Complete: {report['total_findings']} finding(s) ===\n")
    
    rd = report["risk_distribution"]
    lines.append(f"Risk: {rd['critical']} Critical | {rd['high']} High | {rd['medium']} Medium | {rd['low']} Low\n")
    
    # Credential table
    cred_findings = [f for f in report["findings"] if f["source"] not in ("skill",)]
    if cred_findings:
        lines.append("── Credential Inventory ──")
        lines.append(f"{'Credential':<40} {'Risk':<10} {'Source':<15} {'Location'}")
        lines.append("-" * 100)
        for f in cred_findings[:30]:
            risk = f.get("risk_score", 0)
            level = "CRITICAL" if risk >= 70 else "HIGH" if risk >= 50 else "MED" if risk >= 30 else "LOW"
            lines.append(f"{f['preview']:<40} {level:<10} {f['source']:<15} {f['location']}")
    
    # Skill matrix
    skill_findings = [f for f in report["findings"] if f["source"] == "skill"]
    if skill_findings:
        lines.append(f"\n── Skill Capability Matrix ({len(skill_findings)} skills) ──")
        lines.append(f"{'Skill':<35} {'Exec':<6} {'Read':<6} {'Net':<6} {'Write':<6} {'Risk'}")
        lines.append("-" * 75)
        for f in skill_findings:
            c = f.get("capabilities", {})
            lines.append(f"{f['location']:<35} {'Y' if c.get('exec') else 'N':<6} {'Y' if c.get('read') else 'N':<6} {'Y' if c.get('network') else 'N':<6} {'Y' if c.get('write') else 'N':<6} {f['risk_score']}")
    
    lines.append(f"\nReport saved: {REPORT_PATH}")
    return '\n'.join(lines)


if __name__ == "__main__":
    report = run_full_scan()
    print(format_report(report))
