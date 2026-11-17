# -*- coding: utf-8 -*-
# task_classifier_llm.py — 可选 LLM 任务分类器
#
# 设计原则（合规优先）：
#   - **默认不启用**：collect_usage_data.py 的 --task-classifier 默认为 heuristic，
#     本模块只有用户显式传 --task-classifier llm 且提供 --task-llm-endpoint 时才会被加载；
#   - **不内置任何第三方商业 API 默认值**：endpoint 由用户自备（本地 Ollama 的
#     http://localhost:11434/v1，或自有 OpenAI 兼容端点），不联网即零外部依赖；
#   - **失败安全**：任何网络/解析错误都会被 collect_task_types 捕获并回退启发式分类，
#     绝不中断采集。
#
# 用法示例（本地 Ollama）：
#   python scripts/collect_usage_data.py --task-classifier llm \
#       --task-llm-endpoint http://localhost:11434/v1 \
#       --task-llm-model qwen2.5:7b --period week -o data.json

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from ca_core import load_task_rules  # noqa: E402

__all__ = ["build_llm_classifier", "classify_text_with_llm"]

# 送入 LLM 的文本上限：分类只需主题信号，截断省 token
_MAX_TEXT_CHARS = 1500
_HTTP_TIMEOUT = 20  # 秒


def _available_types():
    types, _meta, _src = load_task_rules()
    return [t["name"] for t in types]


def _build_prompt(text, type_names):
    type_list = "、".join(type_names)
    system = (
        "你是 Agent 会话的任务类型分类器。把用户给出的会话内容归入以下类型之一："
        f"{type_list}。\n"
        "规则：\n"
        "1. 按内容的主要意图判断，不要被单个无关关键词带偏；\n"
        "2. 无法判断时回答「其他」；\n"
        "3. 只输出类型名称本身，不要输出任何解释、标点或引号。"
    )
    user = text[:_MAX_TEXT_CHARS]
    return system, user


def classify_text_with_llm(text, endpoint, model, api_key=None, timeout=_HTTP_TIMEOUT):
    """调 LLM 给单条会话文本分类。返回类型字符串；失败抛异常（由调用方兜底）。"""
    if not text or not text.strip():
        return "其他"
    type_names = _available_types()
    system, user = _build_prompt(text, type_names)

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0,
        "max_tokens": 16,
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    url = endpoint.rstrip("/") + "/chat/completions"
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        data = json.loads(resp.read().decode("utf-8"))

    raw = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
    answer = raw.strip().strip("\"'`「」『』。.，, ")
    # 严格白名单：LLM 返回不在类型表里时，尝试子串匹配，仍不行就归「其他」
    if answer in type_names:
        return answer
    for t in type_names:
        if t and (t in answer or answer in t):
            return t
    return "其他"


def build_llm_classifier(endpoint, model, api_key=None, timeout=_HTTP_TIMEOUT):
    """构造 classifier callable：f(text) -> task_type。

    endpoint 须为 OpenAI 兼容 /v1 根（如 http://localhost:11434/v1）。
    失败兜底约定：网络 / 响应异常在本层捕获（打印 WARN 后返回 ""），
    调用方 collect_task_types 据此回退启发式分类——异常边界只留在
    异常类型已知的本模块，避免宽泛 except。
    """
    if not endpoint:
        raise ValueError("LLM 分类器需要 --task-llm-endpoint（OpenAI 兼容 /v1 根地址）")
    if not model:
        raise ValueError("LLM 分类器需要 --task-llm-model（如本地 Ollama 的 qwen2.5:7b）")

    def _classify(text):
        try:
            return classify_text_with_llm(text, endpoint, model, api_key=api_key, timeout=timeout)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError,
                ValueError, KeyError, IndexError, json.JSONDecodeError,
                TimeoutError) as e:
            # urllib.error.HTTPError ⊂ URLError；socket.timeout ⊂ OSError
            print(f"[WARN] LLM 分类失败，本条回退启发式：{type(e).__name__}: {e}",
                  file=sys.stderr)
            return ""
        except re.error as e:  # 防御：响应被误当正则解析的场景
            print(f"[WARN] LLM 分类异常（re.error），本条回退启发式：{e}", file=sys.stderr)
            return ""

    return _classify
