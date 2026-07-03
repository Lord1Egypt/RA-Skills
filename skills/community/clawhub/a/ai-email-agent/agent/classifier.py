"""
LLM 分类器 — 意图分类 + 情感分析 + 实体提取 + 语言检测
"""
import json
import re
from dataclasses import dataclass, field
from openai import OpenAI
from .config_loader import get_config
from .email_fetcher import EmailMessage


@dataclass
class ClassificationResult:
    """分类结果"""
    category: str                     # consultation | complaint | return_refund | cooperation | spam
    confidence: float                 # 0-1
    sentiment: str                    # positive | neutral | negative | angry
    sentiment_score: float            # -1.0 ~ 1.0
    urgency_raw: int                  # LLM 初步评估 1-5
    language: str                     # ISO 639-1: en, zh, ja, ko, es...
    language_confidence: float
    entities: dict = field(default_factory=dict)  # {order_id, product, amount, ...}
    summary: str = ""                 # 中文摘要
    needs_human: bool = False
    needs_human_reason: str = ""
    raw_response: str = ""            # LLM 原始响应 (调试用)


CLASSIFICATION_PROMPT = """你是电商客服邮件分类器。分析以下邮件，严格输出 JSON。

## 分类标准
- consultation: 产品咨询(规格/价格/库存/使用方法/配送时间)
- complaint: 投诉(产品质量/服务态度/描述不符/发货延迟/差评威胁)
- return_refund: 退换货/退款/订单修改/取消订单
- cooperation: 商务合作(供应商/分销/KOL/批发/联盟营销)
- spam: 广告/钓鱼/无关推销/纯垃圾内容

## 情感分析
- positive: 正面(感谢/好评/满意)
- neutral: 中性(客观提问/无情绪)
- negative: 负面(失望/不满/抱怨但不攻击)
- angry: 愤怒(强烈不满/威胁/辱骂)

## 紧急度 (1-5)
1 = 不急(普通咨询)  2 = 一般  3 = 中等(有轻微不满)  
4 = 紧急(强烈投诉/退款要求/多次联系)  5 = 极紧急(法律威胁/安全隐患/社交媒体扩散威胁)

## 语言代码
ISO 639-1: en/zh/ja/ko/es/fr/de/ar/ru/pt/...

## 实体提取
从邮件中提取: order_id(订单号), product(商品名), amount(金额), tracking(运单号), rma(退换货单号, 如有)

## 输出格式 (纯 JSON, 无 markdown 代码块)
{{
  "category": "complaint",
  "confidence": 0.92,
  "sentiment": "angry",
  "sentiment_score": -0.85,
  "urgency_raw": 4,
  "language": "en",
  "language_confidence": 0.99,
  "entities": {{"order_id": "ORD-12345", "product": "Widget X300", "amount": 49.99}},
  "summary": "客户投诉收到的商品屏幕有裂纹，要求立即退款",
  "needs_human": true,
  "needs_human_reason": "情感愤怒+涉及产品质量+附带证据"
}}

## 邮件内容
发件人: {from_name} <{from_addr}>
主题: {subject}
正文:
{body}
"""


