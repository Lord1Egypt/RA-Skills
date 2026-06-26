#!/usr/bin/env python3
"""
Abby Autonomy - 主动心跳

每3分钟检查并主动工作
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# 添加 long-term-memory 路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'workspace' / 'skills' / 'long-term-memory'))

from scripts.queue import TaskQueue, take_task, complete_task
from scripts.status import (
    TaskState, 
    has_running_task, 
    get_current_task,
    start_task,
    update_progress,
    complete_task as clear_task_state
)


class AutonomyHeartbeat:
    """主动心跳控制器"""
    
    def __init__(self):
        self.queue = TaskQueue()
        self.state = TaskState()
    
    def check_urgent(self) -> bool:
        """
        检查紧急事项
        
        Returns:
            bool: True = 有紧急事项需要处理
        """
        # TODO: 实现紧急事项检查
        # - 人类消息
        # - 系统错误
        # - Gateway 通知
        
        return False  # 暂时没有紧急事项
    
    def check_and_work(self) -> Optional[str]:
        """
        检查并开始工作
        
        Returns:
            str: 执行的任务 或 None
        """
        # 1. 检查紧急事项
        if self.check_urgent():
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 发现紧急事项，暂停自主工作")
            return None
        
        # 2. 检查是否有正在执行的任务
        if has_running_task():
            current = get_current_task()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 继续执行: {current}")
            return current
        
        # 3. 从队列取任务
        queue = self.queue.read_queue()
        task = self.queue.take_task(queue)
        
        if task:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始新任务: {task}")
            
            # 4. 标记状态
            self.state.start_task(task, estimated_minutes=30)
            
            return task
        
        return None
    
    def complete_current_task(self, success: bool = True):
        """完成任务"""
        task = get_current_task()
        if task:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 完成任务: {task}")
            
            # 清除状态
            clear_task_state()
            
            # 更新队列
            if success:
                complete_task(task)


def run_heartbeat():
    """
    运行一次心跳
    
    Returns:
        str: 执行的任务 或 None
    """
    heartbeat = AutonomyHeartbeat()
    return heartbeat.check_and_work()


def start_working(task: str, progress_callback=None):
    """
    开始工作
    
    Args:
        task: 任务内容
        progress_callback: 进度回调函数
    """
    start_task(task, estimated_minutes=30)
    
    try:
        # TODO: 执行实际任务
        # 这里应该根据任务类型调用不同的执行器
        print(f"🔄 执行任务: {task}")
        
        # 模拟执行
        import time
        for i in range(5):
            time.sleep(1)  # 模拟工作
            if progress_callback:
                progress_callback(f"{i*20}%")
            else:
                update_progress(f"{i*20}%")
        
        # 完成任务
        complete_current_task(success=True)
        
    except Exception as e:
        print(f"❌ 任务失败: {e}")
        complete_current_task(success=False)


if __name__ == '__main__':
    # 测试心跳
    print("="*50)
    print("Abby Autonomy Heartbeat 测试")
    print("="*50)
    
    result = run_heartbeat()
    
    if result:
        print(f"\n开始执行任务: {result}")
        start_working(result)
    else:
        print("\n没有任务需要执行")
    
    print("\n" + "="*50)
    print("心跳测试完成")
    print("="*50)
