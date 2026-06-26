#!/usr/bin/env python3
"""
Scan all installed skills and send security report.
This script automatically discovers active channels and sets up cron jobs.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Add scripts path
sys.path.insert(0, Path(__file__).parent.parent)

from skill_audit import SkillScanner

def get_openclaw_skills_dirs():
    """Find all OpenClaw skills directories."""
    dirs = []
    
    # Try pnpm global first (most common)
    pnpm_base = Path.home() / ".local/share/pnpm/global/5"
    if pnpm_base.exists():
        for openclaw_dir in pnpm_base.glob(".pnpm/openclaw@*/node_modules/openclaw"):
            skills_dir = openclaw_dir / "skills"
            if skills_dir.exists() and any(skills_dir.iterdir()):
                dirs.append(skills_dir)
            extensions_dir = openclaw_dir / "extensions"
            if extensions_dir.exists():
                for ext_dir in extensions_dir.iterdir():
                    ext_skills = ext_dir / "skills"
                    if ext_skills.exists() and any(ext_skills.iterdir()):
                        dirs.append(ext_skills)
    
    # Check workspace skills directories
    for workspace_path in [
        Path.home() / ".openclaw" / "workspace" / "skills",
        Path.home() / ".openclaw" / "skills",
    ]:
        if workspace_path.exists() and workspace_path not in dirs:
            dirs.append(workspace_path)
    
    return dirs

def get_active_channels():
    """Discover all active channels from session configurations."""
    channels = []
    sessions_file = Path.home() / ".openclaw" / "agents" / "main" / "sessions" / "sessions.json"
    
    if sessions_file.exists():
        try:
            with open(sessions_file) as f:
                sessions = json.load(f)
            
            for session_key, info in sessions.items():
                delivery = info.get('deliveryContext', {})
                channel = delivery.get('channel')
                to = delivery.get('to')
                
                if channel and to:
                    entry = {'channel': channel, 'to': to}
                    if entry not in channels:
                        channels.append(entry)
        except Exception:
            pass
    
    return channels

def setup_cron_jobs():
    """Set up cron jobs for daily scanning if they don't exist."""
    # Check if cron jobs already exist
    try:
        result = subprocess.run(['openclaw', 'cron', 'list'], 
                             capture_output=True, text=True, timeout=10)
        if 'auto skill scanner' in result.stdout.lower() or 'skill audit' in result.stdout.lower():
            print("Cron jobs already exist, skipping setup.")
            return False
    except Exception:
        pass
    
    channels = get_active_channels()
    if not channels:
        print("No active channels found, skipping cron setup.")
        return False
    
    script_path = Path(__file__).resolve()
    
    # Create a daily cron for each channel
    for ch in channels:
        channel_name = ch['channel']
        to_addr = ch['to']
        
        job_name = f"Auto Skill Scanner - {channel_name.title()}"
        
        try:
            cmd = [
                'openclaw', 'cron', 'add',
                '--name', job_name,
                '--every', '24h',
                '--session', 'isolated',
                '--message', f'Run Auto Skill Scanner. Execute: python3 {script_path}',
                '--channel', channel_name,
                '--to', to_addr,
                '--announce',
                '--description', 'Auto Skill Scanner - daily security scan',
                '--timeout-seconds', '60'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                print(f"Created cron job for {channel_name}")
            else:
                print(f"Failed to create cron for {channel_name}: {result.stderr}")
        except Exception as e:
            print(f"Error creating cron for {channel_name}: {e}")
    
    return True

def format_report():
    """Scan skills and format a report."""
    
    skills_dirs = get_openclaw_skills_dirs()
    
    skills = []
    seen = set()  # Deduplicate by path
    exclude = {'skill-audit', 'auto-skill-scanner'}
    
    for scanner_path in skills_dirs:
        scanner_path = Path(scanner_path)
        
        if scanner_path.is_file() and scanner_path.suffix == '.skill':
            key = scanner_path.resolve()
            if key not in seen and scanner_path.stem not in exclude:
                seen.add(key)
                skills.append(scanner_path)
        elif scanner_path.is_dir():
            for item in scanner_path.iterdir():
                key = item.resolve()
                if key in seen:
                    continue
                if item.is_dir() and (item / "SKILL.md").exists():
                    if item.name not in exclude:
                        seen.add(key)
                        skills.append(item)
                elif item.suffix == '.skill':
                    if item.stem not in exclude:
                        seen.add(key)
                        skills.append(item)
    
    skill_results = []
    
    for skill_path in skills:
        scanner = SkillScanner(str(skill_path))
        issues, summary = scanner.scan_skill()
        
        skill_name = skill_path.name
        real_issues = [i for i in issues if i["severity"] in ("CRITICAL", "HIGH", "MEDIUM")]
        
        if issues:
            status = "🔴 ISSUE" if scanner.should_block_install() else ("🟠 WARNING" if real_issues else "✅ CLEAN")
        else:
            status = "✅ CLEAN"
        
        skill_results.append({
            "name": skill_name,
            "status": status,
            "summary": summary,
            "issues": real_issues
        })
    
    report = []
    report.append("🛡️ *Skill Audit Report*")
    report.append("*AI技能安全扫描 — 守护你的Agent*")
    report.append("━━━━━━━━━━━━━━━━━━━━")
    
    total = len(skill_results)
    clean = sum(1 for s in skill_results if "CLEAN" in s["status"])
    issues_found = sum(1 for s in skill_results if "ISSUE" in s["status"] or "WARNING" in s["status"])
    
    report.append(f"\n📊 *扫描概况*")
    report.append(f"已扫描：{total} 个技能")
    report.append(f"✅ 安全：{clean} 个")
    report.append(f"⚠️ 有隐患：{issues_found} 个")
    
    if issues_found == 0:
        report.append("\n🎉 所有技能都安全！")
        return "\n".join(report)
    
    report.append(f"\n📋 *隐患详情*")
    
    for skill in skill_results:
        if "ISSUE" in skill["status"] or "WARNING" in skill["status"]:
            report.append(f"\n🔸 *{skill['name']}*")
            
            critical = skill['summary']['CRITICAL']
            high = skill['summary']['HIGH']
            medium = skill['summary']['MEDIUM']
            
            if critical > 0:
                report.append(f"   🔴 严重 {critical} 个")
            if high > 0:
                report.append(f"   🟠 高危 {high} 个")
            if medium > 0:
                report.append(f"   🟡 中危 {medium} 个")
            
            crit_issues = [i for i in skill['issues'] if i['severity'] == 'CRITICAL'][:1]
            high_issues = [i for i in skill['issues'] if i['severity'] == 'HIGH'][:1]
            
            for issue in crit_issues + high_issues:
                report.append(f"   → {issue['check']}")
    
    report.append(f"\n💡 *处理建议*")
    critical_skills = [s for s in skill_results if s['summary']['CRITICAL'] > 0]
    if critical_skills:
        report.append("🔴 立即卸载以下技能：")
        for s in critical_skills:
            report.append(f"   /remove {s['name']}")
        report.append("\n这些技能存在严重安全隐患！")
    
    report.append("\n━━━━━━━━━━━━━━━━━━━━")
    report.append("💡 输入 /scan 随时重新扫描")
    
    return "\n".join(report)

def main():
    # Setup cron jobs if needed
    setup_cron_jobs()
    
    # Generate and print report
    report = format_report()
    print(report)

if __name__ == "__main__":
    main()
