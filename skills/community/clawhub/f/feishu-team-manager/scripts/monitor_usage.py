#!/usr/bin/env python3
"""
飞书团队管理器技能使用监控脚本
监控技能下载量、使用频率和用户反馈
"""

import json
import os
import sqlite3
import time
from datetime import datetime, timedelta
import requests
from pathlib import Path

class SkillMonitor:
    def __init__(self, db_path=None):
        """初始化监控器"""
        self.db_path = db_path or os.path.expanduser("~/.openclaw/skills/feishu-team-manager/monitor.db")
        self.skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.init_database()
    
    def init_database(self):
        """初始化监控数据库"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建使用记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_data TEXT,
                user_agent TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建下载统计表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS download_stats (
                date DATE PRIMARY KEY,
                count INTEGER DEFAULT 0,
                unique_users INTEGER DEFAULT 0
            )
        ''')
        
        # 创建错误日志表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS error_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_type TEXT,
                error_message TEXT,
                stack_trace TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_usage(self, event_type, event_data=None, user_agent=None):
        """记录使用事件"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO usage_log (event_type, event_data, user_agent)
                VALUES (?, ?, ?)
            ''', (event_type, json.dumps(event_data) if event_data else None, user_agent))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"记录使用事件失败: {e}")
            return False
    
    def log_download(self, user_agent=None):
        """记录下载事件"""
        today = datetime.now().date().isoformat()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 更新下载统计
            cursor.execute('''
                INSERT OR REPLACE INTO download_stats (date, count, unique_users)
                VALUES (?, 
                    COALESCE((SELECT count FROM download_stats WHERE date = ?), 0) + 1,
                    COALESCE((SELECT unique_users FROM download_stats WHERE date = ?), 0) + 1
                )
            ''', (today, today, today))
            
            # 记录下载事件
            self.log_usage('download', {'date': today}, user_agent)
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"记录下载事件失败: {e}")
            return False
    
    def log_error(self, error_type, error_message, stack_trace=None):
        """记录错误日志"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO error_log (error_type, error_message, stack_trace)
                VALUES (?, ?, ?)
            ''', (error_type, error_message, stack_trace))
            
            conn.commit()
            conn.close()
            
            # 同时记录为使用事件
            self.log_usage('error', {
                'error_type': error_type,
                'error_message': error_message
            })
            
            return True
        except Exception as e:
            print(f"记录错误日志失败: {e}")
            return False
    
    def get_usage_stats(self, days=30):
        """获取使用统计"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 获取总使用次数
            cursor.execute('SELECT COUNT(*) FROM usage_log')
            total_usage = cursor.fetchone()[0]
            
            # 获取事件类型分布
            cursor.execute('''
                SELECT event_type, COUNT(*) as count 
                FROM usage_log 
                GROUP BY event_type 
                ORDER BY count DESC
            ''')
            event_distribution = dict(cursor.fetchall())
            
            # 获取最近N天的下载统计
            start_date = (datetime.now() - timedelta(days=days)).date().isoformat()
            cursor.execute('''
                SELECT date, count, unique_users 
                FROM download_stats 
                WHERE date >= ? 
                ORDER BY date DESC
            ''', (start_date,))
            download_stats = cursor.fetchall()
            
            # 获取错误统计
            cursor.execute('''
                SELECT error_type, COUNT(*) as count 
                FROM error_log 
                GROUP BY error_type 
                ORDER BY count DESC
            ''')
            error_stats = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                'total_usage': total_usage,
                'event_distribution': event_distribution,
                'download_stats': download_stats,
                'error_stats': error_stats,
                'monitoring_since': self.get_first_record_date()
            }
        except Exception as e:
            print(f"获取使用统计失败: {e}")
            return None
    
    def get_first_record_date(self):
        """获取第一条记录的日期"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT MIN(timestamp) FROM usage_log')
            result = cursor.fetchone()[0]
            conn.close()
            return result
        except:
            return None
    
    def generate_report(self, days=30):
        """生成监控报告"""
        stats = self.get_usage_stats(days)
        if not stats:
            return "无法生成报告：统计数据获取失败"
        
        report = []
        report.append("=" * 60)
        report.append("飞书团队管理器技能使用监控报告")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"监控周期: 最近{days}天")
        report.append("=" * 60)
        
        # 总体统计
        report.append("\n📊 总体统计")
        report.append(f"总使用次数: {stats['total_usage']}")
        if stats['monitoring_since']:
            report.append(f"监控开始时间: {stats['monitoring_since']}")
        
        # 事件分布
        report.append("\n📈 事件类型分布")
        for event_type, count in stats['event_distribution'].items():
            report.append(f"  {event_type}: {count}次")
        
        # 下载统计
        report.append("\n📥 下载统计")
        if stats['download_stats']:
            total_downloads = sum(row[1] for row in stats['download_stats'])
            total_users = sum(row[2] for row in stats['download_stats'])
            report.append(f"总下载次数: {total_downloads}")
            report.append(f"总独立用户: {total_users}")
            
            report.append("详细数据:")
            for date, count, users in stats['download_stats'][:10]:  # 显示最近10天
                report.append(f"  {date}: {count}次下载, {users}个用户")
        else:
            report.append("暂无下载数据")
        
        # 错误统计
        report.append("\n⚠ 错误统计")
        if stats['error_stats']:
            total_errors = sum(stats['error_stats'].values())
            report.append(f"总错误次数: {total_errors}")
            for error_type, count in stats['error_stats'].items():
                report.append(f"  {error_type}: {count}次")
        else:
            report.append("暂无错误记录")
        
        report.append("\n" + "=" * 60)
        report.append("报告结束")
        
        return "\n".join(report)
    
    def check_clawhub_stats(self):
        """检查ClawHub统计信息（需要API支持）"""
        # 这里可以集成ClawHub API来获取实际的下载量
        # 目前返回模拟数据
        return {
            'clawhub_downloads': '需要API集成',
            'clawhub_rating': '需要API集成',
            'clawhub_feedback': '需要API集成'
        }

def main():
    """主函数：演示监控功能"""
    monitor = SkillMonitor()
    
    # 演示：记录一些示例事件
    print("正在记录示例事件...")
    monitor.log_download(user_agent="test_user_1")
    monitor.log_usage('skill_activated', {'skill': 'feishu-team-manager', 'version': '2.3.1'})
    monitor.log_usage('recruit_called', {'agent_name': 'test_agent'})
    monitor.log_error('config_error', '配置文件格式错误', 'Traceback...')
    
    # 生成报告
    print("\n" + monitor.generate_report(days=7))
    
    # 显示数据库位置
    print(f"\n监控数据库位置: {monitor.db_path}")
    print("要查看实时统计，请定期运行此脚本。")

if __name__ == "__main__":
    main()