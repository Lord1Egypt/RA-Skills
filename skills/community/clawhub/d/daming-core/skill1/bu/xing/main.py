"""
刑部 - 审计检查、合规验证
负责审计任务执行，验证合规性
"""

import json
from datetime import datetime
from pathlib import Path

from ...config import ACTIVE_TASKS_DIR


def audit_task_compliance(task_id: str) -> dict:
    """审计任务合规性"""
    task_dir = Path(ACTIVE_TASKS_DIR) / task_id
    
    # 检查所有必要文件
    required_files = [
        ("task_draft.json", "任务档案"),
        ("audit_log.json", "审核日志"),
        ("token_ledger.json", "Token账本")
    ]
    
    compliance_report = {
        "task_id": task_id,
        "audited_at": datetime.now().isoformat(),
        "files_check": {},
        "compliance_issues": [],
        "overall_compliant": True
    }
    
    # 检查文件存在性
    for filename, description in required_files:
        file_path = task_dir / filename
        exists = file_path.exists()
        compliance_report["files_check"][filename] = {
            "exists": exists,
            "description": description
        }
        
        if not exists:
            compliance_report["compliance_issues"].append(f"缺少{description}: {filename}")
            compliance_report["overall_compliant"] = False
    
    # 检查任务档案完整性
    task_file = task_dir / "task_draft.json"
    if task_file.exists():
        with open(task_file, 'r', encoding='utf-8') as f:
            task_draft = json.load(f)
        
        required_fields = ["task_id", "emperor_order", "status", "created_at"]
        for field in required_fields:
            if field not in task_draft:
                compliance_report["compliance_issues"].append(f"任务档案缺少字段: {field}")
                compliance_report["overall_compliant"] = False
    
    print(f"⚖️  刑部：任务合规审计完成")
    print(f"  任务ID: {task_id}")
    print(f"  合规状态: {'通过' if compliance_report['overall_compliant'] else '不通过'}")
    print(f"  发现问题: {len(compliance_report['compliance_issues'])}个")
    
    return compliance_report


if __name__ == "__main__":
    print("🏛️ 刑部功能测试")
    print("✅ 刑部审计模块已加载")
