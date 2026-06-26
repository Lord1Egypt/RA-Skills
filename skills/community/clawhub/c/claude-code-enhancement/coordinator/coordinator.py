#!/usr/bin/env python3
"""
Claude Code Enhancement Skill - 协调者模块
参考 Claude Code 的 Coordinator 模式实现
"""

import json
import os
import asyncio
import subprocess
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class WorkerStatus(Enum):
    """Worker 状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


@dataclass
class WorkerTask:
    """Worker 任务"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: str = ""
    prompt: str = ""
    status: WorkerStatus = WorkerStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None


@dataclass
class CoordinatorConfig:
    """协调者配置"""
    max_workers: int = 5
    worker_tools: List[str] = field(default_factory=lambda: [
        "BashTool", "FileReadTool", "FileEditTool", "GlobTool", "GrepTool"
    ])
    timeout: int = 300000  # 5分钟
    isolation: str = "none"  # none | worktree


class Coordinator:
    """协调者 - 负责管理多个 Worker Agent"""
    
    def __init__(self, config: Optional[CoordinatorConfig] = None):
        self.config = config or CoordinatorConfig()
        self.workers: Dict[str, WorkerTask] = {}
        self.active = False
        self.results: List[str] = []
    
    def start(self) -> str:
        """启动协调者模式"""
        self.active = True
        return "🤖 Coordinator 模式已启动\n\n可用命令:\n- /coord spawn <描述> <提示> : 派生新 Worker\n- /coord status : 查看所有 Worker 状态\n- /coord stop <id> : 停止指定 Worker\n- /coord stop : 退出协调者模式"
    
    def spawn(self, description: str, prompt: str) -> str:
        """派生新 Worker"""
        if len(self.workers) >= self.config.max_workers:
            return f"❌已达到最大 Worker 数量 ({self.config.max_workers})"
        
        task_id = str(uuid.uuid4())[:8]
        task = WorkerTask(
            id=task_id,
            description=description,
            prompt=prompt,
            status=WorkerStatus.RUNNING
        )
        self.workers[task_id] = task
        
        # 异步启动 Worker（这里简化处理，实际需要调用 OpenClaw API）
        asyncio.create_task(self._run_worker(task_id))
        
        return f"✅ Worker 已创建: `{task_id}`\n📝 描述: {description}\n⏳ 状态: running"
    
    async def _run_worker(self, task_id: str):
        """异步运行 Worker 任务"""
        task = self.workers.get(task_id)
        if not task:
            return
        
        try:
            # 这里调用 OpenClaw Agent 执行任务
            # 简化版：模拟执行
            await asyncio.sleep(2)  # 模拟
            
            task.status = WorkerStatus.COMPLETED
            task.result = f"✅ Worker {task_id} 任务完成"
            task.completed_at = datetime.now().isoformat()
        except Exception as e:
            task.status = WorkerStatus.FAILED
            task.error = str(e)
    
    def status(self) -> str:
        """查看所有 Worker 状态"""
        if not self.workers:
            return "📭 暂无 Worker"
        
        lines = ["**Worker 状态:**\n"]
        for tid, task in self.workers.items():
            emoji = {
                WorkerStatus.PENDING: "⏳",
                WorkerStatus.RUNNING: "🔄",
                WorkerStatus.COMPLETED: "✅",
                WorkerStatus.FAILED: "❌",
                WorkerStatus.STOPPED: "🛑"
            }.get(task.status, "❓")
            
            lines.append(f"{emoji} `{tid}` - {task.description}")
            lines.append(f"   状态: {task.status.value}")
            if task.result:
                lines.append(f"   结果: {task.result[:50]}...")
            lines.append("")
        
        return "\n".join(lines)
    
    def stop(self, worker_id: Optional[str] = None) -> str:
        """停止 Worker"""
        if worker_id:
            if worker_id in self.workers:
                self.workers[worker_id].status = WorkerStatus.STOPPED
                return f"🛑 Worker `{worker_id}` 已停止"
            return f"❌ Worker `{worker_id}` 不存在"
        
        self.active = False
        for task in self.workers.values():
            task.status = WorkerStatus.STOPPED
        return "🤖 Coordinator 模式已退出"
    
    def collect_results(self) -> str:
        """收集所有结果"""
        results = []
        for task in self.workers.values():
            if task.status == WorkerStatus.COMPLETED:
                results.append(f"## {task.description}\n{task.result}\n")
            elif task.status == WorkerStatus.FAILED:
                results.append(f"## {task.description}\n❌ 错误: {task.error}\n")
        
        return "\n---\n".join(results) if results else "📭 无结果"


# 全局协调者实例
_coordinator: Optional[Coordinator] = None


def get_coordinator() -> Coordinator:
    """获取全局协调者实例"""
    global _coordinator
    if _coordinator is None:
        _coordinator = Coordinator()
    return _coordinator


def reset_coordinator():
    """重置协调者"""
    global _coordinator
    _coordinator = None


# CLI 接口
if __name__ == "__main__":
    import sys
    
    coord = get_coordinator()
    
    if len(sys.argv) < 2:
        print("用法: coordinator.py <命令> [参数]")
        print("命令: start | spawn | status | stop")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "start":
        print(coord.start())
    elif cmd == "status":
        print(coord.status())
    elif cmd == "stop":
        worker_id = sys.argv[2] if len(sys.argv) > 2 else None
        print(coord.stop(worker_id))
    elif cmd == "spawn":
        if len(sys.argv) < 4:
            print("用法: coordinator.py spawn <描述> <提示>")
            sys.exit(1)
        description = sys.argv[2]
        prompt = " ".join(sys.argv[3:])
        print(coord.spawn(description, prompt))
    else:
        print(f"未知命令: {cmd}")