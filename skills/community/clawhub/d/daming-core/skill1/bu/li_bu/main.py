"""
吏部 - 结果格式化、报告生成
负责格式化执行结果，生成报告
"""

import json
from datetime import datetime
from pathlib import Path

from ...config import ACTIVE_TASKS_DIR


def format_task_report(task_id: str) -> dict:
    """格式化任务报告"""
    task_dir = Path(ACTIVE_TASKS_DIR) / task_id
    
    # 收集所有信息
    report = {
        "task_id": task_id,
        "report_generated_at": datetime.now().isoformat(),
        "summary": {},
        "details": {},
        "recommendations": []
    }
    
    # 任务档案
    task_file = task_dir / "task_draft.json"
    if task_file.exists():
        with open(task_file, 'r', encoding='utf-8') as f:
            task_draft = json.load(f)
            report["summary"]["task_info"] = {
                "emperor_order": task_draft.get("emperor_order", ""),
                "status": task_draft.get("status", ""),
                "created_at": task_draft.get("created_at", ""),
                "token_budget": task_draft.get("token_budget", 0)
            }
    
    # 审核信息
    audit_file = task_dir / "audit_log.json"
    if audit_file.exists():
        with open(audit_file, 'r', encoding='utf-8') as f:
            audit_log = json.load(f)
            report["summary"]["audit_info"] = {
                "audit_status": audit_log.get("audit_status", ""),
                "audit_message": audit_log.get("audit_message", ""),
                "audited_at": audit_log.get("audited_at", "")
            }
    
    # Token使用
    ledger_file = task_dir / "token_ledger.json"
    if ledger_file.exists():
        with open(ledger_file, 'r', encoding='utf-8') as f:
            token_ledger = json.load(f)
            report["summary"]["token_usage"] = {
                "initial_budget": token_ledger.get("initial_budget", 0),
                "used_tokens": token_ledger.get("used_tokens", 0),
                "available_tokens": token_ledger.get("available_tokens", 0),
                "utilization_rate": f"{(token_ledger.get('used_tokens', 0) / token_ledger.get('initial_budget', 1)) * 100:.1f}%"
            }
    
    # 执行记录
    exec_file = task_dir / "execution_records.json"
    if exec_file.exists():
        with open(exec_file, 'r', encoding='utf-8') as f:
            execution_data = json.load(f)
            report["details"]["execution_records"] = execution_data
            report["summary"]["execution_count"] = len(execution_data)
    
    # 生成建议
    if report["summary"].get("token_usage", {}).get("available_tokens", 0) < 100:
        report["recommendations"].append("Token预算即将用完，建议增加预算")
    
    if report["summary"].get("execution_count", 0) == 0:
        report["recommendations"].append("任务尚未执行，建议调度执行")
    
    # 保存报告
    report_file = task_dir / "task_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"📋 吏部：任务报告已生成")
    print(f"  任务ID: {task_id}")
    print(f"  报告文件: {report_file}")
    
    return report


if __name__ == "__main__":
    print("🏛️ 吏部功能测试")
    print("✅ 吏部报告模块已加载")
