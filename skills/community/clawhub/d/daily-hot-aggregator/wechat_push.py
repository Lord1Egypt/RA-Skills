#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热榜企微推送工具 v1.0
作者: 小天🦞
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# 设置控制台编码
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class WeChatPusher:
    """企微推送器"""

    def __init__(self, config_file: str = 'wechat_push_config.json'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """加载配置"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'groups': [],  # 群聊配置列表
            'push_time': '09:00',
            'enabled': True
        }

    def save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def add_group(self, group_id: str, group_name: str, platforms: List[str] = None):
        """添加推送群"""
        if platforms is None:
            platforms = ['bilibili', 'douyin', 'weibo', 'toutiao']
        
        self.config['groups'].append({
            'group_id': group_id,
            'group_name': group_name,
            'platforms': platforms,
            'enabled': True
        })
        self.save_config()

    def remove_group(self, group_id: str):
        """移除推送群"""
        self.config['groups'] = [g for g in self.config['groups'] if g['group_id'] != group_id]
        self.save_config()

    def format_hot_list(self, data: Dict, platform: str, top_n: int = 5) -> str:
        """格式化热榜数据"""
        platform_names = {
            'bilibili': '📺 B站热门',
            'douyin': '🎵 抖音热搜',
            'weibo': '🔍 微博热搜',
            'toutiao': '📰 今日头条'
        }
        
        items = data.get('data', {}).get(platform, [])
        if not items:
            return ''
        
        lines = [f"\n{platform_names.get(platform, platform)} Top {top_n}:"]
        for i, item in enumerate(items[:top_n], 1):
            title = item.get('title', '')
            value = item.get('value_text', item.get('hot_value', ''))
            label = item.get('label_name', item.get('label', ''))
            label_str = f' [{label}]' if label else ''
            lines.append(f"  #{i} {title}{label_str} ({value})")
        
        return '\n'.join(lines)

    def generate_daily_report(self, data: Dict, platforms: List[str] = None, top_n: int = 5) -> str:
        """生成每日热榜报告（纯文本格式）"""
        if platforms is None:
            platforms = ['bilibili', 'douyin', 'weibo', 'toutiao']
        
        date_str = data.get('date', datetime.now().strftime('%Y-%m-%d %H:%M'))
        
        report = f"🔥 全平台热榜日报\n📅 {date_str}\n"
        report += "=" * 30
        
        for platform in platforms:
            content = self.format_hot_list(data, platform, top_n)
            if content:
                report += content + '\n'
        
        report += "\n" + "=" * 30
        report += "\n🦞 Powered by OpenClaw"
        
        return report

    def generate_markdown_report(self, data: Dict, platforms: List[str] = None, top_n: int = 5) -> str:
        """生成每日热榜报告（Markdown 格式）"""
        if platforms is None:
            platforms = ['bilibili', 'douyin', 'weibo', 'toutiao']
        
        date_str = data.get('date', datetime.now().strftime('%Y-%m-%d %H:%M'))
        
        platform_config = {
            'bilibili': {'name': '📺 B站热门', 'rank_col': '播放量'},
            'douyin': {'name': '🎵 抖音热搜', 'rank_col': '热度'},
            'weibo': {'name': '🔍 微博热搜', 'rank_col': '热度'},
            'toutiao': {'name': '📰 今日头条', 'rank_col': '热度'}
        }
        
        report = f"# 🔥 全平台热榜日报\n> 📅 {date_str} | 数据来源：B站、抖音、微博、头条\n\n---\n"
        
        for platform in platforms:
            items = data.get('data', {}).get(platform, [])
            if not items:
                continue
            
            config = platform_config.get(platform, {'name': platform, 'rank_col': '热度'})
            report += f"\n## {config['name']} Top {top_n}\n"
            report += f"| 排名 | 标题 | {config['rank_col']} |\n"
            report += "|:---:|------|------|\n"
            
            rank_icons = ['🥇', '🥈', '🥉']
            for i, item in enumerate(items[:top_n], 1):
                title = item.get('title', '')
                # 截断过长标题
                if len(title) > 25:
                    title = title[:24] + '...'
                
                value = item.get('value_text', item.get('hot_value', ''))
                label = item.get('label_name', item.get('label', ''))
                
                # 排名图标
                if i <= 3:
                    rank = rank_icons[i-1]
                elif label == '热':
                    rank = '🔥' + str(i)
                elif label == '新':
                    rank = '🆕' + str(i)
                else:
                    rank = str(i)
                
                report += f"| {rank} | {title} | {value} |\n"
            
            report += "\n---\n"
        
        report += "\n> 🦞 **Powered by OpenClaw**"
        
        return report

    def generate_alert(self, keyword: str, platform: str, item: Dict) -> str:
        """生成热点预警消息"""
        title = item.get('title', '')
        value = item.get('value_text', item.get('hot_value', ''))
        
        return f"""🔥 热点预警！

📌 关键词：{keyword}
📊 平台：{platform}
📢 话题：{title}
🔥 热度：{value}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}
🦞 Powered by OpenClaw"""

    def send_webhook(self, webhook_url: str, message: str, msg_type: str = 'markdown') -> bool:
        """通过 webhook 发送消息"""
        import urllib.request
        
        if msg_type == 'markdown':
            data = {
                'msgtype': 'markdown',
                'markdown': {'content': message}
            }
        else:
            data = {
                'msgtype': 'text',
                'text': {'content': message}
            }
        
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                return result.get('errcode') == 0
        except Exception as e:
            print(f"发送失败: {e}")
            return False

    def send_to_all_groups(self, message: str) -> int:
        """发送到所有启用的群"""
        success_count = 0
        for group in self.config.get('groups', []):
            if group.get('enabled') and group.get('webhook'):
                if self.send_webhook(group['webhook'], message):
                    success_count += 1
        return success_count


def main():
    import argparse
    parser = argparse.ArgumentParser(description='💬 热榜企微推送工具 v1.0')
    parser.add_argument('--add-group', nargs=3, metavar=('GROUP_ID', 'GROUP_NAME', 'PLATFORMS'),
                       help='添加推送群 (PLATFORMS用逗号分隔)')
    parser.add_argument('--remove-group', type=str, help='移除推送群')
    parser.add_argument('--list-groups', action='store_true', help='列出所有群')
    parser.add_argument('--test', type=str, help='测试推送 (指定群ID)')
    
    args = parser.parse_args()
    
    pusher = WeChatPusher()
    
    if args.add_group:
        group_id, group_name, platforms_str = args.add_group
        platforms = platforms_str.split(',')
        pusher.add_group(group_id, group_name, platforms)
        print(f"✅ 已添加群: {group_name} ({group_id})")
    
    elif args.remove_group:
        pusher.remove_group(args.remove_group)
        print(f"✅ 已移除群: {args.remove_group}")
    
    elif args.list_groups:
        print("\n📋 推送群列表：")
        for g in pusher.config.get('groups', []):
            status = '✅' if g.get('enabled') else '❌'
            platforms = ', '.join(g.get('platforms', []))
            print(f"  {status} {g['group_name']} ({g['group_id']}) - {platforms}")
    
    elif args.test:
        # 测试生成报告
        test_data = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'data': {
                'bilibili': [{'title': '测试视频1', 'value_text': '100万播放'}, {'title': '测试视频2', 'value_text': '50万播放'}],
                'weibo': [{'title': '测试热搜1', 'value_text': '100万热度', 'label_name': '热'}]
            }
        }
        report = pusher.generate_daily_report(test_data, ['bilibili', 'weibo'], 2)
        print("\n📝 测试报告：")
        print(report)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
