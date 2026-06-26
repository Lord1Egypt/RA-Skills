"""
通用 Webhook 渠道推送实现
通过 HTTP POST 请求发送到自定义 Webhook URL
"""

import json
import requests
import sys
import os
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import BaseChannel


class WebhookChannel(BaseChannel):
    """通用 Webhook 推送渠道"""
    
    def __init__(self, webhook_url: str, headers: dict = None):
        """
        初始化
        
        Args:
            webhook_url: Webhook URL
            headers: 自定义请求头（可选）
        """
        self.webhook_url = webhook_url
        self.headers = headers or {"Content-Type": "application/json"}
        
    def get_name(self) -> str:
        return "Webhook"
    
    def send(self, content: str, title: str = None) -> bool:
        """
        通过 POST 请求发送到 Webhook
        
        请求体格式：
        {
            "text": "早报内容",
            "title": "AI早报 | YYYY.MM.DD",
            "date": "YYYY-MM-DD",
            "timestamp": 1234567890
        }
        """
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            if not title:
                title = f"AI早报 | {today}"
            
            payload = {
                "text": content,
                "title": title,
                "date": today,
                "timestamp": int(datetime.now().timestamp())
            }
            
            response = requests.post(
                self.webhook_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code >= 200 and response.status_code < 300:
                print(f"[INFO] Webhook 发送成功，状态码: {response.status_code}")
                return True
            else:
                print(f"[ERROR] Webhook 发送失败，状态码: {response.status_code}, 响应: {response.text}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Webhook 发送异常: {e}")
            return False
