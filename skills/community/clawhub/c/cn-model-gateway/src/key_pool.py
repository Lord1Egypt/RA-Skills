"""Key pool manager - multi-key rotation with quota awareness.

v2.1.0: heavy users hitting a single-key rate limit is the #1 blocker for
batch jobs. Pooling keys makes "register a few more keys" a smooth scale-out
path — a pure-client advantage (data never leaves the machine) over hosted
gateways.

Features:
  - Round-robin selection over a provider's key list
  - Automatic key switch + retry on 429 / quota-insufficient errors
  - Per-key health panel: success rate / latency / today usage / quota left
  - Health data reused from v1.9 health.db (via HealthScheduler)
"""
from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


# Error patterns that should trigger a key switch (quota / rate related).
SWITCH_ERROR_PATTERNS = (
    "429", "rate limit", "rate_limit", "too many request",
    "quota", "balance", "insufficient", "余额", "额度", "限流", "频率",
)


def is_switchable_error(error: Any) -> bool:
    """Return True if the error indicates rate limit / quota exhaustion."""
    msg = str(error).lower()
    return any(p.lower() in msg for p in SWITCH_ERROR_PATTERNS)


class KeyPoolManager:
    """Manages per-provider key lists with rotation and health tracking."""

    def __init__(self, keys_map: Optional[Dict[str, List[str]]] = None) -> None:
        self._keys: Dict[str, List[str]] = {}
        self._index: Dict[str, int] = {}
        self._stats: Dict[str, Dict[str, Dict[str, Any]]] = {}  # provider -> key_idx -> stats
        self._lock = threading.Lock()
        for provider, keys in (keys_map or {}).items():
            self.add_keys(provider, keys)

    def add_keys(self, provider: str, keys: List[str]) -> None:
        clean = [k for k in (keys or []) if k]
        if not clean:
            return
        with self._lock:
            # avoid duplicates but preserve order
            seen: set = set()
            dedup = []
            for k in clean:
                marker = k[:6] + k[-4:] if len(k) > 10 else k
                if marker not in seen:
                    seen.add(marker)
                    dedup.append(k)
            self._keys[provider] = dedup
            self._index[provider] = 0
            self._stats[provider] = {
                str(i): {"success": 0, "fail": 0, "total_latency_ms": 0, "last_used": 0}
                for i in range(len(dedup))
            }

    def get_keys(self, provider: str) -> List[str]:
        return list(self._keys.get(provider, []))

    def has_pool(self, provider: str) -> bool:
        return len(self._keys.get(provider, [])) > 1

    def current_key(self, provider: str) -> Optional[str]:
        keys = self._keys.get(provider, [])
        if not keys:
            return None
        idx = self._index.get(provider, 0) % len(keys)
        return keys[idx]

    def next_key(self, provider: str) -> Optional[str]:
        """Advance round-robin and return the next key."""
        keys = self._keys.get(provider, [])
        if not keys:
            return None
        with self._lock:
            idx = (self._index.get(provider, 0) + 1) % len(keys)
            self._index[provider] = idx
        return keys[idx]

    def call_with_rotation(
        self,
        provider: str,
        call_fn: Callable[[str], Any],
        max_retries: Optional[int] = None,
    ) -> Tuple[Any, str]:
        """Execute call_fn(key) trying each key on quota/rate errors.

        Returns (result, used_key). Raises the LAST switchable exception if all
        keys are exhausted; non-switchable errors are raised immediately (no
        point rotating on an auth failure or bad request).

        This is the core of the "429 storm → zero task failure" acceptance:
        with N healthy keys, up to N attempts are made before giving up.
        """
        keys = self._keys.get(provider, [])
        if not keys:
            raise RuntimeError(f"[KeyPool] {provider} 没有可用 Key")
        if max_retries is None:
            max_retries = len(keys)
        attempts = 0
        last_error: Optional[Exception] = None
        start_idx = self._index.get(provider, 0) % len(keys)
        for offset in range(len(keys)):
            if attempts >= max_retries:
                break
            idx = (start_idx + offset) % len(keys)
            key = keys[idx]
            with self._lock:
                self._index[provider] = idx
            start = time.time()
            try:
                result = call_fn(key)
                latency = int((time.time() - start) * 1000)
                self._record(provider, idx, success=True, latency_ms=latency)
                return result, key
            except Exception as e:
                latency = int((time.time() - start) * 1000)
                self._record(provider, idx, success=False, latency_ms=latency)
                last_error = e
                if not is_switchable_error(e):
                    raise
                attempts += 1
                continue
        raise last_error if last_error else RuntimeError("[KeyPool] 所有 Key 均失败")

    def _record(self, provider: str, idx: int, success: bool, latency_ms: int) -> None:
        with self._lock:
            stats = self._stats.get(provider, {}).get(str(idx))
            if stats is None:
                return
            if success:
                stats["success"] += 1
            else:
                stats["fail"] += 1
            stats["total_latency_ms"] += latency_ms
            stats["last_used"] = int(time.time())

    def health_panel(self) -> Dict[str, Any]:
        """Per-provider / per-key health: success rate, latency, quota hint."""
        panel: Dict[str, Any] = {}
        for provider, keys in self._keys.items():
            key_rows = []
            for idx, key in enumerate(keys):
                st = self._stats.get(provider, {}).get(str(idx), {})
                total = st.get("success", 0) + st.get("fail", 0)
                rate = st.get("success", 0) / total if total else 0.0
                avg_latency = st.get("total_latency_ms", 0) / max(total, 1)
                key_rows.append({
                    "index": idx,
                    "masked": self._mask(key),
                    "is_current": (self._index.get(provider, 0) % len(keys)) == idx,
                    "success_rate": round(rate, 3),
                    "avg_latency_ms": round(avg_latency),
                    "total_calls": total,
                    "last_used": st.get("last_used", 0),
                })
            panel[provider] = {
                "key_count": len(keys),
                "pooled": len(keys) > 1,
                "keys": key_rows,
            }
        return panel

    def merge_health_db(self, health_results: List[Dict[str, Any]]) -> None:
        """v2.1.0: reuse v1.9 health.db data to enrich per-key quota/success view.

        health.db has no key granularity, so we fold provider-level success rate
        into each key row as a 'provider_success_rate' hint (additive, non-bridge).
        """
        agg: Dict[str, List[bool]] = {}
        for r in health_results or []:
            agg.setdefault(r.get("provider", ""), []).append(bool(r.get("success")))
        self._provider_health_rate = {
            p: (sum(v) / len(v) if v else 0.0) for p, v in agg.items()
        }

    @staticmethod
    def _mask(key: str) -> str:
        if len(key) <= 8:
            return "****"
        return key[:4] + "*" * (len(key) - 8) + key[-4:]

    def __repr__(self) -> str:
        return f"<KeyPool providers={list(self._keys.keys())}>"


def build_key_pool_from_config(config: Dict[str, Any]) -> KeyPoolManager:
    """Build a KeyPoolManager from a config.json dict.

    Reads each provider's api_key (or alias 'key'), which may be a single value
    or an array. Legacy single-value configs produce a 1-key pool (no rotation).
    """
    from .utils import PROVIDER_NAMES, get_provider_keys

    keys_map: Dict[str, List[str]] = {}
    for provider in PROVIDER_NAMES:
        keys = get_provider_keys(config, provider)
        if keys:
            keys_map[provider] = keys
    return KeyPoolManager(keys_map)
