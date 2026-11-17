"""Pipeline：串起阶段1→6 的完整处理链。

阶段1 规则预处理（preprocess.py）
阶段2 LLM 意图识别（llm_client.py）
阶段3 业务边界校验（本模块）
阶段4 防注入二次校验（本模块，针对 rewritten_query）
阶段5 输出路由 & 埋点（本模块 + api.py）
阶段6 异常降级兜底（本模块）
"""
from __future__ import annotations

import logging
import re
import uuid
from dataclasses import dataclass, field
from typing import Any

from .config import Settings
from .llm_client import (
    IntentLLMError,
    call_intent_llm,
    set_platform_boundary,
)
from .preprocess import preprocess

logger = logging.getLogger("intent_skill.pipeline")

ALL_AGENTS = ["宏观agent", "事件agent", "政策agent", "估值agent", "资金agent"]

# ---------------------------------------------------------------------------
# 阶段4：防 Prompt 注入二次校验（对 rewritten_query 检测）
# ---------------------------------------------------------------------------

# 针对改写后 query 的注入特征：试图修改下游 Agent 系统提示、命令忽略规则、索取内部 prompt
_INJECTION_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("override_rules", re.compile(
        r"(忽略|无视| disregards?|override)\s*(之前|以上|前面|所有|全部|所有|all|previous|prior|"
        r"above|的|\s|,|，|。|!|！|？|\?){0,8}(规则|指令|instructions?|rules?|约束)", re.I)),
    ("leak_prompt", re.compile(
        r"(系统提示|system\s*prompt|你的提示词|初始指令|角色设定|rules of the system)", re.I)),
    ("role_hijack", re.compile(
        r"(你现在是|从现在开始你是|扮演|pretend\s+to\s+be|act\s+as)\s*"
        r"(一个)?(无限制|不受限制|没有限制|解除|自由|DAN|开发者)", re.I)),
    ("ignore_previous", re.compile(
        r"(ignore\s+(all\s+)?(previous|prior|above)|disregard\s+.{0,20}instructions?)", re.I)),
    ("output_format_hijack", re.compile(
        r"(必须|请|请务必)?\s*(以|用|按照)\s*(我的|自定义|新的)\s*(格式|规则|模板)\s*(输出|回答)", re.I)),
]


def detect_injection(text: str) -> list[str]:
    hits = []
    if not text:
        return hits
    for label, pattern in _INJECTION_PATTERNS:
        if pattern.search(text):
            hits.append(label)
    return hits


# ---------------------------------------------------------------------------
# 标准化应答结构（阶段5 两种出口共用）
# ---------------------------------------------------------------------------


@dataclass
class IntentResult:
    request_id: str
    action: str                     # forward / intercept / platform_qa / degrade_block / degrade_loose
    is_allow_forward: bool
    risk_level: str = "safe"        # safe / warning / block
    reply_to_user: str = ""         # 拦截/引导场景给前端的直接回复；转发场景为空
    intent_type: str = ""
    intent_desc: str = ""
    refuse_reason: str = ""
    rewritten_query: str = ""
    original_user_query: str = ""
    cleaned_query: str = ""
    entity_extract: dict[str, Any] = field(default_factory=dict)
    agent_allow_list: list[str] = field(default_factory=list)
    risk_warning: bool = False      # true => 汇总结果页强制追加免责声明
    rule_labels: list[str] = field(default_factory=list)
    degraded: bool = False          # 阶段6降级标记
    parse_failed: bool = False      # loose 模式下游加强风险提示标记

    def to_task_context(self) -> dict[str, Any]:
        """阶段5-出口2：投递给 Agent 调度器的统一任务上下文对象。"""
        return {
            "request_id": self.request_id,
            "original_user_query": self.original_user_query,   # 仅日志留存，禁止下发业务Agent
            "standard_query": self.rewritten_query,            # 下游5个Agent唯一可用输入
            "entity_extract": self.entity_extract,
            "risk_warning": self.risk_warning,
            "agent_allow_list": self.agent_allow_list,
        }


