"""
紧急度评分引擎 — 多维度加权评分算法
"""
from dataclasses import dataclass
from .classifier import ClassificationResult
from .email_fetcher import EmailMessage


# 信号权重配置
SIGNAL_WEIGHTS = {
    "legal_threat": 50,
    "safety_issue": 50,
    "social_media_threat": 35,
    "refund_demand": 25,
    "time_sensitive": 15,
    "vip_customer": 10,
}

# 情感加分
SENTIMENT_URGENCY_BONUS = {
    "positive": 0,
    "neutral": 5,
    "negative": 15,
    "angry": 30,
}


@dataclass
class UrgencyResult:
    """紧急度评分结果"""
    score: int                        # 0-100
    level: int                        # 1-5
    level_label: str                  # "低" / "一般" / "中等" / "高" / "紧急"
    factors: list[str]                # 触发加分的因素列表
    sla_minutes: int                  # 推荐 SLA 响应时间 (分钟)


class UrgencyScorer:
    """紧急度综合评分引擎"""

    # 关键词组
    LEGAL_KEYWORDS = [
        "lawyer", "attorney", "sue", "legal action", "court", "lawsuit",
        "律师", "起诉", "法院", "法律", "诉讼"
    ]
    SOCIAL_THREAT_KEYWORDS = [
        "tweet", "post", "expose", "review bomb", "曝光", "差评",
        "社交媒体", "微博", "twitter", "facebook", "reddit"
    ]
    SAFETY_KEYWORDS = [
        "injured", "electric shock", "fire", "allergic", "burn", "cut",
        "受伤", "触电", "起火", "过敏", "烧伤", "割伤", "中毒"
    ]
    REFUND_KEYWORDS = [
        "refund immediately", "money back now", "全额退款", "立刻退款",
        "马上退钱", "退款"
    ]
    TIME_SENSITIVE_KEYWORDS = [
        "urgent", "asap", "deadline", "by tomorrow", "急", "尽快",
        "立刻", "马上"
    ]

    def __init__(self, ticket_db=None):
        self.ticket_db = ticket_db  # 用于查询上下文

    def calculate(self, email: EmailMessage, classification: ClassificationResult) -> UrgencyResult:
        """
        综合评分: 内容信号 60% + 情感加权 25% + 上下文 15%
        """
        score = 0.0
        factors = []
        body_lower = email.body_plain.lower()
        subject_lower = email.subject.lower()
        combined = f"{subject_lower} {body_lower}"

        # ===== 阶段 1: 内容信号 (权重 60%) =====
        # 法律威胁
        if self._match_any(combined, self.LEGAL_KEYWORDS):
            score += SIGNAL_WEIGHTS["legal_threat"]
            factors.append("法律威胁关键词")

        # 安全隐患
        if self._match_any(combined, self.SAFETY_KEYWORDS):
            score += SIGNAL_WEIGHTS["safety_issue"]
            factors.append("产品安全隐患")

        # 社交媒体威胁
        if self._match_any(combined, self.SOCIAL_THREAT_KEYWORDS):
            score += SIGNAL_WEIGHTS["social_media_threat"]
            factors.append("社交媒体扩散威胁")

        # 退款需求
        if self._match_any(combined, self.REFUND_KEYWORDS):
            score += SIGNAL_WEIGHTS["refund_demand"]
            factors.append("退款/退钱要求")

        # 时间敏感
        if self._match_any(combined, self.TIME_SENSITIVE_KEYWORDS):
            score += SIGNAL_WEIGHTS["time_sensitive"]
            factors.append("时间敏感表达")

        # ===== 阶段 2: 情感加权 (权重 25%) =====
        sentiment = classification.sentiment
        score += SENTIMENT_URGENCY_BONUS.get(sentiment, 0)
        if sentiment in ("angry",):
            factors.append(f"客户情绪: {sentiment}")

        # ===== 阶段 3: 上下文加权 (权重 15%) =====
        context_factors = self._context_scoring(email, classification)
        score += context_factors["score"]
        factors.extend(context_factors["reasons"])

        # ===== 得分 → 等级映射 =====
        score = min(100, max(0, int(score)))

        if score >= 70:
            level, label, sla = 5, "紧急", 30
        elif score >= 50:
            level, label, sla = 4, "高", 60
        elif score >= 30:
            level, label, sla = 3, "中等", 240
        elif score >= 15:
            level, label, sla = 2, "一般", 480
        else:
            level, label, sla = 1, "低", 1440

        return UrgencyResult(
            score=score,
            level=level,
            level_label=label,
            factors=factors,
            sla_minutes=sla,
        )

    def _match_any(self, text: str, keywords: list[str]) -> bool:
        """检查文本是否包含任意关键词"""
        return any(kw.lower() in text for kw in keywords)

    def _context_scoring(self, email: EmailMessage, classification: ClassificationResult) -> dict:
        """上下文加权评分"""
        score = 0.0
        reasons = []

        # 从数据库查询该客户最近的邮件
        if self.ticket_db:
            try:
                recent_count = self.ticket_db.get_recent_email_count(email.from_addr, hours=24)
                if recent_count >= 5:
                    score += 20
                    reasons.append(f"24h 内第 {recent_count} 封邮件 (≥5)")
                elif recent_count >= 3:
                    score += 10
                    reasons.append(f"24h 内第 {recent_count} 封邮件 (≥3)")
            except Exception:
                pass

        # 大额订单检测
        amount = classification.entities.get("amount", 0)
        if amount:
            try:
                amount = float(amount)
                if amount > 1000:
                    score += 15
                    reasons.append(f"大额订单 (${amount:.2f})")
                elif amount > 500:
                    score += 10
                    reasons.append(f"中等金额订单 (${amount:.2f})")
            except (ValueError, TypeError):
                pass

        return {"score": score, "reasons": reasons}

    @staticmethod
    def get_sla_display(level: int) -> str:
        """获取 SLA 显示文本"""
        sla_map = {1: "24h", 2: "8h", 3: "4h", 4: "1h", 5: "30min"}
        return sla_map.get(level, "24h")
