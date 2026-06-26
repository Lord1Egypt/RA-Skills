"""
中书省 - 政令草拟、任务创建
负责创建任务档案，设置Token预算，初始化任务状态
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path

# 导入其他部门
from ..config import ACTIVE_TASKS_DIR


def create_task_archive(emperor_order: str, token_budget: int = 1000) -> tuple[str, str]:
    """
    创建任务档案
    返回: (task_id, task_directory_path)
    """
    # 生成任务ID
    date_str = datetime.now().strftime("%Y%m%d")
    short_id = str(uuid.uuid4())[:4]
    task_id = f"T{date_str}-{short_id}"
    
    # 创建任务目录
    task_dir = Path(ACTIVE_TASKS_DIR) / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建任务档案
    task_draft = {
        "task_id": task_id,
        "emperor_order": emperor_order,
        "token_budget": token_budget,
        "status": "draft",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "department_checks": {
            "zhongshu": True,  # 中书省已处理
            "menxia": False,   # 门下省待审核
            "hu": False,       # 户部待处理
            "gong": False,     # 工部待调度
            "bing": False,     # 兵部待状态更新
            "xing": False,     # 刑部待审计
            "li_bu": False,    # 吏部待格式化
            "jinyiwei": False  # 锦衣卫待监控
        }
    }
    
    # 保存任务档案
    task_file = task_dir / "task_draft.json"
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(task_draft, f, ensure_ascii=False, indent=2)
    
    print(f"📜 中书省：任务档案已创建")
    print(f"  任务ID: {task_id}")
    print(f"  圣旨内容: {emperor_order}")
    print(f"  Token预算: {token_budget}")
    print(f"  任务目录: {task_dir}")
    
    return task_id, str(task_dir)


def get_task_draft(task_id: str) -> dict:
    """获取任务档案"""
    task_dir = Path(ACTIVE_TASKS_DIR) / task_id
    task_file = task_dir / "task_draft.json"
    
    if not task_file.exists():
        raise FileNotFoundError(f"任务档案不存在: {task_id}")
    
    with open(task_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def update_task_draft(task_id: str, updates: dict) -> bool:
    """更新任务档案"""
    task_dir = Path(ACTIVE_TASKS_DIR) / task_id
    task_file = task_dir / "task_draft.json"
    
    if not task_file.exists():
        return False
    
    with open(task_file, 'r', encoding='utf-8') as f:
        task_draft = json.load(f)
    
    # 更新字段
    task_draft.update(updates)
    task_draft["updated_at"] = datetime.now().isoformat()
    
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(task_draft, f, ensure_ascii=False, indent=2)
    
    return True


class ZhongShu:
    """中书省类（兼容旧版本）"""
    
    @staticmethod
    def create_task(emperor_order: str, token_budget: int = 1000) -> tuple[str, str]:
        """创建任务（兼容方法）"""
        return create_task_archive(emperor_order, token_budget)
    
    @staticmethod
    def get_task(task_id: str) -> dict:
        """获取任务（兼容方法）"""
        return get_task_draft(task_id)


if __name__ == "__main__":
    # 测试中书省功能
    print("🏛️ 中书省功能测试")
    task_id, task_dir = create_task_archive("测试圣旨：检查系统状态", 500)
    print(f"✅ 测试完成：{task_id} -> {task_dir}")