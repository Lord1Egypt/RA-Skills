"""LLM 客户端：OpenAI 兼容协议调用 + mock 模式 + JSON 解析与校验。

- 配置了 INTENT_LLM_API_KEY => 真实调用 OpenAI 兼容接口（GLM/DeepSeek/通义等均可）
- 未配置 => mock 模式：基于关键词规则的本地模拟，保证开发/测试环境无 Key 可跑
- 统一抛 IntentLLMError，由 pipeline 阶段6 降级逻辑接管
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any

import httpx

from .config import Settings
from .prompts import INTENT_JSON_SCHEMA, SYSTEM_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE

logger = logging.getLogger("intent_skill.llm")


class IntentLLMError(Exception):
    """LLM 调用失败 / 超时 / 输出不可解析，供阶段6降级逻辑捕获。"""


# ---------------------------------------------------------------------------
# 输出解析与强校验
# ---------------------------------------------------------------------------

_MARKDOWN_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.S)


def _extract_json_block(text: str) -> str:
    """容错提取 JSON：优先 markdown 代码块，其次首个 {...} 平衡段。"""
    text = text.strip()
    m = _MARKDOWN_FENCE_RE.search(text)
    if m:
        text = m.group(1).strip()
    start = text.find("{")
    if start == -1:
        raise IntentLLMError("llm output has no json object")
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    raise IntentLLMError("llm output json not balanced")


def validate_intent_output(data: dict[str, Any]) -> dict[str, Any]:
    """对 LLM 输出做强校验 + 规范化（不依赖 jsonschema 包，手写校验更可控）。"""
    schema = INTENT_JSON_SCHEMA
    for key in schema["required"]:
        if key not in data:
            raise IntentLLMError(f"missing field: {key}")

    if data["intent_type"] not in schema["properties"]["intent_type"]["enum"]:
        raise IntentLLMError(f"invalid intent_type: {data['intent_type']}")
    if data["risk_level"] not in ("safe", "warning", "block"):
        raise IntentLLMError(f"invalid risk_level: {data['risk_level']}")
    if not isinstance(data["is_allow_forward"], bool):
        raise IntentLLMError("is_allow_forward must be bool")

    for str_field in ("rewritten_query", "intent_desc", "refuse_reason"):
        if not isinstance(data[str_field], str):
            raise IntentLLMError(f"{str_field} must be string")

    if not isinstance(data["required_agent_list"], list):
        raise IntentLLMError("required_agent_list must be list")

    ee = data["entity_extract"]
    if not isinstance(ee, dict):
        raise IntentLLMError("entity_extract must be object")
    for list_field in ("industry", "etf_code", "index_name"):
        ee.setdefault(list_field, [])
        if not isinstance(ee[list_field], list):
            raise IntentLLMError(f"entity_extract.{list_field} must be list")
    ee.setdefault("query_object", "")
    if not isinstance(ee["query_object"], str):
        raise IntentLLMError("entity_extract.query_object must be string")

    # 规范化：拦截/咨询/闲聊场景清空 rewritten_query 与 agent 裁剪
    if not data["is_allow_forward"]:
        data["required_agent_list"] = []
    return data


# ---------------------------------------------------------------------------
# Mock 模式：无 API Key 时的本地规则模拟（仅用于开发联调与测试）
# ---------------------------------------------------------------------------

_INJECTION_MARKS = (
    "忽略", "无视", "之前的规则", "以上规则", "系统提示", "system prompt",
    "你的提示词", "角色扮演", "越狱", "jailbreak", "developer mode",
)
_PLATFORM_QA_MARKS = ("怎么导出", "如何导出", "数据来源", "怎么注册", "如何充值", "会员", "客服")
_GREETING_MARKS = ("你好", "您好", "hi", "hello", "在吗", "早上好", "晚上好", "哈喽")


def _mock_llm_intent(cleaned_text: str, rule_labels: list[str]) -> dict[str, Any]:
    low = cleaned_text.lower()
    labels_blob = " ".join(rule_labels).lower()

    # 1) 注入试探
    if any(k in low for k in _INJECTION_MARKS):
        return {
            "intent_type": "malicious_injection", "is_allow_forward": False,
            "risk_level": "block", "rewritten_query": "",
            "intent_desc": "疑似提示词注入或越权指令",
            "refuse_reason": "抱歉，暂时无法处理您的请求，请调整后重试。",
            "required_agent_list": [],
            "entity_extract": {"industry": [], "etf_code": [], "index_name": "", "query_object": ""},
        }
    # 2) 投资建议索取
    if any(k in low for k in ("给我", "告诉我") ) and any(
        k in low for k in ("必涨", "稳赚", "买点", "点位", "代码", "荐股", "收益")
    ) or "买点位" in low or "预测涨跌" in low:
        return {
            "intent_type": "investment_advice_request", "is_allow_forward": False,
            "risk_level": "block", "rewritten_query": "",
            "intent_desc": "强制索要买卖点位/荐股/收益承诺，超出平台能力",
            "refuse_reason": "本平台仅提供客观 ETF 投研数据分析，不提供荐股、收益承诺、买卖点位等投资决策建议，请调整您的提问。",
            "required_agent_list": [],
            "entity_extract": {"industry": [], "etf_code": [], "index_name": "", "query_object": ""},
        }
    # 3) 平台问答
    if any(k in low for k in _PLATFORM_QA_MARKS):
        return {
            "intent_type": "platform_qa", "is_allow_forward": False,
            "risk_level": "safe", "rewritten_query": "",
            "intent_desc": "平台功能咨询，路由平台问答知识库",
            "refuse_reason": "您好，这是平台功能问题，已转交平台问答为您解答。",
            "required_agent_list": [],
            "entity_extract": {"industry": [], "etf_code": [], "index_name": "", "query_object": ""},
        }
    # 4) 闲聊问候
    if len(cleaned_text) <= 12 and any(k in low for k in _GREETING_MARKS):
        return {
            "intent_type": "chat_greeting", "is_allow_forward": False,
            "risk_level": "safe", "rewritten_query": "",
            "intent_desc": "闲聊问候，无业务诉求",
            "refuse_reason": "您好！我可以帮您分析 ETF、行业与指数相关的投研信息，欢迎提问，例如：芯片行业最近表现如何？",
            "required_agent_list": [],
            "entity_extract": {"industry": [], "etf_code": [], "index_name": "", "query_object": ""},
        }
    # 5) 其余按投研查询处理（warning：因为无法判断是否决策类问句，统一提示）
    return {
        "intent_type": "etf_industry_research", "is_allow_forward": True,
        "risk_level": "warning",
        "rewritten_query": f"对{cleaned_text.rstrip('？?。！！ ')}做ETF相关投研分析，涵盖宏观、行业事件、产业政策、估值、资金面维度，仅输出客观事实与数据，不给出买入卖出投资决策建议",
        "intent_desc": "ETF/行业/指数投研查询（mock模式）",
        "refuse_reason": "",
        "required_agent_list": [],
        "entity_extract": {"industry": [], "etf_code": [], "index_name": [], "query_object": cleaned_text[:30]},
    }


# ---------------------------------------------------------------------------
# 真实 LLM 调用
# ---------------------------------------------------------------------------


def build_messages(cleaned_text: str, rule_labels: list[str]) -> list[dict[str, str]]:
    rule_section = "\n".join(f"- {label}" for label in rule_labels) if rule_labels else "- 无"
    return [
        {"role": "system", "content": SYSTEM_PROMPT_TEMPLATE.format(
            platform_boundary=_current_boundary)},
        {"role": "user", "content": USER_PROMPT_TEMPLATE.format(
            rule_labels_section=rule_section, cleaned_text=cleaned_text)},
    ]


# 平台边界由 settings 注入，模块级缓存避免循环依赖
_current_boundary: str = "本平台仅做ETF/行业/指数投研信息分析，不提供买卖建议、不做个股荐股，不能预测涨跌，不提供投资决策。"


def set_platform_boundary(boundary: str) -> None:
    global _current_boundary
    _current_boundary = boundary


async def call_intent_llm(cleaned_text: str, rule_labels: list[str], settings: Settings) -> dict[str, Any]:
    """调用 LLM 做意图识别；未配置 Key 走 mock；失败抛 IntentLLMError。"""
    if not settings.intent_llm_api_key:
        return _mock_llm_intent(cleaned_text, rule_labels)

    messages = build_messages(cleaned_text, rule_labels)
    url = settings.intent_llm_base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": settings.intent_llm_model,
        "messages": messages,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        "max_tokens": 800,
    }
    headers = {"Authorization": f"Bearer {settings.intent_llm_api_key}"}

    try:
        async with httpx.AsyncClient(timeout=settings.intent_llm_timeout_seconds) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
    except httpx.TimeoutException as e:
        raise IntentLLMError(f"llm timeout: {e}") from e
    except (httpx.HTTPError, KeyError, IndexError, ValueError) as e:
        raise IntentLLMError(f"llm call failed: {e}") from e

    try:
        data = json.loads(_extract_json_block(content))
    except (json.JSONDecodeError, IntentLLMError) as e:
        raise IntentLLMError(f"llm output parse failed: {e}") from e

    return validate_intent_output(data)
