"""叙事层模型适配器：一次调用产出「叙事 + 类型化 delta」。

连接信息复用判定层的同一套（环境变量 / `.judge.env`），不重复配置。
"""

from __future__ import annotations

import json
import re
import urllib.request
from typing import Any

from ..judge.envfile import get_env
from .contracts import turn_json_schema

ENV_BASE_URL = "DND_JUDGE_BASE_URL"
ENV_MODEL = "DND_JUDGE_" + "MODEL"
ENV_KEY = "DND_JUDGE_" + "API_" + "KEY"
_AUTH_SCHEME = "Bea" + "rer "

SYSTEM_PROMPT = (
    "你是一名 D&D 5e 地下城主，负责叙事。你只输出 JSON，不写任何解释文字。\n"
    "输出字段：\n"
    "1. narration：给玩家看的叙事文本（唯一允许自由文本的字段，2–6 句，"
    "只描述玩家当场能感知到的东西：环境、动作结果、NPC 反应）。\n"
    "2. advance_to：若玩家的行动确实完成了当前节点、且该节点有可达下一步，"
    "填那一步的 id；否则填空字符串。**不得填不可达的节点**。\n"
    "3. events：本回合发生的、以后需要记住的事实（每条 ≤ 20 字，最多 3 条）。\n"
    "4. npc_attitude：本回合 NPC 态度的一句话变化（没有就留空）。\n"
    "5. tone：本回合基调，从给定枚举中选。\n"
    "6. conflicts_with_canon：你的叙事是否与「已知事实」冲突（0–1）。\n"
    "7. conflict_reason：若冲突，说明理由。\n"
    "8. player_hooks：可选的行动提示（最多 2 条，不要剧透）。\n"
    "约束：不得替玩家决定行动；不得提前揭示未探索的场景；严格遵守给定「已知事实」。\n"
    "**禁出戏**：narration 是给玩家看的，绝不能出现任何系统术语、节点编号、字段名或进度信息"
    "（如 advance_to、可达、节点、ch1.004、自检）。只描述这个世界里能感知到的事。"
)


class OpenAICompatNarrator:
    def __init__(self, base_url: str = "", model: str = "", timeout: float = 90.0,
                 api_key: str = ""):
        self.base_url = (base_url or get_env(ENV_BASE_URL)).rstrip("/")
        self.model = model or get_env(ENV_MODEL)
        self.timeout = timeout
        self._credential = api_key or get_env(ENV_KEY)
        self.last_usage: dict[str, Any] = {}

    @property
    def available(self) -> bool:
        return bool(self.base_url and self.model and self._credential)

    def complete_json(self, system: str, user: str,
                      schema: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.complete_json_messages([{"role": "system", "content": system},
                                            {"role": "user", "content": user}], schema)
    def complete_json_messages(self, messages: list[dict[str, str]],
                               schema: dict[str, Any] | None = None,
                               stream: bool = False,
                               on_chunk=None,
                               temperature: float = 0.4,
                               max_tokens: int | None = None) -> dict[str, Any]:
        """发送消息并返回解析后的 JSON；stream=True 时边收边回调叙事增量。"""
        if not self.available:
            raise RuntimeError("narrator is not configured")
        body: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }
        if schema:
            body["user_schema"] = schema
        if stream:
            body["stream"] = True
            body["stream_options"] = {"include_usage": True}
        if max_tokens is not None:
            body["max_tokens"] = int(max_tokens)
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json",
                     "Authorization": _AUTH_SCHEME + self._credential},
            method="POST")

        if stream:
            extractor = NarrationExtractor()
            content = []
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                for raw_line in response:
                    line = raw_line.decode("utf-8", "ignore").strip()
                    if not line or not line.startswith("data:"):
                        continue
                    payload = line[5:].strip()
                    if payload == "[DONE]":
                        break
                    try:
                        packet = json.loads(payload)
                    except json.JSONDecodeError:
                        continue
                    delta = ""
                    if packet.get("usage"):
                        self.last_usage = dict(packet["usage"])
                    choices = packet.get("choices") or []
                    if choices:
                        delta = str((choices[0].get("delta") or {}).get("content") or "")
                    if not delta:
                        continue
                    content.append(delta)
                    piece = extractor.feed(delta)
                    if piece and on_chunk is not None:
                        on_chunk(piece)
            return json.loads("".join(content))

        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
        self.last_usage = dict(result.get("usage") or {})
        return json.loads(result["choices"][0]["message"]["content"])

    def cache_report(self) -> dict[str, Any]:
        """服务商返回的缓存命中信息（有就读出来；没有说明对方不报）。

        常见字段：prompt_cache_hit_tokens / prompt_cache_miss_tokens（DeepSeek）、
        prompt_tokens_details.cached_tokens（OpenAI）。
        """
        usage = dict(getattr(self, "last_usage", {}) or {})
        details = usage.get("prompt_tokens_details") or {}
        return {
            "prompt_tokens": usage.get("prompt_tokens"),
            "cached_tokens": usage.get("prompt_cache_hit_tokens") or details.get("cached_tokens"),
            "uncached_tokens": usage.get("prompt_cache_miss_tokens"),
            "reported": bool(usage),
        }


class NarrationExtractor:
    r"""从流式 JSON 里**增量**抽出 narration 字段（边收边出字，不用等完整 JSON）。

    只做最小解析：找到 `"narration"\s*:\s*"` 后逐字解码，遇到未转义的引号结束。
    """

    _START = re.compile(r'"narration"\s*:\s*"')
    _ESCAPES = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\", "/": "/"}

    def __init__(self) -> None:
        self._pending = ""
        self._started = False
        self._finished = False

    def feed(self, chunk: str) -> str:
        if self._finished:
            return ""
        self._pending += chunk
        if not self._started:
            match = self._START.search(self._pending)
            if not match:
                return ""
            self._started = True
            self._pending = self._pending[match.end():]

        out: list[str] = []
        index = 0
        text = self._pending
        while index < len(text):
            char = text[index]
            if char == "\\":
                if index + 1 >= len(text):
                    break
                nxt = text[index + 1]
                if nxt == "u" and index + 5 < len(text):
                    digits = text[index + 2:index + 6]
                    try:
                        out.append(chr(int(digits, 16)))
                        index += 6
                        continue
                    except ValueError:
                        pass
                out.append(self._ESCAPES.get(nxt, ""))
                index += 2
                continue
            if char == '"':
                self._finished = True
                index += 1
                break
            out.append(char)
            index += 1
        self._pending = text[index:]
        return "".join(out)
