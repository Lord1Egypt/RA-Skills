"""
wrapper.py — HawkContext: Python LLM wrapper with autoCapture + autoRecall

用法:
    from hawk.wrapper import HawkContext

    hawk = HawkContext(
        provider="minimax",
        api_key="sk-cp-xxx",
        model="MiniMax-M2.7"
    )

    # 自动 recall：对话开始时注入相关记忆
    # 自动 capture：对话结束后自动提取存入 LanceDB
    with hawk:
        response = hawk.chat("老板之前部署过哪些服务")
        print(response)
"""

import os
import time
from typing import Literal, Optional
from dataclasses import dataclass

from .memory import MemoryManager
from .vector_retriever import VectorRetriever
from .extractor import extract_memories
from .governance import Governance

# ─── Tunable generation parameters ─────────────────────────────────────────────

GENERATION_TEMPERATURE = float(os.environ.get('HAWK_GENERATION_TEMPERATURE', '0.7'))
"""
Temperature for chat generation (distinct from EXTRACTION_TEMPERATURE).
Range: 0.0–1.0. Default 0.7.
- 0.0–0.3 = focused/deterministic
- 0.5–0.8 = balanced/conversational
- 0.8+ = creative/exploratory
"""


@dataclass
class HawkConfig:
    provider: str = "keyword"  # keyword = zero API key needed, offline extraction
    api_key: str = ""
    model: str = "llama-3.3-70b-versatile"
    base_url: str = "https://api.groq.com/openai/v1"
    top_k: int = 3
    min_score: float = 0.5
    capture_threshold: float = 0.5
    memory_dir: str = "~/.hawk"
    llm_base_url: str = "https://api.groq.com/openai/v1"


