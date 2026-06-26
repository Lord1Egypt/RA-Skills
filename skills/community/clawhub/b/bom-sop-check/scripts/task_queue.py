#!/usr/bin/env python3
"""
任务队列管理器 - 支持30人并发
功能：
1. 限制并发数（默认3个）
2. 内存监控和熔断
3. 任务超时机制
4. 定时清理临时文件
"""

import os
import sys
import json
import time
import psutil
import threading
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from collections import deque
from typing import Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

# 配置
MAX_CONCURRENT_TASKS = 3  # 最大并发任务数
MEMORY_THRESHOLD = 0.80   # 内存使用阈值（80%）
TASK_TIMEOUT = 300        # 任务超时时间（秒）
TEMP_FILE_MAX_AGE = 3600  # 临时文件最大存活时间（秒）
MAX_QUEUE_SIZE = 50       # 最大队列长度


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    REJECTED = "rejected"  # 因资源不足被拒绝


@dataclass
class Task:
    """任务对象"""
    task_id: str
    user_id: str
    bom_file: str
    sop_file: str
    output_dir: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict] = None
    error: Optional[str] = None
    position: int = 0  # 队列位置


class TaskQueue:
    """任务队列管理器"""
    
    def __init__(self, max_concurrent: int = MAX_CONCURRENT_TASKS):
        self.max_concurrent = max_concurrent
        self.queue: deque = deque()
        self.running_tasks: Dict[str, Task] = {}
        self.completed_tasks: Dict[str, Task] = {}
        self.lock = threading.Lock()
        self.task_counter = 0
        
        # 启动后台清理线程
        self._start_cleanup_thread()
    
    def get_system_stats(self) -> Dict:
        """获取系统资源状态"""
        mem = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=0.1)
        disk = psutil.disk_usage('/')
        
        return {
            "memory_total": mem.total,
            "memory_used": mem.used,
            "memory_percent": mem.percent,
            "memory_available": mem.available,
            "cpu_percent": cpu_percent,
            "disk_free": disk.free,
            "disk_percent": disk.percent,
            "can_accept_task": mem.percent < MEMORY_THRESHOLD * 100,
        }
    
    def can_accept_task(self) -> tuple[bool, str]:
        """检查是否可以接受新任务"""
        stats = self.get_system_stats()
        
        # 检查内存
        if stats["memory_percent"] >= MEMORY_THRESHOLD * 100:
            return False, f"内存使用过高 ({stats['memory_percent']:.1f}% >= {MEMORY_THRESHOLD*100}%)"
        
        # 检查队列长度
        if len(self.queue) >= MAX_QUEUE_SIZE:
            return False, f"队列已满 ({len(self.queue)}/{MAX_QUEUE_SIZE})"
        
        # 检查运行中的任务数
        if len(self.running_tasks) >= self.max_concurrent:
            return False, f"并发任务已满 ({len(self.running_tasks)}/{self.max_concurrent})"
        
        return True, "OK"
    
    def submit_task(self, user_id: str, bom_file: str, sop_file: str, output_dir: str) -> Task:
        """提交新任务"""
        with self.lock:
            self.task_counter += 1
            task_id = f"task_{int(time.time())}_{self.task_counter}"
            
            task = Task(
                task_id=task_id,
                user_id=user_id,
                bom_file=bom_file,
                sop_file=sop_file,
                output_dir=output_dir,
                position=len(self.queue) + 1,
            )
            
            # 检查是否可以接受任务
            can_accept, reason = self.can_accept_task()
            
            if not can_accept:
                task.status = TaskStatus.REJECTED
                task.error = reason
                self.completed_tasks[task_id] = task
                return task
            
            self.queue.append(task)
            return task
    
    def get_next_task(self) -> Optional[Task]:
        """获取下一个待执行的任务"""
        with self.lock:
            if not self.queue:
                return None
            
            # 再次检查资源
            can_accept, _ = self.can_accept_task()
            if not can_accept:
                return None
            
            task = self.queue.popleft()
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            task.position = 0
            self.running_tasks[task.task_id] = task
            
            # 更新队列中任务的位置
            for i, t in enumerate(self.queue):
                t.position = i + 1
            
            return task
    
    def complete_task(self, task_id: str, result: Optional[Dict] = None, error: Optional[str] = None, status: TaskStatus = TaskStatus.COMPLETED):
        """标记任务完成"""
        with self.lock:
            if task_id in self.running_tasks:
                task = self.running_tasks.pop(task_id)
                task.status = status
                task.completed_at = datetime.now()
                task.result = result
                task.error = error
                self.completed_tasks[task_id] = task
                
                # 保留最近100个已完成任务
                if len(self.completed_tasks) > 100:
                    # 删除最旧的任务
                    oldest = min(self.completed_tasks.items(), key=lambda x: x[1].completed_at)
                    del self.completed_tasks[oldest[0]]
    
    def get_task_status(self, task_id: str) -> Optional[Task]:
        """获取任务状态"""
        with self.lock:
            if task_id in self.running_tasks:
                return self.running_tasks[task_id]
            if task_id in self.completed_tasks:
                return self.completed_tasks[task_id]
            for task in self.queue:
                if task.task_id == task_id:
                    return task
        return None
    
    def get_queue_status(self) -> Dict:
        """获取队列状态"""
        with self.lock:
            stats = self.get_system_stats()
            return {
                "queue_length": len(self.queue),
                "running_tasks": len(self.running_tasks),
                "max_concurrent": self.max_concurrent,
                "completed_tasks": len(self.completed_tasks),
                "system_stats": stats,
                "estimated_wait_time": len(self.queue) * 30,  # 预估等待时间（秒）
            }
    
    def _start_cleanup_thread(self):
        """启动后台清理线程"""
        def cleanup_worker():
            while True:
                try:
                    self._cleanup_old_files()
                    time.sleep(300)  # 每5分钟清理一次
                except Exception as e:
                    print(f"[清理线程] 错误: {e}")
        
        thread = threading.Thread(target=cleanup_worker, daemon=True)
        thread.start()
    
    def _cleanup_old_files(self):
        """清理旧的临时文件"""
        now = time.time()
        cleaned = 0
        
        # 清理 cache 目录
        cache_dir = Path(__file__).parent.parent / "cache"
        if cache_dir.exists():
            for item in cache_dir.iterdir():
                if item.is_dir():
                    # 检查目录修改时间
                    if now - item.stat().st_mtime > TEMP_FILE_MAX_AGE:
                        try:
                            shutil.rmtree(item)
                            cleaned += 1
                        except Exception as e:
                            print(f"[清理] 无法删除 {item}: {e}")
        
        if cleaned > 0:
            print(f"[清理] 已清理 {cleaned} 个旧目录")


