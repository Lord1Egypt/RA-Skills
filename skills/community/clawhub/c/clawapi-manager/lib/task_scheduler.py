#!/usr/bin/env python3
"""
Task Scheduler - 任务调度系统
负载均衡、任务队列、节点选择、失败重试、性能追踪
"""

import sqlite3
import json
import time
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

@dataclass
class Node:
    """节点信息"""
    node_id: str
    name: str
    ip: str
    status: str  # online, offline, degraded
    health_score: float  # 0-100
    cpu_usage: float
    memory_usage: float
    active_tasks: int
    total_tasks: int
    success_rate: float
    avg_response_time: float  # seconds
    last_heartbeat: float  # timestamp
    
@dataclass
class Task:
    """任务信息"""
    task_id: str
    description: str
    complexity: str  # free, medium, expensive
    status: str  # pending, running, completed, failed
    assigned_node: Optional[str]
    created_at: float
    started_at: Optional[float]
    completed_at: Optional[float]
    retry_count: int
    max_retries: int
    result: Optional[str]
    error: Optional[str]


class TaskScheduler:
    def __init__(self, db_path: str = None):
        """初始化调度器"""
        if db_path is None:
            db_path = Path(__file__).parent.parent / "data" / "scheduler.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 节点表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                node_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                ip TEXT NOT NULL,
                status TEXT NOT NULL,
                health_score REAL DEFAULT 100.0,
                cpu_usage REAL DEFAULT 0.0,
                memory_usage REAL DEFAULT 0.0,
                active_tasks INTEGER DEFAULT 0,
                total_tasks INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 1.0,
                avg_response_time REAL DEFAULT 0.0,
                last_heartbeat REAL NOT NULL,
                created_at REAL NOT NULL
            )
        """)
        
        # 任务表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                complexity TEXT NOT NULL,
                status TEXT NOT NULL,
                assigned_node TEXT,
                created_at REAL NOT NULL,
                started_at REAL,
                completed_at REAL,
                retry_count INTEGER DEFAULT 0,
                max_retries INTEGER DEFAULT 3,
                result TEXT,
                error TEXT,
                FOREIGN KEY (assigned_node) REFERENCES nodes(node_id)
            )
        """)
        
        # 性能历史表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id TEXT NOT NULL,
                timestamp REAL NOT NULL,
                cpu_usage REAL,
                memory_usage REAL,
                response_time REAL,
                success INTEGER,
                FOREIGN KEY (node_id) REFERENCES nodes(node_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def register_node(self, node: Node):
        """注册节点"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO nodes 
            (node_id, name, ip, status, health_score, cpu_usage, memory_usage,
             active_tasks, total_tasks, success_rate, avg_response_time, 
             last_heartbeat, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            node.node_id, node.name, node.ip, node.status,
            node.health_score, node.cpu_usage, node.memory_usage,
            node.active_tasks, node.total_tasks, node.success_rate,
            node.avg_response_time, node.last_heartbeat, time.time()
        ))
        
        conn.commit()
        conn.close()
    
    def update_node_heartbeat(self, node_id: str, metrics: Dict):
        """更新节点心跳和指标"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE nodes SET
                status = ?,
                cpu_usage = ?,
                memory_usage = ?,
                last_heartbeat = ?
            WHERE node_id = ?
        """, (
            metrics.get('status', 'online'),
            metrics.get('cpu_usage', 0.0),
            metrics.get('memory_usage', 0.0),
            time.time(),
            node_id
        ))
        
        # 记录性能历史
        cursor.execute("""
            INSERT INTO performance_history
            (node_id, timestamp, cpu_usage, memory_usage, response_time, success)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            node_id,
            time.time(),
            metrics.get('cpu_usage', 0.0),
            metrics.get('memory_usage', 0.0),
            metrics.get('response_time', 0.0),
            1  # heartbeat success
        ))
        
        conn.commit()
        conn.close()
    
    def calculate_health_score(self, node_id: str) -> float:
        """计算节点健康评分（0-100）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取节点当前状态
        cursor.execute("""
            SELECT status, cpu_usage, memory_usage, success_rate, 
                   avg_response_time, last_heartbeat
            FROM nodes WHERE node_id = ?
        """, (node_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return 0.0
        
        status, cpu, mem, success_rate, response_time, last_hb = row
        
        # 评分因素
        score = 100.0
        
        # 1. 状态（40分）
        if status == 'offline':
            score -= 40
        elif status == 'degraded':
            score -= 20
        
        # 2. 心跳（20分）
        time_since_hb = time.time() - last_hb
        if time_since_hb > 300:  # 5分钟
            score -= 20
        elif time_since_hb > 60:  # 1分钟
            score -= 10
        
        # 3. CPU使用率（15分）
        if cpu > 90:
            score -= 15
        elif cpu > 70:
            score -= 10
        elif cpu > 50:
            score -= 5
        
        # 4. 内存使用率（15分）
        if mem > 90:
            score -= 15
        elif mem > 70:
            score -= 10
        elif mem > 50:
            score -= 5
        
        # 5. 成功率（10分）
        score -= (1.0 - success_rate) * 10
        
        conn.close()
        return max(0.0, min(100.0, score))
    
    def select_node(self, complexity: str) -> Optional[str]:
        """选择最佳节点（负载均衡算法）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取所有在线节点
        cursor.execute("""
            SELECT node_id, name, active_tasks, health_score, 
                   cpu_usage, memory_usage, success_rate
            FROM nodes 
            WHERE status = 'online'
            ORDER BY health_score DESC, active_tasks ASC
        """)
        
        nodes = cursor.fetchall()
        conn.close()
        
        if not nodes:
            return None
        
        # 计算每个节点的得分
        best_node = None
        best_score = -1
        
        for node_id, name, active, health, cpu, mem, success in nodes:
            # 综合评分
            score = (
                health * 0.4 +                    # 健康评分（40%）
                (100 - cpu) * 0.2 +               # CPU空闲度（20%）
                (100 - mem) * 0.2 +               # 内存空闲度（20%）
                success * 100 * 0.1 +             # 成功率（10%）
                (100 - min(active * 10, 100)) * 0.1  # 负载（10%）
            )
            
            if score > best_score:
                best_score = score
                best_node = node_id
        
        return best_node
    
    def submit_task(self, description: str, complexity: str = "medium", 
                   max_retries: int = 3) -> str:
        """提交任务"""
        import uuid
        task_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tasks
            (task_id, description, complexity, status, created_at, max_retries)
            VALUES (?, ?, ?, 'pending', ?, ?)
        """, (task_id, description, complexity, time.time(), max_retries))
        
        conn.commit()
        conn.close()
        
        return task_id
    
    def assign_task(self, task_id: str) -> bool:
        """分配任务到节点"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取任务信息
        cursor.execute("""
            SELECT complexity FROM tasks WHERE task_id = ?
        """, (task_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False
        
        complexity = row[0]
        
        # 选择节点
        node_id = self.select_node(complexity)
        if not node_id:
            conn.close()
            return False
        
        # 分配任务
        cursor.execute("""
            UPDATE tasks SET
                assigned_node = ?,
                status = 'running',
                started_at = ?
            WHERE task_id = ?
        """, (node_id, time.time(), task_id))
        
        # 更新节点活跃任务数
        cursor.execute("""
            UPDATE nodes SET
                active_tasks = active_tasks + 1
            WHERE node_id = ?
        """, (node_id,))
        
        conn.commit()
        conn.close()
        
        return True
    
    def complete_task(self, task_id: str, success: bool, 
                     result: str = None, error: str = None):
        """完成任务"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取任务信息
        cursor.execute("""
            SELECT assigned_node, started_at FROM tasks WHERE task_id = ?
        """, (task_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return
        
        node_id, started_at = row
        response_time = time.time() - started_at if started_at else 0
        
        # 更新任务状态
        status = 'completed' if success else 'failed'
        cursor.execute("""
            UPDATE tasks SET
                status = ?,
                completed_at = ?,
                result = ?,
                error = ?
            WHERE task_id = ?
        """, (status, time.time(), result, error, task_id))
        
        # 更新节点统计
        if node_id:
            cursor.execute("""
                UPDATE nodes SET
                    active_tasks = active_tasks - 1,
                    total_tasks = total_tasks + 1,
                    success_rate = (
                        SELECT AVG(CASE WHEN status = 'completed' THEN 1.0 ELSE 0.0 END)
                        FROM tasks WHERE assigned_node = ?
                    ),
                    avg_response_time = (
                        SELECT AVG(completed_at - started_at)
                        FROM tasks 
                        WHERE assigned_node = ? AND completed_at IS NOT NULL
                    )
                WHERE node_id = ?
            """, (node_id, node_id, node_id))
            
            # 记录性能历史
            cursor.execute("""
                INSERT INTO performance_history
                (node_id, timestamp, response_time, success)
                VALUES (?, ?, ?, ?)
            """, (node_id, time.time(), response_time, 1 if success else 0))
        
        conn.commit()
        conn.close()
    
    def retry_failed_tasks(self):
        """重试失败的任务"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 查找需要重试的任务
        cursor.execute("""
            SELECT task_id, retry_count, max_retries
            FROM tasks
            WHERE status = 'failed' AND retry_count < max_retries
        """)
        
        tasks = cursor.fetchall()
        
        for task_id, retry_count, max_retries in tasks:
            # 重置任务状态
            cursor.execute("""
                UPDATE tasks SET
                    status = 'pending',
                    assigned_node = NULL,
                    started_at = NULL,
                    completed_at = NULL,
                    retry_count = retry_count + 1,
                    error = NULL
                WHERE task_id = ?
            """, (task_id,))
            
            # 重新分配
            self.assign_task(task_id)
        
        conn.commit()
        conn.close()
        
        return len(tasks)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 节点统计
        cursor.execute("""
            SELECT 
                COUNT(*) as total_nodes,
                SUM(CASE WHEN status = 'online' THEN 1 ELSE 0 END) as online_nodes,
                AVG(health_score) as avg_health,
                SUM(active_tasks) as total_active_tasks
            FROM nodes
        """)
        node_stats = cursor.fetchone()
        
        # 任务统计
        cursor.execute("""
            SELECT
                COUNT(*) as total_tasks,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'running' THEN 1 ELSE 0 END) as running,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                AVG(CASE WHEN completed_at IS NOT NULL 
                    THEN completed_at - started_at ELSE NULL END) as avg_duration
            FROM tasks
        """)
        task_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            'nodes': {
                'total': node_stats[0] or 0,
                'online': node_stats[1] or 0,
                'avg_health': round(node_stats[2] or 0, 2),
                'active_tasks': node_stats[3] or 0
            },
            'tasks': {
                'total': task_stats[0] or 0,
                'pending': task_stats[1] or 0,
                'running': task_stats[2] or 0,
                'completed': task_stats[3] or 0,
                'failed': task_stats[4] or 0,
                'avg_duration': round(task_stats[5] or 0, 2)
            }
        }


def main():
    """CLI 测试"""
    import sys
    
    scheduler = TaskScheduler()
    
    if len(sys.argv) < 2:
        print("\nTask Scheduler CLI")
        print("\nCommands:")
        print("  register <node_id> <name> <ip>  Register a node")
        print("  submit <description>            Submit a task")
        print("  assign <task_id>                Assign task to node")
        print("  complete <task_id> <success>    Complete task")
        print("  retry                           Retry failed tasks")
        print("  stats                           Show statistics")
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'register':
        node = Node(
            node_id=sys.argv[2],
            name=sys.argv[3],
            ip=sys.argv[4],
            status='online',
            health_score=100.0,
            cpu_usage=0.0,
            memory_usage=0.0,
            active_tasks=0,
            total_tasks=0,
            success_rate=1.0,
            avg_response_time=0.0,
            last_heartbeat=time.time()
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
            print(f"❌ Failed to assign task {task_id}")
    
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


if __name__ == '__main__':
    main()
