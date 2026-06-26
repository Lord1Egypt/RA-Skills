#!/usr/bin/env python3
"""
任务状态管理脚本
实现子弹笔记的完整任务状态变化：● → × → > → 划掉 → <
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class TaskManager:
    """任务状态管理器"""

    # 任务状态定义
    STATUSES = {
        'task': {
            'symbol': '●',
            'name': '待办任务',
            'description': '需要执行的动作',
            'next_statuses': ['completed', 'migrated', 'cancelled', 'planned']
        },
        'completed': {
            'symbol': '×',
            'name': '已完成',
            'description': '任务已成功完成',
            'next_statuses': []  # 终态
        },
        'migrated': {
            'symbol': '>',
            'name': '已迁移',
            'description': '任务未完成但重要，延期到新日期',
            'next_statuses': ['task', 'cancelled']
        },
        'cancelled': {
            'symbol': '~~',
            'name': '已取消',
            'description': '任务不再需要，已取消',
            'next_statuses': []  # 终态
        },
        'planned': {
            'symbol': '<',
            'name': '已计划',
            'description': '任务升级为项目，需要详细规划',
            'next_statuses': ['task']
        }
    }

    # 事件定义
    EVENTS = {
        'event': {
            'symbol': '○',
            'name': '事件',
            'description': '已经或即将发生的事实，与特定日期/时间/地点相关',
            'features': {
                'has_date': True,      # 必须有日期
                'has_time': False,     # 可选时间
                'has_location': False, # 可选地点
                'passive': True,       # 被动的，不是主动执行的动作
                'can_migrate': True    # 可以重新安排（迁移）
            }
        }
    }

    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))

        self.base_dir = base_dir
        self.tasks_dir = os.path.join(base_dir, 'data', 'tasks')
        self.events_dir = os.path.join(base_dir, 'data', 'events')

        # 确保目录存在
        os.makedirs(self.tasks_dir, exist_ok=True)
        os.makedirs(self.events_dir, exist_ok=True)

    def create_task(
        self,
        date: str,
        task_id: str,
        content: str,
        status: str = 'task',
        time: str = '',
        notes: str = ''
    ) -> Dict:
        """
        创建新任务

        Args:
            date: 日期（YYYY-MM-DD）
            task_id: 任务ID
            content: 任务内容
            status: 初始状态（默认为task）
            time: 时间（可选）
            notes: 备注（可选）

        Returns:
            创建的任务信息
        """
        # 确保任务文件存在
        task_file = os.path.join(self.tasks_dir, date, 'tasks.json')
        os.makedirs(os.path.dirname(task_file), exist_ok=True)

        # 加载现有任务
        if os.path.exists(task_file):
            with open(task_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
        else:
            tasks_data = {'date': date, 'tasks': []}

        # 检查任务是否已存在
        existing_task = next((t for t in tasks_data['tasks'] if t['id'] == task_id), None)
        if existing_task:
            # 更新现有任务
            existing_task['content'] = content
            existing_task['status'] = status
            existing_task['time'] = time
            existing_task['notes'] = notes
            existing_task['updated_at'] = datetime.now().isoformat()

            # 保存任务数据
            with open(task_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, ensure_ascii=False, indent=2)

            print(f"任务已更新：{task_id} - {content}")
            return existing_task
        else:
            # 创建新任务
            task = {
                'id': task_id,
                'content': content,
                'status': status,
                'time': time,
                'notes': notes,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'history': []
            }

            # 记录初始状态
            if status != 'task':
                task['history'].append({
                    'status': 'task',
                    'changed_at': datetime.now().isoformat(),
                    'notes': '初始状态'
                })
                task['history'].append({
                    'status': status,
                    'changed_at': datetime.now().isoformat(),
                    'notes': notes or '任务创建'
                })

            tasks_data['tasks'].append(task)

            # 保存任务数据
            with open(task_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, ensure_ascii=False, indent=2)

            print(f"任务已创建：{task_id} - {content}")
            return task

    def update_task_status(
        self,
        date: str,
        task_id: str,
        new_status: str,
        notes: str = None
    ) -> Dict:
        """
        更新任务状态

        Args:
            date: 日期（YYYY-MM-DD）
            task_id: 任务ID
            new_status: 新状态（task/completed/migrated/cancelled/planned）
            notes: 状态变化备注

        Returns:
            更新后的任务信息
        """
        # 读取任务文件
        task_file = os.path.join(self.tasks_dir, date, 'tasks.json')
        if not os.path.exists(task_file):
            raise FileNotFoundError(f"任务文件不存在：{task_file}")

        with open(task_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 查找任务
        task = None
        for t in data['tasks']:
            if t['id'] == task_id:
                task = t
                break

        if not task:
            raise ValueError(f"任务不存在：{task_id}")

        # 验证状态转换
        current_status = task['status']
        if new_status not in self.STATUSES[current_status]['next_statuses']:
            raise ValueError(
                f"无效的状态转换：{current_status} → {new_status}。"
                f"允许的转换：{self.STATUSES[current_status]['next_statuses']}"
            )

        # 更新任务状态
        old_status = task['status']
        task['status'] = new_status
        task['status_history'].append({
            'from': old_status,
            'to': new_status,
            'timestamp': datetime.now().isoformat(),
            'notes': notes
        })

        # 保存文件
        os.makedirs(os.path.dirname(task_file), exist_ok=True)
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return task

    def migrate_task(
        self,
        date: str,
        task_id: str,
        new_date: str
    ) -> Dict:
        """
        迁移任务到新日期

        Args:
            date: 当前日期（YYYY-MM-DD）
            task_id: 任务ID
            new_date: 新日期（YYYY-MM-DD）

        Returns:
            迁移后的任务信息
        """
        # 更新当前任务状态为已迁移
        task = self.update_task_status(
            date=date,
            task_id=task_id,
            new_status='migrated',
            notes=f'迁移到 {new_date}'
        )

        # 在新日期创建任务副本（状态为待办）
        new_task_file = os.path.join(self.tasks_dir, new_date, 'tasks.json')
        os.makedirs(os.path.dirname(new_task_file), exist_ok=True)

        # 读取或创建新日期的任务文件
        if os.path.exists(new_task_file):
            with open(new_task_file, 'r', encoding='utf-8') as f:
                new_data = json.load(f)
        else:
            new_data = {'date': new_date, 'tasks': []}

        # 创建新任务（保持原有ID或生成新ID）
        new_task = task.copy()
        new_task['status'] = 'task'  # 重置为待办
        new_task['status_history'] = [{
            'from': 'migrated',
            'to': 'task',
            'timestamp': datetime.now().isoformat(),
            'notes': f'从 {date} 迁移而来'
        }]
        new_task['migrated_from'] = date

        new_data['tasks'].append(new_task)

        # 保存新日期的任务文件
        with open(new_task_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)

        return task

    def cancel_task(
        self,
        date: str,
        task_id: str,
        reason: str = None
    ) -> Dict:
        """
        取消任务（划掉）

        Args:
            date: 日期（YYYY-MM-DD）
            task_id: 任务ID
            reason: 取消原因

        Returns:
            取消后的任务信息
        """
        return self.update_task_status(
            date=date,
            task_id=task_id,
            new_status='cancelled',
            notes=reason
        )

    def complete_task(
        self,
        date: str,
        task_id: str,
        notes: str = None
    ) -> Dict:
        """
        完成任务

        Args:
            date: 日期（YYYY-MM-DD）
            task_id: 任务ID
            notes: 完成备注

        Returns:
            完成后的任务信息
        """
        return self.update_task_status(
            date=date,
            task_id=task_id,
            new_status='completed',
            notes=notes
        )

    def plan_task(
        self,
        date: str,
        task_id: str,
        collection_name: str = None
    ) -> Dict:
        """
        将任务升级为项目（需要详细规划）

        Args:
            date: 日期（YYYY-MM-DD）
            task_id: 任务ID
            collection_name: 项目/集子名称

        Returns:
            计划后的任务信息
        """
        notes = '升级为项目'
        if collection_name:
            notes += f"，移至集子：{collection_name}"

        return self.update_task_status(
            date=date,
            task_id=task_id,
            new_status='planned',
            notes=notes
        )

    def get_daily_tasks(
        self,
        date: str,
        status_filter: str = None
    ) -> List[Dict]:
        """
        获取指定日期的任务

        Args:
            date: 日期（YYYY-MM-DD）
            status_filter: 状态过滤器（可选）

        Returns:
            任务列表
        """
        task_file = os.path.join(self.tasks_dir, date, 'tasks.json')

        if not os.path.exists(task_file):
            return []

        with open(task_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        tasks = data['tasks']

        if status_filter:
            tasks = [t for t in tasks if t['status'] == status_filter]

        return tasks

    def get_task_statistics(
        self,
        date: str
    ) -> Dict:
        """
        获取任务统计信息

        Args:
            date: 日期（YYYY-MM-DD）

        Returns:
            统计信息
        """
        tasks = self.get_daily_tasks(date)

        stats = {
            'total': len(tasks),
            'pending': 0,
            'completed': 0,
            'migrated': 0,
            'cancelled': 0,
            'planned': 0
        }

        for task in tasks:
            stats[task['status']] += 1

        # 计算完成率
        if stats['total'] > 0:
            stats['completion_rate'] = stats['completed'] / stats['total'] * 100
        else:
            stats['completion_rate'] = 0

        return stats

    def format_task_with_symbol(self, task: Dict) -> str:
        """
        格式化任务为子弹笔记格式

        Args:
            task: 任务字典

        Returns:
            格式化字符串
        """
        symbol = self.STATUSES[task['status']]['symbol']
        time_str = f"{task.get('time', '')} " if task.get('time') else ""
        content = task['content']

        # 取消任务使用划线
        if task['status'] == 'cancelled':
            return f"{symbol} {time_str}~~{content}~~"
        else:
            return f"{symbol} {time_str}{content}"

    def format_event_with_details(self, event: Dict) -> str:
        """
        格式化事件为子弹笔记格式（包含日期、地点等详细信息）

        Args:
            event: 事件字典

        Returns:
            格式化字符串
        """
        symbol = self.EVENTS['event']['symbol']

        parts = []
        if event.get('time'):
            parts.append(event['time'])

        parts.append(event['content'])

        # 添加地点信息
        if event.get('location'):
            parts.append(f"📍 {event['location']}")

        return f"{symbol} {' '.join(parts)}"


def main():
    """测试用例"""
    manager = TaskManager()

    # 创建示例任务数据
    date = '2025-03-16'
    tasks_data = {
        'date': date,
        'tasks': [
            {
                'id': 'task_001',
                'content': '整理有机逆合成逻辑',
                'time': '09:00',
                'status': 'task',
                'priority': 'high',
                'status_history': []
            },
            {
                'id': 'task_002',
                'content': '购买卫生纸',
                'time': '09:00',
                'status': 'task',
                'priority': 'normal',
                'status_history': []
            },
            {
                'id': 'task_003',
                'content': '处理立项书摘要',
                'time': '09:17',
                'status': 'task',
                'priority': 'high',
                'status_history': []
            }
        ]
    }

    # 保存示例数据
    task_file = os.path.join(manager.tasks_dir, date, 'tasks.json')
    os.makedirs(os.path.dirname(task_file), exist_ok=True)
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(tasks_data, f, ensure_ascii=False, indent=2)

    print("✓ 示例任务数据已创建")

    # 测试完成任务
    print("\n" + "=" * 60)
    print("测试：完成任务 task_001")
    print("=" * 60)
    task = manager.complete_task(date, 'task_001', '已完成')
    print(f"任务状态：{task['status']}")
    print(f"格式化：{manager.format_task_with_symbol(task)}")

    # 测试迁移任务
    print("\n" + "=" * 60)
    print("测试：迁移任务 task_002 到 2025-03-17")
    print("=" * 60)
    task = manager.migrate_task(date, 'task_002', '2025-03-17')
    print(f"任务状态：{task['status']}")
    print(f"格式化：{manager.format_task_with_symbol(task)}")

    # 测试取消任务
    print("\n" + "=" * 60)
    print("测试：取消任务 task_003")
    print("=" * 60)
    task = manager.cancel_task(date, 'task_003', '不再需要')
    print(f"任务状态：{task['status']}")
    print(f"格式化：{manager.format_task_with_symbol(task)}")

    # 获取统计信息
    print("\n" + "=" * 60)
    print(f"任务统计（{date}）")
    print("=" * 60)
    stats = manager.get_task_statistics(date)
    print(f"总任务数：{stats['total']}")
    print(f"待办：{stats['pending']}")
    print(f"已完成：{stats['completed']}")
    print(f"已迁移：{stats['migrated']}")
    print(f"已取消：{stats['cancelled']}")
    print(f"完成率：{stats['completion_rate']:.1f}%")


if __name__ == '__main__':
    main()
