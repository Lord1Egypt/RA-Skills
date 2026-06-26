#!/usr/bin/env python3
"""
FocusMind 通知模块
支持多种通知方式
"""

import os
import json
import urllib.request
import urllib.error
from typing import Any, Dict, Optional, List
from dataclasses import dataclass
from enum import Enum


class NotificationType(Enum):
    """通知类型"""
    WEBHOOK = "webhook"
    CONSOLE = "console"
    FILE = "file"


@dataclass
class WebhookConfig:
    """Webhook 配置"""
    url: str
    method: str = "POST"
    headers: Dict[str, str] = None
    
    def __post_init__(self):
        if self.headers is None:
            self.headers = {"Content-Type": "application/json"}


@dataclass
class NotificationConfig:
    """通知配置"""
    enabled: bool = True
    notification_type: NotificationType = NotificationType.CONSOLE
    webhook: Optional[WebhookConfig] = None
    file_path: Optional[str] = None


class Notifier:
    """
    通知器
    
    支持 webhook、console、file 三种通知方式
    """
    
    def __init__(self, config: Optional[NotificationConfig] = None):
        self.config = config or NotificationConfig()
    
    def notify(self, title: str, message: str, data: Optional[Dict] = None):
        """
        发送通知
        
        Args:
            title: 通知标题
            message: 通知消息
            data: 附加数据
        """
        if not self.config.enabled:
            return
        
        payload = {
            "title": title,
            "message": message,
            "data": data or {}
        }
        
        if self.config.notification_type == NotificationType.WEBHOOK:
            self._send_webhook(payload)
        elif self.config.notification_type == NotificationType.CONSOLE:
            self._send_console(payload)
        elif self.config.notification_type == NotificationType.FILE:
            self._send_file(payload)
    
    def _send_webhook(self, payload: Dict):
        """发送 Webhook"""
        if not self.config.webhook:
            return
        
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                self.config.webhook.url,
                data=data,
                headers=self.config.webhook.headers,
                method=self.config.webhook.method
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                print(f"✓ Webhook 发送成功: {response.status}")
        except urllib.error.URLError as e:
            print(f"❌ Webhook 发送失败: {e}")
        except Exception as e:
            print(f"❌ Webhook 错误: {e}")
    
    def _send_console(self, payload: Dict):
        """发送控制台通知"""
        print(f"\n{'='*50}")
        print(f"🔔 {payload['title']}")
        print(f"{'='*50}")
        print(payload['message'])
        if payload.get('data'):
            print(f"\n数据: {json.dumps(payload['data'], ensure_ascii=False, indent=2)}")
        print(f"{'='*50}\n")
    
    def _send_file(self, payload: Dict):
        """发送文件通知"""
        if not self.config.file_path:
            return
        
        try:
            with open(self.config.file_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")
            print(f"✓ 已写入文件: {self.config.file_path}")
        except Exception as e:
            print(f"❌ 文件写入失败: {e}")
    
    def notify_cleanup_needed(self, health: Dict[str, Any], recommendations: List[str]):
        """通知需要清理"""
        self.notify(
            title="🧠 FocusMind: 需要清理脑雾",
            message=f"上下文健康度: {health['emoji']} {health['score']}/100 ({health['label']})\n" +
                    f"\n建议:\n" + "\n".join(f"• {r}" for r in recommendations),
            data=health
        )
    
    def notify_cleanup_complete(self, summary: Dict[str, Any], goals: Dict[str, Any]):
        """通知清理完成"""
        self.notify(
            title="✅ FocusMind: 清理完成",
            message=f"摘要已生成，包含 {len(goals.get('sub_goals', []))} 个子目标",
            data={"summary": summary, "goals": goals}
        )


# 便捷函数

def create_webhook_notifier(url: str) -> Notifier:
    """创建 Webhook 通知器"""
    config = NotificationConfig(
        enabled=True,
        notification_type=NotificationType.WEBHOOK,
        webhook=WebhookConfig(url=url)
    )
    return Notifier(config)


def create_console_notifier() -> Notifier:
    """创建控制台通知器"""
    config = NotificationConfig(
        enabled=True,
        notification_type=NotificationType.CONSOLE
    )
    return Notifier(config)


# 导出
__all__ = ["Notifier", "NotificationConfig", "WebhookConfig", "NotificationType",
           "create_webhook_notifier", "create_console_notifier"]
