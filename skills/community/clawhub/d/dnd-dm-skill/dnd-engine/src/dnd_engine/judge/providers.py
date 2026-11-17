"""判定层实现的可插拔选择。

判定层之上（compose / bridge / API）只依赖"回答问题"这一个能力，
因此模型可以随时替换，而不改动上层逻辑：

  none/rules  → 纯规则查表（不需要任何模型）
  openai      → OpenAI 兼容 chat/completions（+ JSON Schema 强制输出）
  http        → 通用"类型化判定服务"适配器（见下）
  scripted    → 离线脚本（测试/演示）

`http` 适配器的契约由本层定义，与具体厂商无关：
    POST <url>
      {"state": ..., "action": ..., "questions": [{"id","type","instructions","criteria"}]}
    → {"answers": {id: {"value": ..., "confidence": 0.0-1.0, "probabilities": {...}?}}}
凡符合该契约的"类型化判定模型"（含未来的 System One 类 API）都可直接接入，
判定层以上无需改动。
"""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Any

from .client import OpenAICompatJudge, ScriptedJudge
from .contracts import Question
from .envfile import describe_env_source, env_file_path, get_env

PROVIDER_ENV = "DND_JUDGE_PROVIDER"
HTTP_URL_ENV = "DND_JUDGE_HTTP_URL"


class HttpQuestionsProvider:
    """通用类型化判定服务适配器（契约见模块 docstring）。"""

    def __init__(self, url: str = "", timeout: float = 30.0):
        self.url = url or get_env(HTTP_URL_ENV)
        self.timeout = timeout

    @property
    def available(self) -> bool:
        return bool(self.url)

    def __call__(self, questions: list[Question], state: dict[str, Any],
                 action: str, repair_hint: str = "") -> dict[str, Any]:
        if not self.available:
            raise RuntimeError("judge http provider is not configured")
        body: dict[str, Any] = {
            "state": state,
            "action": action,
            "questions": [q.to_json() for q in questions],
        }
        if repair_hint:
            body["repair_hint"] = repair_hint
        request = urllib.request.Request(
            self.url, data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))


def resolve_provider(name: str | None = None, **kwargs: Any):
    """按名称/环境变量选择判定层实现；返回 None 表示走纯规则路径。"""
    selected = (name or get_env(PROVIDER_ENV) or "").strip().lower()
    if selected in ("", "none", "rules", "rule"):
        return None
    if selected in ("openai", "openai-compat"):
        allowed = {"base_url", "model", "timeout", "api_key"}
        return OpenAICompatJudge(**{k: v for k, v in kwargs.items() if k in allowed})
    if selected == "http":
        allowed = {"url", "timeout"}
        return HttpQuestionsProvider(**{k: v for k, v in kwargs.items() if k in allowed})
    if selected == "scripted":
        return ScriptedJudge(kwargs.get("script") or {"answers": {}})
    raise ValueError(f"unknown judge provider: {selected}")


def describe_providers() -> dict[str, Any]:
    """诊断：当前选中的实现与可用项。"""
    return {
        "env_var": PROVIDER_ENV,
        "selected": get_env(PROVIDER_ENV),
        "selected_source": describe_env_source(PROVIDER_ENV),
        "http_env_var": HTTP_URL_ENV,
        "http_url_set": bool(get_env(HTTP_URL_ENV)),
        "env_file": str(env_file_path()),
        "available": ["none", "openai", "http", "scripted"],
    }
