"""
户部 - 资源管理、Token预算
负责管理Token预算，记录账本，资源分配
"""

import json
from datetime import datetime
from pathlib import Path

from ...config import ACTIVE_TASKS_DIR


def create_token_ledger(task_id: str, initial_budget: int = 1000) -> dict:
    """创建Token账本"""
    task_dir = Path(ACTIVE_TASKS_DIR) / task_id
    ledger_file = task_dir / "token_ledger.json"
    
    ledger = {
        "task_id": task_id,
        "initial_budget": initial_budget,
        "used_tokens": 0,
        "available_tokens": initial_budget,
        "transactions": [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    with open(ledger_file, 'w', encoding='utf-8') as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
    
    print(f"💰 户部：Token账本已创建")
    print(f"  任务ID: {task_id}")
    print(f"  初始预算: {initial_budget}")
    
    return ledger


def get_token_ledger(task_id: str) -> dict:
    """获取Token账本"""
    task_dir = Path(ACTIVE_TASKS_DIR) / task_id
    ledger_file = task_dir / "token_ledger.json"
    
    if not ledger_file.exists():
        return {}
    
    with open(ledger_file, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    print("🏛️ 户部功能测试")
    print("✅ 户部模块已加载")