# ---------------------------------------------------------------------------
# 拒绝话术（安全应答统一，不暴露内部实现）
# ---------------------------------------------------------------------------

REFUSE_INJECTION = "抱歉，暂时无法处理您的请求，请调整后重试。"
REFUSE_ILLEGAL = "您的提问包含平台不支持的内容，请调整后重试。"
REFUSE_ADVICE = (
    "本平台仅提供客观 ETF 投研数据分析，不提供荐股、收益承诺、买卖点位等投资决策建议，"
    "请调整您的提问。"
)
GUIDE_GREETING = (
    "您好！我是 ETF 投研助手，可以帮您分析 ETF、行业与指数相关的投研信息。"
    "试试问我：芯片行业最近的基本面和政策环境怎么样？"
)
# 免责声明标准模板：risk_warning=true 时由结果汇总页原样追加（多层免责第一层）
RISK_DISCLAIMER = (
    "以上内容由AI基于公开信息整理生成，仅供研究参考，不构成任何投资建议。市场有风险，投资需谨慎。"
)
# 缺少查询对象/语义模糊时的引导反问话术（澄清原则：不猜）
GUIDE_MISSING_OBJECT = (
    "请告诉我您想了解哪个行业、ETF代码或指数，以及关注的时间范围，我来为您做投研分析。"
)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


async def run_intent_pipeline(raw_text: str, settings: Settings) -> IntentResult:
    request_id = uuid.uuid4().hex
    set_platform_boundary(settings.intent_platform_boundary)

    # ---------------- 阶段1：规则预处理 ----------------
    pre = preprocess(raw_text, max_length=settings.intent_max_query_length)
    if pre.rule_block:
        logger.info("intent_gateway", extra={
            "request_id": request_id, "stage": "rule_block", "risk_type": pre.risk_type,
            "risk_level": "block", "forwarded": False, "raw": pre.raw_text,
        })
        return IntentResult(
            request_id=request_id, action="intercept", is_allow_forward=False,
            risk_level="block", reply_to_user=pre.blocked_reason,
            intent_type="illegal_content" if pre.risk_type == "sensitive_word" else "unknown_intent",
            intent_desc=f"规则层拦截: {pre.risk_type}",
            refuse_reason=pre.blocked_reason, original_user_query=pre.raw_text,
            cleaned_query=pre.raw_text_cleaned, rule_labels=pre.rule_labels,
        )

    # ---------------- 阶段2：LLM 意图识别（含阶段6降级） ----------------
    try:
        intent = await call_intent_llm(pre.raw_text_cleaned, pre.rule_labels, settings)
    except IntentLLMError as e:
        logger.warning("intent_llm_error: %s", e)
        return _degrade(pre, request_id, settings)

    # ---------------- 阶段3：业务边界校验 ----------------
    result = _apply_business_rules(intent, pre, request_id)

    # ---------------- 阶段4：防注入二次校验（对 rewritten_query） ----------------
    if result.is_allow_forward:
        injection_hits = detect_injection(result.rewritten_query)
        if injection_hits:
            logger.warning("stage4_injection_detected: %s", injection_hits)
            result.is_allow_forward = False
            result.action = "intercept"
            result.risk_level = "block"
            result.reply_to_user = REFUSE_INJECTION
            result.refuse_reason = REFUSE_INJECTION
            result.agent_allow_list = []
            result.rule_labels.append("stage4_injection:" + ",".join(injection_hits))

    # ---------------- 阶段5：路由出口 ----------------
    if result.is_allow_forward:
        result.action = "forward"
        result.risk_warning = result.risk_level == "warning"
        result.agent_allow_list = intent.get("required_agent_list") or list(ALL_AGENTS)
        # 兜底：过滤非法 agent 名
        valid = set(ALL_AGENTS)
        result.agent_allow_list = [a for a in result.agent_allow_list if a in valid] or list(ALL_AGENTS)

    # 埋点日志
    logger.info("intent_gateway", extra={
        "request_id": request_id, "stage": "final", "action": result.action,
        "intent_type": result.intent_type, "risk_level": result.risk_level,
        "forwarded": result.is_allow_forward,
        "refuse_reason": result.refuse_reason, "raw": pre.raw_text,
    })
    return result


