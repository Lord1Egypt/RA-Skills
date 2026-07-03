"""
升级引擎 — 人工介入判断 + 多渠道通知
"""
import json
import requests
from datetime import datetime
from typing import Optional

from .config_loader import get_config
from .classifier import ClassificationResult
from .email_fetcher import EmailMessage
from .urgency import UrgencyResult


class EscalationEngine:
    """升级决策与通知引擎"""

    ESCALATION_RULES = [
        # (条件函数, 升级级别, 原因, SLA)
        ("extreme_sentiment", "P0", "客户情绪极端愤怒 (S3/S4)", 30),
        ("urgency_critical", "P0", "紧急度评分 ≥ 4", 60),
        ("legal_threat", "P0", "检测到法律威胁关键词", 15),
        ("safety_issue", "P0", "产品安全隐患", 15),
        ("social_threat", "P1", "社交媒体扩散威胁", 60),
        ("repeat_contact_5", "P1", "24h 内第 5+ 封邮件", 120),
        ("repeat_contact_3", "P1", "24h 内第 3+ 封未解决邮件", 120),
        ("high_value_order", "P1", "大额订单 (>$1000) + 投诉/退换货", 120),
        ("low_confidence", "P2", "LLM 分类置信度 < 0.7", 240),
        ("cooperation_cat", "P2", "商务合作类邮件", 1440),
        ("reply_loop_3", "P1", "自动回复 3 轮后客户仍回复", 60),
    ]

    def __init__(self, config: dict = None, ticket_db=None):
        cfg = config or get_config()
        self.rules = cfg.get("rules", {})
        esc_cfg = cfg.get("escalation", {})
        self.wecom_webhook = esc_cfg.get("notification_channels", {}).get("wecom_webhook", "")
        self.feishu_webhook = esc_cfg.get("notification_channels", {}).get("feishu_webhook", "")
        self.sms_enabled = esc_cfg.get("notification_channels", {}).get("sms_enabled", False)
        self.sla = esc_cfg.get("sla", {})
        self.ticket_db = ticket_db

    def evaluate(
        self,
        email: EmailMessage,
        classification: ClassificationResult,
        urgency: UrgencyResult,
        ticket_id: str = "",
    ) -> dict:
        """
        评估是否需要升级
        返回 {"should_escalate": bool, "level": str, "reason": str, "sla_minutes": int}
        """
        # 检查每条升级规则
        for rule_func, level, reason, sla in self.ESCALATION_RULES:
            if getattr(self, f"_check_{rule_func}")(email, classification, urgency):
                return {
                    "should_escalate": True,
                    "level": level,
                    "reason": reason,
                    "sla_minutes": sla,
                }

        return {"should_escalate": False, "level": "", "reason": "", "sla_minutes": 0}

    def notify(self, email: EmailMessage, classification: ClassificationResult,
               urgency: UrgencyResult, ticket_id: str, level: str, reason: str):
        """发送升级通知"""
        message = self._build_notification(email, classification, urgency, ticket_id, level, reason)

        # 企微通知
        if self.wecom_webhook and level in ("P0", "P1"):
            self._send_wecom(message, level)

        # 飞书通知
        if self.feishu_webhook and level in ("P0",):
            self._send_feishu(message)

        print(f"[ESCALATE] {level} | {ticket_id} | {reason}")

    def _build_notification(self, email, classification, urgency, ticket_id, level, reason) -> str:
        """构建通知消息"""
        level_emoji = {"P0": "🔴", "P1": "🟠", "P2": "🟡"}

        return f"""{level_emoji.get(level, '🔵')} {level} 紧急升级 — 邮件工单 #{ticket_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【客户】 {email.from_name} <{email.from_addr}>
【分类】 {classification.category} — {classification.summary}
【情感】 {classification.sentiment} ({classification.sentiment_score:+.2f})
【紧急度】 {urgency.level}/5 ({urgency.level_label})
【摘要】 {classification.summary}
【订单】 {classification.entities.get('order_id', 'N/A')}
【升级原因】 {reason}
【SLA 倒计时】 {urgency.sla_minutes} 分钟
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    def _send_wecom(self, message: str, level: str):
        """发送企业微信通知"""
        if not self.wecom_webhook:
            return
        try:
            # 企微 Markdown 消息格式
            payload = {
                "msgtype": "markdown",
                "markdown": {"content": message.replace("\n", "\n> ")},
            }
            requests.post(self.wecom_webhook, json=payload, timeout=10)
        except Exception as e:
            print(f"[WARN] 企微通知发送失败: {e}")

    def _send_feishu(self, message: str):
        """发送飞书通知"""
        if not self.feishu_webhook:
            return
        try:
            payload = {
                "msg_type": "text",
                "content": {"text": message},
            }
            requests.post(self.feishu_webhook, json=payload, timeout=10)
        except Exception as e:
            print(f"[WARN] 飞书通知发送失败: {e}")

    # ===== 升级条件检查函数 =====

    def _check_extreme_sentiment(self, email, classification, urgency) -> bool:
        return classification.sentiment in ("angry",)

    def _check_urgency_critical(self, email, classification, urgency) -> bool:
        return urgency.level >= 4

    def _check_legal_threat(self, email, classification, urgency) -> bool:
        legal_kws = self.rules.get("legal_keywords", [])
        body = email.body_plain.lower()
        return any(kw.lower() in body for kw in legal_kws)

    def _check_safety_issue(self, email, classification, urgency) -> bool:
        safety_kws = self.rules.get("safety_keywords", [])
        body = email.body_plain.lower()
        return any(kw.lower() in body for kw in safety_kws)

    def _check_social_threat(self, email, classification, urgency) -> bool:
        social_kws = self.rules.get("social_threat_keywords", [])
        body = email.body_plain.lower()
        return any(kw.lower() in body for kw in social_kws)

    def _check_repeat_contact_5(self, email, classification, urgency) -> bool:
        if self.ticket_db:
            return self.ticket_db.get_recent_email_count(email.from_addr, hours=24) >= 5
        return False

    def _check_repeat_contact_3(self, email, classification, urgency) -> bool:
        if self.ticket_db:
            count = self.ticket_db.get_recent_email_count(email.from_addr, hours=24)
            return 3 <= count < 5
        return False

    def _check_high_value_order(self, email, classification, urgency) -> bool:
        try:
            amount = float(classification.entities.get("amount", 0))
        except (ValueError, TypeError):
            return False
        return amount > 1000 and classification.category in ("complaint", "return_refund")

    def _check_low_confidence(self, email, classification, urgency) -> bool:
        return classification.confidence < 0.7

    def _check_cooperation_cat(self, email, classification, urgency) -> bool:
        return classification.category == "cooperation"

    def _check_reply_loop_3(self, email, classification, urgency) -> bool:
        if self.ticket_db:
            return self.ticket_db.get_reply_rounds(email.from_addr) >= 3
        return False
