#!/usr/bin/env python3
"""
Lightweight Task Scheduler - 轻量级任务调度器
纯内存 + JSON 持久化，零依赖，极速
"""

import json
import time
import uuid
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Node:
    """节点信息"""
    node_id: str
    name: str
    ip: str
    status: str = "online"
    health_score: float = 100.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    active_tasks: int = 0
    total_tasks: int = 0
    success_rate: float = 1.0
    avg_response_time: float = 0.0
    last_heartbeat: float = 0.0
    created_at: float = 0.0

@dataclass
class Task:
    """任务信息"""
    task_id: str
    description: str
    complexity: str = "medium"
    status: str = "pending"
    assigned_node: Optional[str] = None
    created_at: float = 0.0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 3
    result: Optional[str] = None
    error: Optional[str] = None


class LightweightScheduler:
    def __init__(self, data_file: str = None):
        """初始化调度器"""
        if data_file is None:
            data_file = Path(__file__).parent.parent / "data" / "scheduler.json"
        
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 内存存储
        self.nodes: Dict[str, Node] = {}
        self.tasks: Dict[str, Task] = {}
        self.performance_history: List[Dict] = []
        
        # 自动保存
        self.last_save = time.time()
        self.save_interval = 60  # 每分钟保存一次
        
        # 启动时加载
        self.load()
    
    def save(self):
        """保存到 JSON"""
        data = {
            'nodes': {k: asdict(v) for k, v in self.nodes.items()},
            'tasks': {k: asdict(v) for k, v in self.tasks.items()},
            'performance_history': self.performance_history[-1000:]  # 只保留最近1000条
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.last_save = time.time()
    
    def load(self):
        """从 JSON 加载"""
        if not self.data_file.exists():
            return
        
        try:
            with open(self.data_file) as f:
                data = json.load(f)
            
            # 恢复节点
            for node_id, node_data in data.get('nodes', {}).items():
                self.nodes[node_id] = Node(**node_data)
            
            # 恢复任务
            for task_id, task_data in data.get('tasks', {}).items():
                self.tasks[task_id] = Task(**task_data)
            
            # 恢复性能历史
            self.performance_history = data.get('performance_history', [])
        
        except Exception as e:
            print(f"⚠️  Failed to load data: {e}")
    
    def auto_save(self):
        """自动保存（如果需要）"""
        if time.time() - self.last_save > self.save_interval:
            self.save()
    
    def register_node(self, node: Node):
        """注册节点"""
        node.created_at = time.time()
        node.last_heartbeat = time.time()
        self.nodes[node.node_id] = node
        self.auto_save()
    
    def update_node_heartbeat(self, node_id: str, metrics: Dict):
        """更新节点心跳"""
        if node_id not in self.nodes:
            return
        
        node = self.nodes[node_id]
        node.status = metrics.get('status', 'online')
        node.cpu_usage = metrics.get('cpu_usage', 0.0)
        node.memory_usage = metrics.get('memory_usage', 0.0)
        node.last_heartbeat = time.time()
        
        # 记录性能历史
        self.performance_history.append({
            'node_id': node_id,
            'timestamp': time.time(),
            'cpu_usage': node.cpu_usage,
            'memory_usage': node.memory_usage,
            'response_time': metrics.get('response_time', 0.0),
            'success': 1
        })
        
        self.auto_save()
    
    def calculate_health_score(self, node_id: str) -> float:
        """计算节点健康评分"""
        if node_id not in self.nodes:
            return 0.0
        
        node = self.nodes[node_id]
        score = 100.0
        
        # 状态
        if node.status == 'offline':
            score -= 40
        elif node.status == 'degraded':
            score -= 20
        
        # 心跳
        time_since_hb = time.time() - node.last_heartbeat
        if time_since_hb > 300:
            score -= 20
        elif time_since_hb > 60:
            score -= 10
        
        # CPU
        if node.cpu_usage > 90:
            score -= 15
        elif node.cpu_usage > 70:
            score -= 10
        elif node.cpu_usage > 50:
            score -= 5
        
        # 内存
        if node.memory_usage > 90:
            score -= 15
        elif node.memory_usage > 70:
            score -= 10
        elif node.memory_usage > 50:
            score -= 5
        
        # 成功率
        score -= (1.0 - node.success_rate) * 10
        
        node.health_score = max(0.0, min(100.0, score))
        return node.health_score
    
    def select_node(self, complexity: str) -> Optional[str]:
        """选择最佳节点"""
        online_nodes = [
            (node_id, node) for node_id, node in self.nodes.items()
            if node.status == 'online'
        ]
        
        if not online_nodes:
            return None
        
        best_node = None
        best_score = -1
        
        for node_id, node in online_nodes:
            # 更新健康评分
            health = self.calculate_health_score(node_id)
            
            # 综合评分
            score = (
                health * 0.4 +
                (100 - node.cpu_usage) * 0.2 +
                (100 - node.memory_usage) * 0.2 +
                node.success_rate * 100 * 0.1 +
                (100 - min(node.active_tasks * 10, 100)) * 0.1
            )
            
            if score > best_score:
                best_score = score
                best_node = node_id
        
        return best_node
    
    def submit_task(self, description: str, complexity: str = "medium",
                   max_retries: int = 3) -> str:
        """提交任务"""
        task_id = str(uuid.uuid4())
        
        task = Task(
            task_id=task_id,
            description=description,
            complexity=complexity,
            status="pending",
            created_at=time.time(),
            max_retries=max_retries
        )
        
        self.tasks[task_id] = task
        self.auto_save()
        
        return task_id
    
    def assign_task(self, task_id: str) -> bool:
        """分配任务"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        
        # 选择节点
        node_id = self.select_node(task.complexity)
        if not node_id:
            return False
        
        # 分配
        task.assigned_node = node_id
        task.status = "running"
        task.started_at = time.time()
        
        # 更新节点
        self.nodes[node_id].active_tasks += 1
        
        self.auto_save()
        return True
    
    def complete_task(self, task_id: str, success: bool,
                     result: str = None, error: str = None):
        """完成任务"""
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        node_id = task.assigned_node
        
        # 更新任务
        task.status = "completed" if success else "failed"
        task.completed_at = time.time()
        task.result = result
        task.error = error
        
        # 更新节点
        if node_id and node_id in self.nodes:
            node = self.nodes[node_id]
            node.active_tasks = max(0, node.active_tasks - 1)
            node.total_tasks += 1
            
            # 重新计算成功率
            completed_tasks = [
                t for t in self.tasks.values()
                if t.assigned_node == node_id and t.status in ['completed', 'failed']
            ]
            if completed_tasks:
                success_count = sum(1 for t in completed_tasks if t.status == 'completed')
                node.success_rate = success_count / len(completed_tasks)
            
            # 重新计算平均响应时间
            finished_tasks = [
                t for t in self.tasks.values()
                if t.assigned_node == node_id and t.completed_at
            ]
            if finished_tasks:
                total_time = sum(t.completed_at - t.started_at for t in finished_tasks)
                node.avg_response_time = total_time / len(finished_tasks)
            
            # 记录性能
            if task.started_at:
                response_time = task.completed_at - task.started_at
                self.performance_history.append({
                    'node_id': node_id,
                    'timestamp': time.time(),
                    'response_time': response_time,
                    'success': 1 if success else 0
                })
        
        self.auto_save()
    
    def retry_failed_tasks(self) -> int:
        """重试失败任务"""
        count = 0
        
        for task in self.tasks.values():
            if task.status == 'failed' and task.retry_count < task.max_retries:
                # 重置
                task.status = 'pending'
                task.assigned_node = None
                task.started_at = None
                task.completed_at = None
                task.retry_count += 1
                task.error = None
                
                # 重新分配
                self.assign_task(task.task_id)
                count += 1
        
        if count > 0:
            self.auto_save()
        
        return count
    
    def get_stats(self) -> Dict:
        """获取统计"""
        # 节点统计
        total_nodes = len(self.nodes)
        online_nodes = sum(1 for n in self.nodes.values() if n.status == 'online')
        avg_health = sum(n.health_score for n in self.nodes.values()) / total_nodes if total_nodes > 0 else 0
        active_tasks = sum(n.active_tasks for n in self.nodes.values())
        
        # 任务统计
        total_tasks = len(self.tasks)
        pending = sum(1 for t in self.tasks.values() if t.status == 'pending')
        running = sum(1 for t in self.tasks.values() if t.status == 'running')
        completed = sum(1 for t in self.tasks.values() if t.status == 'completed')
        failed = sum(1 for t in self.tasks.values() if t.status == 'failed')
        
        # 平均时长
        finished = [t for t in self.tasks.values() if t.completed_at and t.started_at]
        avg_duration = sum(t.completed_at - t.started_at for t in finished) / len(finished) if finished else 0
        
        return {
            'nodes': {
                'total': total_nodes,
                'online': online_nodes,
                'avg_health': round(avg_health, 2),
                'active_tasks': active_tasks
            },
            'tasks': {
                'total': total_tasks,
                'pending': pending,
                'running': running,
                'completed': completed,
                'failed': failed,
                'avg_duration': round(avg_duration, 2)
            }
        }
    
    def cleanup_old_data(self, days: int = 7):
        """清理旧数据"""
        cutoff = time.time() - (days * 86400)
        
        # 清理旧任务
        old_tasks = [
            task_id for task_id, task in self.tasks.items()
            if task.completed_at and task.completed_at < cutoff
        ]
        for task_id in old_tasks:
            del self.tasks[task_id]
        
        # 清理旧性能记录
        self.performance_history = [
            h for h in self.performance_history
            if h['timestamp'] > cutoff
        ]
        
        if old_tasks or len(self.performance_history) < len(self.performance_history):
            self.save()
        
        return len(old_tasks)


def main():
    """CLI 测试"""
    import sys
    
    scheduler = LightweightScheduler()
    
    if len(sys.argv) < 2:
        print("\n🚀 Lightweight Task Scheduler")
        print("\nCommands:")
        print("  register <node_id> <name> <ip>")
        print("  submit <description>")
        print("  assign <task_id>")
        print("  complete <task_id> <success>")
        print("  retry")
        print("  stats")
        print("  cleanup [days]")
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'register':
        node = Node(
            node_id=sys.argv[2],
            name=sys.argv[3],
            ip=sys.argv[4]
        )
        scheduler.register_node(node)
        print(f"✅ Node {node.name} registered")
    
    elif cmd == 'submit':
        description = ' '.join(sys.argv[2:])
        task_id = scheduler.submit_task(description)
        print(f"✅ Task submitted: {task_id}")
    
    elif cmd == 'assign':
        task_id = sys.argv[2]
        success = scheduler.assign_task(task_id)
        if success:
            print(f"✅ Task {task_id} assigned")
        else:
            print(f"❌ Failed to assign task")
    
    elif cmd == 'complete':
        task_id = sys.argv[2]
        success = sys.argv[3].lower() == 'true'
        scheduler.complete_task(task_id, success)
        print(f"✅ Task {task_id} completed")
    
    elif cmd == 'retry':
        count = scheduler.retry_failed_tasks()
        print(f"✅ Retried {count} tasks")
    
    elif cmd == 'stats':
        stats = scheduler.get_stats()
        print("\n📊 Scheduler Statistics")
        print(f"\nNodes:")
        print(f"  Total: {stats['nodes']['total']}")
        print(f"  Online: {stats['nodes']['online']}")
        print(f"  Avg Health: {stats['nodes']['avg_health']}")
        print(f"  Active Tasks: {stats['nodes']['active_tasks']}")
        print(f"\nTasks:")
        print(f"  Total: {stats['tasks']['total']}")
        print(f"  Pending: {stats['tasks']['pending']}")
        print(f"  Running: {stats['tasks']['running']}")
        print(f"  Completed: {stats['tasks']['completed']}")
        print(f"  Failed: {stats['tasks']['failed']}")
        print(f"  Avg Duration: {stats['tasks']['avg_duration']}s")
    
    elif cmd == 'cleanup':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        count = scheduler.cleanup_old_data(days)
        print(f"✅ Cleaned up {count} old tasks")


if __name__ == '__main__':
    main()