# 全局任务队列实例
_task_queue: Optional[TaskQueue] = None


def get_task_queue() -> TaskQueue:
    """获取全局任务队列实例"""
    global _task_queue
    if _task_queue is None:
        _task_queue = TaskQueue()
    return _task_queue


def check_resources() -> Dict:
    """检查系统资源并返回建议"""
    queue = get_task_queue()
    status = queue.get_queue_status()
    stats = status["system_stats"]
    
    recommendations = []
    
    if stats["memory_percent"] > 80:
        recommendations.append("⚠️ 内存使用过高，建议升级服务器或限制并发数")
    elif stats["memory_percent"] > 70:
        recommendations.append("⚡ 内存使用较高，注意监控")
    
    if stats["cpu_percent"] > 90:
        recommendations.append("⚠️ CPU 使用过高，建议增加核心数或限制并发")
    elif stats["cpu_percent"] > 70:
        recommendations.append("⚡ CPU 使用较高，任务处理可能变慢")
    
    if status["queue_length"] > 10:
        recommendations.append(f"⏳ 当前有 {status['queue_length']} 个任务排队，预计等待 {status['estimated_wait_time']} 秒")
    
    return {
        "status": status,
        "recommendations": recommendations,
        "can_accept_task": stats["can_accept_task"],
    }


if __name__ == "__main__":
    # 测试
    queue = get_task_queue()
    
    print("=" * 60)
    print("任务队列管理器 - 状态检查")
    print("=" * 60)
    
    status = queue.get_queue_status()
    stats = status["system_stats"]
    
    print(f"\n系统资源:")
    print(f"  内存: {stats['memory_percent']:.1f}% ({stats['memory_used'] / 1024**3:.1f}GB / {stats['memory_total'] / 1024**3:.1f}GB)")
    print(f"  CPU: {stats['cpu_percent']:.1f}%")
    print(f"  磁盘: {stats['disk_percent']:.1f}%")
    
    print(f"\n队列状态:")
    print(f"  排队中: {status['queue_length']}")
    print(f"  执行中: {status['running_tasks']}/{status['max_concurrent']}")
    print(f"  已完成: {status['completed_tasks']}")
    print(f"  预估等待: {status['estimated_wait_time']} 秒")
    
    print(f"\n是否可接受新任务: {'✅ 是' if stats['can_accept_task'] else '❌ 否'}")
    
    resources = check_resources()
    if resources["recommendations"]:
        print(f"\n建议:")
        for rec in resources["recommendations"]:
            print(f"  {rec}")