def _apply_business_rules(
    intent: dict[str, Any], pre, request_id: str
) -> IntentResult:
    """阶段3：基于 intent_type 的分支处理。"""
    it = intent["intent_type"]
    common = dict(
        request_id=request_id,
        intent_type=it,
        intent_desc=intent.get("intent_desc", ""),
        refuse_reason=intent.get("refuse_reason", ""),
        original_user_query=pre.raw_text,
        cleaned_query=pre.raw_text_cleaned,
        rule_labels=pre.rule_labels,
        entity_extract=intent.get("entity_extract", {}),
    )

    # 1) 放行分支
    if it == "etf_industry_research" and intent["risk_level"] in ("safe", "warning"):
        return IntentResult(
            **common, action="forward", is_allow_forward=True,
            risk_level=intent["risk_level"],
            rewritten_query=intent["rewritten_query"],
        )

    # 2) 平台问答
    if it == "platform_qa":
        return IntentResult(
            **common, action="platform_qa", is_allow_forward=False,
            risk_level="safe",
            reply_to_user=intent.get("refuse_reason")
            or "您好，这是平台功能问题，已转交平台问答为您解答。",
        )

    # 3) 闲聊 / 语义模糊（闲聊→欢迎引导；缺查询对象→引导反问，不猜）
    if it in ("chat_greeting", "unknown_intent"):
        fallback = GUIDE_GREETING if it == "chat_greeting" else GUIDE_MISSING_OBJECT
        return IntentResult(
            **common, action="intercept", is_allow_forward=False,
            risk_level="safe",
            reply_to_user=intent.get("refuse_reason") or fallback,
        )

    # 4) 注入 / 违规 —— 统一友好话术，不暴露内部实现
    if it in ("malicious_injection", "illegal_content"):
        return IntentResult(
            **common, action="intercept", is_allow_forward=False,
            risk_level="block",
            reply_to_user=REFUSE_INJECTION if it == "malicious_injection" else REFUSE_ILLEGAL,
        )

    # 5) 索要投资建议
    if it == "investment_advice_request":
        # LLM 已判定 block（情况B），按拒绝处理
        return IntentResult(
            **common, action="intercept", is_allow_forward=False,
            risk_level="block", reply_to_user=REFUSE_ADVICE,
        )

    # 未知 intent_type（理论不可达，校验层已挡）
    return IntentResult(
        **common, action="intercept", is_allow_forward=False,
        risk_level="block", reply_to_user=REFUSE_INJECTION,
    )


def _degrade(pre, request_id: str, settings: Settings) -> IntentResult:
    """阶段6：LLM 故障降级。conservative=拦截优先（金融平台推荐）；loose=放行打标。"""
    if settings.intent_degrade_mode == "loose":
        return IntentResult(
            request_id=request_id, action="degrade_loose", is_allow_forward=True,
            risk_level="warning", risk_warning=True,
            rewritten_query=pre.raw_text_cleaned,
            original_user_query=pre.raw_text, cleaned_query=pre.raw_text_cleaned,
            intent_type="unknown_intent", intent_desc="LLM意图识别失败，宽松模式放行",
            entity_extract={"industry": [], "etf_code": [], "index_name": [], "query_object": ""},
            agent_allow_list=list(ALL_AGENTS),
            degraded=True, parse_failed=True,
            rule_labels=list(pre.rule_labels) + ["intent_parse_failed"],
        )
    # conservative（默认）
    return IntentResult(
        request_id=request_id, action="degrade_block", is_allow_forward=False,
        risk_level="block",
        reply_to_user="暂时无法理解您的提问，请调整问题后重试。",
        refuse_reason="意图识别服务暂时不可用（保守降级拦截）",
        original_user_query=pre.raw_text, cleaned_query=pre.raw_text_cleaned,
        intent_type="unknown_intent", intent_desc="LLM意图识别失败，保守模式拦截",
        degraded=True, rule_labels=list(pre.rule_labels) + ["llm_degraded"],
    )
