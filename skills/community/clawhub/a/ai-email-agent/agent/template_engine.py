"""
模板引擎 — 多语言邮件模板变量渲染 + LLM 润色
"""
import yaml
import os
from datetime import datetime, timedelta
from typing import Optional
from openai import OpenAI

from .config_loader import get_config
from .classifier import ClassificationResult
from .email_fetcher import EmailMessage
from .urgency import UrgencyResult


# ============================================================
# 预设模板库
# ============================================================
DEFAULT_TEMPLATES = {
    "consultation": {
        "en": {
            "subject": "Re: {original_subject} | Ticket #{ticket_id}",
            "body": """Hi {customer_name},

Thank you for reaching out! Regarding your inquiry about **{product_name}**:

{knowledge_base_snippet}

💡 Additional Info:
- Current stock: Available for order
- Estimated shipping: 1-3 business days after order
- If you have more questions, simply reply to this email.

Ticket ID: #{ticket_id}
For further assistance, we'll get back to you within {reply_deadline}.

Happy shopping!
{agent_name}
---
[This is an automated response. Our support team will follow up if needed.]"""
        },
        "zh-CN": {
            "subject": "Re: {original_subject} | 工单 #{ticket_id}",
            "body": """您好 {customer_name}，

感谢您联系我们！关于您咨询的 **{product_name}**：

{knowledge_base_snippet}

💡 补充信息：
- 当前库存状态：可下单
- 预计发货时间：下单后 1-3 个工作日
- 如还有其他问题，直接回复本邮件即可

工单编号：#{ticket_id}
如需人工协助，我们将在 {reply_deadline} 内回复您。

祝您购物愉快！
{agent_name}
---
[这是一封系统自动生成的回复。如有未尽之处，客服团队将尽快跟进。]"""
        },
    },
    "complaint": {
        "en": {
            "subject": "Re: {original_subject} | We take your feedback seriously — Ticket #{ticket_id}",
            "body": """Hi {customer_name},

We're truly sorry to hear about your experience with **{product_name}**: {issue_summary}.

This is not the experience we want for you. Here's what we've done immediately:

🛡️ Immediate Actions:
1. Your feedback has been escalated to our Quality Team
2. Ticket #{ticket_id} has been created — a specialist will follow up within {reply_deadline}
3. If this involves a return/exchange, simply reply with photos for faster processing

⚠️ As a token of apology, we've prepared a **15% off coupon** for your next purchase — it will be sent during the manual follow-up.

Every piece of feedback helps us improve. Thank you for your patience and understanding.

{agent_name}"""
        },
        "zh-CN": {
            "subject": "Re: {original_subject} | 我们非常重视您的反馈 — 工单 #{ticket_id}",
            "body": """您好 {customer_name}，

我们非常抱歉您在 **{product_name}** 的使用中遇到了问题：{issue_summary}。

我们已采取以下措施：

🛡️ 立即行动：
1. 您的反馈已升级至品质管理团队
2. 工单 #{ticket_id} 已创建，专人将在 {reply_deadline} 内跟进
3. 如涉及退换货，可直接回复本邮件提供照片，我们将第一时间处理

⚠️ 作为歉意，我们为您准备了一张 **85 折优惠券**，将在人工跟进时一并发送。

感谢您的耐心与理解，您的每一次反馈都帮助我们变得更好。

{agent_name}"""
        },
    },
    "return_refund": {
        "en": {
            "subject": "Re: {original_subject} | Return/Exchange Accepted — RMA #{rma_number}",
            "body": """Hi {customer_name},

Your return/exchange request has been received. Here are the details:

📦 Return/Exchange Info
┌─────────────────────────────────────┐
│ Order ID:    {order_id}             │
│ Product:     {product_name}         │
│ RMA Number:  {rma_number}           │
│ Type:        Return/Exchange        │
│ Status:      Pending Review         │
└─────────────────────────────────────┘

📋 Next Steps:
1. We'll review your request (usually within 24 hours)
2. Once approved, you'll receive a Return Label with detailed instructions
3. Refund will be processed within 3-5 business days after warehouse receives the return

💬 If convenient, you can reply with photos of the issue to speed up the review.

RMA valid for {rma_valid_days} days.

{agent_name}"""
        },
        "zh-CN": {
            "subject": "Re: {original_subject} | 退换货申请已受理 — RMA #{rma_number}",
            "body": """您好 {customer_name}，

您的退换货申请已收到，详情如下：

📦 退换货信息
┌─────────────────────────────────────┐
│ 订单号：    {order_id}              │
│ 商品：      {product_name}          │
│ RMA 编号：  {rma_number}            │
│ 申请类型：  退货/换货                │
│ 受理状态：  待审核                   │
└─────────────────────────────────────┘

📋 下一步操作：
1. 我们会审核您的申请（通常 24 小时内）
2. 审核通过后，您将收到退货标签和详细指引
3. 仓库收到退货后 3-5 个工作日完成退款

💬 如方便，可提前将商品问题照片回复至本邮件，加速审核。

RMA 有效期为 {rma_valid_days} 天。

{agent_name}"""
        },
    },
    "cooperation": {
        "en": {
            "subject": "Re: {original_subject} | Cooperation Inquiry Forwarded — Ticket #{ticket_id}",
            "body": """Hi {customer_name},

Thank you for your interest in partnering with us!

Your cooperation inquiry has been forwarded to our **Business Development Team**. They will reach out to you directly within **1-2 business days**.

📩 Ticket ID: #{ticket_id}
📞 For urgent matters: +86-XXX-XXXX-XXXX (Mon-Fri, 9:00-18:00 CST)

Looking forward to connecting with you!

{agent_name}"""
        },
        "zh-CN": {
            "subject": "Re: {original_subject} | 合作咨询已转接 — 工单 #{ticket_id}",
            "body": """您好 {customer_name}，

感谢您对我们的关注与合作意向！

您的合作咨询已转接至我们的 **商务拓展团队**，他们将在 **1-2 个工作日内** 直接与您联系。

📩 工单编号：#{ticket_id}
📞 如紧急，可致电：+86-XXX-XXXX-XXXX（工作日 9:00-18:00）

期待与您进一步沟通！

{agent_name}"""
        },
    },
}

