"""
门下省 - 政令审核、封驳权
负责审核中书省创建的任务，行使封驳权（通过/驳回）
"""

import json
from datetime import datetime
from pathlib import Path

# 导入中书省函数
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from skill1.zhongshu.main import get_task_draft, update_task_draft
from skill1.config import ACTIVE_TASKS_DIR


def audit_task_draft(task_id: str, audit_result: str = "pass", audit_message: str = "") -> dict:
    """
    审核任务档案
    返回审核结果
    """
    # 获取任务档案
    try:
        task_draft = get_task_draft(task_id)
    except FileNotFoundError:
        return {
            "success": False,
            "error": f"任务档案不存在: {task_id}",
            "audit_status": "error"
        }
    
    # 检查当前状态
    if task_draft["status"] != "draft":
        return {
            "success": False,
            "error": f"任务状态不是draft: {task_draft['status']}",
            "audit_status": "error"
        }
    
    # 审核逻辑
    audit_status = audit_result.lower()
    if audit_status not in ["pass", "reject"]:
        audit_status = "pass"  # 默认通过
    
    # 更新任务状态
    new_status = "audited_pass" if audit_status == "pass" else "audited_reject"
    
    updates = {
        "status": new_status,
        "audit_status": audit_status,
        "audit_message": audit_message,
        "audited_at": datetime.now().isoformat(),
        "department_checks": {
            **task_draft["department_checks"],
            "menxia": True  # 门下省已处理
        }
    }
    
    # 保存更新
    success = update_task_draft(task_id, updates)
    
    if not success:
        return {
            "success": False,
            "error": "更新任务档案失败",
            "audit_status": "error"
        }
    
    # 创建审核日志
    task_dir = Path(ACTIVE_TASKS_DIR) / task_id
    audit_log = {
        "task_id": task_id,
        "audit_status": audit_status,
        "audit_message": audit_message,
        "audited_at": datetime.now().isoformat(),
        "original_order": task_draft["emperor_order"],
        "token_budget": task_draft["token_budget"]
    }
    
    audit_log_file = task_dir / "audit_log.json"
    with open(audit_log_file, 'w', encoding='utf-8') as f:
        json.dump(audit_log, f, ensure_ascii=False, indent=2)
    
    # 输出结果
    if audit_status == "pass":
        print(f"✅ 门下省：任务审核通过")
        print(f"  任务ID: {task_id}")
        print(f"  审核意见: {audit_message}")
    else:
        print(f"❌ 门下省：任务审核驳回")
        print(f"  任务ID: {task_id}")
        print(f"  驳回原因: {audit_message}")
    
    return {
        "success": True,
        "task_id": task_id,
        "audit_status": audit_status,
        "audit_message": audit_message,
        "new_status": new_status,
        "task_dir": str(task_dir)
    }


def get_audit_log(task_id: str) -> dict:
    """获取审核日志"""
    task_dir = Path(ACTIVE_TASKS_DIR) / task_id
    audit_log_file = task_dir / "audit_log.json"
    
    if not audit_log_file.exists():
        return {}
    
    with open(audit_log_file, 'r', encoding='utf-8') as f:
        return json.load(f)


class MenXia:
    """门下省类（兼容旧版本）"""
    
    @staticmethod
    def audit_task(task_id: str, audit_result: str = "pass", audit_message: str = "") -> dict:
        """审核任务（兼容方法）"""
        return audit_task_draft(task_id, audit_result, audit_message)


if __name__ == "__main__":
    # 测试门下省功能
    print("🏛️ 门下省功能测试")
    
    # 先创建一个测试任务
    from ..zhongshu.main import create_task_archive
    task_id, task_dir = create_task_archive("测试圣旨：门下省审核测试", 300)
    
    # 审核任务
    result = audit_task_draft(task_id, "pass", "测试审核通过")
    print(f"✅ 测试完成：{result}")