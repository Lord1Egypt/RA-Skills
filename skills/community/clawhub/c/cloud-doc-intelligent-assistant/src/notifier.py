"""通知发送模块"""

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import requests

from .models import ChangeReport, DocumentChange, Notification


class NotifierBase(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> bool:
        pass


class WebhookNotifier(NotifierBase):
    def __init__(self, url: str, retry_count: int = 3, timeout: int = 30):
        self.url = url
        self.retry_count = retry_count
        self.timeout = timeout

    def send(self, notification: Notification) -> bool:
        if not self.url:
            return False
        payload = {
            "title": notification.title,
            "summary": notification.summary,
            "timestamp": notification.timestamp.isoformat(),
            "changes_count": len(notification.changes),
            "metadata": notification.metadata,
        }
        for attempt in range(1, self.retry_count + 1):
            try:
                response = requests.post(self.url, json=payload, timeout=self.timeout,
                                         headers={"Content-Type": "application/json"})
                response.raise_for_status()
                return True
            except Exception as e:
                logging.error(f"Webhook 发送失败 (尝试 {attempt}/{self.retry_count}): {e}")
                if attempt < self.retry_count:
                    time.sleep(2 * attempt)
        return False


class AiflowNotifier(NotifierBase):
    def __init__(self, webhook_url: str, retry_count: int = 3, timeout: int = 30,
                 notify_users: List[str] = None):
        self.webhook_url = webhook_url
        self.retry_count = retry_count
        self.timeout = timeout
        # 默认为空列表，由配置文件指定通知用户
        self.notify_users = notify_users or []

    def _build_message_text(self, notification: Notification) -> str:
        lines = [f"📢 {notification.title}", "", f"📝 {notification.summary}", ""]
        if notification.changes:
            lines.append("📋 变更详情:")
            for i, change in enumerate(notification.changes[:5], 1):
                doc = change.document
                lines.append(f"  {i}. [{doc.title}]({doc.url})")
            if len(notification.changes) > 5:
                lines.append(f"  ... 还有 {len(notification.changes) - 5} 条变更")
        if notification.metadata:
            meta = notification.metadata
            lines.append(f"")
            lines.append(f"📊 统计: 新增 {meta.get('added_count', 0)}, 修改 {meta.get('modified_count', 0)}, 删除 {meta.get('deleted_count', 0)}")
        return "\n".join(lines)

    def send(self, notification: Notification) -> bool:
        if not self.webhook_url:
            return False
        text = self._build_message_text(notification)
        for attempt in range(1, self.retry_count + 1):
            all_success = True
            for user in self.notify_users:
                try:
                    response = requests.post(
                        self.webhook_url,
                        data={"user": user, "text": text},
                        timeout=self.timeout,
                    )
                    response.raise_for_status()
                except Exception as e:
                    logging.error(f"aiflow 发送给 {user} 失败 (尝试 {attempt}/{self.retry_count}): {e}")
                    all_success = False
            if all_success:
                return True
            if attempt < self.retry_count:
                time.sleep(2 * attempt)
        return False


class RuliuNotifier(NotifierBase):
    def __init__(self, webhook_url: str, retry_count: int = 3, timeout: int = 30):
        self.webhook_url = webhook_url
        self.retry_count = retry_count
        self.timeout = timeout

    def _build_markdown_content(self, notification: Notification) -> str:
        lines = [
            f"## {notification.title}",
            f"**时间**: {notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "### 变更摘要",
            notification.summary,
            "",
        ]
        if notification.changes:
            lines.append("### 变更详情")
            for i, change in enumerate(notification.changes[:10], 1):
                doc = change.document
                lines.append(f"{i}. [{doc.title}]({doc.url})")
            if len(notification.changes) > 10:
                lines.append(f"\n... 还有 {len(notification.changes) - 10} 条变更")
        return "\n".join(lines)

    def send(self, notification: Notification) -> bool:
        if not self.webhook_url:
            return False
        markdown_content = self._build_markdown_content(notification)
        payload = {
            "msgtype": "markdown",
            "markdown": {"title": notification.title, "text": markdown_content},
        }
        for attempt in range(1, self.retry_count + 1):
            try:
                response = requests.post(self.webhook_url, json=payload, timeout=self.timeout,
                                         headers={"Content-Type": "application/json"})
                response.raise_for_status()
                result = response.json()
                if result.get("errcode") == 0:
                    return True
                logging.error(f"如流机器人返回错误: {result}")
            except Exception as e:
                logging.error(f"如流机器人发送失败 (尝试 {attempt}/{self.retry_count}): {e}")
                if attempt < self.retry_count:
                    time.sleep(2 * attempt)
        return False


class FileNotifier(NotifierBase):
    def __init__(self, output_dir: str = "./notifications"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def send(self, notification: Notification) -> bool:
        try:
            timestamp = notification.timestamp.strftime("%Y%m%d_%H%M%S")
            filepath = self.output_dir / f"notification_{timestamp}.md"
            content = self._format_notification(notification)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            logging.info(f"通知已保存到文件: {filepath}")
            return True
        except Exception as e:
            logging.error(f"文件通知保存失败: {e}")
            return False

    def _format_notification(self, notification: Notification) -> str:
        lines = [
            f"# {notification.title}",
            f"\n**生成时间**: {notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"\n## 摘要\n\n{notification.summary}",
            "\n## 变更详情\n",
        ]
        if notification.changes:
            for i, change in enumerate(notification.changes, 1):
                doc = change.document
                lines.append(f"### {i}. {doc.title}")
                lines.append(f"\n- **URL**: {doc.url}")
                lines.append(f"- **变更类型**: {change.change_type.value}")
                lines.append(f"\n**Diff 摘要**:\n```diff\n{change.diff[:1000]}\n```\n")
        else:
            lines.append("无详细变更记录")
        return "\n".join(lines)


class NotificationManager:
    def __init__(self, config: Dict[str, Any]):
        self.notifiers: List[NotifierBase] = []
        self._init_notifiers(config)

    def _init_notifiers(self, config: Dict[str, Any]) -> None:
        for notifier_config in config.get("notifications", []):
            if not notifier_config.get("enabled", True):
                continue
            notifier_type = notifier_config.get("type", "")
            if notifier_type == "webhook":
                self.notifiers.append(WebhookNotifier(
                    url=notifier_config.get("url", ""),
                    retry_count=notifier_config.get("retry_count", 3),
                ))
            elif notifier_type == "aiflow":
                self.notifiers.append(AiflowNotifier(
                    webhook_url=notifier_config.get("webhook_url", ""),
                    retry_count=notifier_config.get("retry_count", 3),
                    notify_users=notifier_config.get("notify_users", []),
                ))
            elif notifier_type == "ruliu":
                self.notifiers.append(RuliuNotifier(
                    webhook_url=notifier_config.get("webhook_url", ""),
                    retry_count=notifier_config.get("retry_count", 3),
                ))
            elif notifier_type == "file":
                self.notifiers.append(FileNotifier(
                    output_dir=notifier_config.get("output_dir", "./notifications"),
                ))

    def send_all(self, notification: Notification) -> Dict[str, bool]:
        results = {}
        for notifier in self.notifiers:
            name = notifier.__class__.__name__
            try:
                results[name] = notifier.send(notification)
            except Exception as e:
                logging.error(f"{name} 发送异常: {e}")
                results[name] = False
        return results

    def notify_changes(self, report: ChangeReport, summary: str) -> Dict[str, bool]:
        total_changes = len(report.added) + len(report.modified) + len(report.deleted)
        title = (
            f"云文档监控报告 - 检测到 {total_changes} 个变更"
            if total_changes > 0
            else "云文档监控报告 - 定时检查完成"
        )
        notification = Notification(
            title=title,
            summary=summary,
            changes=report.modified,
            timestamp=report.timestamp,
            metadata={
                "added_count": len(report.added),
                "modified_count": len(report.modified),
                "deleted_count": len(report.deleted),
            },
        )
        return self.send_all(notification)
