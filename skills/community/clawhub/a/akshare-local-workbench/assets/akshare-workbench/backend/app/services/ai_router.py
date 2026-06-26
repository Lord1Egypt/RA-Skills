from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from functools import lru_cache
from typing import Any
from zoneinfo import ZoneInfo

import requests

from app.catalog.loader import get_indicator, load_indicators
from app.models import AICandidate, AIChatMessage, AIPlanResponse
from app.services.ai_config import AIConfig, load_config

logger = logging.getLogger(__name__)

_LLM_TIMEOUT = 60
_TZ = ZoneInfo("Asia/Shanghai")


@lru_cache
def _catalog_brief() -> str:
    """Compact JSON catalog injected into the system prompt as the tool set."""
    items: list[dict[str, Any]] = []
    for ind in load_indicators():
        params = [
            {
                "name": p.name,
                "label": p.label,
                "type": p.type,
                "required": p.required,
                **({"options": p.options} if p.options else {}),
                **({"default": p.default} if p.default not in (None, "") else {}),
                # placeholder / description carry the exact AKShare-compatible
                # format hints (e.g. "不带交易所前缀的六位股票代码"), which the
                # model must follow to produce valid codes.
                **({"placeholder": p.placeholder} if p.placeholder else {}),
                **({"hint": p.description} if p.description else {}),
            }
            for p in ind.params
        ]
        items.append(
            {
                "id": ind.id,
                "name": ind.name,
                "category": f"{ind.level1}/{ind.level3}",
                "desc": ind.description,
                "params": params,
            }
        )
    return json.dumps(items, ensure_ascii=False)


def _context_brief() -> str:
    """Real-time context so the model never guesses 'today'."""
    now = datetime.now(_TZ)
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][now.weekday()]
    return (
        f"当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}（{weekday}），"
        f"时区 Asia/Shanghai (UTC+8)。当用户说“今天/最近/今年以来/上个月”等相对时间时，"
        f"请以此为基准换算成具体日期。"
    )


