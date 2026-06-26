"""异步 Skill 包装器 - 解决 OpenClaw 调用超时问题"""

import logging
from typing import Any, Dict

from .skills import DocAssistant
from .task_queue import TaskStatus, get_task_queue


class AsyncDocAssistant:
    """DocAssistant 的异步包装器
    
    为耗时的 skill 提供异步执行能力：
    1. 调用 *_async 方法立即返回 task_id
    2. 使用 get_task_status 查询任务状态
    3. 使用 get_task_result 获取任务结果
    """
    
    def __init__(self, config_path: str = "config.yaml", **kwargs):
        self._assistant = DocAssistant(config_path=config_path)
        self._task_queue = get_task_queue()
    
    # ========== 同步方法（保持兼容性）==========
    
    def fetch_doc(self, **kwargs) -> Dict[str, Any]:
        """同步抓取文档"""
        return self._assistant.fetch_doc(**kwargs)
    
    def check_changes(self, **kwargs) -> Dict[str, Any]:
        """同步检查变更"""
        return self._assistant.check_changes(**kwargs)
    
    def compare_docs(self, **kwargs) -> Dict[str, Any]:
        """同步对比文档"""
        return self._assistant.compare_docs(**kwargs)
    
    def summarize_diff(self, **kwargs) -> Dict[str, Any]:
        """同步生成差异摘要"""
        return self._assistant.summarize_diff(**kwargs)
    
    def run_monitor(self, **kwargs) -> Dict[str, Any]:
        """同步运行监控"""
        return self._assistant.run_monitor(**kwargs)
    
    # ========== 异步方法（立即返回 task_id）==========
    
    def fetch_doc_async(self, **kwargs) -> Dict[str, Any]:
        """异步抓取文档，立即返回 task_id
        
        Returns:
            {"task_id": "xxx", "status": "pending", "message": "任务已提交"}
        """
        task_id = self._task_queue.submit(self._assistant.fetch_doc, **kwargs)
        return {
            "task_id": task_id,
            "status": TaskStatus.PENDING,
            "message": "任务已提交，请使用 get_task_status 查询进度",
        }
    
    def check_changes_async(self, **kwargs) -> Dict[str, Any]:
        """异步检查变更，立即返回 task_id"""
        task_id = self._task_queue.submit(self._assistant.check_changes, **kwargs)
        return {
            "task_id": task_id,
            "status": TaskStatus.PENDING,
            "message": "任务已提交，请使用 get_task_status 查询进度",
        }
    
    def compare_docs_async(self, **kwargs) -> Dict[str, Any]:
        """异步对比文档，立即返回 task_id"""
        task_id = self._task_queue.submit(self._assistant.compare_docs, **kwargs)
        return {
            "task_id": task_id,
            "status": TaskStatus.PENDING,
            "message": "任务已提交，请使用 get_task_status 查询进度",
        }
    
    def run_monitor_async(self, **kwargs) -> Dict[str, Any]:
        """异步运行监控，立即返回 task_id"""
        task_id = self._task_queue.submit(self._assistant.run_monitor, **kwargs)
        return {
            "task_id": task_id,
            "status": TaskStatus.PENDING,
            "message": "任务已提交，请使用 get_task_status 查询进度",
        }
    
    # ========== 任务管理方法 ==========
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """查询任务状态
        
        Args:
            task_id: 任务 ID
            
        Returns:
            {
                "task_id": "xxx",
                "status": "pending|running|completed|failed",
                "created_at": "2024-01-01T00:00:00",
                "started_at": "2024-01-01T00:00:01",
                "completed_at": "2024-01-01T00:00:10",
                "result": {...},  # 仅在 completed 时有值
                "error": "...",   # 仅在 failed 时有值
            }
        """
        task_info = self._task_queue.get_status(task_id)
        
        if not task_info:
            return {
                "task_id": task_id,
                "status": "not_found",
                "error": "任务不存在或已过期",
            }
        
        return task_info
    
    def get_task_result(self, task_id: str, wait: bool = False, timeout: float = 300) -> Dict[str, Any]:
        """获取任务结果
        
        Args:
            task_id: 任务 ID
            wait: 是否等待任务完成（默认 False）
            timeout: 等待超时时间（秒，默认 300）
            
        Returns:
            任务结果，如果任务未完成返回状态信息
        """
        result = self._task_queue.get_result(task_id, wait=wait, timeout=timeout)
        
        if result is not None:
            return result
        
        # 任务未完成，返回当前状态
        return self.get_task_status(task_id)
    
    def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """取消任务（注意：已经在运行的任务无法取消）
        
        Args:
            task_id: 任务 ID
            
        Returns:
            操作结果
        """
        task_info = self._task_queue.get_status(task_id)
        
        if not task_info:
            return {
                "success": False,
                "message": "任务不存在",
            }
        
        if task_info["status"] == TaskStatus.RUNNING:
            return {
                "success": False,
                "message": "任务正在运行中，无法取消",
            }
        
        if task_info["status"] in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            return {
                "success": False,
                "message": f"任务已{task_info['status']}，无需取消",
            }
        
        # TODO: 实现真正的取消逻辑
        return {
            "success": False,
            "message": "取消功能暂未实现",
        }


__all__ = ["AsyncDocAssistant"]
