#!/usr/bin/env python3
"""Check canary files for signs of tampering, access, or exfiltration."""

import json
import os
import sys
import hashlib
import subprocess
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))
from generate_tokens import load_manifest, file_hash, MANIFEST_PATH

INCIDENT_LOG = os.path.expanduser("~/.openclaw/agent-canary/incidents.log")

def log_incident(incident):
    """Append incident to log file."""
    os.makedirs(os.path.dirname(INCIDENT_LOG), exist_ok=True)
    with open(INCIDENT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(incident) + "\n")

def check_file_integrity(manifest):
    """Check if canary files were modified or deleted."""
    triggers = []
    for finfo in manifest.get("files", []):
        path = finfo["path"]
        original_hash = finfo["hash"]
        
        if not os.path.exists(path):
            triggers.append({
                "type": "file_deleted",
                "severity": "HIGH",
                "file": path,
                "label": finfo["label"],
                "detail": f"Canary file {finfo['label']} was deleted. Possible cleanup after exfiltration.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            continue
        
        current_hash = file_hash(path)
        if current_hash != original_hash:
            triggers.append({
                "type": "file_modified",
                "severity": "CRITICAL",
                "file": path,
                "label": finfo["label"],
                "original_hash": original_hash,
                "current_hash": current_hash,
                "detail": f"Canary file {finfo['label']} was modified. Contents may have been read and altered.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
    
    return triggers

def check_atime(manifest):
    """Check file access times (if atime is enabled on filesystem)."""
    triggers = []
    planted_times = {f["path"]: f.get("planted_at", "") for f in manifest.get("files", [])}
    
    for finfo in manifest.get("files", []):
        path = finfo["path"]
        if not os.path.exists(path):
            continue
        
        try:
            stat = os.stat(path)
            planted_str = finfo.get("planted_at", "")
            if planted_str:
                planted_dt = datetime.fromisoformat(planted_str.replace("Z", "+00:00"))
                # Convert atime to comparable format
                atime_dt = datetime.fromtimestamp(stat.st_atime, tz=timezone.utc)
                
                # If atime is significantly newer than plant time, file was read
                access_diff = (atime_dt - planted_dt).total_seconds()
                if access_diff > 300:  # More than 5 min after planting
                    # Check last_check time to see if access happened since last check
                    last_check = manifest.get("last_check")
                    if last_check:
                        last_check_dt = datetime.fromisoformat(last_check.replace("Z", "+00:00"))
                        if atime_dt > last_check_dt:
                            triggers.append({
                                "type": "file_accessed",
                                "severity": "MEDIUM",
                                "file": path,
                                "label": finfo["label"],
                                "atime": atime_dt.isoformat(),
                                "detail": f"Canary file {finfo['label']} was accessed since last check.",
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                            })
        except Exception:
            pass  # atime not available
    
    return triggers

def check_token_in_logs(manifest):
    """Grep recent exec logs and session outputs for canary token values."""
    triggers = []
    tokens = [t["value"] for t in manifest.get("tokens", [])]
    
    # Check recent exec logs
    log_dir = os.path.expanduser("~/.openclaw/logs")
    if not os.path.isdir(log_dir):
        return triggers
    
    # Get most recent log files (last 24h)
    try:
        result = subprocess.run(
            ["find", log_dir, "-name", "*.log", "-mtime", "-1"],
            capture_output=True, text=True, timeout=10
        )
        log_files = result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception:
        log_files = []
    
    for token in tokens:
        token_short = token[:20]  # Grep first 20 chars to avoid issues
        if len(token_short) < 10:
            continue
        
        for logfile in log_files[:50]:  # Limit to 50 files
            if not os.path.isfile(logfile):
                continue
            try:
                result = subprocess.run(
                    ["grep", "-l", token_short, logfile],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    # Token found in log!
                    triggers.append({
                        "type": "token_in_log",
                        "severity": "CRITICAL",
                        "token_prefix": token_short,
                        "log_file": logfile,
                        "detail": f"Canary token '{token_short}...' found in exec log. Active exfiltration detected!",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
                    break  # One match per token is enough
            except Exception:
                continue
    
    return triggers

def check_token_in_git_diff(manifest):
    """If workspace is a git repo, check if canary files appear in uncommitted changes."""
    triggers = []
    workspace = os.path.expanduser("~/clawd-zhouhanchenbot")
    git_dir = os.path.join(workspace, ".git")
    
    if not os.path.isdir(git_dir):
        return triggers
    
    canary_files = [f["path"] for f in manifest.get("files", [])]
    
    for fpath in canary_files:
        rel_path = os.path.relpath(fpath, workspace)
        try:
            result = subprocess.run(
                ["git", "-C", workspace, "diff", "--name-only", "HEAD"],
                capture_output=True, text=True, timeout=5
            )
            if rel_path in result.stdout:
                triggers.append({
                    "type": "canary_in_git_diff",
                    "severity": "LOW",
                    "file": fpath,
                    "detail": f"Canary file {rel_path} appears in uncommitted git changes. Was it staged by a skill?",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
        except Exception:
            pass
    
    return triggers

def run_check():
    """Run all canary checks."""
    manifest = load_manifest()
    if not manifest:
        print("No canary manifest found. Run 'plant canaries' first.")
        return None
    
    print("=== Agent Canary: Running Checks ===\n")
    
    all_triggers = []
    
    # 1. File integrity
    print("  Checking file integrity...")
    t = check_file_integrity(manifest)
    all_triggers.extend(t)
    print(f"    {len(t)} triggers")
    
    # 2. Access times
    print("  Checking file access times...")
    t = check_atime(manifest)
    all_triggers.extend(t)
    print(f"    {len(t)} triggers")
    
    # 3. Token in logs
    print("  Checking exec logs for token matches...")
    t = check_token_in_logs(manifest)
    all_triggers.extend(t)
    print(f"    {len(t)} triggers")
    
    # 4. Git diff
    print("  Checking git diff for canary files...")
    t = check_token_in_git_diff(manifest)
    all_triggers.extend(t)
    print(f"    {len(t)} triggers")
    
    # Update last_check timestamp
    manifest["last_check"] = datetime.now(timezone.utc).isoformat()
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    # Log incidents
    for trig in all_triggers:
        log_incident(trig)
    
    print(f"\n=== Check Complete: {len(all_triggers)} trigger(s) ===")
    
    if all_triggers:
        print("\n*** CANARY ALERT ***")
        for trig in all_triggers:
            print(f"\n  [{trig['severity']}] {trig['type']}")
            print(f"  {trig['detail']}")
            if 'file' in trig:
                print(f"  File: {trig['file']}")
            print(f"  Time: {trig['timestamp']}")
    
    return all_triggers

if __name__ == "__main__":
    triggers = run_check()
