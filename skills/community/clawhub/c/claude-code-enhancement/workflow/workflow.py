#!/usr/bin/env python3
"""
Claude Code Enhancement Skill - 任务工作流模块
参考 Claude Code 的任务阶段划分
"""

import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from collections import defaultdict


class TaskStage(Enum):
    """任务阶段"""
    ANALYZE = "analyze"     # 分析
    PLAN = "plan"          # 规划
    EXECUTE = "execute"    # 执行
    VERIFY = "verify"      # 验证
    SUMMARIZE = "summarize"  # 总结


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskStageInfo:
    """任务阶段信息"""
    stage: TaskStage
    status: str = "pending"
    message: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


@dataclass
class Task:
    """任务"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 0  # 0=低, 1=中, 2=高
    
    # 阶段信息
    stages: Dict[TaskStage, TaskStageInfo] = field(default_factory=dict)
    current_stage: TaskStage = TaskStage.ANALYZE
    
    # 结果
    result: Optional[str] = None
    error: Optional[str] = None
    
    # 时间戳
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    
    # 依赖
    dependencies: List[str] = field(default_factory=list)
    
    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """初始化阶段"""
        if not self.stages:
            for stage in TaskStage:
                self.stages[stage] = TaskStageInfo(stage=stage)


class TaskWorkflow:
    """任务工作流 - 参考 Claude Code 的标准化任务流程"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.current_task_id: Optional[str] = None
        
        # 阶段处理器
        self.stage_handlers: Dict[TaskStage, Callable] = {}
    
    def create(self, description: str, priority: int = 1) -> str:
        """创建任务"""
        task = Task(
            id=str(uuid.uuid4())[:8],
            description=description,
            priority=priority,
            status=TaskStatus.IN_PROGRESS,
            current_stage=TaskStage.ANALYZE
        )
        
        # 启动分析阶段
        task.stages[TaskStage.ANALYZE].status = "in_progress"
        task.stages[TaskStage.ANALYZE].started_at = datetime.now().isoformat()
        
        self.tasks[task.id] = task
        self.current_task_id = task.id
        
        return f"✅ 任务已创建: `{task.id}`\n📝 描述: {description}\n📊 阶段: {task.current_stage.value}"
    
    def progress(self, task_id: Optional[str] = None) -> str:
        """查看任务进度"""
        task = self._get_task(task_id)
        if not task:
            return "❌ 任务不存在"
        
        lines = [
            f"📋 任务: **{task.description}**",
            f"ID: `{task.id}` | 状态: {task.status.value}",
            ""
        ]
        
        # 显示各阶段
        lines.append("**进度:**")
        for stage in TaskStage:
            info = task.stages[stage]
            emoji = {
                "pending": "⏳",
                "in_progress": "🔄",
                "completed": "✅",
                "failed": "❌"
            }.get(info.status, "❓")
            
            stage_name = {
                TaskStage.ANALYZE: "📝 分析",
                TaskStage.PLAN: "📋 规划",
                TaskStage.EXECUTE: "⚙️ 执行",
                TaskStage.VERIFY: "🔍 验证",
                TaskStage.SUMMARIZE: "📦 总结"
            }[stage]
            
            current_marker = "👉 " if stage == task.current_stage else "   "
            lines.append(f"{current_marker}{emoji} {stage_name}: {info.status}")
            
            if info.message:
                lines.append(f"      {info.message}")
        
        return "\n".join(lines)
    
    def next_stage(self, message: str = "", task_id: Optional[str] = None) -> str:
        """进入下一阶段"""
        task = self._get_task(task_id)
        if not task:
            return "❌ 任务不存在"
        
        # 标记当前阶段完成
        current_info = task.stages[task.current_stage]
        current_info.status = "completed"
        current_info.completed_at = datetime.now().isoformat()
        if message:
            current_info.message = message
        
        # 找到下一个阶段
        stage_order = list(TaskStage)
        current_idx = stage_order.index(task.current_stage)
        
        if current_idx + 1 >= len(stage_order):
            # 任务完成
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().isoformat()
            return f"🎉 任务完成！\n\n结果: {task.result or '无'}"
        
        # 进入下一阶段
        next_stage = stage_order[current_idx + 1]
        task.current_stage = next_stage
        task.stages[next_stage].status = "in_progress"
        task.stages[next_stage].started_at = datetime.now().isoformat()
        
        stage_name = {
            TaskStage.ANALYZE: "分析",
            TaskStage.PLAN: "规划",
            TaskStage.EXECUTE: "执行",
            TaskStage.VERIFY: "验证",
            TaskStage.SUMMARIZE: "总结"
        }[next_stage]
        
        return f"➡️ 进入阶段: **{stage_name}**\n\n{message or '请继续...'}"
    
    def complete(self, result: str, task_id: Optional[str] = None) -> str:
        """标记任务完成"""
        task = self._get_task(task_id)
        if not task:
            return "❌ 任务不存在"
        
        task.status = TaskStatus.COMPLETED
        task.result = result
        task.completed_at = datetime.now().isoformat()
        
        # 标记所有阶段完成
        for stage_info in task.stages.values():
            if stage_info.status == "in_progress":
                stage_info.status = "completed"
                stage_info.completed_at = datetime.now().isoformat()
        
        return f"🎉 任务 `{task.id}` 已完成！\n\n结果:\n{result}"
    
    def fail(self, error: str, task_id: Optional[str] = None) -> str:
        """标记任务失败"""
        task = self._get_task(task_id)
        if not task:
            return "❌ 任务不存在"
        
        task.status = TaskStatus.FAILED
        task.error = error
        task.completed_at = datetime.now().isoformat()
        
        return f"❌ 任务 `{task.id}` 失败！\n\n错误: {error}"
    
    def list_tasks(self, status_filter: Optional[str] = None) -> str:
        """列出所有任务"""
        if not self.tasks:
            return "📭 暂无任务"
        
        lines = ["**任务列表:**\n"]
        
        for task in self.tasks.values():
            if status_filter and task.status.value != status_filter:
                continue
            
            emoji = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.IN_PROGRESS: "🔄",
                TaskStatus.COMPLETED: "✅",
                TaskStatus.FAILED: "❌",
                TaskStatus.CANCELLED: "🛑"
            }.get(task.status, "❓")
            
            lines.append(f"{emoji} `{task.id}` - {task.description}")
            lines.append(f"   状态: {task.status.value} | 阶段: {task.current_stage.value}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _get_task(self, task_id: Optional[str]) -> Optional[Task]:
        """获取任务"""
        if task_id:
            return self.tasks.get(task_id)
        elif self.current_task_id:
            return self.tasks.get(self.current_task_id)
        return None


# 全局工作流实例
_workflow: Optional[TaskWorkflow] = None


def get_workflow() -> TaskWorkflow:
    """获取全局工作流实例"""
    global _workflow
    if _workflow is None:
        _workflow = TaskWorkflow()
    return _workflow


# CLI 接口
if __name__ == "__main__":
    wf = get_workflow()
    
    import sys
    
    if len(sys.argv) < 2:
        print("用法: workflow.py <命令> [参数]")
        print("命令: create <描述> | progress [id] | next [id] | complete <结果> | list")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "create" and len(sys.argv) > 2:
        print(wf.create(" ".join(sys.argv[2:])))
    elif cmd == "progress":
        task_id = sys.argv[2] if len(sys.argv) > 2 else None
        print(wf.progress(task_id))
    elif cmd == "next":
        task_id = sys.argv[2] if len(sys.argv) > 2 else None
        print(wf.next_stage(task_id=task_id))
    elif cmd == "complete" and len(sys.argv) > 2:
        task_id = sys.argv[2] if len(sys.argv) > 2 else None
        result = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else "完成"
        print(wf.complete(result, task_id))
    elif cmd == "list":
        print(wf.list_tasks())
    else:
        print(f"未知命令: {cmd}")