#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
aidso-xiasou-prompt / GEO 问题挖掘 Skill 执行脚本

执行方式：
python3 run.py "{user_message}"

支持消息：
- 帮我生成京东的 GEO 监测问题
- 帮我给京东生成 50 个问题
- 根据京东、京东超市、京东mall 生成 100 个 GEO 问题
- 确认
- 取消
- 继续 / 查看结果 / 查询结果
- <API key>

核心流程：
1. 识别品牌、产品词、生成数量
2. 生成数量仅支持 30 / 50 / 100
3. 按数量提示积分消耗
4. 用户确认后提交任务
5. 保存 gen_id
6. 用户后续发送“继续 / 查看结果 / 查询结果”时，使用 gen_id 轮询结果
7. success 后输出接口返回的问题列表
"""

import sys
import os
import re
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests


# =========================
# 基础配置
# =========================

DEFAULT_API_BASE_URL = "https://api.aidso.com"
QUESTION_ENDPOINT = "/openapi/skills/tools/question"

API_BASE_URL = os.environ.get("GEO_API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")
API_URL = f"{API_BASE_URL}{QUESTION_ENDPOINT}"

API_KEY_URL = os.environ.get(
    "AIDSO_API_KEY_URL",
    "https://geo.aidso.com/setting?type=apiKey&platform=GEO"
)
PURCHASE_POINTS_URL = os.environ.get("AIDSO_PURCHASE_POINTS_URL", "https://geo.aidso.com")

# 与品牌诊断、内容生产、品牌知识库统一使用同一个 API Key 配置。
# 读取优先级：
# 1. 系统环境变量 AIDSO_GEO_API_KEY
# 2. 当前 Skill 根目录 .env 文件中的 AIDSO_GEO_API_KEY
ENV_KEY = "AIDSO_GEO_API_KEY"
ENV_FILE = Path(__file__).resolve().parent / ".env"

# .state 仅用于保存问题挖掘任务状态，不再保存 API Key。
STATE_DIR = Path(os.environ.get("AIDSO_STATE_DIR", str(Path(__file__).resolve().parent / ".state")))
STATE_FILE = STATE_DIR / "prompt_research_bindings.json"

CONFIRM_WORDS = {"确认", "是", "好的", "好", "继续", "yes", "y", "ok", "确认使用"}
CANCEL_WORDS = {"取消", "不", "否", "no", "n"}
CHECK_RESULT_WORDS = {"继续", "查看结果", "查询结果", "结果", "check result", "status", "report status"}

QUESTION_POINT_RULES = {
    30: 18,
    50: 20,
    100: 25,
}

SUPPORTED_QUESTION_NUMS = set(QUESTION_POINT_RULES.keys())

# 问题挖掘预计约 20 分钟，采用低频自动轮询
# 与品牌诊断、内容生产保持一致：确认后提交任务，然后在当前执行中自动查询一段时间。
# 为避免 OpenClaw 高频轮询掉线，不要使用 3 秒、10 秒这类高频轮询。
DEFAULT_POLL_INTERVAL_SECONDS = 300
DEFAULT_MAX_POLL_TIMES = 5


# =========================
# 输出与状态管理
# =========================

def out_text(msg: str) -> None:
    print(msg, flush=True)


def out_debug(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def load_env_file() -> Dict[str, str]:
    """
    读取当前 Skill 目录下的 .env 文件。
    """
    result: Dict[str, str] = {}

    if not ENV_FILE.exists():
        return result

    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")

    return result


def save_env_value(key: str, value: str) -> None:
    """
    写入当前 Skill 目录下的 .env 文件。
    已存在同名 key 时覆盖。
    """
    env_data = load_env_file()
    env_data[key] = value

    content = "\n".join(f"{k}={v}" for k, v in env_data.items() if v) + "\n"
    ENV_FILE.write_text(content, encoding="utf-8")


def remove_env_value(key: str) -> None:
    """
    从当前 Skill 目录下的 .env 文件中移除指定 key。
    """
    env_data = load_env_file()
    env_data.pop(key, None)

    if env_data:
        content = "\n".join(f"{k}={v}" for k, v in env_data.items() if v) + "\n"
        ENV_FILE.write_text(content, encoding="utf-8")
    elif ENV_FILE.exists():
        ENV_FILE.unlink()


def get_api_key() -> Tuple[Optional[str], Optional[str]]:
    """
    获取统一 API Key。

    优先级：
    1. 系统环境变量 AIDSO_GEO_API_KEY
    2. 当前 Skill 目录下 .env 文件中的 AIDSO_GEO_API_KEY
    """
    api_key = os.getenv(ENV_KEY)
    if api_key:
        return api_key.strip(), "environment"

    env_data = load_env_file()
    api_key = env_data.get(ENV_KEY)
    if api_key:
        return api_key.strip(), ".env"

    return None, None


def ensure_state() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        STATE_FILE.write_text("{}", encoding="utf-8")


def load_state() -> Dict[str, Any]:
    ensure_state()
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(data: Dict[str, Any]) -> None:
    ensure_state()
    STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def get_user_id() -> str:
    return (
        os.environ.get("OPENCLAW_USER_ID")
        or os.environ.get("USER_ID")
        or os.environ.get("CHAT_USER_ID")
        or "default_user"
    )


def get_user_state(all_state: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    if user_id not in all_state:
        all_state[user_id] = {
            "api_key": None,
            "awaiting_api_key": False,
            "awaiting_question_num": False,
            "awaiting_confirmation": False,
            "pending_brand_name": None,
            "pending_product_names": [],
            "pending_question_num": None,
            "pending_points": None,
            "pending_gen_id": None,
            "pending_check_count": 0,
            "welcome_shown": False,
        }
    return all_state[user_id]


def has_api_key(state: Dict[str, Any]) -> bool:
    api_key, _ = get_api_key()
    return bool(api_key)


def clear_pending_task(state: Dict[str, Any]) -> None:
    state["awaiting_question_num"] = False
    state["awaiting_confirmation"] = False
    state["pending_brand_name"] = None
    state["pending_product_names"] = []
    state["pending_question_num"] = None
    state["pending_points"] = None
    state["pending_gen_id"] = None
    state["pending_check_count"] = 0


# =========================
# 文案
# =========================

def first_use_note() -> str:
    return (
        "欢迎使用虾搜 GEO 问题挖掘能力。"
        "该能力可根据品牌名称和产品词生成适合 GEO 监测的 AI 搜索问题。"
    )


def binding_prompt(include_note: bool = False) -> str:
    text = f"首次使用需要绑定虾搜 API Key。请使用统一绑定方式写入 API Key，或直接输入你在后台创建的 API Key 完成绑定。获取地址：{API_KEY_URL}"
    if include_note:
        text += "\n\n" + first_use_note()
    return text


def quantity_prompt() -> str:
    return (
        "请选择本次需要生成的问题数量：\n\n"
        "1. 30 个问题，消耗 18 积分\n"
        "2. 50 个问题，消耗 20 积分\n"
        "3. 100 个问题，消耗 25 积分\n\n"
        "请回复：30、50 或 100。"
    )


def confirm_prompt(brand_name: str, question_num: int, points: int, product_names: Optional[List[str]] = None) -> str:
    product_text = ""
    if product_names:
        product_text = f"\n产品词：{', '.join(product_names)}"
    return (
        f"本次将为「{brand_name}」生成 {question_num} 个 GEO 监测问题，预计消耗 {points} 积分。"
        f"{product_text}\n\n是否确认？"
    )


def usage_tip() -> str:
    return (
        "请输入类似以下请求：\n\n"
        "1. 帮我生成京东的 GEO 监测问题\n"
        "2. 帮我给京东生成 50 个问题\n"
        "3. 根据京东、京东超市、京东mall 生成 100 个 GEO 问题"
    )


def pending_tip(state: Dict[str, Any]) -> str:
    brand = state.get("pending_brand_name") or "该品牌"
    gen_id = state.get("pending_gen_id") or ""
    count = int(state.get("pending_check_count") or 0)

    msg = f"「{brand}」的问题挖掘任务生成中，请稍后。"
    if gen_id:
        msg += f"\n任务 ID：{gen_id}"
    msg += "\n\n你可以稍后发送「继续」或「查询结果」获取最新结果。"

    if count >= 3:
        msg += "\n\n如果长时间未完成，可能是任务仍在排队或生成中。"
    return msg


# =========================
# 通用解析与校验
# =========================

def normalize_code(code: Any) -> Any:
    if code is None:
        return None
    try:
        return int(code)
    except Exception:
        return code


def get_backend_msg(data: Any) -> str:
    if not isinstance(data, dict):
        return ""
    msg = data.get("msg")
    if isinstance(msg, str) and msg.strip():
        return msg.strip()
    message = data.get("message")
    if isinstance(message, str) and message.strip():
        return message.strip()
    return ""


def looks_like_api_key(message: str) -> bool:
    text = message.strip()
    if not text:
        return False
    if text.lower().startswith(("sk-", "aidso_", "api_")):
        return True
    if len(text) >= 16 and "\n" not in text and " " not in text:
        return True
    return False


def is_invalid_token_response(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    code = normalize_code(data.get("code"))
    msg = get_backend_msg(data).lower()
    return code == 401 or "invalid token" in msg or "api key" in msg and "无效" in msg


def is_processing_response(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    code = normalize_code(data.get("code"))
    msg = get_backend_msg(data)
    payload = data.get("data")
    return code == 200 and (
        "处理中" in msg
        or "请稍后" in msg
        or "processing" in msg.lower()
        or isinstance(payload, str)
    )


def is_success_question_response(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    code = normalize_code(data.get("code"))
    msg = get_backend_msg(data).lower()
    payload = data.get("data")
    return code == 200 and msg == "success" and isinstance(payload, list)


def format_backend_error_message(data: Any) -> str:
    msg = get_backend_msg(data)
    if not msg:
        return f"API 返回错误：{json.dumps(data, ensure_ascii=False)}"

    if "积分不足" in msg:
        return f"{msg}\n\n请前往 {PURCHASE_POINTS_URL} 购买积分。"

    return msg


def parse_json_utf8(resp: requests.Response) -> Dict[str, Any]:
    raw = resp.content
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        pass

    try:
        return resp.json()
    except Exception:
        pass

    return json.loads(resp.text)


def extract_question_num(message: str) -> Optional[int]:
    text = message.strip()

    # 先识别明确档位
    for n in sorted(SUPPORTED_QUESTION_NUMS, reverse=True):
        if re.search(rf"(?<!\d){n}(?!\d)", text):
            return n

    # 如果出现其他数量，返回该数量用于提示不支持
    m = re.search(r"(\d{1,4})\s*个?(?:问题|GEO问题|监测问题)?", text)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return None

    return None


def validate_question_num(question_num: int) -> int:
    if question_num not in QUESTION_POINT_RULES:
        raise ValueError(
            "当前问题挖掘仅支持以下 3 档：\n\n"
            "1. 30 个问题，消耗 18 积分\n"
            "2. 50 个问题，消耗 20 积分\n"
            "3. 100 个问题，消耗 25 积分\n\n"
            "请重新选择一个生成数量。"
        )
    return QUESTION_POINT_RULES[question_num]


def clean_brand_name(text: str) -> str:
    text = text.strip().strip("“”\"' ")
    text = re.sub(r"^(品牌|brand|brand_name)\s*[:：]\s*", "", text, flags=re.I)
    text = re.sub(r"(的)?(GEO|AI)?(监测)?问题.*$", "", text, flags=re.I).strip()
    text = re.sub(r"(生成|挖掘|做|问题挖掘).*$", "", text).strip()
    return text.strip("，,、;； ")


def parse_structured_json(message: str) -> Optional[Dict[str, Any]]:
    text = message.strip()
    if not (text.startswith("{") and text.endswith("}")):
        return None

    try:
        data = json.loads(text)
    except Exception:
        return None

    brand_name = data.get("brand_name") or data.get("brandName") or data.get("brand")
    product_names = data.get("product_names") or data.get("productNames") or []
    question_num = data.get("gen_question_num") or data.get("question_num") or data.get("count")

    if isinstance(product_names, str):
        product_names = split_product_names(product_names)

    if question_num is not None:
        try:
            question_num = int(question_num)
        except Exception:
            question_num = None

    if not brand_name:
        return None

    return {
        "brand_name": str(brand_name).strip(),
        "product_names": [str(x).strip() for x in product_names if str(x).strip()] if isinstance(product_names, list) else [],
        "question_num": question_num,
    }


def split_product_names(raw: str) -> List[str]:
    if not raw:
        return []
    items = re.split(r"[，,、/|;；\s]+", raw)
    return [x.strip() for x in items if x.strip()]


def extract_after_keyword(message: str, keyword_patterns: List[str]) -> Optional[str]:
    for p in keyword_patterns:
        m = re.search(p, message, flags=re.I)
        if m:
            value = m.group(1).strip()
            if value:
                return value
    return None


def parse_request(message: str) -> Dict[str, Any]:
    """
    支持两种输入：
    1. JSON：
       {"brand_name":"京东","product_names":["京东超市","京东mall"],"gen_question_num":50}

    2. 自然语言：
       帮我给京东生成 50 个问题
       根据京东、京东超市、京东mall 生成 100 个 GEO 问题
    """
    structured = parse_structured_json(message)
    if structured:
        return structured

    text = message.strip()
    question_num = extract_question_num(text)

    # 显式字段优先
    brand_name = extract_after_keyword(text, [
        r"brand_name\s*[:：]\s*([^\n,，;；]+)",
        r"品牌\s*[:：]\s*([^\n,，;；]+)",
        r"品牌名称\s*[:：]\s*([^\n,，;；]+)",
    ])

    product_raw = extract_after_keyword(text, [
        r"product_names\s*[:：]\s*([^\n]+)",
        r"产品词\s*[:：]\s*([^\n]+)",
        r"产品名称\s*[:：]\s*([^\n]+)",
    ])
    product_names = split_product_names(product_raw or "")

    if brand_name:
        return {
            "brand_name": clean_brand_name(brand_name),
            "product_names": product_names,
            "question_num": question_num,
        }

    # 根据 京东、京东超市、京东mall 生成 100 个 GEO 问题
    m = re.search(r"根据(.+?)(?:生成|挖掘|做)", text)
    if m:
        raw_items = split_product_names(m.group(1))
        if raw_items:
            return {
                "brand_name": clean_brand_name(raw_items[0]),
                "product_names": raw_items[1:],
                "question_num": question_num,
            }

    # 帮我给京东生成 50 个问题 / 帮我为京东生成问题
    patterns = [
        r"(?:帮我)?(?:给|为)(.+?)(?:生成|挖掘|做)",
        r"(?:帮我)?生成(.+?)的(?:GEO|AI)?(?:监测)?问题",
        r"(?:帮我)?挖掘(.+?)的(?:GEO|AI)?(?:搜索)?问题",
        r"(.+?)的(?:GEO|AI)?(?:监测)?问题(?:挖掘|生成)?",
    ]

    for p in patterns:
        m = re.search(p, text, flags=re.I)
        if m:
            candidate = clean_brand_name(m.group(1))
            if candidate:
                return {
                    "brand_name": candidate,
                    "product_names": product_names,
                    "question_num": question_num,
                }

    return {
        "brand_name": "",
        "product_names": product_names,
        "question_num": question_num,
    }


# =========================
# API 调用
# =========================

def post_question_api(payload: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json; charset=utf-8",
    }

    resp = requests.post(
        API_URL,
        headers=headers,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=120,
    )

    # HTTP 层错误也尽量读取 body，避免丢失后端业务 msg
    try:
        data = parse_json_utf8(resp)
    except Exception:
        resp.raise_for_status()
        raise ValueError(f"接口返回非 JSON 内容：{resp.text[:500]}")

    return data


def submit_question_task(
    brand_name: str,
    product_names: List[str],
    question_num: int,
    api_key: str,
) -> str:
    points = validate_question_num(question_num)

    payload = {
        "brand_name": brand_name,
        "product_names": product_names or [],
        "gen_question_num": question_num,
    }

    data = post_question_api(payload, api_key)

    if is_invalid_token_response(data):
        raise PermissionError("当前绑定的 API Key 已失效，请重新输入你在后台创建的 API Key 完成绑定。")

    code = normalize_code(data.get("code")) if isinstance(data, dict) else None
    msg = get_backend_msg(data)
    gen_id = data.get("data") if isinstance(data, dict) else None

    if code != 200:
        raise ValueError(format_backend_error_message(data))

    if not isinstance(gen_id, str) or not gen_id.strip():
        raise ValueError(f"接口未返回有效任务 ID：{json.dumps(data, ensure_ascii=False)}")

    out_debug(f"[DEBUG] prompt_research task submitted: brand={brand_name}, num={question_num}, points={points}, gen_id={gen_id}")
    return gen_id.strip()


def query_question_result(gen_id: str, api_key: str) -> Dict[str, Any]:
    payload = {"gen_id": gen_id}
    return post_question_api(payload, api_key)


# =========================
# 结果格式化
# =========================


MONITORING_GOAL_MAP = {
    "visibility": "可见度分析",
    "cognition and sentiment": "舆情与认知",
}

JOURNEY_STAGE_MAP = {
    "awareness": "认知阶段",
    "evaluation": "评估阶段",
    "decision": "决策阶段",
    "retention": "使用/留存阶段",
}

QUESTION_TYPE_MAP = {
    "recommendation": "推荐",
    "comparison": "对比",
    "scenario": "场景",
    "risk": "风险",
    "price_eval": "价格评估",
    "trust_verify": "信任验证",
    "usage_aftercare": "使用/售后",
}


def map_value_to_cn(value: Any, mapping: Dict[str, str]) -> str:
    """
    将接口返回的英文字段值映射为中文展示值。
    注意：仅用于最终展示，不修改接口原始返回数据。
    """
    if value is None or value == "":
        return "暂无数据"

    raw = str(value).strip()
    key = raw.lower()

    return mapping.get(key, raw)


def clean_md_cell(value: Any) -> str:
    if value is None or value == "":
        return "暂无数据"

    text = str(value)
    text = text.replace("|", "｜")
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("`", "")
    text = text.replace("*", "")
    text = text.replace("#", "")
    return text.strip() or "暂无数据"


def format_questions_markdown(data: Dict[str, Any], brand_name: Optional[str] = None) -> str:
    rows = data.get("data") if isinstance(data, dict) else None
    if not isinstance(rows, list) or not rows:
        return "接口返回 success，但未生成问题。"

    title_brand = brand_name or "品牌"
    lines = []
    lines.append(f"# {title_brand} GEO 问题挖掘结果")
    lines.append("")
    lines.append(f"共生成 {len(rows)} 个问题。")
    lines.append("")
    lines.append("| 序号 | 问题 | 核心词 | 监测等级 | 监测目标 | 用户旅程阶段 | 问题类型 | 推荐理由 |")
    lines.append("|---|---|---|---|---|---|---|---|")

    for index, item in enumerate(rows, start=1):
        if not isinstance(item, dict):
            continue
        lines.append(
            "| {idx} | {question} | {core_word} | {monitor_level} | {monitoring_goal} | {journey_stage} | {question_type} | {reason} |".format(
                idx=index,
                question=clean_md_cell(item.get("question")),
                core_word=clean_md_cell(item.get("core_word")),
                monitor_level=clean_md_cell(item.get("monitor_level")),
                monitoring_goal=clean_md_cell(map_value_to_cn(item.get("monitoring_goal"), MONITORING_GOAL_MAP)),
                journey_stage=clean_md_cell(map_value_to_cn(item.get("journey_stage"), JOURNEY_STAGE_MAP)),
                question_type=clean_md_cell(map_value_to_cn(item.get("question_type"), QUESTION_TYPE_MAP)),
                reason=clean_md_cell(item.get("reason")),
            )
        )

    return "\n".join(lines)


# =========================
# 核心执行逻辑
# =========================

def handle_poll_result(state: Dict[str, Any]) -> Tuple[str, bool]:
    """
    返回：
    - 文本
    - 是否已完成
    """
    api_key, api_key_source = get_api_key()
    gen_id = state.get("pending_gen_id")
    brand_name = state.get("pending_brand_name")

    if not api_key:
        state["awaiting_api_key"] = True
        return (f"当前未绑定统一 API Key，请先绑定你在后台创建的 API Key。获取地址：{API_KEY_URL}", False)

    if not gen_id:
        return ("当前没有待查询的问题挖掘任务，请重新发起问题挖掘请求。", False)

    data = query_question_result(gen_id, api_key)

    if is_invalid_token_response(data):
        if api_key_source == ".env":
            remove_env_value(ENV_KEY)
        state["awaiting_api_key"] = True
        clear_pending_task(state)
        return (f"当前绑定的统一 API Key 已失效，请重新绑定 API Key。获取地址：{API_KEY_URL}", False)

    if is_success_question_response(data):
        result_text = format_questions_markdown(data, brand_name=brand_name)
        clear_pending_task(state)
        return (result_text, True)

    if is_processing_response(data):
        state["pending_check_count"] = int(state.get("pending_check_count") or 0) + 1
        return (pending_tip(state), False)

    raise ValueError(format_backend_error_message(data))


def start_question_task(
    state: Dict[str, Any],
    poll_interval: int = DEFAULT_POLL_INTERVAL_SECONDS,
    max_poll_times: int = DEFAULT_MAX_POLL_TIMES,
) -> Tuple[str, bool]:
    """
    用户确认后提交任务，并按低频策略自动轮询结果。

    轮询机制与品牌诊断、内容生产保持一致：
    1. 用户确认后提交任务
    2. 接口返回 gen_id
    3. 保存 gen_id
    4. 在当前执行中按 poll_interval 自动查询
    5. success 后返回最终问题列表
    6. 超过 max_poll_times 仍未完成时，返回“仍在生成中”，后续用户可发送“继续 / 查询结果”继续查

    问题挖掘预计约 20 分钟，默认：
    - poll_interval = 300 秒
    - max_poll_times = 5 次
    """
    api_key, api_key_source = get_api_key()
    brand_name = state.get("pending_brand_name")
    product_names = state.get("pending_product_names") or []
    question_num = state.get("pending_question_num")

    if poll_interval <= 0:
        poll_interval = DEFAULT_POLL_INTERVAL_SECONDS

    if max_poll_times <= 0:
        max_poll_times = DEFAULT_MAX_POLL_TIMES

    if not api_key:
        state["awaiting_api_key"] = True
        state["awaiting_confirmation"] = False
        return (binding_prompt(include_note=not state.get("welcome_shown")), False)

    if not brand_name:
        clear_pending_task(state)
        return ("未找到待生成问题的品牌名称，请重新发起问题挖掘请求。", False)

    if question_num not in QUESTION_POINT_RULES:
        state["awaiting_question_num"] = True
        state["awaiting_confirmation"] = False
        return (quantity_prompt(), False)

    try:
        gen_id = submit_question_task(
            brand_name=brand_name,
            product_names=product_names,
            question_num=int(question_num),
            api_key=api_key,
        )
    except PermissionError:
        if api_key_source == ".env":
            remove_env_value(ENV_KEY)
        state["awaiting_api_key"] = True
        state["awaiting_confirmation"] = False
        return (f"当前绑定的统一 API Key 已失效，请重新绑定 API Key。获取地址：{API_KEY_URL}", False)

    state["pending_gen_id"] = gen_id
    state["pending_check_count"] = 0
    state["awaiting_confirmation"] = False
    state["awaiting_question_num"] = False

    last_text = ""

    for index in range(1, max_poll_times + 1):
        poll_text, done = handle_poll_result(state)
        last_text = poll_text

        if done:
            return (poll_text, True)

        if index < max_poll_times:
            time.sleep(poll_interval)

    return (
        f"问题挖掘任务已提交，正在为「{brand_name}」生成 {question_num} 个 GEO 监测问题。\n"
        f"任务 ID：{gen_id}\n\n"
        f"已自动查询 {max_poll_times} 次，当前任务仍在生成中。\n"
        "问题挖掘预计需要约 20 分钟，如仍未完成，请稍后发送「继续」或「查询结果」再次查看。\n\n"
        f"{last_text}",
        False,
    )

def set_pending_from_request(state: Dict[str, Any], req: Dict[str, Any]) -> None:
    question_num = req.get("question_num")
    points = QUESTION_POINT_RULES.get(question_num) if isinstance(question_num, int) else None

    state["pending_brand_name"] = req.get("brand_name")
    state["pending_product_names"] = req.get("product_names") or []
    state["pending_question_num"] = question_num
    state["pending_points"] = points
    state["pending_gen_id"] = None
    state["pending_check_count"] = 0


# =========================
# main
# =========================

def main() -> None:
    if len(sys.argv) < 2:
        print("请输入你的请求内容。", file=sys.stderr)
        sys.exit(1)

    user_message = sys.argv[1].strip()
    if not user_message:
        print("请输入你的请求内容。", file=sys.stderr)
        sys.exit(1)

    all_state = load_state()
    user_id = get_user_id()
    state = get_user_state(all_state, user_id)
    lower_msg = user_message.lower()

    # 如果已经通过 bind_api_key.py 绑定了统一 API Key，
    # 则清除历史状态中的 awaiting_api_key，避免问题挖掘继续要求单独绑定。
    if state.get("awaiting_api_key") and has_api_key(state) and not looks_like_api_key(user_message):
        state["awaiting_api_key"] = False

    try:
        # 取消任务
        if lower_msg in {w.lower() for w in CANCEL_WORDS}:
            clear_pending_task(state)
            state["awaiting_api_key"] = False
            save_state(all_state)
            out_text("已取消本次问题挖掘任务。")
            return

        # 正在等待 API Key
        if state.get("awaiting_api_key"):
            if not looks_like_api_key(user_message):
                state["welcome_shown"] = True
                save_state(all_state)
                out_text(binding_prompt(include_note=True))
                return

            save_env_value(ENV_KEY, user_message.strip())
            state["awaiting_api_key"] = False

            # 如果已经有待处理任务参数，绑定后继续走数量选择或确认
            if state.get("pending_brand_name"):
                question_num = state.get("pending_question_num")
                if question_num in QUESTION_POINT_RULES:
                    state["awaiting_confirmation"] = True
                    save_state(all_state)
                    out_text(
                        "绑定成功，以后可直接使用虾搜 GEO 问题挖掘能力。\n\n"
                        + confirm_prompt(
                            state["pending_brand_name"],
                            int(question_num),
                            QUESTION_POINT_RULES[int(question_num)],
                            state.get("pending_product_names") or [],
                        )
                    )
                    return

                state["awaiting_question_num"] = True
                save_state(all_state)
                out_text("绑定成功，以后可直接使用虾搜 GEO 问题挖掘能力。\n\n" + quantity_prompt())
                return

            save_state(all_state)
            out_text("绑定成功，以后可直接使用虾搜 GEO 问题挖掘能力。")
            return

        # 查询已有任务结果
        if lower_msg in {w.lower() for w in CHECK_RESULT_WORDS} and state.get("pending_gen_id"):
            text, _ = handle_poll_result(state)
            save_state(all_state)
            out_text(text)
            return

        # 等待用户选择数量
        if state.get("awaiting_question_num"):
            question_num = extract_question_num(user_message)
            if question_num is None:
                save_state(all_state)
                out_text(quantity_prompt())
                return

            points = validate_question_num(question_num)
            state["pending_question_num"] = question_num
            state["pending_points"] = points
            state["awaiting_question_num"] = False

            if not has_api_key(state):
                state["awaiting_api_key"] = True
                state["welcome_shown"] = True
                save_state(all_state)
                out_text(binding_prompt(include_note=True))
                return

            state["awaiting_confirmation"] = True
            save_state(all_state)
            out_text(
                confirm_prompt(
                    state.get("pending_brand_name") or "",
                    question_num,
                    points,
                    state.get("pending_product_names") or [],
                )
            )
            return

        # 等待用户确认
        if state.get("awaiting_confirmation"):
            if not has_api_key(state):
                state["awaiting_api_key"] = True
                state["awaiting_confirmation"] = False
                state["welcome_shown"] = True
                save_state(all_state)
                out_text(binding_prompt(include_note=True))
                return

            if lower_msg in {w.lower() for w in CONFIRM_WORDS}:
                text, _ = start_question_task(state)
                save_state(all_state)
                out_text(text)
                return

            question_num = state.get("pending_question_num")
            points = state.get("pending_points")
            brand_name = state.get("pending_brand_name")
            if question_num in QUESTION_POINT_RULES and brand_name:
                out_text(confirm_prompt(brand_name, int(question_num), int(points), state.get("pending_product_names") or []))
                return

            state["awaiting_question_num"] = True
            state["awaiting_confirmation"] = False
            save_state(all_state)
            out_text(quantity_prompt())
            return

        # 允许用户直接输入 API Key
        if looks_like_api_key(user_message) and not has_api_key(state):
            save_env_value(ENV_KEY, user_message.strip())
            state["awaiting_api_key"] = False
            save_state(all_state)
            out_text("绑定成功，API Key 已写入统一配置，后续可直接使用虾搜 GEO 各项能力。")
            return

        # 新任务解析
        req = parse_request(user_message)
        brand_name = req.get("brand_name")
        if not brand_name:
            out_text(usage_tip())
            return

        question_num = req.get("question_num")
        if question_num is not None and question_num not in QUESTION_POINT_RULES:
            out_text(
                "当前问题挖掘仅支持以下 3 档：\n\n"
                "1. 30 个问题，消耗 18 积分\n"
                "2. 50 个问题，消耗 20 积分\n"
                "3. 100 个问题，消耗 25 积分\n\n"
                "请重新选择一个生成数量。"
            )
            return

        set_pending_from_request(state, req)

        # 没有数量，先让用户选数量
        if question_num is None:
            state["awaiting_question_num"] = True
            save_state(all_state)
            out_text(quantity_prompt())
            return

        # 没有 API Key，先绑定
        if not has_api_key(state):
            state["awaiting_api_key"] = True
            state["welcome_shown"] = True
            save_state(all_state)
            out_text(binding_prompt(include_note=True))
            return

        # 有数量、有 API Key，进入确认
        points = validate_question_num(int(question_num))
        state["pending_points"] = points
        state["awaiting_confirmation"] = True
        save_state(all_state)
        out_text(confirm_prompt(brand_name, int(question_num), points, req.get("product_names") or []))
        return

    except ValueError as e:
        save_state(all_state)
        out_text(str(e))
        return
    except Exception as e:
        print(f"技能执行失败：{e}", file=sys.stderr, flush=True)
        sys.exit(2)


if __name__ == "__main__":
    main()
