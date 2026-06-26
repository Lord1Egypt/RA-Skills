"""Model health tracking — probe, auto-skip dead models, substitute.

Health state is in-memory (per-process). Dead models get retried after
DEAD_TTL_S seconds in case NIM brings them back.
"""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from .models import MODELS, get_model

# In-memory health state
_dead_models: dict[str, float] = {}  # alias → timestamp when marked dead
DEAD_TTL_S = 300  # retry dead models after 5 minutes

HEALTH_PROBE = "Reply with exactly: OK"


@dataclass
class ModelHealth:
    alias: str
    model_id: str
    status: str     # "ok", "dead", "slow", "error"
    latency_s: float
    error: str = ""


def _mark_dead(alias: str):
    """Mark a model as dead (404/410). Will be retried after DEAD_TTL_S."""
    _dead_models[alias] = time.time()


def _is_dead(alias: str) -> bool:
    """Check if a model is marked dead (respects TTL for auto-retry)."""
    ts = _dead_models.get(alias)
    if ts is None:
        return False
    if time.time() - ts > DEAD_TTL_S:
        _dead_models.pop(alias, None)
        return False
    return True


def _get_substitute(alias: str) -> str | None:
    """Find a substitute model from the same speed tier but different family."""
    if alias not in MODELS:
        return None
    
    dead_info = MODELS[alias]
    dead_family = dead_info["family"]
    dead_speed = dead_info.get("speed", "medium")
    
    # Prefer same speed tier, different family, not dead
    candidates = []
    for a, m in MODELS.items():
        if a == alias:
            continue
        if _is_dead(a):
            continue
        if m.get("thinking"):  # don't substitute with thinking models (too slow)
            continue
        same_speed = m.get("speed") == dead_speed
        diff_family = m["family"] != dead_family
        candidates.append((a, same_speed, diff_family))
    
    # Sort: prefer same-speed + different-family, then any different-family
    candidates.sort(key=lambda x: (not x[1], not x[2]))
    return candidates[0][0] if candidates else None


def probe_model(alias: str) -> ModelHealth:
    """Probe a single model with a trivial question."""
    from .voter import call_model
    
    info = get_model(alias)
    t0 = time.time()
    
    try:
        ans, raw = call_model(HEALTH_PROBE, alias, max_tokens=10, temperature=0.0)
        latency = time.time() - t0
        
        if ans == "ERROR":
            if any(code in raw for code in ["HTTP 404", "HTTP 410"]):
                _mark_dead(alias)
                return ModelHealth(alias, info["id"], "dead", latency, raw[:100])
            return ModelHealth(alias, info["id"], "error", latency, raw[:100])
        
        if latency > 10:
            return ModelHealth(alias, info["id"], "slow", latency)
        
        # Clear dead status if model responds
        _dead_models.pop(alias, None)
        return ModelHealth(alias, info["id"], "ok", latency)
    
    except Exception as e:
        return ModelHealth(alias, info["id"], "error", time.time() - t0, str(e)[:100])


def health(models: list[str] = None, parallel: bool = True) -> dict[str, ModelHealth]:
    """Probe all (or specified) models and return health status.
    
    Returns:
        Dict mapping model alias → ModelHealth
    """
    aliases = models or list(MODELS.keys())
    results = {}
    
    if parallel:
        with ThreadPoolExecutor(max_workers=min(len(aliases), 10)) as pool:
            futures = {pool.submit(probe_model, a): a for a in aliases}
            for fut in as_completed(futures):
                alias = futures[fut]
                try:
                    results[alias] = fut.result()
                except Exception as e:
                    results[alias] = ModelHealth(alias, "", "error", 0, str(e)[:100])
    else:
        for alias in aliases:
            results[alias] = probe_model(alias)
    
    return results
