"""MCP resources manager - catalog/usage snapshots + change subscriptions.

v2.1.0: standardized MCP resources allow frameworks (Claude Code / Cursor) to
READ the model catalog instead of hard-coding model names. Model onboarding /
offboarding no longer requires client config changes.

Resources:
  - models://catalog : capability / context window / archive price / updated date
  - usage://summary  : usage snapshot
  - cn-model-gateway://status : merged config + usage (legacy, kept)

Change subscription follows MCP spec:
  initialize declares resources.subscribe=true, listChanged=true.
  clients call resources/subscribe {uri}; server emits
  notifications/resources/updated when a snapshot's version changes.
"""
from __future__ import annotations

import hashlib
import json
import threading
import time
from typing import Any, Dict, List, Optional, Set

# Static catalog metadata (capability profile + context window + update date).
# Archive price comes from router.ARCHIVE_PRICES (single source).
CATALOG_META: Dict[str, Dict[str, Any]] = {
    "deepseek": {"context_window": 65536, "capabilities": ["chat", "code", "reasoning"], "updated": "2026-09-10", "default_model": "deepseek-chat"},
    "tongyi": {"context_window": 131072, "capabilities": ["chat", "vision", "embedding"], "updated": "2026-09-05", "default_model": "qwen-turbo"},
    "zhipu": {"context_window": 128000, "capabilities": ["chat", "vision", "embedding", "rerank"], "updated": "2026-09-08", "default_model": "glm-4"},
    "kimi": {"context_window": 200000, "capabilities": ["chat", "long-context"], "updated": "2026-09-01", "default_model": "moonshot-v1-8k"},
    "hunyuan": {"context_window": 256000, "capabilities": ["chat", "vision"], "updated": "2026-09-12", "default_model": "hunyuan"},
    "doubao": {"context_window": 128000, "capabilities": ["chat", "vision", "audio"], "updated": "2026-09-06", "default_model": "doubao-pro-32k"},
    "minimax": {"context_window": 200000, "capabilities": ["chat", "long-context"], "updated": "2026-09-03", "default_model": "abab6.5s-chat"},
    "lingyi": {"context_window": 128000, "capabilities": ["chat"], "updated": "2026-08-28", "default_model": "yi-lightning"},
    "baichuan": {"context_window": 32000, "capabilities": ["chat"], "updated": "2026-08-25", "default_model": "Baichuan4"},
    "stepfun": {"context_window": 200000, "capabilities": ["chat", "code"], "updated": "2026-09-02", "default_model": "step-1-8k"},
}

MODELS_CATALOG_URI = "models://catalog"
USAGE_SUMMARY_URI = "usage://summary"
STATUS_URI = "cn-model-gateway://status"


class ResourceManager:
    """Generates resource snapshots and manages subscriptions / change notices."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, Set[str]] = {}
        self._versions: Dict[str, str] = {}
        self._lock = threading.Lock()
        # Initialize versions from current snapshots so first subscribe is stable.
        self._versions[MODELS_CATALOG_URI] = self._hash(self.catalog_snapshot({}))
        self._versions[USAGE_SUMMARY_URI] = self._hash({})

    @staticmethod
    def _hash(obj: Any) -> str:
        raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]

    # --- snapshot generators ---

    def catalog_snapshot(self, adapters: Dict[str, Any], archive_prices: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """Build models://catalog snapshot: capability / context / price / updated date."""
        prices = archive_prices or {}
        models: List[Dict[str, Any]] = []
        for provider, meta in CATALOG_META.items():
            adapter = adapters.get(provider)
            available = bool(adapter and adapter.is_available())
            models.append({
                "provider": provider,
                "default_model": (getattr(adapter, "default_model", "") or meta["default_model"]),
                "available": available,
                "capabilities": meta["capabilities"],
                "context_window": meta["context_window"],
                "archive_price_per_1m": prices.get(provider),
                "updated": meta["updated"],
            })
        return {
            "uri": MODELS_CATALOG_URI,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "count": len(models),
            "models": models,
        }

    def usage_snapshot(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Build usage://summary snapshot."""
        return {
            "uri": USAGE_SUMMARY_URI,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "today": stats.get("today", {}),
            "total": stats.get("total", {}),
            "by_provider": stats.get("by_provider", {}),
            "concurrency_limit": stats.get("concurrency_limit"),
        }

    # --- subscription management ---

    def subscribe(self, uri: str, client_id: str) -> bool:
        with self._lock:
            self._subscribers.setdefault(uri, set()).add(client_id)
        return True

    def unsubscribe(self, uri: str, client_id: str) -> bool:
        with self._lock:
            subs = self._subscribers.get(uri)
            if subs:
                subs.discard(client_id)
                if not subs:
                    self._subscribers.pop(uri, None)
        return True

    def is_subscribed(self, uri: str, client_id: str) -> bool:
        return client_id in self._subscribers.get(uri, set())

    def subscriber_ids(self) -> List[str]:
        ids: Set[str] = set()
        for subs in self._subscribers.values():
            ids |= subs
        return sorted(ids)

    # --- change notification ---

    def refresh_version(self, uri: str, snapshot: Any) -> List[str]:
        """Update a resource version; return client IDs to notify if changed.

        Only subscribed clients are returned. This is called after tool calls
        that may mutate usage/config state.
        """
        new_hash = self._hash(snapshot)
        with self._lock:
            old_hash = self._versions.get(uri)
            self._versions[uri] = new_hash
            if old_hash == new_hash:
                return []
            return sorted(self._subscribers.get(uri, set()))

    def get_version(self, uri: str) -> str:
        return self._versions.get(uri, "")
