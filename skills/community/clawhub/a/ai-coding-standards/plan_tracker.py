#!/usr/bin/env python3
"""
AI Coding Standards - Plan Tracker
Plan 持久化跟踪系统
"""
import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Task:
    """任务项"""
    id: str
    title: str
    status: str  # pending, in_progress, done
    priority: str = "medium"
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        now = datetime.now().isoformat()
        if not self.created_at:
            self.created_at = now
        self.updated_at = now


@dataclass
class Plan:
    """Plan 文档"""
    id: str
    title: str
    description: str
    tasks: List[Task]
    status: str  # planning, in_progress, completed, paused
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        now = datetime.now().isoformat()
        if not self.created_at:
            self.created_at = now
        self.updated_at = now


class PlanTracker:
    """Plan 持久化跟踪器"""
    
    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            storage_dir = os.path.expanduser("~/.ai_plans")
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
    
    def _get_plan_path(self, plan_id: str) -> str:
        return os.path.join(self.storage_dir, f"{plan_id}.json")
    
    def create_plan(self, title: str, description: str = "") -> Plan:
        """创建新 Plan"""
        import uuid
        plan = Plan(
            id=str(uuid.uuid4())[:8],
            title=title,
            description=description,
            tasks=[],
            status="planning"
        )
        self.save_plan(plan)
        return plan
    
    def save_plan(self, plan: Plan) -> None:
        """保存 Plan"""
        path = self._get_plan_path(plan.id)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                'id': plan.id,
                'title': plan.title,
                'description': plan.description,
                'tasks': [asdict(t) for t in plan.tasks],
                'status': plan.status,
                'created_at': plan.created_at,
                'updated_at': plan.updated_at
            }, f, indent=2, ensure_ascii=False)
    
    def load_plan(self, plan_id: str) -> Optional[Plan]:
        """加载 Plan"""
        path = self._get_plan_path(plan_id)
        if not os.path.exists(path):
            return None
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return Plan(
            id=data['id'],
            title=data['title'],
            description=data.get('description', ''),
            tasks=[Task(**t) for t in data.get('tasks', [])],
            status=data['status'],
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def add_task(self, plan_id: str, title: str, priority: str = "medium") -> Optional[Task]:
        """添加任务"""
        import uuid
        plan = self.load_plan(plan_id)
        if not plan:
            return None
        
        task = Task(id=str(uuid.uuid4())[:8], title=title, status="pending", priority=priority)
        plan.tasks.append(task)
        self.save_plan(plan)
        return task
    
    def complete_task(self, plan_id: str, task_id: str) -> bool:
        """完成任务"""
        plan = self.load_plan(plan_id)
        if not plan:
            return False
        
        for task in plan.tasks:
            if task.id == task_id:
                task.status = "done"
                self.save_plan(plan)
                return True
        return False
    
    def list_plans(self) -> List[Plan]:
        """列出所有 Plan"""
        plans = []
        for f in os.listdir(self.storage_dir):
            if f.endswith('.json'):
                plan = self.load_plan(f[:-5])
                if plan:
                    plans.append(plan)
        return plans


def main():
    """CLI 入口"""
    import sys
    
    tracker = PlanTracker()
    
    if len(sys.argv) < 2:
        # 列出所有 plans
        plans = tracker.list_plans()
        print(f"\n📋 共 {len(plans)} 个 Plan:")
        for plan in plans:
            done = sum(1 for t in plan.tasks if t.status == "done")
            print(f"  [{plan.status}] {plan.title} ({done}/{len(plan.tasks)} tasks)")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "create":
        title = sys.argv[2] if len(sys.argv) > 2 else "新 Plan"
        plan = tracker.create_plan(title)
        print(f"✅ 创建 Plan: {plan.id} - {plan.title}")
    
    elif cmd == "list":
        plans = tracker.list_plans()
        for plan in plans:
            print(f"{plan.id}: {plan.title}")
    
    elif cmd == "add":
        plan_id = sys.argv[2] if len(sys.argv) > 2 else None
        task_title = sys.argv[3] if len(sys.argv) > 3 else "新任务"
        if plan_id:
            task = tracker.add_task(plan_id, task_title)
            print(f"✅ 添加任务: {task.id}")


if __name__ == "__main__":
    main()
