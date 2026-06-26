#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务模块

设置定时任务，自动运行财经新闻分析

用法:
    python scheduler.py add --time "08:00" --daily     # 每天 8 点运行
    python scheduler.py add --time "08:00" --weekday 1 # 每周一 8 点运行
    python scheduler.py list                            # 查看任务列表
    python scheduler.py remove --id 1                   # 删除任务
    python scheduler.py run --id 1                      # 手动运行任务
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class Scheduler:
    """简易任务调度器"""
    
    def __init__(self, config_file: str = "scheduler_config.json"):
        self.config_file = Path(config_file)
        self.tasks = self.load_tasks()
    
    def load_tasks(self) -> list:
        """加载任务配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_tasks(self):
        """保存任务配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def add_task(self, time: str, daily: bool = False, weekday: Optional[int] = None,
                 source: str = "all", limit: int = 20, output: str = "brief"):
        """添加定时任务"""
        task = {
            'id': len(self.tasks) + 1,
            'time': time,
            'daily': daily,
            'weekday': weekday,
            'source': source,
            'limit': limit,
            'output': output,
            'enabled': True,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_run': None
        }
        
        self.tasks.append(task)
        self.save_tasks()
        
        print(f"✅ 任务已添加 (ID: {task['id']})")
        print(f"   时间：{time}")
        print(f"   频率：{'每天' if daily else f'每周{self.weekday_name(weekday)}'}")
        print(f"   新闻源：{source}")
        print(f"   输出格式：{output}")
    
    def weekday_name(self, weekday: Optional[int]) -> str:
        """获取星期名称"""
        names = {
            0: '日', 1: '一', 2: '二', 3: '三',
            4: '四', 5: '五', 6: '六'
        }
        return names.get(weekday, '?')
    
    def list_tasks(self):
        """列出所有任务"""
        if not self.tasks:
            print("📋 暂无定时任务")
            return
        
        print("\n📋 定时任务列表")
        print("=" * 70)
        
        for task in self.tasks:
            status = "✅" if task['enabled'] else "❌"
            frequency = "每天" if task['daily'] else f"每周{self.weekday_name(task['weekday'])}"
            last_run = task['last_run'] or "未运行"
            
            print(f"\n{status} 任务 ID: {task['id']}")
            print(f"   时间：{task['time']}")
            print(f"   频率：{frequency}")
            print(f"   新闻源：{task['source']}")
            print(f"   输出：{task['output']}")
            print(f"   最后运行：{last_run}")
        
        print("\n" + "=" * 70)
    
    def remove_task(self, task_id: int):
        """删除任务"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                removed = self.tasks.pop(i)
                self.save_tasks()
                print(f"✅ 任务已删除：{removed}")
                return
        
        print(f"❌ 未找到任务 ID: {task_id}")
    
    def run_task(self, task_id: int):
        """手动运行任务"""
        task = None
        for t in self.tasks:
            if t['id'] == task_id:
                task = t
                break
        
        if not task:
            print(f"❌ 未找到任务 ID: {task_id}")
            return
        
        print(f"🚀 运行任务 {task_id}...")
        print(f"   命令：python scripts/main.py --source {task['source']} --limit {task['limit']} --output {task['output']}")
        
        # 执行命令
        try:
            result = subprocess.run(
                [sys.executable, "scripts/main.py", 
                 "--source", task['source'],
                 "--limit", str(task['limit']),
                 "--output", task['output']],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print(f"✅ 任务执行成功")
                task['last_run'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_tasks()
            else:
                print(f"❌ 任务执行失败：{result.stderr}")
        
        except subprocess.TimeoutExpired:
            print("❌ 任务执行超时（>5 分钟）")
        except Exception as e:
            print(f"❌ 任务执行异常：{e}")
    
    def enable_task(self, task_id: int, enable: bool = True):
        """启用/禁用任务"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['enabled'] = enable
                self.save_tasks()
                status = "启用" if enable else "禁用"
                print(f"✅ 任务已{status}")
                return
        
        print(f"❌ 未找到任务 ID: {task_id}")
    
    def check_and_run(self):
        """检查并运行到期的任务（用于 cron 调用）"""
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        current_weekday = now.weekday()  # 0=周一，6=周日
        
        for task in self.tasks:
            if not task['enabled']:
                continue
            
            # 检查时间
            if task['time'] != current_time:
                continue
            
            # 检查频率
            if task['daily']:
                self.run_task(task['id'])
            elif task['weekday'] is not None:
                # 转换为 Python 的 weekday (0=周一)
                python_weekday = (current_weekday + 1) % 7
                if python_weekday == task['weekday']:
                    self.run_task(task['id'])


def main():
    parser = argparse.ArgumentParser(description='财经新闻分析定时任务')
    
    subparsers = parser.add_subparsers(dest='action', help='操作类型')
    
    # 添加任务
    add_parser = subparsers.add_parser('add', help='添加定时任务')
    add_parser.add_argument('--time', type=str, required=True,
                           help='运行时间 (HH:MM 格式，如 08:00)')
    add_parser.add_argument('--daily', action='store_true',
                           help='每天运行')
    add_parser.add_argument('--weekday', type=int, choices=range(7),
                           help='星期几运行 (0=周日，1=周一，...6=周六)')
    add_parser.add_argument('--source', type=str, default='all',
                           help='新闻源（默认：all）')
    add_parser.add_argument('--limit', type=int, default=20,
                           help='每源新闻数量（默认：20）')
    add_parser.add_argument('--output', type=str, default='brief',
                           choices=['brief', 'full', 'industry'],
                           help='输出格式（默认：brief）')
    
    # 列出任务
    subparsers.add_parser('list', help='列出所有任务')
    
    # 删除任务
    remove_parser = subparsers.add_parser('remove', help='删除任务')
    remove_parser.add_argument('--id', type=int, required=True,
                              help='任务 ID')
    
    # 运行任务
    run_parser = subparsers.add_parser('run', help='手动运行任务')
    run_parser.add_argument('--id', type=int, required=True,
                           help='任务 ID')
    
    # 启用/禁用任务
    toggle_parser = subparsers.add_parser('toggle', help='启用/禁用任务')
    toggle_parser.add_argument('--id', type=int, required=True,
                              help='任务 ID')
    toggle_parser.add_argument('--enable', action='store_true',
                              help='启用（默认禁用）')
    
    # 检查并运行（用于 cron）
    subparsers.add_parser('check', help='检查并运行到期任务')
    
    args = parser.parse_args()
    
    scheduler = Scheduler()
    
    if args.action == 'add':
        if not args.daily and args.weekday is None:
            print("❌ 请指定 --daily 或 --weekday")
            return
        
        scheduler.add_task(
            time=args.time,
            daily=args.daily,
            weekday=args.weekday,
            source=args.source,
            limit=args.limit,
            output=args.output
        )
    
    elif args.action == 'list':
        scheduler.list_tasks()
    
    elif args.action == 'remove':
        scheduler.remove_task(args.id)
    
    elif args.action == 'run':
        scheduler.run_task(args.id)
    
    elif args.action == 'toggle':
        scheduler.enable_task(args.id, args.enable)
    
    elif args.action == 'check':
        scheduler.check_and_run()
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
