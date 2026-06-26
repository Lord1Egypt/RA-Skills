"""异步任务队列 - 解决长时间运行的 skill 超时问题"""

import json
import logging
import threading
import time
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Optional


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"      # 等待执行
    RUNNING = "running"      # 执行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 失败


class TaskQueue:
    """简单的任务队列，用于异步执行长时间运行的任务"""
    
    def __init__(self, task_dir: str = "./tasks"):
        """
        Args:
            task_dir: 任务状态存储目录
        """
        self.task_dir = Path(task_dir)
        self.task_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
    
    def _get_task_path(self, task_id: str) -> Path:
        """获取任务文件路径"""
        return self.task_dir / f"{task_id}.json"
    
    def submit(self, func: Callable, *args, **kwargs) -> str:
        """
        提交一个任务到队列
        
        Args:
            func: 要执行的函数
            args: 位置参数
            kwargs: 关键字参数
            
        Returns:
            task_id: 任务 ID
        """
        task_id = str(uuid.uuid4())
        
        # 保存任务初始状态
        task_info = {
            "task_id": task_id,
            "status": TaskStatus.PENDING,
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None,
            "result": None,
            "error": None,
        }
        
        self._save_task(task_id, task_info)
        
        # 在后台线程中执行任务
        thread = threading.Thread(
            target=self._execute_task,
            args=(task_id, func, args, kwargs),
            daemon=True
        )
        thread.start()
        
        logging.info(f"任务已提交: {task_id}")
        return task_id
    
    def _execute_task(self, task_id: str, func: Callable, args: tuple, kwargs: dict) -> None:
        """在后台执行任务"""
        task_info = self._load_task(task_id)
        
        try:
            # 更新状态为运行中
            task_info["status"] = TaskStatus.RUNNING
            task_info["started_at"] = datetime.now().isoformat()
            self._save_task(task_id, task_info)
            
            logging.info(f"开始执行任务: {task_id}")
            
            # 执行实际任务
            result = func(*args, **kwargs)
            
            # 更新状态为完成
            task_info["status"] = TaskStatus.COMPLETED
            task_info["completed_at"] = datetime.now().isoformat()
            task_info["result"] = result
            self._save_task(task_id, task_info)
            
            logging.info(f"任务执行完成: {task_id}")
        
        except Exception as e:
            # 更新状态为失败
            task_info["status"] = TaskStatus.FAILED
            task_info["completed_at"] = datetime.now().isoformat()
            task_info["error"] = str(e)
            self._save_task(task_id, task_info)
            
            logging.error(f"任务执行失败: {task_id}, 错误: {e}")
    
    def get_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        获取任务状态
        
        Args:
            task_id: 任务 ID
            
        Returns:
            任务信息字典，如果任务不存在返回 None
        """
        return self._load_task(task_id)
    
    def get_result(self, task_id: str, wait: bool = False, timeout: float = 300) -> Optional[Any]:
        """
        获取任务结果
        
        Args:
            task_id: 任务 ID
            wait: 是否等待任务完成
            timeout: 等待超时时间（秒）
            
        Returns:
            任务结果，如果任务未完成或失败返回 None
        """
        if wait:
            start_time = time.time()
            while time.time() - start_time < timeout:
                task_info = self._load_task(task_id)
                if not task_info:
                    return None
                
                if task_info["status"] == TaskStatus.COMPLETED:
                    return task_info["result"]
                elif task_info["status"] == TaskStatus.FAILED:
                    logging.error(f"任务失败: {task_id}, 错误: {task_info.get('error')}")
                    return None
                
                time.sleep(1)  # 每秒检查一次
            
            logging.warning(f"等待任务超时: {task_id}")
            return None
        else:
            task_info = self._load_task(task_id)
            if task_info and task_info["status"] == TaskStatus.COMPLETED:
                return task_info["result"]
            return None
    
    def _save_task(self, task_id: str, task_info: dict) -> None:
        """保存任务信息到文件"""
        with self._lock:
            task_path = self._get_task_path(task_id)
            with open(task_path, 'w', encoding='utf-8') as f:
                json.dump(task_info, f, ensure_ascii=False, indent=2)
    
    def _load_task(self, task_id: str) -> Optional[dict]:
        """从文件加载任务信息"""
        task_path = self._get_task_path(task_id)
        if not task_path.exists():
            return None
        
        try:
            with open(task_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"加载任务失败: {task_id}, 错误: {e}")
            return None
    
    def cleanup_old_tasks(self, days: int = 7) -> int:
        """
        清理旧任务文件
        
        Args:
            days: 保留最近 N 天的任务
            
        Returns:
            清理的任务数量
        """
        count = 0
        cutoff_time = datetime.now().timestamp() - (days * 86400)
        
        for task_file in self.task_dir.glob("*.json"):
            try:
                if task_file.stat().st_mtime < cutoff_time:
                    task_file.unlink()
                    count += 1
            except Exception as e:
                logging.warning(f"清理任务文件失败 {task_file}: {e}")
        
        if count > 0:
            logging.info(f"已清理 {count} 个旧任务文件")
        
        return count


# 全局任务队列实例
_task_queue = None


def get_task_queue() -> TaskQueue:
    """获取全局任务队列实例"""
    global _task_queue
    if _task_queue is None:
        _task_queue = TaskQueue()
    return _task_queue
