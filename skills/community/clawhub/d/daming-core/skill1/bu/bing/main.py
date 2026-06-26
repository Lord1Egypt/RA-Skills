"""
兵部 - 状态监控、执行追踪
负责监控任务状态，追踪执行进度
"""

import json
from datetime import datetime
from pathlib import Path

from ...config import ACTIVE_TASKS_DIR, TASK_STATUSES


def monitor_task_status(task_id: str) -> dict:
    """监控任务状态"""
    task_dir = Path(ACTIVE_TASKS_DIR) / task_id
    
    # 检查任务档案
    task_file = task_dir / "task_draft.json"
    if not task_file.exists():
        return {
            "success": False,
            "error": f"任务档案不存在: {task_id}",
            "status": "not_found"
        }
    
    with open(task_file, 'r', encoding='utf-8') as f:
        task_draft = json.load(f)
    
    # 检查审核日志
    audit_file = task_dir / "audit_log.json"
    audit_status = "未审核"
    if audit_file.exists():
        with open(audit_file, 'r', encoding='utf-8') as f:
            audit_log = json.load(f)
            audit_status = audit_log.get("audit_status", "未审核")
    
    # 检查执行记录
    exec_file = task_dir / "execution_records.json"
    execution_count = 0
    if exec_file.exists():
        with open(exec_file, 'r', encoding='utf-8') as f:
            execution_data = json.load(f)
            execution_count = len(execution_data)
    
    # 检查Token账本
    ledger_file = task_dir / "token_ledger.json"
    token_info = {}
    if ledger_file.exists():
        with open(ledger_file, 'r', encoding='utf-8') as f:
            token_ledger = json.load(f)
            token_info = {
                "initial_budget": token_ledger.get("initial_budget", 0),
                "used_tokens": token_ledger.get("used_tokens", 0),
                "available_tokens": token_ledger.get("available_tokens", 0)
            }
    
    status = task_draft.get("status", "unknown")
    status_display = TASK_STATUSES.get(status, "未知状态")
    
    return {
        "success": True,
        "task_id": task_id,
        "status": status,
        "status_display": status_display,
        "audit_status": audit_status,
        "execution_count": execution_count,
        "token_info": token_info,
        "department_checks": task_draft.get("department_checks", {}),
        "last_updated": task_draft.get("updated_at", "")
    }


if __name__ == "__main__":
    print("🏛️ 兵部功能测试")
    print("✅ 兵部监控模块已加载")
