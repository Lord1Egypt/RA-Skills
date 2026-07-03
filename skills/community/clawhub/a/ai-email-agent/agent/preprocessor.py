"""
预处理器 — 去重、黑名单、垃圾过滤、自动通知检测
"""
import re
import hashlib
from datetime import datetime, timedelta
from .email_fetcher import EmailMessage
from .config_loader import get_config


class Preprocessor:
    """邮件预处理管道"""

    FILTER_REASONS = {
        "auto_submitted": "自动回复/系统通知",
        "blacklist_domain": "发件域在黑名单",
        "blacklist_keyword": "正文含垃圾关键词",
        "list_unsubscribe": "营销邮件",
        "duplicate_24h": "24h 内重复邮件",
        "empty_body": "空正文",
    }

    def __init__(self, config: dict = None):
        cfg = config or get_config()
        rules = cfg["rules"]
        self.blacklist_domains = set(rules.get("blacklist_domains", []))
        self.blacklist_keywords = [kw.lower() for kw in rules.get("blacklist_keywords", [])]
        # 24h 内已处理发件人缓存: {from_addr_lower: last_timestamp}
        self.recent_senders: dict[str, datetime] = {}

    def process(self, emails: list[EmailMessage]) -> tuple[list[EmailMessage], dict[str, list[EmailMessage]]]:
        """
        处理邮件列表，返回 (有效邮件, {过滤原因: 被过滤邮件列表})
        """
        valid = []
        filtered = {}

        for em in emails:
            reason = self._check_filters(em)
            if reason:
                filtered.setdefault(reason, []).append(em)
            else:
                valid.append(em)
                self._track_sender(em.from_addr)

        return valid, filtered

    def _check_filters(self, em: EmailMessage) -> str | None:
        """逐层过滤检查，返回过滤原因或 None"""

        # 1. 自动回复/系统通知检测
        if em.auto_submitted:
            return "auto_submitted"
        headers = em.raw_headers
        if headers.get("precedence", "").lower() in ("bulk", "junk", "list"):
            return "auto_submitted"

        # 2. 发件域黑名单
        sender_domain = em.from_addr.split("@")[-1].lower() if "@" in em.from_addr else ""
        if sender_domain in self.blacklist_domains:
            return "blacklist_domain"

        # 3. 营销邮件 (List-Unsubscribe)
        if headers.get("list-unsubscribe", ""):
            return "list_unsubscribe"

        # 4. 正文垃圾关键词
        body_lower = em.body_plain.lower()
        for kw in self.blacklist_keywords:
            if kw in body_lower:
                return "blacklist_keyword"

        # 5. 空正文
        if not em.body_plain.strip() and not em.body_html.strip():
            return "empty_body"

        # 6. 24h 内同发件人已处理过 (去重)
        sender_key = em.from_addr.lower()
        if sender_key in self.recent_senders:
            last_time = self.recent_senders[sender_key]
            if datetime.now() - last_time < timedelta(hours=24):
                return "duplicate_24h"

        return None

    def _track_sender(self, from_addr: str):
        """记录已处理的发件人"""
        self.recent_senders[from_addr.lower()] = datetime.now()

    @staticmethod
    def generate_fingerprint(em: EmailMessage) -> str:
        """生成邮件指纹 (用于去重) — Subject + From 的 hash"""
        raw = f"{em.from_addr.lower()}|{em.subject.strip()}"
        return hashlib.md5(raw.encode()).hexdigest()[:16]

    @staticmethod
    def extract_domain(email_addr: str) -> str:
        """提取邮箱域名"""
        return email_addr.split("@")[-1].lower() if "@" in email_addr else ""