# 文化适配规则
CULTURAL_ADAPTATIONS = {
    "ja": {
        "greeting": "{customer_name} 様",
        "apology_prefix": "誠に申し訳ございません。",
        "closing": "何卒よろしくお願いいたします。",
        "emoji_policy": "none",
    },
    "ko": {
        "greeting": "{customer_name}님, 안녕하세요.",
        "apology_prefix": "불편을 드려 진심으로 죄송합니다.",
        "closing": "감사합니다.",
        "emoji_policy": "minimal",
    },
    "es": {
        "greeting": "Hola {customer_name},",
        "apology_prefix": "Lamentamos sinceramente",
        "closing": "Saludos cordiales,",
        "emoji_policy": "allowed",
    },
}


class TemplateEngine:
    """多语言模板渲染引擎"""

    def __init__(self, config: dict = None, llm_client: OpenAI = None):
        cfg = config or get_config()
        self.templates = DEFAULT_TEMPLATES.copy()

        # 加载外部模板文件 (如果存在)
        tmpl_path = os.path.join(os.path.dirname(__file__), "..", "templates", "replies.yaml")
        if os.path.exists(tmpl_path):
            with open(tmpl_path, "r", encoding="utf-8") as f:
                external = yaml.safe_load(f)
                if external:
                    self._merge_templates(external)

        self.llm = llm_client
        if self.llm is None:
            llm_cfg = cfg.get("llm", {})
            self.llm = OpenAI(
                api_key=llm_cfg.get("api_key", ""),
                base_url=llm_cfg.get("base_url", ""),
            )
        self.llm_model = cfg.get("llm", {}).get("model", "gpt-4o-mini")
        self.sender_name = cfg.get("smtp", {}).get("sender_name", "AI 客服助手")
        self.languages_config = cfg.get("languages", {})

    def render(
        self,
        email: EmailMessage,
        classification: ClassificationResult,
        urgency: UrgencyResult,
        ticket_id: str,
        rma_number: str = "",
        kb_snippet: str = "",
    ) -> dict:
        """
        渲染最终回复邮件
        返回 {"subject": str, "body": str, "language": str, "mode": "native"|"translated"|"llm"}
        """
        lang = classification.language
        category = classification.category

        # 确定模板语言策略
        template_lang, mode = self._select_language_strategy(lang, category)

        # 构建变量
        variables = self._build_variables(
            email, classification, urgency, ticket_id, rma_number, kb_snippet
        )

        # 获取模板并填充
        if category in self.templates and template_lang in self.templates[category]:
            # 有原生/已翻译模板 → 直接填充 + LLM 微调
            tmpl = self.templates[category][template_lang]
            subject = tmpl["subject"].format(**variables)
            body = tmpl["body"].format(**variables)
        else:
            # 无模板 → LLM 零样本生成
            subject, body = self._llm_generate_reply(email, classification, urgency, ticket_id, variables)
            mode = "llm"

        # 文化适配
        body = self._apply_cultural_adaptation(body, lang, classification)

        # LLM 润色 (P1/P2 翻译场景)
        if mode in ("translated", "llm"):
            body = self._llm_polish(body, lang, classification)

        return {
            "subject": subject,
            "body": body,
            "language": lang,
            "mode": mode,
        }

    def _build_variables(self, email, classification, urgency, ticket_id, rma_number, kb_snippet):
        """构建模板变量字典"""
        entities = classification.entities

        # SLA 响应时限
        sla_hours = urgency.sla_minutes / 60
        sla_text = f"{urgency.sla_minutes}分钟" if urgency.sla_minutes < 120 else f"{int(sla_hours)}小时"

        return {
            "customer_name": email.from_name or email.from_addr.split("@")[0],
            "original_subject": email.subject,
            "order_id": entities.get("order_id", "订单号待补充"),
            "product_name": entities.get("product", "相关商品"),
            "issue_summary": classification.summary,
            "ticket_id": ticket_id,
            "rma_number": rma_number or f"RMA-{ticket_id}",
            "agent_name": self.sender_name,
            "reply_deadline": sla_text,
            "knowledge_base_snippet": kb_snippet or "我们的产品支持团队随时为您服务。",
            "rma_valid_days": "14",
        }

    def _select_language_strategy(self, lang: str, category: str) -> tuple[str, str]:
        """
        选择语言策略
        返回: (实际使用的模板语言, 模式)
        """
        p0 = self.languages_config.get("p0", ["en", "zh-CN"])
        p1 = self.languages_config.get("p1", ["ja", "ko", "es"])

        if lang in p0:
            return lang, "native"
        elif lang in p1:
            # P1 语言用英文模板 + LLM 翻译
            return "en", "translated"
        else:
            # P2/P3 → 英文 + LLM
            return "en", "translated"

    def _apply_cultural_adaptation(self, body: str, lang: str, classification: ClassificationResult) -> str:
        """应用文化适配规则"""
        if lang not in CULTURAL_ADAPTATIONS:
            return body

        rules = CULTURAL_ADAPTATIONS[lang]

        # Emoji 策略
        if rules.get("emoji_policy") == "none":
            import re
            body = re.sub(r'[\U0001F300-\U0001F9FF\u2600-\u26FF\u2700-\u27BF]', '', body)

        # 结尾替换
        if "closing" in rules:
            body = body.replace("Best regards,", rules["closing"])
            body = body.replace("祝您购物愉快！", rules["closing"])

        return body

    def _llm_polish(self, body: str, lang: str, classification: ClassificationResult) -> str:
        """LLM 润色：翻译 + 本地化适配"""
        prompt = f"""请将以下客服邮件回复翻译为 {lang} 语言，并进行本地化润色：

- 保持专业友好的语气
- 保留原有格式和结构
- 正确翻译产品名称和技术术语
- 适配目标语言的文化习惯

原文：
{body}

请只输出润色后的邮件正文，不要添加任何说明。"""

        try:
            response = self.llm.chat.completions.create(
                model=self.llm_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[WARN] LLM 润色失败: {e}")
            # 降级：在末尾附加英文原文
            return body + f"\n\n---\n[Auto-translated. For accuracy, see English below:]\n{body}"

    def _llm_generate_reply(self, email, classification, urgency, ticket_id, variables) -> tuple[str, str]:
        """LLM 零样本生成回复 (无模板语言)"""
        prompt = f"""作为电商客服，请用 {classification.language} 语言回复以下客户邮件：

客户: {email.from_name} <{email.from_addr}>
主题: {email.subject}
原文: {email.body_plain[:500]}

分类: {classification.category}
情感: {classification.sentiment}
工单号: {ticket_id}
承诺回复时限: {variables['reply_deadline']}

要求：
- 回复专业、友好、体贴
- 如果客户不满，先道歉
- 包含工单号和回复时限
- 提供切实可行的后续步骤
- 字数控制在 150 词以内

请输出格式：
SUBJECT: <邮件主题>
BODY:
<邮件正文>"""

        try:
            response = self.llm.chat.completions.create(
                model=self.llm_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.4,
            )
            content = response.choices[0].message.content.strip()

            # 解析
            subject = email.subject
            body = content
            if "BODY:" in content:
                parts = content.split("BODY:", 1)
                subj_line = parts[0].replace("SUBJECT:", "").strip()
                if subj_line:
                    subject = subj_line
                body = parts[1].strip()

            return subject, body
        except Exception as e:
            print(f"[WARN] LLM 生成失败: {e}")
            return email.subject, f"Thank you for your email. Ticket #{ticket_id}. We'll respond within {variables['reply_deadline']}."

    def _merge_templates(self, external: dict):
        """合并外部模板到默认模板"""
        for category, langs in external.items():
            if category not in self.templates:
                self.templates[category] = {}
            for lang, tmpl in langs.items():
                self.templates[category][lang] = tmpl
