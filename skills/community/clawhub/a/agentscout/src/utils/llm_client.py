"""LLM 调用封装 - OpenAI 兼容协议"""

import json
import re
from typing import Optional
from openai import OpenAI

from src.config import LLMConfig


class LLMClient:
    """通用 LLM 客户端，支持任意 OpenAI 兼容 API"""

    def __init__(self, config: LLMConfig):
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
        )
        self.model = config.model
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens

    def chat(
        self,
        prompt: str,
        system: str = "",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """单轮对话，返回文本"""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens,
        )
        return response.choices[0].message.content.strip()

    def chat_json(
        self,
        prompt: str,
        system: str = "",
        temperature: Optional[float] = None,
    ) -> dict:
        """对话并解析 JSON 输出"""
        raw = self.chat(prompt, system, temperature)
        # 尝试从 markdown 代码块中提取 JSON
        json_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
        if json_match:
            raw = json_match.group(1).strip()
        return json.loads(raw)
