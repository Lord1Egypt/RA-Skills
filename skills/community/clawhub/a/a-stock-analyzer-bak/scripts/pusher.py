#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析报告推送模块
支持飞书、钉钉、企业微信
"""

import json
import requests
from pathlib import Path


class ReportPusher:
    """报告推送器"""
    
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.json"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.push_config = self.config.get('push', {})
        self.enabled = self.push_config.get('enabled', False)
    
    def send_to_feishu(self, message, webhook=None):
        """发送到飞书"""
        if not webhook:
            webhook = self.push_config.get('feishu_webhook')
        
        if not webhook:
            print("⚠️ 未配置飞书Webhook")
            return False
        
        try:
            # 构建飞书消息卡片
            card = {
                "msg_type": "interactive",
                "card": {
                    "header": {
                        "title": {
                            "tag": "plain_text",
                            "content": "📈 A股分析报告"
                        },
                        "template": "blue"
                    },
                    "elements": [
                        {
                            "tag": "div",
                            "text": {
                                "tag": "lark_md",
                                "content": message
                            }
                        }
                    ]
                }
            }
            
            response = requests.post(webhook, json=card, timeout=10)
            
            if response.status_code == 200:
                print("✅ 飞书推送成功")
                return True
            else:
                print(f"❌ 飞书推送失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 飞书推送异常: {e}")
            return False
    
    def send_to_dingtalk(self, message, webhook=None):
        """发送到钉钉"""
        if not webhook:
            webhook = self.push_config.get('dingtalk_webhook')
        
        if not webhook:
            print("⚠️ 未配置钉钉Webhook")
            return False
        
        try:
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": "A股分析报告",
                    "text": message
                }
            }
            
            response = requests.post(webhook, json=data, timeout=10)
            
            if response.status_code == 200:
                print("✅ 钉钉推送成功")
                return True
            else:
                print(f"❌ 钉钉推送失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 钉钉推送异常: {e}")
            return False
    
    def send_report(self, report_content, title="A股分析报告"):
        """发送报告"""
        if not self.enabled:
            print("推送功能未启用")
            return False
        
        channels = self.push_config.get('channels', [])
        
        # 转换markdown格式
        message = f"## {title}\n\n{report_content}"
        
        success = False
        for channel in channels:
            if channel == 'feishu':
                if self.send_to_feishu(message):
                    success = True
            elif channel == 'dingtalk':
                if self.send_to_dingtalk(message):
                    success = True
        
        return success


if __name__ == '__main__':
    # 测试推送
    pusher = ReportPusher()
    pusher.send_report("测试消息", "测试")