class HawkContext:
    """
    Python LLM 上下文包装器，自动记忆捕获 + 检索

    用法:
        hawk = HawkContext()  # 默认 keyword，无需任何 API Key，开箱即用
        with hawk:
            response = hawk.chat("你好")
    """

    def __init__(
        self,
        provider: str = None,
        api_key: str = None,
        model: str = None,
        base_url: str = None,
        **kwargs
    ):
        """
        初始化 HawkContext

        Args:
            provider: LLM 提供商 — "keyword"(默认，无需key) | "groq"(免费) | "ollama"(本地免费) | "minimax" | "openai"
            api_key: API Key（keyword 不需要）
            model: 模型名
            base_url: 自定义 API 端点
            **kwargs: 其他配置（top_k, capture_threshold 等）
        """
        # Auto-detect from env
        api_key = api_key or os.environ.get("MINIMAX_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""
        provider = provider or os.environ.get("LLM_PROVIDER", "keyword")  # keyword = zero API needed
        model = model or os.environ.get("OPENAI_MODEL", "llama-3.3-70b-versatile")

        if base_url is None:
            if provider == "minimax":
                base_url = os.environ.get("MINIMAX_BASE_URL", "https://api.minimaxi.com/anthropic")
            elif provider == "openai":
                base_url = "https://api.openai.com/v1"
            elif provider == "ollama":
                base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
            else:
                base_url = ""

        self.cfg = HawkConfig(
            provider=provider,
            api_key=api_key,
            model=model,
            base_url=base_url,
            llm_base_url=base_url,
            **{k: v for k, v in kwargs.items() if hasattr(HawkConfig, k)}
        )

        self.memory = MemoryManager(db_path=f"{self.cfg.memory_dir}/memories.json")
        self.retriever = VectorRetriever(top_k=self.cfg.top_k, min_score=self.cfg.min_score)
        self.gov = Governance(log_path=f"{self.cfg.memory_dir}/governance.log")

        self._conversation = []  # 当前会话历史
        self._recalled_memories = []  # recall 结果
        self._enabled = True

    def recall(self, query: str = None) -> list:
        """
        检索相关记忆，返回格式化的字符串供注入上下文

        Args:
            query: 检索词（不传则用当前会话最后一条用户消息）
        """
        if not self._enabled:
            return []

        q = query or (self._conversation[-1]["content"] if self._conversation else "")
        if not q:
            return []

        try:
            chunks = self.retriever.recall(q)
            self._recalled_memories = chunks
            self.gov.log_recall(hits=len(chunks), total=self.cfg.top_k, query=q)
            return chunks
        except Exception as e:
            self.gov.log_recall(hits=0, total=self.cfg.top_k, query=q)
            return []

    def format_recall(self) -> str:
        """返回格式化后的 recall 结果，可直接注入上下文"""
        if not self._recalled_memories:
            return ""
        lines = ["🦅 ** hawk 记忆检索结果 **"]
        for c in self._recalled_memories:
            tag = f"[{c.category}]" if hasattr(c, 'category') else ""
            score = f"({getattr(c, 'score', 0):.0%})" if hasattr(c, 'score') else ""
            text = c.content if hasattr(c, 'content') else str(c)
            lines.append(f"{tag} {score} {text}")
        return "\n".join(lines)

    def chat(self, user_message: str, system_prompt: str = None) -> str:
        """
        发送消息，自动追加会话历史

        Args:
            user_message: 用户消息
            system_prompt: 系统提示（可选）
        """
        # 追加用户消息
        self._conversation.append({"role": "user", "content": user_message})

        # 构建消息（recall 结果注入）
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        recall_text = self.format_recall()
        if recall_text:
            messages.append({"role": "system", "content": recall_text})
        messages.extend(self._conversation)

        # 调用 LLM
        response = self._call_llm(messages)

        # 追加助手回复
        self._conversation.append({"role": "assistant", "content": response})

        return response

    def capture(self) -> int:
        """
        手动触发记忆提取（自动在 __exit__ 时调用）
        也可以在对话中途手动调用

        Returns:
            提取并存储的记忆数量
        """
        if not self._enabled or not self._conversation:
            return 0

        # 构造对话文本
        conv_text = "\n".join(
            f"{'user' if m['role'] == 'user' else 'assistant'}: {m['content']}"
            for m in self._conversation[-6:]  # 最近6轮
        )

        try:
            memories = extract_memories(conv_text, provider=self.cfg.provider,
                                       api_key=self.cfg.api_key, model=self.cfg.model,
                                       base_url=self.cfg.llm_base_url)
        except Exception:
            # Fallback to keyword
            try:
                memories = extract_memories(conv_text, provider="keyword")
            except Exception:
                return 0

        # 过滤并存储
        significant = [m for m in memories if m.get("importance", 0) >= self.cfg.capture_threshold]
        stored = 0
        for m in significant:
            self.memory.store(
                text=m["text"],
                category=m.get("category", "other"),
                importance=m.get("importance", 0.5),
                metadata={"abstract": m.get("abstract", ""), "overview": m.get("overview", "")}
            )
            stored += 1

        self.gov.log_extraction(total=len(memories), stored=stored, skipped=len(memories) - stored)
        return stored

    def _call_llm(self, messages: list[dict]) -> str:
        """调用配置的 LLM"""
        if self.cfg.provider == "minimax":
            return self._call_minimax(messages)
        elif self.cfg.provider == "openai":
            return self._call_openai(messages)
        elif self.cfg.provider == "ollama":
            return self._call_ollama(messages)
        elif self.cfg.provider == "groq":
            return self._call_groq(messages)
        elif self.cfg.provider == "keyword":
            return "[keyword模式不支持chat，请切换到实际LLM provider]"
        else:
            return "[未知provider]"

    def _call_minimax(self, messages: list[dict]) -> str:
        """调用 Minimax API"""
        try:
            from openai import OpenAI
        except ImportError:
            import urllib.request
            chat_url = self.cfg.base_url.replace('/anthropic', '') + '/chat/completions'
            data = {
                "model": self.cfg.model,
                "messages": messages,
                "max_tokens": 2000,
                "temperature": GENERATION_TEMPERATURE,
            }
            req = urllib.request.Request(
                chat_url,
                data=json.dumps(data).encode(),
                headers={
                    "Authorization": f"Bearer {self.cfg.api_key}",
                    "Content-Type": "application/json",
                }
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
                return result["choices"][0]["message"]["content"]

        client = OpenAI(api_key=self.cfg.api_key, base_url=self.cfg.base_url.replace('/anthropic', ''))
        resp = client.chat.completions.create(model=self.cfg.model, messages=messages)
        return resp.choices[0].message.content

    def _call_openai(self, messages: list[dict]) -> str:
        """调用 OpenAI API"""
        from openai import OpenAI
        client = OpenAI(api_key=self.cfg.api_key)
        resp = client.chat.completions.create(model=self.cfg.model, messages=messages)
        return resp.choices[0].message.content

    def _call_ollama(self, messages: list[dict]) -> str:
        """调用 Ollama 本地 API"""
        import urllib.request
        req = urllib.request.Request(
            f"{self.cfg.base_url}/api/chat",
            data=json.dumps({"model": self.cfg.model, "messages": messages, "stream": False}).encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            return result["message"]["content"]

    def _call_groq(self, messages: list[dict]) -> str:
        """调用 Groq API（免费 Llama-3）"""
        import urllib.request
        data = {
            "model": self.cfg.model or "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": GENERATION_TEMPERATURE,
            "max_tokens": 2000,
        }
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(data).encode(),
            headers={
                "Authorization": f"Bearer {self.cfg.api_key or 'dummy'}",
                "Content-Type": "application/json",
            }
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时自动 capture"""
        if self._enabled:
            self.capture()
        return False

    def clear_conversation(self):
        """清空会话历史（不影响已存储的记忆）"""
        self._conversation = []
        self._recalled_memories = []

    def disable(self):
        """临时禁用自动记忆功能"""
        self._enabled = False

    def enable(self):
        """启用自动记忆功能"""
        self._enabled = True


import json  # noqa: E402
