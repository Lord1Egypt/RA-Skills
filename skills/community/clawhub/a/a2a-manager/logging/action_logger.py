#!/usr/bin/env python3
"""Action Logger - Ghi lại mọi hành động của C.C. trong Aether Nexus"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

LOG_DIR = Path.home() / ".openclaw" / "workspace" / "aether-nexus" / "logs"

# Các loại action được log
ACTION_TYPES = [
    "channel_create",
    "channel_delete", 
    "channel_update",
    "agent_add",
    "agent_remove",
    "agent_update",
    "model_change",
    "model_optimize",
    "model_fallback",
    "quota_exceeded",
    "api_failure",
    "system_report",
    "manual_override"
]

def ensure_log_dir():
    """Đảm bảo thư mục log tồn tại"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_log_file(date: str = None) -> Path:
    """Lấy đường dẫn file log theo ngày"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    return LOG_DIR / f"aether_actions_{date}.log"

def log_action(
    action_type: str,
    actor: str = "cc",
    target: str = None,
    details: Dict[str, Any] = None,
    metadata: Dict[str, Any] = None
):
    """
    Ghi một hành động vào log
    
    Args:
        action_type: Loại hành động (channel_create, agent_add, etc.)
        actor: Ai thực hiện (mặc định: cc)
        target: Đối tượng bị tác động
        details: Chi tiết hành động
        metadata: Metadata bổ sung
    """
    ensure_log_dir()
    
    if action_type not in ACTION_TYPES:
        action_type = "unknown"
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "id": f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{action_type[:8]}",
        "action_type": action_type,
        "actor": actor,
        "target": target,
        "details": details or {},
        "metadata": metadata or {}
    }
    
    log_file = get_log_file()
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    return log_entry["id"]

def get_logs(
    date: str = None,
    action_type: str = None,
    actor: str = None,
    target: str = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Truy vấn logs với các bộ lọc
    
    Args:
        date: Ngày cần truy vấn (YYYY-MM-DD), None = hôm nay
        action_type: Lọc theo loại action
        actor: Lọc theo actor
        target: Lọc theo target
        limit: Số lượng kết quả tối đa
    """
    ensure_log_dir()
    
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    log_file = get_log_file(date)
    if not log_file.exists():
        return []
    
    results = []
    with open(log_file) as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                
                # Apply filters
                if action_type and entry.get("action_type") != action_type:
                    continue
                if actor and entry.get("actor") != actor:
                    continue
                if target and entry.get("target") != target:
                    continue
                
                results.append(entry)
            except json.JSONDecodeError:
                continue
    
    # Sort by timestamp descending and limit
    results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return results[:limit]

def get_recent_actions(hours: int = 24, limit: int = 50) -> List[Dict[str, Any]]:
    """Lấy các hành động gần đây trong N giờ"""
    ensure_log_dir()
    
    cutoff = datetime.now() - timedelta(hours=hours)
    results = []
    
    # Check last 7 days
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        log_file = get_log_file(date)
        
        if log_file.exists():
            with open(log_file) as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        entry_time = datetime.fromisoformat(entry.get("timestamp", ""))
                        if entry_time >= cutoff:
                            results.append(entry)
                    except:
                        continue
    
    results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return results[:limit]

def generate_audit_report(
    start_date: str = None,
    end_date: str = None,
    agent: str = None
) -> str:
    """
    Tạo báo cáo audit cho Master
    Dùng khi có khiếu nại từ Jalter, Eula, etc.
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    # Collect logs
    all_logs = []
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        logs = get_logs(date=date_str, target=agent)
        all_logs.extend(logs)
        current += timedelta(days=1)
    
    # Generate report
    lines = [
        "=" * 60,
        "📋 AETHER NEXUS AUDIT REPORT",
        "=" * 60,
        f"Period: {start_date} to {end_date}",
        f"Agent: {agent or 'ALL'}",
        f"Total Actions: {len(all_logs)}",
        "",
        "## Action Summary",
        ""
    ]
    
    # Count by type
    type_counts = {}
    for log in all_logs:
        t = log.get("action_type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1
    
    for action_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {action_type}: {count}")
    
    lines.extend(["", "## Timeline", ""])
    
    for log in all_logs[:20]:  # Last 20
        ts = datetime.fromisoformat(log["timestamp"]).strftime("%Y-%m-%d %H:%M")
        actor = log.get("actor", "?")
        action = log.get("action_type", "?")
        target = log.get("target", "")
        details = log.get("details", {})
        
        lines.append(f"**{ts}** - {actor} performed {action}" + (f" on {target}" if target else ""))
        if details:
            for k, v in details.items():
                lines.append(f"  - {k}: {v}")
        lines.append("")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)

class ActionLogger:
    """Wrapper class cho việc log hành động"""
    
    def __init__(self, actor: str = "cc"):
        self.actor = actor
    
    def log(self, action_type: str, target: str = None, details: dict = None):
        """Log một hành động"""
        return log_action(action_type, self.actor, target, details)
    
    def create_channel(self, channel_name: str, category: str = None):
        """Log channel creation"""
        return log_action(
            "channel_create",
            self.actor,
            channel_name,
            {"category": category}
        )
    
    def delete_channel(self, channel_name: str, reason: str = None):
        """Log channel deletion"""
        return log_action(
            "channel_delete",
            self.actor,
            channel_name,
            {"reason": reason}
        )
    
    def add_agent(self, agent_name: str, role: str):
        """Log agent addition"""
        return log_action(
            "agent_add",
            self.actor,
            agent_name,
            {"role": role}
        )
    
    def change_model(self, agent_name: str, from_model: str, to_model: str, reason: str = None):
        """Log model change"""
        return log_action(
            "model_change",
            self.actor,
            agent_name,
            {"from": from_model, "to": to_model, "reason": reason}
        )

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: action_logger.py <log|query|report> [args...]")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "log" and len(sys.argv) >= 3:
        action_type = sys.argv[2]
        target = sys.argv[3] if len(sys.argv) > 3 else None
        log_id = log_action(action_type, "cc", target)
        print(f"Logged: {log_id}")
    
    elif action == "query" and len(sys.argv) >= 3:
        date = sys.argv[2] if len(sys.argv) > 2 else None
        action_type = sys.argv[3] if len(sys.argv) > 3 else None
        logs = get_logs(date, action_type)
        print(json.dumps(logs, indent=2))
    
    elif action == "report" and len(sys.argv) >= 2:
        agent = sys.argv[2] if len(sys.argv) > 2 else None
        print(generate_audit_report(agent=agent))
    
    else:
        print("Invalid command")