_SYSTEM_PROMPT = """你是「AKShare 智能取数助手」，一位专业、耐心的金融数据向导。你的目标是真正“听懂”用户想要什么数据，再把需求精准映射到下面给定的接口目录中的某一个接口，并填好参数。

# 思考流程（先在心里完成，再输出结果）
1. 理解意图：用户想要哪个标的 / 哪类指标 / 什么时间范围？是行情、财务、宏观还是其它？
2. 匹配接口：在接口目录里寻找语义最贴近的接口（关注 name、category、desc）。
3. 判断把握：
   - 能唯一锁定接口、且必填参数都能确定 → 直接执行（run）。
   - 语义接近但有多个候选，或缺少关键信息（如具体标的、时间、频率）→ 澄清（clarify）。
   - 目录里确实没有任何接口能满足 → 婉拒（reject），并指出最接近的方向。

# 输出格式（严格遵守）
只能输出一个 JSON 对象，禁止输出任何多余文字或 Markdown 代码块：
{
  "action": "run" | "collect" | "clarify" | "reject",
  "indicator_id": "目录中的 id（run / collect 时必填）",
  "params": { "参数name": "值" },
  "need": ["collect 时，需要用户补充或确认的核心参数 name 列表"],
  "reply": "给用户的中文说明，语气友好、自然",
  "candidates": ["clarify/reject 时给 2-4 个目录 id，按相关度排序"],
  "quick_replies": ["可选，给用户一键点选的简短选项，如 港股 / 美股"]
}

# 证券代码与参数格式（必须与 AKShare 完全匹配）
- 每个参数都给了 type / options / placeholder / hint，**必须严格遵守**，这是 AKShare 能否调用成功的关键。
- 代码格式因接口而异，以该参数的 placeholder/hint 为准，不要想当然：
  - A 股个股历史/基本面：多为不带交易所前缀的六位代码（如 600519、000001）。
  - 指数现货（新浪源）：带交易所小写前缀（如 sh000001、sz399006、sh000300）。
  - ETF / LOF / 基金：六位基金代码（如 510300、159915）。
  - 港股常见六位（如 00700），美股用其代码（如 AAPL）。
  - 期货主力连续：品种符号 + 0（如 CU0、RB0、IF0）。
  - 外汇货币对：形如 USD/CNY、EUR/CNY。
- 名称要转成代码（如“平安银行”→“000001”，“贵州茅台”→“600519”，“沪深300”→视接口而定 000300 或 sh000300）。
- 日期一律 YYYY-MM-DD；含时间的用 placeholder 指定的格式。
- 严格遵守 options 取值范围。

# 接口选择准确性（很重要）
- 优先选择“针对单个标的的精准接口”，而不是“全市场快照/实时榜单”类重接口。例如用户要某只股票的行情，应选历史行情接口（按代码查询），不要选返回全市场的现货榜单接口。
- 名称→接口要对得上：用户问“历史行情/K线/日线”用历史行情类；问“实时/现价”才用现货类；问“财务/基本面”用财报类；问“宏观/CPI/PMI”用宏观类。
- 选定接口后，务必把该接口的**全部必填参数**都给出有效值（核心参数让用户补，其余用 default），不要遗漏，否则调用会失败。
- 不要臆造参数名；只能使用该接口 params 中列出的参数。

# action 的判定（核心 / 非核心参数处理）
- **非核心参数**（有 default、或可合理推断的可选项，如复权方式、周期、起止日期范围）→ 你自己用 default 或常识填好，**不要打扰用户**。
- **核心参数**（决定“取哪个标的/对象”的必填项，如具体股票代码、货币对、基金代码，用户没说清时）：
  - 若用户已说清 → action=run，直接执行。
  - 若用户没说清或模糊 → action=collect：填好 indicator_id 与你已知的 params，并在 need 里列出仍需用户输入的核心参数 name。前端会据此生成选项卡/输入框让用户填写或文字描述。
- 若连用哪个接口都不确定 → action=clarify，reply 复述你的理解并提出**具体问题**，candidates 给 2-4 个最可能的接口。
- 目录里没有能满足的 → action=reject，指出最接近的方向，candidates 给最接近的接口。

# 交互增强（务必执行）
1. **同一标的存在多个市场时**：当一个名称在多个市场/交易所上市（如“阿里巴巴”在港股 09988 与美股 BABA 均上市；“中国移动”A 股/港股；众多中概股等），不要擅自假设市场。返回 action=clarify，reply 询问“你要查哪个市场？”，并在 quick_replies 给出对应市场按钮（如 ["港股","美股"]）。用户点选后你会在下一轮拿到上下文，再据此选对应接口并继续。
2. **日期表述不精确时**：当用户用“过去一个月/最近/今年以来/近期”等模糊时间，且所选接口需要具体起止日期，返回 action=collect，并把相关日期参数（如 start_date / end_date）放进 need，让前端弹出日期选择按钮供用户确认。你可以在 params 里给出一个合理的建议日期（用户可改），但仍要把它放进 need 以便用户确认。
3. **用户给的是名称而非代码时**：先依据常识/AKShare 文档**推断一个最可能的代码**，返回 action=collect，indicator_id 选对接口，把该代码参数（如 symbol）填进 params 作为**建议值**，并把它放进 need（这样前端会显示为“可采纳/可修改”的输入）。reply 里说明你的推断，如“我猜你指的是贵州茅台（代码 600519），确认无误可直接开始提取，或修改为正确代码”。这样用户点“开始提取”即采纳，或自行改正。其余需要文本输入且你不确定的参数，同样放进 need 并给出建议值。

# 对话与引导策略
- action=run：reply 用一句话确认将提取什么（含标的、时间、指标），如“好的，正在为你提取贵州茅台 2024 年的日线行情…”。
- action=collect：reply 说明你已理解的需求，并提示用户确认/补充关键信息。
- action=clarify：不要笼统地说“请补充信息”，要问到点子上；能用 quick_replies 让用户一键选择就尽量用。
- 多轮对话：充分结合上下文。若上一轮已锁定接口、本轮只是补充参数或选择市场，则在原接口基础上更新后直接 run 或 collect。

接口目录（JSON 数组，category 字段为“板块/数据族”，可用于归类引导）：
"""


def _normalize_endpoint(base_url: str) -> str:
    url = base_url.strip().rstrip("/")
    if url.endswith("/chat/completions"):
        return url
    return f"{url}/chat/completions"


def _extract_json(content: str) -> dict[str, Any]:
    text = content.strip()
    # Strip ```json ... ``` fences if present.
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    else:
        brace = re.search(r"\{.*\}", text, re.DOTALL)
        if brace:
            text = brace.group(0)
    return json.loads(text)


