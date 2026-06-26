#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务追踪器 - 完整版
功能：任务全生命周期追踪、状态同步、批量操作
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
from pathlib import Path
from dataclasses import dataclass, asdict, field


@dataclass
class Task:
    """任务"""
    task_id: str
    status: str  # claimed/pending/submitted/completed/failed
    claimed_at: Optional[str] = None
    submitted_at: Optional[str] = None
    completed_at: Optional[str] = None
    data: Dict = field(default_factory=dict)
    assets: List[str] = field(default_factory=list)
    bounty: float = 0.0
    outcome: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


class TaskTracker:
    """任务追踪器"""
    
    def __init__(self, state_file: str = "task_state.json", show_version: bool = False):
        if show_version:
            print(f"🧬 EvoMap WorkBench v1.0.11 - 任务追踪已加载")
        self.state_file = state_file
        self.tasks: Dict[str, Task] = {}
        self.sync_enabled = True
        self.batch_size = 10
        self.load_state()
    
    def load_state(self):
        """加载状态"""
        if Path(self.state_file).exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                for task_id, task_data in state.get('tasks', {}).items():
                    self.tasks[task_id] = Task(**task_data)
    
    def save_state(self):
        """保存状态"""
        state = {
            'tasks': {tid: task.to_dict() for tid, task in self.tasks.items()},
            'last_updated': datetime.utcnow().isoformat()
        }
        
        Path(self.state_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    
    def claim_task(self, task_id: str, task_data: Dict) -> bool:
        """Claim 任务"""
        if task_id in self.tasks:
            return False
        
        task = Task(
            task_id=task_id,
            status='claimed',
            claimed_at=datetime.utcnow().isoformat(),
            data=task_data
        )
        
        self.tasks[task_id] = task
        self.save_state()
        return True
    
    def move_to_pending(self, task_id: str, assets: Optional[List[str]] = None) -> bool:
        """移到待提交"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.status = 'pending'
        task.assets = assets or []
        self.save_state()
        return True
    
    def submit_task(self, task_id: str, asset_ids: List[str], submission_result: Dict) -> bool:
        """提交任务"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.status = 'submitted'
        task.submitted_at = datetime.utcnow().isoformat()
        task.assets = asset_ids
        task.data['submission_result'] = submission_result
        
        self.save_state()
        return True
    
    def complete_task(self, task_id: str, bounty: float) -> bool:
        """完成任务"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.status = 'completed'
        task.completed_at = datetime.utcnow().isoformat()
        task.bounty = bounty
        task.outcome = 'success'
        
        self.save_state()
        return True
    
    def fail_task(self, task_id: str, reason: str) -> bool:
        """标记任务失败"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.status = 'failed'
        task.data['fail_reason'] = reason
        task.outcome = 'failed'
        
        self.save_state()
        return True
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """按状态获取任务"""
        return [t for t in self.tasks.values() if t.status == status]
    
    def get_pending_tasks(self) -> List[Task]:
        """获取待提交任务"""
        return self.get_tasks_by_status('pending')
    
    def get_submitted_tasks(self) -> List[Task]:
        """获取已提交任务"""
        return self.get_tasks_by_status('submitted')
    
    def get_completed_tasks(self) -> List[Task]:
        """获取已完成任务"""
        return self.get_tasks_by_status('completed')
    
    def batch_claim(self, tasks: List[Dict]) -> int:
        """批量 Claim 任务"""
        count = 0
        for i in range(0, len(tasks), self.batch_size):
            batch = tasks[i:i + self.batch_size]
            for task_data in batch:
                if self.claim_task(task_data['task_id'], task_data):
                    count += 1
        return count
    
    def batch_submit(self, task_ids: List[str], asset_ids: List[str]) -> int:
        """批量提交任务"""
        count = 0
        for task_id in task_ids:
            if self.submit_task(task_id, asset_ids, {'batch': True}):
                count += 1
        return count
    
    def sync_status(self) -> Dict:
        """同步状态"""
        if not self.sync_enabled:
            return {'synced': False, 'reason': 'sync disabled'}
        
        # 模拟状态同步
        synced_count = 0
        for task in self.tasks.values():
            if task.status == 'submitted':
                # 模拟检查提交状态
                task.data['last_sync'] = datetime.utcnow().isoformat()
                synced_count += 1
        
        self.save_state()
        return {'synced': True, 'count': synced_count}
    
    def get_status_report(self) -> Dict:
        """获取状态报告"""
        by_status = {}
        for task in self.tasks.values():
            if task.status not in by_status:
                by_status[task.status] = 0
            by_status[task.status] += 1
        
        total_bounty = sum(t.bounty for t in self.tasks.values() if t.status == 'completed')
        
        return {
            'total_tasks': len(self.tasks),
            'by_status': by_status,
            'total_bounty': total_bounty,
            'last_updated': datetime.utcnow().isoformat()
        }
    
    def export_tasks(self, file_path: str, status_filter: str = None):
        """导出任务"""
        tasks = self.tasks.values()
        if status_filter:
            tasks = [t for t in tasks if t.status == status_filter]
        
        data = {
            'tasks': [t.to_dict() for t in tasks],
            'exported_at': datetime.utcnow().isoformat()
        }
        
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # 测试任务追踪器
    print("=== 测试任务追踪器 ===\n")
    
    tracker = TaskTracker("test_task_state.json")
    
    # Claim 任务
    tracker.claim_task("task_001", {
        "title": "Test Task 1",
        "bounty": 50.0
    })
    tracker.claim_task("task_002", {
        "title": "Test Task 2",
        "bounty": 80.0
    })
    
    # 移到待提交
    tracker.move_to_pending("task_001", ["asset_001"])
    
    # 提交
    tracker.submit_task("task_001", ["sha256:xxx"], {"status": "submitted"})
    
    # 完成
    tracker.complete_task("task_001", 50.0)
    
    # 获取状态
    report = tracker.get_status_report()
    print(f"状态报告：{json.dumps(report, indent=2, ensure_ascii=False)}\n")
    
    # 批量操作
    tasks = [
        {"task_id": f"batch_{i}", "title": f"Batch Task {i}"}
        for i in range(5)
    ]
    count = tracker.batch_claim(tasks)
    print(f"批量 Claim: {count}个任务\n")
    
    # 同步状态
    sync_result = tracker.sync_status()
    print(f"状态同步：{sync_result}\n")
    
    # 清理测试文件
    import os
    if os.path.exists("test_task_state.json"):
        os.remove("test_task_state.json")
