#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监控服务主程序
定时执行监控任务，检测异常并发送通知
"""

import os
import sys
import json
import time
import signal
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper import DataScraper
from detector import AnomalyDetector, Alert
from notifier import NotificationManager

# 尝试导入schedule
try:
    import schedule
    HAS_SCHEDULE = True
except ImportError:
    HAS_SCHEDULE = False
    print("警告: 未安装schedule，请运行: pip install schedule")


class MonitorService:
    """监控服务"""
    
    def __init__(self, config_path: str):
        """
        初始化监控服务
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.tasks = self.config.get('tasks', [])
        self.global_config = self.config.get('global', {})
        
        # 数据存储目录
        self.data_dir = Path(self.global_config.get('data_dir', '../assets/data'))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 截图存储目录
        self.screenshot_dir = Path(self.global_config.get('screenshot_dir', '../assets/screenshots'))
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # 告警存储目录
        self.alert_dir = self.data_dir / 'alerts'
        self.alert_dir.mkdir(parents=True, exist_ok=True)
        
        # 运行状态
        self.running = False
        
        # 信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _signal_handler(self, signum, frame):
        """信号处理"""
        print(f"\n收到信号 {signum}，正在停止监控服务...")
        self.running = False
    
    def _get_task_data_file(self, task_id: str) -> Path:
        """获取任务数据文件路径"""
        task_dir = self.data_dir / 'raw' / task_id
        task_dir.mkdir(parents=True, exist_ok=True)
        
        today = datetime.now().strftime('%Y-%m-%d')
        return task_dir / f'{today}.jsonl'
    
    def _load_task_history(self, task_id: str, days: int = 7) -> List[Dict]:
        """加载任务历史数据"""
        history = []
        task_dir = self.data_dir / 'raw' / task_id
        
        if not task_dir.exists():
            return history
        
        # 读取最近几天的数据
        for i in range(days):
            date_str = (datetime.now() - __import__('datetime').timedelta(days=i)).strftime('%Y-%m-%d')
            data_file = task_dir / f'{date_str}.jsonl'
            
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            history.append(json.loads(line.strip()))
                        except:
                            pass
        
        return sorted(history, key=lambda x: x.get('timestamp', ''))
    
    def _save_task_data(self, task_id: str, data: Dict):
        """保存任务数据"""
        data_file = self._get_task_data_file(task_id)
        
        with open(data_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    def _save_alert(self, alert: Alert):
        """保存告警"""
        today = datetime.now().strftime('%Y-%m-%d')
        alert_file = self.alert_dir / f'{today}.jsonl'
        
        with open(alert_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(alert.to_dict(), ensure_ascii=False) + '\n')
    
    def execute_task(self, task: Dict) -> Dict:
        """
        执行单个监控任务
        
        Args:
            task: 任务配置
            
        Returns:
            执行结果
        """
        task_id = task['id']
        task_name = task['name']
        url = task['url']
        platform = task.get('platform')
        
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 执行任务: {task_name}")
        
        result = {
            'task_id': task_id,
            'task_name': task_name,
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'data': {},
            'alerts': [],
            'screenshot': None
        }
        
        try:
            # 抓取数据
            with DataScraper(headless=True) as scraper:
                scrape_result = scraper.scrape(url, platform=platform)
                
                if not scrape_result['success']:
                    print(f"抓取失败: {scrape_result.get('error')}")
                    return result
                
                result['data'] = scrape_result['data']
                result['success'] = True
                
                # 保存数据
                self._save_task_data(task_id, {
                    'task_id': task_id,
                    'timestamp': result['timestamp'],
                    'url': url,
                    'data': result['data']
                })
                
                print(f"抓取成功: {result['data']}")
                
                # 异常检测
                history = self._load_task_history(task_id)
                
                detector = AnomalyDetector()
                detector.load_history(history)
                
                alerts = detector.detect({
                    'task_id': task_id,
                    'timestamp': result['timestamp'],
                    'data': result['data']
                }, task)
                
                result['alerts'] = [a.to_dict() for a in alerts]
                
                # 处理告警
                if alerts:
                    print(f"检测到 {len(alerts)} 个异常")
                    
                    # 是否需要截图
                    screenshot_on_alert = task.get('screenshot_on_alert', True)
                    screenshot_path = None
                    
                    if screenshot_on_alert:
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        screenshot_path = str(self.screenshot_dir / f'{task_id}_{timestamp}.png')
                        
                        # 重新访问页面截图
                        scrape_result = scraper.scrape(url, platform=platform, screenshot=True, screenshot_path=screenshot_path)
                        result['screenshot'] = screenshot_path
                        print(f"截图已保存: {screenshot_path}")
                    
                    # 发送通知
                    notification_config = task.get('notification', {})
                    if notification_config:
                        notifier = NotificationManager(notification_config)
                        
                        for alert in alerts:
                            self._save_alert(alert)
                            notifier.send_alert(alert.to_dict(), screenshot_path)
                
        except Exception as e:
            print(f"任务执行失败: {e}")
            result['error'] = str(e)
        
        return result
    
    def run_task(self, task_id: str = None):
        """
        运行任务
        
        Args:
            task_id: 指定任务ID，None则运行所有任务
        """
        if task_id:
            # 运行指定任务
            task = next((t for t in self.tasks if t['id'] == task_id), None)
            if task:
                self.execute_task(task)
            else:
                print(f"未找到任务: {task_id}")
        else:
            # 运行所有任务
            for task in self.tasks:
                self.execute_task(task)
                time.sleep(2)  # 避免请求过快
    
    def schedule_tasks(self):
        """设置定时任务"""
        if not HAS_SCHEDULE:
            print("错误: 未安装schedule模块")
            return
        
        for task in self.tasks:
            schedule_str = task.get('schedule', self.global_config.get('default_schedule', '0 */6 * * *'))
            
            # 解析cron格式（简化版，只支持部分格式）
            parts = schedule_str.split()
            
            if len(parts) == 5:
                minute, hour, day, month, weekday = parts
                
                # 构建schedule任务
                if hour.startswith('*/') and minute == '0':
                    # 每N小时
                    hours = int(hour.replace('*/', ''))
                    schedule.every(hours).hours.do(self.execute_task, task)
                    print(f"已设置定时任务: {task['name']} 每{hours}小时")
                    
                elif ',' in hour and minute == '0':
                    # 指定多个时间点
                    for h in hour.split(','):
                        schedule.every().day.at(f"{h}:00").do(self.execute_task, task)
                    print(f"已设置定时任务: {task['name']} 每天 {hour} 点")
                    
                elif hour == '*' and minute.startswith('*/'):
                    # 每N分钟
                    minutes = int(minute.replace('*/', ''))
                    schedule.every(minutes).minutes.do(self.execute_task, task)
                    print(f"已设置定时任务: {task['name']} 每{minutes}分钟")
                    
                else:
                    # 默认每6小时
                    schedule.every(6).hours.do(self.execute_task, task)
                    print(f"已设置定时任务: {task['name']} 每6小时")
    
    def start(self):
        """启动监控服务"""
        if not HAS_SCHEDULE:
            print("错误: 请先安装schedule模块: pip install schedule")
            return
        
        print("=" * 50)
        print("竞品监控服务启动")
        print("=" * 50)
        print(f"配置文件: {self.config_path}")
        print(f"监控任务数: {len(self.tasks)}")
        print(f"数据存储: {self.data_dir}")
        print(f"截图存储: {self.screenshot_dir}")
        print("=" * 50)
        
        # 设置定时任务
        self.schedule_tasks()
        
        # 立即执行一次
        print("\n立即执行首次监控...")
        self.run_task()
        
        # 启动定时循环
        self.running = True
        print("\n监控服务运行中，按 Ctrl+C 停止...")
        
        while self.running:
            schedule.run_pending()
            time.sleep(1)
        
        print("\n监控服务已停止")
    
    def generate_report(self, days: int = 7, output: str = None):
        """
        生成监控报告
        
        Args:
            days: 统计天数
            output: 输出文件路径
        """
        from datetime import timedelta
        
        # 统计告警
        alert_stats = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'total': 0
        }
        
        alerts = []
        for i in range(days):
            date_str = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            alert_file = self.alert_dir / f'{date_str}.jsonl'
            
            if alert_file.exists():
                with open(alert_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            alert = json.loads(line.strip())
                            alerts.append(alert)
                            level = alert.get('level', 'info')
                            if level in alert_stats:
                                alert_stats[level] += 1
                            alert_stats['total'] += 1
                        except:
                            pass
        
        # 生成报告
        report = f"""
# 竞品监控报告

**统计时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**统计周期**: 最近 {days} 天

## 告警统计

| 级别 | 数量 |
|------|------|
| 🔴 严重 | {alert_stats['critical']} |
| 🟠 高 | {alert_stats['high']} |
| 🟡 中 | {alert_stats['medium']} |
| 🟢 低 | {alert_stats['low']} |
| **总计** | **{alert_stats['total']}** |

## 最近告警

"""
        
        for alert in sorted(alerts, key=lambda x: x.get('timestamp', ''), reverse=True)[:10]:
            report += f"""
### {alert.get('message', '告警')}

- 时间: {alert.get('timestamp', 'N/A')}
- 任务: {alert.get('task_id', 'N/A')}
- 级别: {alert.get('level', 'N/A')}
- 详情: {json.dumps(alert.get('details', {}), ensure_ascii=False)}

"""
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存: {output}")
        else:
            print(report)
        
        return report


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='竞品监控服务')
    parser.add_argument('--config', '-c', default='../assets/config/monitor_tasks.json',
                       help='配置文件路径')
    parser.add_argument('action', choices=['start', 'run', 'report'],
                       help='操作: start(启动服务), run(执行一次), report(生成报告)')
    parser.add_argument('--task', '-t', help='指定任务ID')
    parser.add_argument('--days', '-d', type=int, default=7, help='报告统计天数')
    parser.add_argument('--output', '-o', help='报告输出路径')
    
    args = parser.parse_args()
    
    # 确保配置文件路径正确
    config_path = args.config
    if not os.path.isabs(config_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, config_path)
    
    service = MonitorService(config_path)
    
    if args.action == 'start':
        service.start()
    elif args.action == 'run':
        service.run_task(args.task)
    elif args.action == 'report':
        service.generate_report(args.days, args.output)


if __name__ == '__main__':
    main()
