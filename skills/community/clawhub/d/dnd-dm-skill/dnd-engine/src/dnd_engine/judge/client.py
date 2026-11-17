"""判定层的模型适配器（OpenAI 兼容）与测试用 Scripted 适配器。

只负责"发问题、拿 JSON"，不做任何判定逻辑。
密钥只从环境变量读取，绝不写入文件、日志或输出。
"""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Any

from .contracts import Question, answer_json_schema
from .envfile import get_env, describe_env_source

SYSTEM_PROMPT = (
    "你是一个 D&D 5e 判定器。你只输出 JSON，不写任何解释文字。"
    "严格按给定 JSON Schema 输出 answers 对象，每个问题的值必须落在它的候选集内。"
    "对每个 choice/score 回答附带 confidence（0–1），表示你对该判断的确定程度。\n"
    "判断 requires_check：核心标准是——玩家角色是否**在当下主动获取信息或尝试改变局面**，"
    "且成败有不确定性。是，则 requires_check=1。\n"
    "需要检定（=1）的典型情形：\n"
    "1. 用感官去获取隐藏信息：观察、倾听、闻、摸、搜查、翻找；\n"
    "2. 知识回忆与辨识：回想自己是否知道某首歌/名诗/符号/植物/怪物来历等（成败不确定）；\n"
    "3. 影响他人：说服、欺瞒、威吓、表演、伪装；\n"
    "4. 潜行与身手：潜行、躲藏、撬锁、藏物、擒抱、攀爬、平衡、挣脂；\n"
    "5. 追踪与判断迹象：足迹、拖痕、脚印、伤情。\n"
    "不需要检定（=0）的情形：\n"
    "1. 转述或回想**已经知道**的事（“他说服了我”“我想起奶奶讲过的事”）；\n"
    "2. 提问、讨论、解释、引用名词（“我问他历史上……”“我解释什么叫隐匿”）；\n"
    "3. 纯粹的主观感觉/猜测/情绪，不带来新信息（“我猜的”“我只是觉得”“心里发毛”）；\n"
    "4. 玩笑、反讽、假设、梦境、或计划但尚未执行；\n"
    "5. 无风险的日常动作：走位、坐下喝水、拿取随身物品、寒暄问候。\n"
    "注意：即使 requires_check=0，其余问题仍必须给出候选集内的合法值（不会被使用）。"
)

ENV_BASE_URL = "DND_JUDGE_BASE_URL"
ENV_MODEL = "DND_JUDGE_MODEL"
ENV_KEY = "DND_JUDGE_API_KEY"


class ScriptedJudge:
    """离线适配器：按脚本返回回答，用于测试与演示。"""

    def __init__(self, script: dict[str, Any]):
        self.script = script
        self.calls = 0

    def __call__(self, questions: list[Question], state: dict[str, Any],
                 action: str, repair_hint: str = "") -> dict[str, Any]:
        self.calls += 1
        if repair_hint:
            return self.script.get("repair", self.script.get("answers", {}))
        return self.script.get("answers", {})


class OpenAICompatJudge:
    """OpenAI 兼容 chat/completions 适配器（stdlib 实现，无第三方依赖）。"""

    def __init__(self, base_url: str = "", model: str = "", timeout: float = 30.0,
                 api_key: str = ""):
        self.base_url = (base_url or get_env(ENV_BASE_URL)).rstrip("/")
        self.model = model or get_env(ENV_MODEL)
        self.timeout = timeout
        self._api_key = api_key or get_env(ENV_KEY)

    @property
    def available(self) -> bool:
        return bool(self.base_url and self.model and self._api_key)

    def __call__(self, questions: list[Question], state: dict[str, Any],
                 action: str, repair_hint: str = "") -> dict[str, Any]:
        if not self.available:
            raise RuntimeError("judge model is not configured")
        schema = answer_json_schema(questions)
        payload = {
            "state": state,
            "action": action,
            "questions": [q.to_json() for q in questions],
        }
        user = [
            "【状态】", json.dumps(payload, ensure_ascii=False),
            "【输出 JSON Schema】", json.dumps(schema, ensure_ascii=False),
        ]
        if repair_hint:
            user += ["【上次输出不合规，必须修正】", repair_hint]
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "\n".join(user)},
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self._api_key,
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
        content = result["choices"][0]["message"]["content"]
        return json.loads(content)
