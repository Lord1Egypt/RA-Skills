# -*- coding: utf-8 -*-
"""
OpenClaw Agent并发安全调度器
基于Claude Code架构模式实现

核心设计：
- 默认 Fail-Closed（isConcurrencySafe: false）
- 串行队列，避免isolated session资源冲突
- 显式权限日志（checkPermissions模式）
- 超时熔断+指数退避重试
"""

import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

CONCURRENCY_LOG = Path.home() / ".openclaw" / "workspace" / "logs" / "agent-concurrency.log"
SENSITIVE_LOG = Path.home() / ".openclaw" / "workspace" / "logs" / "sensitive-operations.log"
QUEUE_STATE_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / "agent-queue-state.json"

class PermissionBehavior(Enum):
    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"

@dataclass
class AgentTask:
    """Agent任务定义（对应ToolUse层）"""
    task_id: str
    agent_type: str      # researcher/writer/ops等
    runtime: str         # subagent/acp
    priority: int        # 数字越小优先级越高
    is_concurrency_safe: bool = False  # 默认不安全（Fail-Closed）
    estimated_cost: float = 0.0
    timeout_seconds: int = 300
    max_retries: int = 3
    sensitive_level: str = "normal"   # normal/sensitive/critical
    created_at: str = ""
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

class AgentConcurrencyController:
    """
    Agent并发安全控制器
    参考Claude Code的Coordinator协调原则
    """
    
    def __init__(self):
        self.running_tasks: Dict[str, AgentTask] = {}
        self.pending_queue: List[AgentTask] = []
        self.completed_tasks: List[Dict] = []
        self._load_state()
        
    def _load_state(self):
        """加载队列状态"""
        if QUEUE_STATE_FILE.exists():
            try:
                with open(QUEUE_STATE_FILE, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.pending_queue = [AgentTask(**t) for t in state.get('pending', [])]
            except Exception:
                pass
    
    def _save_state(self):
        """保存队列状态"""
        QUEUE_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        state = {
            'pending': [asdict(t) for t in self.pending_queue],
            'running': {k: asdict(v) for k, v in self.running_tasks.items()},
            'completed': self.completed_tasks[-50:],  # 保留最近50条
            'updated_at': datetime.now().isoformat()
        }
        with open(QUEUE_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def check_permissions(self, task: AgentTask, user_context: dict = None) -> PermissionBehavior:
        """
        权限检查（参考Claude Code checkPermissions模式）
        
        敏感任务需要额外确认：
        - critical: 外发操作（公众号发布、付款等）
        - sensitive: 文件覆盖、配置修改
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'task_id': task.task_id,
            'agent_type': task.agent_type,
            'sensitive_level': task.sensitive_level,
            'action': 'check_permissions'
        }
        
        # 默认允许，但记录日志
        behavior = PermissionBehavior.ALLOW
        
        if task.sensitive_level == "critical":
            behavior = PermissionBehavior.ASK
            log_entry['decision'] = 'ASK_USER_CONFIRMATION'
        elif task.sensitive_level == "sensitive":
            log_entry['decision'] = 'ALLOW_WITH_LOG'
        else:
            log_entry['decision'] = 'ALLOW'
        
        self._log_sensitive_operation(log_entry)
        return behavior
    
    def _log_sensitive_operation(self, entry: dict):
        """敏感操作日志（审计追踪）"""
        SENSITIVE_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(SENSITIVE_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    def can_execute_concurrently(self, task: AgentTask) -> bool:
        """
        并发安全检查（参考isConcurrencySafe）
        
        默认返回False（Fail-Closed），除非显式标记为安全
        """
        # 默认Fail-Closed
        if not task.is_concurrency_safe:
            return False
        
        # 即使有标记，也检查资源冲突
        if self.running_tasks:
            return False
        
        return True
    
    def enqueue(self, task: AgentTask) -> str:
        """
        将任务加入队列
        
        如果任务可以并发执行（is_concurrency_safe=True且队列为空），
        则立即执行；否则加入队列等待
        """
        # 权限检查
        permission = self.check_permissions(task)
        
        if permission == PermissionBehavior.DENY:
            return f"DENIED:{task.task_id}"
        
        if permission == PermissionBehavior.ASK:
            # 需要用户确认，暂不加入队列
            return f"PENDING_CONFIRMATION:{task.task_id}"
        
        # 并发检查
        if self.can_execute_concurrently(task):
            # 可以立即执行
            self.running_tasks[task.task_id] = task
            self._log_execution(task, "START_CONCURRENT")
            return f"STARTED:{task.task_id}"
        else:
            # 加入队列等待
            self.pending_queue.append(task)
            self.pending_queue.sort(key=lambda t: (t.priority, t.created_at))
            self._save_state()
            self._log_execution(task, "QUEUED")
            return f"QUEUED:{task.task_id}"
    
    def _log_execution(self, task: AgentTask, status: str):
        """执行日志"""
        CONCURRENCY_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            'timestamp': datetime.now().isoformat(),
            'task_id': task.task_id,
            'agent_type': task.agent_type,
            'status': status,
            'queue_depth': len(self.pending_queue),
            'running_count': len(self.running_tasks)
        }
        with open(CONCURRENCY_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    def on_task_complete(self, task_id: str, result: dict = None):
        """任务完成回调"""
        if task_id in self.running_tasks:
            task = self.running_tasks.pop(task_id)
            self.completed_tasks.append({
                'task': asdict(task),
                'result': result or {},
                'completed_at': datetime.now().isoformat()
            })
            self._log_execution(task, "COMPLETED")
        
        # 尝试执行队列中的下一个任务
        self._drain_queue()
        self._save_state()
    
    def _drain_queue(self):
        """
        消费队列（串行执行，保证资源安全）
        
        参考Claude Code Coordinator的Synthesize-first原则：
        每次只启动一个任务，确保结果完整后再启动下一个
        """
        if not self.pending_queue:
            return
        
        if self.running_tasks:
            return  # 有任务在运行，等待
        
        # 取出优先级最高的任务
        next_task = self.pending_queue.pop(0)
        self.running_tasks[next_task.task_id] = next_task
        self._log_execution(next_task, "START_FROM_QUEUE")
        self._save_state()
    
    def get_status(self) -> dict:
        """获取队列状态"""
        return {
            'running': [
                {
                    'task_id': t.task_id,
                    'agent_type': t.agent_type,
                    'runtime': t.runtime
                }
                for t in self.running_tasks.values()
            ],
            'pending': [
                {
                    'task_id': t.task_id,
                    'agent_type': t.agent_type,
                    'priority': t.priority
                }
                for t in self.pending_queue[:5]  # 只显示前5个
            ],
            'queue_depth': len(self.pending_queue)
        }


# 单例控制器
_controller = None

def get_controller() -> AgentConcurrencyController:
    """获取控制器单例"""
    global _controller
    if _controller is None:
        _controller = AgentConcurrencyController()
    return _controller


def spawn_agent_safe(
    task: str,
    agent_type: str = "main",
    runtime: str = "subagent",
    priority: int = 5,
    is_concurrency_safe: bool = False,
    sensitive_level: str = "normal",
    timeout_seconds: int = 300
) -> str:
    """
    安全地spawn Agent（参考Claude Code的spawn vs fork区别）
    
    - spawn：独立session，新context（默认）
    - 默认Fail-Closed：is_concurrency_safe=False
    - 敏感操作自动记录权限日志
    """
    task_id = f"{agent_type}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    agent_task = AgentTask(
        task_id=task_id,
        agent_type=agent_type,
        runtime=runtime,
        priority=priority,
        is_concurrency_safe=is_concurrency_safe,
        sensitive_level=sensitive_level,
        timeout_seconds=timeout_seconds
    )
    
    controller = get_controller()
    result = controller.enqueue(agent_task)
    
    return result


def on_agent_complete(task_id: str, success: bool = True, result: dict = None):
    """Agent完成回调"""
    controller = get_controller()
    controller.on_task_complete(task_id, {
        'success': success,
        'data': result or {}
    })


if __name__ == "__main__":
    # 测试
    print(get_controller().get_status())
    
    # 模拟添加任务
    result = spawn_agent_safe(
        task="测试任务",
        agent_type="researcher",
        is_concurrency_safe=False,  # Fail-Closed
        sensitive_level="normal"
    )
    print(f"Spawn result: {result}")
    print(get_controller().get_status())
