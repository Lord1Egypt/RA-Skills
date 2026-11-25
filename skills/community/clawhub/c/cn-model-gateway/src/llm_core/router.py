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

# v2.1.0: archive prices (yuan per 1M tokens, blended input/output) for cheap strategy.
# Kept inside llm_core so the decision engine is a single self-contained source,
# independent of the upper-layer src/price_tracker scraping module.
ARCHIVE_PRICES: Dict[str, float] = {
    "deepseek": 1.5,
    "tongyi": 4.0,
    "zhipu": 10.0,
    "kimi": 12.0,
    "hunyuan": 10.0,
    "doubao": 6.0,
    "minimax": 0.75,
    "lingyi": 2.0,
    "baichuan": 0.5,
    "stepfun": 10.0,
}

VALID_STRATEGIES = ("auto", "cheap", "quality")


class ModelRouter:
    """Routes requests to the correct model adapter."""

    PROVIDER_REGISTRY: Dict[str, Type[BaseAdapter]] = {}

    def __init__(self, timeout: int = 30, failover: bool = True) -> None:
        self._adapters: Dict[str, BaseAdapter] = {}
        self._timeout = timeout
        self._failover = failover
        self._capability_scores: Dict[str, float] = {}
        self._health_cache: Dict[str, tuple] = {}
        self._key_pool = None  # v2.1.0: injected KeyPoolManager (optional)
        self._load_capability_scores()

    def set_key_pool(self, key_pool: Any) -> None:
        """v2.1.0: inject a KeyPoolManager for quota-aware key rotation."""
        self._key_pool = key_pool

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
                api_key = provider_cfg.get("api_key", provider_cfg.get("key", ""))
            # v2.1.0: accept array api_key (Key pool); adapter uses the first key,
            # rotation is handled by the injected KeyPoolManager. Legacy str unaffected.
            if isinstance(api_key, (list, tuple)):
                api_key = api_key[0] if api_key else ""
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

    # --- v2.1.0: single-source strategy selection ---
    def select(self, strategy: str = "auto") -> Optional[str]:
        """Select a provider by strategy. Single decision source shared by MCP & CLI.

        Strategies:
          - auto: capability profile × health cache (existing auto_select)
          - cheap: lowest archive price
          - quality: highest benchmark capability score (falls back to auto)
        Invalid strategies gracefully fall back to 'auto'.
        """
        strategy = (strategy or "auto").lower()
        if strategy not in VALID_STRATEGIES:
            strategy = "auto"
        if strategy == "cheap":
            return self._select_cheap()
        if strategy == "quality":
            return self._select_quality()
        return self.auto_select()

    def _select_cheap(self) -> Optional[str]:
        available = self.list_available()
        if not available:
            return None
        # Lowest price first; unknown price sorted last (stable by name).
        return min(
            available,
            key=lambda p: (ARCHIVE_PRICES.get(p, float("inf")), p),
        )

    def _select_quality(self) -> Optional[str]:
        available = self.list_available()
        if not available:
            return None
        # Highest benchmark score first; providers without a benchmark fall back
        # to capability default (0.5) then health, so quality never picks a dead node.
        candidates = [
            p for p in available
            if self._get_capability_score(p) > 0.5 or self._check_health_cached(p)
        ]
        pool = candidates or available
        return max(
            pool,
            key=lambda p: (self._get_capability_score(p), p),
        )

    def chat(self, messages: List[ChatMessage], provider: Optional[str] = None,
             strategy: Optional[str] = None, **kwargs: Any) -> ChatResponse:
        """Chat with routing.

        v2.1.0: when ``strategy`` is given and no explicit provider, the SAME
        ``select()`` decision engine is used here and by the MCP layer, so
        gateway and router always agree (single-source verification).
        """
        if strategy:
            selected = self.select(strategy)
            if not selected:
                raise RuntimeError("没有可用的模型提供商，无法按策略选择。")
            return self._chat_with_provider(messages, selected, **kwargs)
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

    def stream_chat(self, messages: List[ChatMessage], provider: Optional[str] = None,
                    strategy: Optional[str] = None, **kwargs: Any):
        if strategy:
            selected = self.select(strategy)
            if not selected:
                raise RuntimeError("没有可用的模型提供商，无法按策略选择。")
            yield from self._stream_with_provider(messages, selected, **kwargs)
            return
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

        # v2.1.0: multi-key rotation on quota/rate errors (429 storm → zero failure)
        if self._key_pool is not None and self._key_pool.has_pool(provider):
            def _call(key: str):
                adapter.api_key = key
                return adapter.chat(messages, **{k: v for k, v in kwargs.items() if k != "member"})
            try:
                result, used_key = self._key_pool.call_with_rotation(provider, _call)
                return result
            except Exception as e:
                raise self._map_error(provider, str(e))

        try:
            return adapter.chat(messages, **{k: v for k, v in kwargs.items() if k != "member"})
        except RuntimeError:
            raise
        except Exception as e:
            raise self._map_error(provider, str(e))

    def _stream_with_provider(self, messages: List[ChatMessage], provider: str, **kwargs: Any):
        adapter = self._adapters.get(provider)
        if not adapter:
            raise RuntimeError(f"未知的模型提供商: {provider}")
        # v2.1.0: for streaming, rotation applies at stream-establishment only;
        # mid-stream 429 is rare and chunk buffer handles reconnect.
        if self._key_pool is not None and self._key_pool.has_pool(provider):
            adapter.api_key = self._key_pool.current_key(provider) or adapter.api_key
        try:
            yield from adapter.stream_chat(messages, **{k: v for k, v in kwargs.items() if k != "member"})
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