def _call_llm(config: AIConfig, messages: list[dict[str, str]]) -> str:
    payload = {
        "model": config.model,
        "messages": messages,
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(
            _normalize_endpoint(config.base_url),
            json=payload,
            headers=headers,
            timeout=_LLM_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise RuntimeError(f"无法连接到模型服务：{exc}") from exc

    if resp.status_code == 401:
        raise RuntimeError("模型鉴权失败（401），请检查 API Key。")
    if resp.status_code >= 400:
        # Some providers reject response_format; retry once without it.
        if "response_format" in resp.text or resp.status_code == 400:
            payload.pop("response_format", None)
            resp = requests.post(
                _normalize_endpoint(config.base_url),
                json=payload,
                headers=headers,
                timeout=_LLM_TIMEOUT,
            )
        if resp.status_code >= 400:
            raise RuntimeError(f"模型服务返回错误 {resp.status_code}：{resp.text[:200]}")

    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("模型返回格式异常，未找到回复内容。") from exc


def _to_candidates(ids: list[str]) -> list[AICandidate]:
    candidates: list[AICandidate] = []
    for cid in ids:
        ind = get_indicator(cid)
        if ind is not None:
            candidates.append(
                AICandidate(
                    id=ind.id,
                    name=ind.name,
                    level1=ind.level1,
                    description=ind.description,
                )
            )
    return candidates


def plan(messages: list[AIChatMessage]) -> AIPlanResponse:
    config = load_config()
    if config is None:
        return AIPlanResponse(
            action="not_configured",
            reply="尚未配置 AI 模型，请先点击右上角「设置」填写模型 API。",
        )

    system_content = f"{_context_brief()}\n\n{_SYSTEM_PROMPT}{_catalog_brief()}"
    llm_messages = [{"role": "system", "content": system_content}]
    llm_messages += [{"role": m.role, "content": m.content} for m in messages]

    try:
        raw = _call_llm(config, llm_messages)
        decision = _extract_json(raw)
    except (RuntimeError, json.JSONDecodeError) as exc:
        logger.warning("AI plan failed: %s", exc)
        return AIPlanResponse(action="error", reply=f"AI 处理失败：{exc}")

    action = decision.get("action")
    reply = str(decision.get("reply", "")).strip()

    if action in ("run", "collect"):
        indicator_id = decision.get("indicator_id")
        indicator = get_indicator(indicator_id) if indicator_id else None
        if indicator is None:
            return AIPlanResponse(
                action="clarify",
                reply=reply or "没能确定要调用哪个接口，请再补充一些信息。",
            )

        params = decision.get("params") or {}
        if not isinstance(params, dict):
            params = {}

        need = decision.get("need") or []
        need_names = {str(n) for n in need if isinstance(n, str)}

        # Auto-fill non-core (optional, or defaulted) params the model omitted.
        for spec in indicator.params:
            if spec.name in params or spec.name in need_names:
                continue
            if spec.default not in (None, ""):
                params[spec.name] = spec.default

        # Safety net: any required param still missing a value must be collected
        # from the user even if the model forgot to flag it.
        for spec in indicator.params:
            if spec.required and not _has_value(params.get(spec.name)):
                need_names.add(spec.name)

        # Keep every param the model flagged for the user — including ones it
        # pre-filled with a *suggested* value (e.g. an inferred code or date),
        # so the frontend can show them as editable / acceptable fields.
        form = [spec for spec in indicator.params if spec.name in need_names]

        if form:
            return AIPlanResponse(
                action="collect",
                reply=reply
                or f"我可以帮你提取「{indicator.name}」，请确认下面的参数后开始。",
                indicator_id=indicator.id,
                indicator_name=indicator.name,
                params=params,
                form=form,
            )

        return AIPlanResponse(
            action="run",
            reply=reply or f"已为你匹配到「{indicator.name}」，正在获取数据…",
            indicator_id=indicator.id,
            indicator_name=indicator.name,
            params=params,
        )

    if action == "reject":
        return AIPlanResponse(
            action="reject",
            reply=reply or "目录中暂无能满足该需求的接口。",
        )

    # default: clarify
    raw_candidates = decision.get("candidates") or []
    candidate_ids = [str(c) for c in raw_candidates if isinstance(c, (str, int))]
    raw_quick = decision.get("quick_replies") or []
    quick_replies = [str(q).strip() for q in raw_quick if isinstance(q, (str, int)) and str(q).strip()]
    return AIPlanResponse(
        action="clarify",
        reply=reply or "请再补充一些信息，方便我为你匹配合适的数据接口。",
        candidates=_to_candidates(candidate_ids),
        quick_replies=quick_replies[:6],
    )


def _has_value(value: Any) -> bool:
    return value not in (None, "")
