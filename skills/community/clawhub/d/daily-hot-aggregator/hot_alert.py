#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点预警工具 v1.0 - 检测热榜话题变化并预警
作者: 小天🦞
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional
from pathlib import Path

# 设置控制台编码
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class HotAlert:
    """热点预警器"""

    def __init__(self, data_dir: str = 'hot_reports', config_file: str = 'alert_config.json'):
        self.data_dir = data_dir
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """加载配置"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'keywords': [],  # 监控关键词
            'threshold': 1000000,  # 热度阈值（100万）
            'new_entry_alert': True,  # 新上榜预警
            'rank_jump_alert': True,  # 排名飙升预警
            'enabled': True
        }

    def save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def load_report(self, date_str: str) -> Optional[Dict]:
        """加载指定日期的报告"""
        filepath = os.path.join(self.data_dir, f'daily_report_{date_str}.json')
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_today_titles(self, data: Dict) -> Dict[str, List[Dict]]:
        """获取今日各平台标题"""
        result = {}
        for platform in ['bilibili', 'douyin', 'weibo', 'toutiao']:
            items = data.get('data', {}).get(platform, [])
            result[platform] = items
        return result

    def detect_new_entries(self, today_data: Dict, yesterday_data: Optional[Dict]) -> List[Dict]:
        """检测新上榜话题"""
        alerts = []
        
        if not yesterday_data:
            return alerts
        
        for platform in ['bilibili', 'douyin', 'weibo', 'toutiao']:
            today_items = today_data.get('data', {}).get(platform, [])
            yesterday_items = yesterday_data.get('data', {}).get(platform, [])
            
            # 提取昨天标题
            yesterday_titles = {item.get('title', '') for item in yesterday_items}
            
            # 检测新上榜
            for item in today_items:
                title = item.get('title', '')
                if title and title not in yesterday_titles:
                    alerts.append({
                        'type': 'new_entry',
                        'platform': platform,
                        'title': title,
                        'value': item.get('value', item.get('hot_value', 0)),
                        'value_text': item.get('value_text', ''),
                        'rank': item.get('rank', 0)
                    })
        
        return alerts

    def detect_keyword_match(self, data: Dict) -> List[Dict]:
        """检测关键词匹配"""
        alerts = []
        keywords = self.config.get('keywords', [])
        
        if not keywords:
            return alerts
        
        for platform in ['bilibili', 'douyin', 'weibo', 'toutiao']:
            items = data.get('data', {}).get(platform, [])
            
            for item in items:
                title = item.get('title', '')
                for keyword in keywords:
                    if keyword in title:
                        alerts.append({
                            'type': 'keyword_match',
                            'platform': platform,
                            'keyword': keyword,
                            'title': title,
                            'value': item.get('value', item.get('hot_value', 0)),
                            'value_text': item.get('value_text', '')
                        })
        
        return alerts

    def detect_high_heat(self, data: Dict) -> List[Dict]:
        """检测高热度话题"""
        alerts = []
        threshold = self.config.get('threshold', 1000000)
        
        for platform in ['bilibili', 'douyin', 'weibo', 'toutiao']:
            items = data.get('data', {}).get(platform, [])
            
            for item in items:
                value = item.get('value', item.get('hot_value', 0))
                if value >= threshold:
                    alerts.append({
                        'type': 'high_heat',
                        'platform': platform,
                        'title': item.get('title', ''),
                        'value': value,
                        'value_text': item.get('value_text', ''),
                        'threshold': threshold
                    })
        
        return alerts

    def run_detection(self, date_str: str = None) -> List[Dict]:
        """运行预警检测"""
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 加载今日数据
        today_data = self.load_report(date_str)
        if not today_data:
            return []
        
        # 加载昨日数据
        yesterday = (datetime.strptime(date_str, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
        yesterday_data = self.load_report(yesterday)
        
        all_alerts = []
        
        # 检测新上榜
        if self.config.get('new_entry_alert', True):
            all_alerts.extend(self.detect_new_entries(today_data, yesterday_data))
        
        # 检测关键词匹配
        all_alerts.extend(self.detect_keyword_match(today_data))
        
        # 检测高热度
        if self.config.get('rank_jump_alert', True):
            all_alerts.extend(self.detect_high_heat(today_data))
        
        return all_alerts

    def format_alert(self, alert: Dict) -> str:
        """格式化预警消息"""
        platform_names = {
            'bilibili': 'B站',
            'douyin': '抖音',
            'weibo': '微博',
            'toutiao': '头条'
        }
        
        platform = platform_names.get(alert['platform'], alert['platform'])
        
        if alert['type'] == 'new_entry':
            return f"🆕 新上榜 | {platform}: {alert['title']} ({alert['value_text']})"
        elif alert['type'] == 'keyword_match':
            return f"🔍 关键词 | {platform}: [{alert['keyword']}] {alert['title']}"
        elif alert['type'] == 'high_heat':
            return f"🔥 高热度 | {platform}: {alert['title']} ({alert['value_text']})"
        else:
            return f"⚠️ 预警 | {platform}: {alert['title']}"

    def add_keyword(self, keyword: str):
        """添加监控关键词"""
        if keyword not in self.config['keywords']:
            self.config['keywords'].append(keyword)
            self.save_config()

    def remove_keyword(self, keyword: str):
        """移除监控关键词"""
        if keyword in self.config['keywords']:
            self.config['keywords'].remove(keyword)
            self.save_config()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='🔥 热点预警工具 v1.0')
    parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='检测日期')
    parser.add_argument('--add-keyword', type=str, help='添加监控关键词')
    parser.add_argument('--remove-keyword', type=str, help='移除监控关键词')
    parser.add_argument('--list-keywords', action='store_true', help='列出所有关键词')
    parser.add_argument('--set-threshold', type=int, help='设置热度阈值')
    
    args = parser.parse_args()
    
    alert = HotAlert()
    
    if args.add_keyword:
        alert.add_keyword(args.add_keyword)
        print(f"✅ 已添加关键词: {args.add_keyword}")
    
    elif args.remove_keyword:
        alert.remove_keyword(args.remove_keyword)
        print(f"✅ 已移除关键词: {args.remove_keyword}")
    
    elif args.list_keywords:
        print("\n📋 监控关键词：")
        for kw in alert.config.get('keywords', []):
            print(f"  - {kw}")
        print(f"\n🔥 热度阈值: {alert.config.get('threshold', 1000000)}")
    
    elif args.set_threshold:
        alert.config['threshold'] = args.set_threshold
        alert.save_config()
        print(f"✅ 已设置热度阈值: {args.set_threshold}")
    
    else:
        # 运行检测
        alerts = alert.run_detection(args.date)
        if alerts:
            print(f"\n🔔 {args.date} 预警 ({len(alerts)} 条)：")
            for a in alerts:
                print(f"  {alert.format_alert(a)}")
        else:
            print(f"\n✅ {args.date} 无预警")


if __name__ == '__main__':
    main()