class EmailClassifier:
    """基于 LLM 的邮件分类器"""

    def __init__(self, config: dict = None):
        cfg = config or get_config()
        llm_cfg = cfg["llm"]
        self.client = OpenAI(
            api_key=llm_cfg["api_key"],
            base_url=llm_cfg["base_url"],
        )
        self.model = llm_cfg["model"]
        self.max_tokens = llm_cfg.get("max_tokens", 800)
        self.temperature = llm_cfg.get("temperature", 0.1)
        self.rules = cfg.get("rules", {})

    def classify(self, email: EmailMessage) -> ClassificationResult:
        """对邮件进行全维度分析"""
        # 截断正文以控制 token
        body = email.body_plain[:3000]
        if len(email.body_plain) > 3000:
            body += "\n... [正文已截断]"

        prompt = CLASSIFICATION_PROMPT.format(
            from_name=email.from_name,
            from_addr=email.from_addr,
            subject=email.subject,
            body=body,
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个精确的邮件分类器。只输出 JSON，不要输出 markdown 代码块或任何其他文本。"},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            raw = response.choices[0].message.content.strip()
        except Exception as e:
            # LLM 调用失败，返回默认分类
            return ClassificationResult(
                category="consultation",
                confidence=0.3,
                sentiment="neutral",
                sentiment_score=0.0,
                urgency_raw=2,
                language="en",
                language_confidence=0.5,
                summary=f"LLM 调用失败: {str(e)[:100]}",
                needs_human=True,
                needs_human_reason="LLM 调用异常，需人工判断",
            )

        # 解析 JSON
        parsed = self._parse_json(raw)

        # 规则增强校验
        parsed = self._rule_enhancement(email, parsed)

        return ClassificationResult(
            category=parsed.get("category", "consultation"),
            confidence=float(parsed.get("confidence", 0.5)),
            sentiment=parsed.get("sentiment", "neutral"),
            sentiment_score=float(parsed.get("sentiment_score", 0.0)),
            urgency_raw=int(parsed.get("urgency_raw", 2)),
            language=parsed.get("language", "en"),
            language_confidence=float(parsed.get("language_confidence", 0.5)),
            entities=parsed.get("entities", {}),
            summary=parsed.get("summary", ""),
            needs_human=parsed.get("needs_human", False),
            needs_human_reason=parsed.get("needs_human_reason", ""),
            raw_response=raw,
        )

    def _rule_enhancement(self, email: EmailMessage, parsed: dict) -> dict:
        """规则增强：对 LLM 结果进行二次校验和修正"""
        body_lower = email.body_plain.lower()

        # 法律威胁检测 → 强制 anger + urgency=5 + 人工
        legal_kws = self.rules.get("legal_keywords", [])
        if any(kw.lower() in body_lower for kw in legal_kws):
            parsed["sentiment"] = "angry"
            parsed["sentiment_score"] = -0.95
            parsed["urgency_raw"] = 5
            parsed["needs_human"] = True
            parsed["needs_human_reason"] = "检测到法律威胁关键词"

        # 社交媒体扩散威胁
        social_kws = self.rules.get("social_threat_keywords", [])
        if any(kw.lower() in body_lower for kw in social_kws):
            if parsed["urgency_raw"] < 4:
                parsed["urgency_raw"] = 4
            parsed["needs_human"] = True
            if not parsed.get("needs_human_reason"):
                parsed["needs_human_reason"] = "检测到社交媒体扩散威胁"

        # 安全隐患
        safety_kws = self.rules.get("safety_keywords", [])
        if any(kw.lower() in body_lower for kw in safety_kws):
            parsed["urgency_raw"] = 5
            parsed["needs_human"] = True
            parsed["needs_human_reason"] = "检测到产品安全隐患"

        # 置信度过低 → 标记人工
        if parsed.get("confidence", 1.0) < 0.7:
            parsed["needs_human"] = True
            if not parsed.get("needs_human_reason"):
                parsed["needs_human_reason"] = f"分类置信度过低 ({parsed['confidence']:.2f})"

        return parsed

    @staticmethod
    def _parse_json(raw: str) -> dict:
        """从 LLM 输出中提取 JSON"""
        # 尝试直接解析
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        # 尝试从 markdown 代码块中提取
        code_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', raw, re.DOTALL)
        if code_match:
            try:
                return json.loads(code_match.group(1).strip())
            except json.JSONDecodeError:
                pass

        # 尝试找到第一个 { 到最后一个 }
        brace_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if brace_match:
            try:
                return json.loads(brace_match.group(0))
            except json.JSONDecodeError:
                pass

        # 解析失败，返回默认
        print(f"[WARN] LLM JSON 解析失败，原始输出: {raw[:200]}")
        return {"category": "consultation", "confidence": 0.3, "needs_human": True,
                "needs_human_reason": "JSON 解析失败"}
