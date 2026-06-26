#!/usr/bin/env python3
"""
feishu_pusher.py — 飞书推送模块
推送摘要卡片到飞书，支持 webhook 或 user_id 推送
紧急邮件实时推送 + 每日定时摘要推送
"""

import json
import time
import hashlib
import hmac
import base64
import requests
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any


class FeishuPusher:
    """飞书推送模块"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化飞书推送器

        Args:
            config: 配置字典，包含 webhook 或 user_push 配置
        """
        self.config = config
        self.webhook_config = config.get("webhook", {})
        self.user_push_config = config.get("user_push", {})
        self.urgent_keywords = config.get("urgent_keywords", [
            "紧急", "urgent", "critical", "宕机", "故障", "p0", "p1"
        ])
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json; charset=utf-8"
        })

    # ─────────────────────────────────────────────────────────────
    # Webhook 推送
    # ─────────────────────────────────────────────────────────────

    def _sign(self, secret: str, timestamp: int) -> str:
        """
        生成飞书签名

        Args:
            secret: 签名密钥
            timestamp: 时间戳（毫秒）

        Returns:
            签名字符串
        """
        string_to_sign = f"{timestamp}\n{secret}"
        import codecs
        return base64.b64encode(
            hmac.new(
                codecs.encode(string_to_sign),
                digestmod=hashlib.sha256
            ).digest()
        ).decode("utf-8")

    def _build_webhook_payload(
        self,
        title: str,
        content: str,
        card_type: str = "interactive"
    ) -> Dict[str, Any]:
        """
        构建飞书卡片消息载荷

        Args:
            title: 卡片标题
            content: 卡片内容（支持富文本）
            card_type: 卡片类型

        Returns:
            消息载荷字典
        """
        # 飞书自适应卡片结构
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title
                    },
                    "template": self._get_card_template(title)
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": content
                        }
                    },
                    {
                        "tag": "hr"
                    },
                    {
                        "tag": "note",
                        "elements": [
                            {
                                "tag": "plain_text",
                                "content": f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} · 邮件客服助手"
                            }
                        ]
                    }
                ]
            }
        }
        return payload

    def _get_card_template(self, title: str) -> str:
        """根据标题关键词选择卡片颜色"""
        title_lower = title.lower()
        if any(kw in title_lower for kw in ["紧急", "critical", "urgent", "宕机", "故障"]):
            return "red"      # 红色
        elif any(kw in title_lower for kw in ["摘要", "digest", "日报"]):
            return "blue"     # 蓝色
        elif any(kw in title_lower for kw in ["回复", "reply"]):
            return "green"    # 绿色
        return "purple"       # 默认紫色

    def push_via_webhook(
        self,
        title: str,
        content: str,
        webhook_url: Optional[str] = None
    ) -> bool:
        """
        通过 Webhook 推送消息到飞书群

        Args:
            title: 卡片标题
            content: 卡片内容
            webhook_url: Webhook地址（不传则使用配置中的）

        Returns:
            是否推送成功
        """
        url = webhook_url or self.webhook_config.get("url")
        if not url:
            print("[FeishuPusher] ❌ 未配置 Webhook URL")
            return False

        payload = self._build_webhook_payload(title, content)

        # 如果配置了签名密钥
        secret = self.webhook_config.get("secret", "")
        if secret:
            timestamp = int(time.time() * 1000)
            sign = self._sign(secret, timestamp)
            url = f"{url}&timestamp={timestamp}&sign={sign}"

        try:
            resp = self.session.post(url, json=payload, timeout=10)
            result = resp.json()
            if result.get("code") == 0 or result.get("StatusCode") == 0:
                print(f"[FeishuPusher] ✅ Webhook推送成功: {title}")
                return True
            else:
                print(f"[FeishuPusher] ❌ Webhook推送失败: {result}")
                return False
        except Exception as e:
            print(f"[FeishuPusher] ❌ Webhook推送异常: {e}")
            return False

    # ─────────────────────────────────────────────────────────────
    # 用户推送（通过飞书开放平台 API）
    # ─────────────────────────────────────────────────────────────

    def push_to_user(
        self,
        user_id: str,
        title: str,
        content: str,
        app_token: Optional[str] = None
    ) -> bool:
        """
        通过用户ID推送消息到个人

        Args:
            user_id: 飞书用户 Open ID（ou_xxx）
            title: 消息标题
            content: 消息内容
            app_token: 飞书应用Token（不传则使用配置中的）

        Returns:
            是否推送成功
        """
        open_id = user_id or self.user_push_config.get("user_id")
        if not open_id:
            print("[FeishuPusher] ❌ 未配置用户ID")
            return False

        token = app_token or self.user_push_config.get("app_token")
        if not token:
            print("[FeishuPusher] ❌ 未配置 App Token")
            return False

        url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        payload = {
            "receive_id": open_id,
            "msg_type": "interactive",
            "content": json.dumps(self._build_webhook_payload(title, content)["card"])
        }

        try:
            resp = self.session.post(url, headers=headers, json=payload, timeout=10)
            result = resp.json()
            if result.get("code") == 0:
                print(f"[FeishuPusher] ✅ 用户推送成功: {open_id}")
                return True
            else:
                print(f"[FeishuPusher] ❌ 用户推送失败: {result}")
                return False
        except Exception as e:
            print(f"[FeishuPusher] ❌ 用户推送异常: {e}")
            return False

    # ─────────────────────────────────────────────────────────────
    # 邮件推送入口
    # ─────────────────────────────────────────────────────────────

    def is_urgent(self, email_data: Dict[str, Any]) -> bool:
        """
        判断邮件是否为紧急邮件

        Args:
            email_data: 邮件数据字典

        Returns:
            是否紧急
        """
        subject = email_data.get("subject", "").lower()
        body = email_data.get("body", "").lower()
        sender = email_data.get("sender", "").lower()

        text_to_check = f"{subject} {body} {sender}"
        return any(kw.lower() in text_to_check for kw in self.urgent_keywords)

    def push_email(
        self,
        email_data: Dict[str, Any],
        summary: str,
        category: str,
        reply_suggestion: Optional[str] = None,
        force_urgent: bool = False
    ) -> bool:
        """
        推送单封邮件摘要到飞书

        Args:
            email_data: 邮件数据
            summary: 摘要内容
            category: 分类结果
            reply_suggestion: 回复建议（可选）
            force_urgent: 是否强制标记为紧急

        Returns:
            是否推送成功
        """
        is_urgent_email = force_urgent or self.is_urgent(email_data)

        # 构建卡片内容
        urgent_tag = "🚨 紧急" if is_urgent_email else ""
        category_tag = f"📁 {category}" if category else ""

        content_lines = [
            f"**发件人：** {email_data.get('sender', '未知')}",
            f"**主题：** {email_data.get('subject', '无主题')}",
            f"**时间：** {email_data.get('date', '未知')}",
            f"{urgent_tag} {category_tag}",
            "",
            f"**摘要：**\n{summary}",
        ]

        if reply_suggestion:
            content_lines.extend([
                "",
                f"**💡 回复建议：**\n{reply_suggestion}"
            ])

        content = "\n".join(content_lines)
        title = f"{'🚨 紧急' if is_urgent_email else '📧'} 新邮件: {email_data.get('subject', '无主题')}"

        # 优先使用 webhook 推送
        if self.webhook_config.get("url"):
            return self.push_via_webhook(title, content)

        # 备选：用户推送
        if self.user_push_config.get("user_id"):
            return self.push_to_user(
                self.user_push_config["user_id"],
                title,
                content
            )

        print("[FeishuPusher] ❌ 未配置任何推送方式")
        return False

    # ─────────────────────────────────────────────────────────────
    # 每日摘要推送
    # ─────────────────────────────────────────────────────────────

    def push_daily_digest(
        self,
        emails: List[Dict[str, Any]],
        date: Optional[str] = None
    ) -> bool:
        """
        推送每日邮件摘要

        Args:
            emails: 邮件列表
            date: 日期字符串（默认今天）

        Returns:
            是否推送成功
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        urgent_count = sum(1 for e in emails if self.is_urgent(e))
        total_count = len(emails)

        # 按分类统计
        category_stats: Dict[str, int] = {}
        for e in emails:
            cat = e.get("category", "其他")
            category_stats[cat] = category_stats.get(cat, 0) + 1

        # 构建摘要内容
        content_parts = [
            f"**📊 {date} 邮件摘要报告**",
            "",
            f"- 总邮件数：{total_count}",
            f"- 🚨 紧急邮件：{urgent_count}",
            "",
            "**📁 分类统计：**"
        ]

        for cat, count in sorted(category_stats.items(), key=lambda x: -x[1]):
            content_parts.append(f"  - {cat}: {count} 封")

        content_parts.append("")
        content_parts.append("**📋 邮件列表：**")

        for i, email in enumerate(emails[:10], 1):  # 最多显示10封
            is_urg = self.is_urgent(email)
            urg_flag = "🚨" if is_urg else "  "
            content_parts.append(
                f"{urg_flag} **{i}. {email.get('subject', '无主题')}**\n"
                f"    发件人: {email.get('sender', '未知')} | "
                f"分类: {email.get('category', '其他')}"
            )

        if total_count > 10:
            content_parts.append(f"\n_...还有 {total_count - 10} 封邮件_")

        content = "\n".join(content_parts)
        title = f"📊 每日邮件摘要 · {date} · 共{total_count}封"

        if self.webhook_config.get("url"):
            return self.push_via_webhook(title, content)

        if self.user_push_config.get("user_id"):
            return self.push_to_user(
                self.user_push_config["user_id"],
                title,
                content
            )

        print("[FeishuPusher] ❌ 未配置任何推送方式")
        return False


# ─────────────────────────────────────────────────────────────────
# 独立运行测试
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import yaml

    print("=" * 60)
    print("飞书推送模块测试")
    print("=" * 60)

    # 尝试加载配置
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        feishu_cfg = config.get("feishu", {})
    except FileNotFoundError:
        print("⚠️  config.yaml 未找到，使用空配置测试")
        feishu_cfg = {}

    pusher = FeishuPusher(feishu_cfg)

    # 测试邮件数据
    test_email = {
        "sender": "customer@example.com",
        "subject": "【紧急】系统无法登录，请尽快处理",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "body": "我们的系统宕机了，所有用户都无法登录，请立即处理！",
        "category": "技术支持",
        "summary": "用户报告系统宕机，无法登录，需要紧急处理。"
    }

    # 测试紧急邮件推送
    print("\n📤 测试紧急邮件推送...")
    pusher.push_email(
        test_email,
        summary=test_email["summary"],
        category=test_email["category"],
        force_urgent=True
    )

    # 测试每日摘要推送
    print("\n📤 测试每日摘要推送...")
    pusher.push_daily_digest([test_email] * 3)

    print("\n✅ 测试完成")
