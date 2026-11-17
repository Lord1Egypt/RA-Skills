"""Model router for llm-core shared kernel.

Routes requests to the correct model adapter with error mapping and failover.
Shared between MCP and CLI forms.
"""
from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Optional, Type

from .adapters.base import BaseAdapter
from .error_map import ERROR_MAP, ERROR_INTERNAL, ERROR_PROVIDER_NOT_FOUND
from .types import ChatMessage, ChatResponse, ContentChunk


# Environment variable names for API keys
ENV_KEY_MAP: Dict[str, str] = {
    "deepseek": "DEEPSEEK_API_KEY",
    "tongyi": "DASHSCOPE_API_KEY",
    "zhipu": "ZHIPU_API_KEY",
    "kimi": "KIMI_API_KEY",
    "hunyuan": "HUNYUAN_SECRET_ID",
    "doubao": "DOUBAO_API_KEY",
    "minimax": "MINIMAX_API_KEY",
    "lingyi": "LINGYI_API_KEY",
    "baichuan": "BAICHUAN_API_KEY",
    "stepfun": "STEPFUN_API_KEY",
}

# Health check cache TTL (seconds)
HEALTH_CHECK_CACHE_TTL = 60


class ModelRouter:
    """Routes requests to the correct model adapter."""

    PROVIDER_REGISTRY: Dict[str, Type[BaseAdapter]] = {}

    def __init__(self, timeout: int = 30, failover: bool = True) -> None:
        self._adapters: Dict[str, BaseAdapter] = {}
        self._timeout = timeout
        self._failover = failover
        self._capability_scores: Dict[str, float] = {}
        self._health_cache: Dict[str, tuple] = {}
        self._load_capability_scores()

    def register_adapter(self, provider: str, adapter: BaseAdapter) -> None:
        self._adapters[provider] = adapter

    def register_all(self, config: Dict[str, Any]) -> Dict[str, bool]:
        from .adapters import (
            DeepSeekAdapter, TongYiAdapter, ZhiPuAdapter,
            KimiAdapter, HunYuanAdapter, DouBaoAdapter,
            MiniMaxAdapter, LingYiAdapter, BaichuanAdapter, StepFunAdapter,
        )
        mapping: Dict[str, Type[BaseAdapter]] = {
            "deepseek": DeepSeekAdapter,
            "tongyi": TongYiAdapter,
            "zhipu": ZhiPuAdapter,
            "kimi": KimiAdapter,
            "hunyuan": HunYuanAdapter,
            "doubao": DouBaoAdapter,
            "minimax": MiniMaxAdapter,
            "lingyi": LingYiAdapter,
            "baichuan": BaichuanAdapter,
            "stepfun": StepFunAdapter,
        }
        availability: Dict[str, bool] = {}
        for provider, cls in mapping.items():
            provider_cfg = config.get(provider, {})
            env_key = ENV_KEY_MAP.get(provider, "")
            api_key = os.environ.get(env_key, "") if env_key else ""
            if not api_key:
                api_key = provider_cfg.get("api_key", "")
            if not api_key:
                availability[provider] = False
                continue
            try:
                adapter = cls(api_key, **{k: v for k, v in provider_cfg.items() if k != "api_key"})
                self.register_adapter(provider, adapter)
                availability[provider] = True
            except Exception:
                availability[provider] = False
        return availability

    def get_adapter(self, provider: str) -> Optional[BaseAdapter]:
        return self._adapters.get(provider)

    def list_available(self) -> List[str]:
        return [p for p, a in self._adapters.items() if a.is_available()]

    def auto_select(self) -> Optional[str]:
        available = self.list_available()
        if not available:
            return None
        scored: List[tuple] = []
        for provider in available:
            score = self._get_capability_score(provider) * (1 if self._check_health_cached(provider) else 0)
            scored.append((provider, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[0][0] if scored else None

    def chat(self, messages: List[ChatMessage], provider: Optional[str] = None, **kwargs: Any) -> ChatResponse:
        if provider:
            return self._chat_with_provider(messages, provider, **kwargs)
        if not self._failover:
            return self._chat_with_provider(messages, self.auto_select(), **kwargs)
        sorted_providers = self._get_sorted_providers()
        last_error: Optional[Exception] = None
        for p in sorted_providers:
            try:
                return self._chat_with_provider(messages, p, **kwargs)
            except Exception as e:
                last_error = e
                continue
        raise RuntimeError(
            f"所有模型提供商均调用失败。已尝试: {sorted_providers}。最后错误: {last_error}"
        )

    def stream_chat(self, messages: List[ChatMessage], provider: Optional[str] = None, **kwargs: Any):
        if provider:
            yield from self._stream_with_provider(messages, provider, **kwargs)
            return
        if not self._failover:
            yield from self._stream_with_provider(messages, self.auto_select(), **kwargs)
            return
        sorted_providers = self._get_sorted_providers()
        last_error: Optional[Exception] = None
        for p in sorted_providers:
            try:
                yield from self._stream_with_provider(messages, p, **kwargs)
                return
            except Exception as e:
                last_error = e
                continue
        raise RuntimeError(
            f"所有模型提供商均调用失败。已尝试: {sorted_providers}。最后错误: {last_error}"
        )

    def _chat_with_provider(self, messages: List[ChatMessage], provider: str, **kwargs: Any) -> ChatResponse:
        adapter = self._adapters.get(provider)
        if not adapter:
            raise RuntimeError(f"未知的模型提供商: {provider}。支持的提供商: {list(self._adapters.keys())}")
        try:
            return adapter.chat(messages, **kwargs)
        except RuntimeError:
            raise
        except Exception as e:
            raise self._map_error(provider, str(e))

    def _stream_with_provider(self, messages: List[ChatMessage], provider: str, **kwargs: Any):
        adapter = self._adapters.get(provider)
        if not adapter:
            raise RuntimeError(f"未知的模型提供商: {provider}")
        try:
            yield from adapter.stream_chat(messages, **kwargs)
        except RuntimeError:
            raise
        except Exception as e:
            raise self._map_error(provider, str(e))

    def _get_sorted_providers(self) -> List[str]:
        available = self.list_available()
        scored: List[tuple] = []
        for provider in available:
            score = self._get_capability_score(provider) * (1 if self._check_health_cached(provider) else 0)
            scored.append((provider, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [p for p, _ in scored]

    def _load_capability_scores(self) -> None:
        try:
            import sqlite3
            from pathlib import Path
            db_path = str(Path.home() / ".cn-model-gateway" / "benchmark.db")
            if not Path(db_path).exists():
                return
            with sqlite3.connect(db_path) as conn:
                rows = conn.execute(
                    "SELECT provider, AVG(score) as avg_score FROM benchmark_results GROUP BY provider"
                ).fetchall()
            for row in rows:
                self._capability_scores[row[0]] = row[1]
        except Exception:
            pass

    def _get_capability_score(self, provider: str) -> float:
        return self._capability_scores.get(provider, 0.5)

    def _check_health_cached(self, provider: str) -> bool:
        now = time.time()
        if provider in self._health_cache:
            timestamp, result = self._health_cache[provider]
            if now - timestamp < HEALTH_CHECK_CACHE_TTL:
                return result
        adapter = self._adapters.get(provider)
        if not adapter:
            return False
        try:
            result = adapter.check_health()
        except Exception:
            result = False
        self._health_cache[provider] = (now, result)
        return result

    def _map_error(self, provider: str, error_msg: str) -> RuntimeError:
        provider_map = ERROR_MAP.get(provider, {})
        for pattern, info in provider_map.items():
            if pattern.lower() in error_msg.lower():
                return RuntimeError(f"[MCP {info['code']}] {info['message']}")
        return RuntimeError(f"[MCP {ERROR_INTERNAL}] {provider} 调用失败: {error_msg}")

    def compare_models(self, messages: List[ChatMessage], providers: Optional[List[str]] = None, **kwargs: Any) -> Dict[str, Any]:
        targets = providers or self.list_available()
        results: Dict[str, Any] = {}
        for p in targets:
            adapter = self._adapters.get(p)
            if not adapter or not adapter.is_available():
                results[p] = {"error": "不可用"}
                continue
            try:
                resp = adapter.chat(messages, **kwargs)
                results[p] = {
                    "content": resp.content, "model": resp.model,
                    "duration_ms": resp.duration_ms, "usage": resp.usage,
                }
            except Exception as e:
                results[p] = {"error": str(e)}
        return results
