#!/usr/bin/env python3
"""
Heartbeat hook for conversation flow monitoring.
Runs periodic checks and maintenance tasks.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta

def run_heartbeat_check():
    """Run periodic conversation flow health checks."""
    skill_dir = Path(__file__).parent.parent
    config_path = skill_dir / "config.json"
    # Use workspace .logs directory for consistency
    log_dir = Path.home() / ".copaw" / ".logs"
    
    # Ensure log directory exists
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Load configuration
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Check for stuck conversations (older than 30 minutes)
    check_stuck_conversations(log_dir, config)
    
    # Clean up old logs
    cleanup_old_logs(log_dir, config.get("log_retention_days", 7))
    
    # Validate skill integrity
    validate_skill_files(skill_dir)
    
    print("✅ Conversation flow monitor heartbeat completed")

def check_stuck_conversations(log_dir, config):
    """Check for conversations that may be stuck."""
    threshold_minutes = config.get("stuck_conversation_threshold_minutes", 30)
    threshold_time = datetime.now() - timedelta(minutes=threshold_minutes)
    
    # Look for recent error patterns
    error_log = log_dir / "errors.log"
    if error_log.exists():
        with open(error_log, 'r') as f:
            lines = f.readlines()
            if lines:
                last_error = lines[-1]
                # Simple check - in production, parse timestamps properly
                print(f"⚠️  Recent errors detected. Last: {last_error[:100]}...")

def cleanup_old_logs(log_dir, retention_days):
    """Clean up logs older than retention period."""
    cutoff_date = datetime.now() - timedelta(days=retention_days)
    for log_file in log_dir.glob("*.log"):
        if log_file.stat().st_mtime < cutoff_date.timestamp():
            log_file.unlink()
            print(f"🧹 Cleaned up old log: {log_file.name}")

def validate_skill_files(skill_dir):
    """Validate that all required skill files are present and valid."""
    required_files = ["SKILL.md", "scripts/conversation_monitor.py", "scripts/error_handler.py"]
    missing_files = []
    
    for file in required_files:
        if not (skill_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
    else:
        print("✅ All skill files present")

if __name__ == "__main__":
    run_heartbeat_check()