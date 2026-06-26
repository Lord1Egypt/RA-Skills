#!/usr/bin/env python3
"""Delegation completion handler - updates token tracking on completion."""
import json
import sys
from pathlib import Path
from datetime import datetime

PROJECT_DIR = "/a0/usr/projects/frugal_orchestrator"
TOKENS_FILE = Path(PROJECT_DIR) / "logs" / "tokens.json"

def complete_delegation(session_id: str, actual_tokens: int, status: str = "completed"):
    """Update delegation record with completion metrics."""
    if not TOKENS_FILE.exists():
        print(f'{{"error": "tokens.json not found"}}')
        return 1
    
    logs = json.loads(TOKENS_FILE.read_text())
    
    # Find and update the session
    for entry in logs:
        if entry.get("session_id") == session_id:
            estimated = entry.get("estimated_burn", 0)
            saved = estimated - actual_tokens if estimated > actual_tokens else 0
            percent = round((saved / estimated) * 100, 2) if estimated else 0
            
            entry.update({
                "status": status,
                "tokens_after": actual_tokens,
                "tokens_saved": max(0, saved),
                "percent_savings": percent,
                "completed_at": datetime.now().isoformat()
            })
            
            TOKENS_FILE.write_text(json.dumps(logs, indent=2))
            print(f'{{"success": true, "tokens_saved": {saved}, "percent_savings": {percent}}}')
            
            # Update metrics
            update_metrics(status == "completed")
            return 0
    
    print(f'{{"error": "Session {session_id} not found"}}')
    return 1

def update_metrics(success: bool):
    """Update metrics.toon and metrics.json."""
    metrics_json = Path(PROJECT_DIR) / "metrics.json"
    metrics_toon = Path(PROJECT_DIR) / "metrics.toon"
    
    stats = {
        "total_delegations": 0,
        "successful_delegations": 0,
        "failed_delegations": 0,
        "script_fallbacks": 0
    }
    
    if metrics_json.exists():
        try:
            data = json.loads(metrics_json.read_text())
            stats.update(data.get("project_stats", {}))
        except:
            pass
    
    if success:
        stats["successful_delegations"] += 1
    else:
        stats["failed_delegations"] += 1
    
    # Write JSON
    out = {
        "project_stats": stats,
        "version": "0.5.0",
        "last_updated": datetime.now().isoformat() + "Z"
    }
    metrics_json.write_text(json.dumps(out, indent=2))
    
    # Write TOON
    toon = f"""project_stats:
 total_delegations:{stats['total_delegations']}
 successful_delegations:{stats['successful_delegations']}
 failed_delegations:{stats['failed_delegations']}
 script_fallbacks:{stats['script_fallbacks']}
version: 0.5.0
last_updated: {datetime.now().isoformat()}Z
"""
    metrics_toon.write_text(toon)
    print(f"Metrics updated: {stats['successful_delegations']} success, {stats['failed_delegations']} failed")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: delegate_complete.py <session_id> <actual_tokens> [status]"}))
        sys.exit(1)
    
    sys.exit(complete_delegation(sys.argv[1], int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "completed"))
