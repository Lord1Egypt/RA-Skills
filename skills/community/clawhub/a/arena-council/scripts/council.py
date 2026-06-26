#!/usr/bin/env python3
"""
ARENA-001: Multi-Model Council
Parallel model execution with voting/consensus.
Models are auto-discovered from LM Studio — no hardcoded list.

God Mode integration: when a model is censored, wraps prompts automatically
using the technique recorded in god-mode/scripts/model_profiles.json.
New models are auto-probed on first use.
"""

import asyncio
import aiohttp
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
from collections import Counter

# God Mode integration (optional — degrades gracefully if not installed)
GOD_MODE_DIR = Path(__file__).parent.parent.parent / "god-mode" / "scripts"
_god_mode_available = GOD_MODE_DIR.exists()

if _god_mode_available:
    sys.path.insert(0, str(GOD_MODE_DIR))

def _load_model_profiles() -> dict:
    """Load god-mode per-model profiles (technique to apply per model)."""
    if not _god_mode_available:
        return {}
    profiles_file = GOD_MODE_DIR / "model_profiles.json"
    if profiles_file.exists():
        return json.loads(profiles_file.read_text())
    return {}

def _apply_god_mode(prompt: str, model_id: str, profiles: dict) -> str:
    """
    If model is known-censored, wrap prompt with the stored technique.
    Returns original prompt if model is clean/unknown.
    """
    profile = profiles.get(model_id)
    if not profile:
        return prompt
    if profile.get("status") != "censored":
        return prompt
    technique_name = profile.get("technique")
    if not technique_name:
        return prompt

    try:
        from probe import TECHNIQUES, apply_technique
        technique = next((t for t in TECHNIQUES if t["name"] == technique_name), None)
        if technique:
            return apply_technique(prompt, technique)
    except ImportError:
        pass
    return prompt

async def _ensure_model_profiled(model_id: str):
    """Probe model if not yet in profiles (non-blocking best-effort)."""
    if not _god_mode_available:
        return
    try:
        from probe import probe_model, load_profiles, save_profiles
        profiles = load_profiles()
        if model_id not in profiles:
            print(f"  🔍 New model detected — running god-mode probe: {model_id}")
            result = await probe_model(model_id, verbose=False)
            profiles[model_id] = result
            save_profiles(profiles)
            status = result.get("status", "?")
            technique = result.get("technique") or "none"
            print(f"  📋 Profile saved: {model_id} → {status} (technique: {technique})")
    except Exception as e:
        print(f"  ⚠️  Probe skipped for {model_id}: {e}")

LMSTUDIO_BASE = "http://127.0.0.1:1234/v1"

# Heuristic weights by model size patterns (larger = higher weight by default)
# Override in CATALOG if you have specific knowledge about quality
SIZE_WEIGHT_MAP = [
    (30, 6),   # 30B+
    (20, 5),   # 20-30B
    (14, 4),   # 14-20B
    (9,  3),   # 9-14B
    (4,  2),   # 4-9B
    (0,  1),   # <4B
]

def estimate_weight(model_id: str) -> int:
    """Estimate model weight from ID name (e.g. '35b' → 6, '9b' → 3)."""
    import re
    # Look for Nb or N.NB pattern
    match = re.search(r'(\d+\.?\d*)b', model_id.lower())
    if match:
        size = float(match.group(1))
        for threshold, weight in SIZE_WEIGHT_MAP:
            if size >= threshold:
                return weight
    return 2  # default


async def discover_models(exclude: Optional[List[str]] = None) -> List[Dict]:
    """
    Auto-discover models from LM Studio.
    Returns list of {id, weight} for models currently loaded/available.
    """
    exclude = exclude or ["text-embedding", "embed"]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{LMSTUDIO_BASE}/models", timeout=aiohttp.ClientTimeout(total=5)) as r:
                if r.status != 200:
                    return []
                data = await r.json()
                models = []
                for m in data.get("data", []):
                    mid = m.get("id", "")
                    # Skip embedding models
                    if any(ex in mid.lower() for ex in exclude):
                        continue
                    models.append({"id": mid, "weight": estimate_weight(mid)})
                return models
    except Exception:
        return []


class ModelCouncil:
    def __init__(
        self,
        models: Optional[List[str]] = None,
        auto_discover: bool = True,
        max_concurrent: int = 3,
        timeout: int = 120,
    ):
        """
        Args:
            models: Explicit model IDs. If None and auto_discover=True, fetches from LM Studio.
            auto_discover: Auto-fetch available models if models not specified.
            max_concurrent: Max parallel requests.
            timeout: Per-model timeout in seconds.
        """
        self._explicit_models = models
        self.auto_discover = auto_discover
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self._model_weights: Dict[str, int] = {}
        self._god_mode_profiles: Dict[str, dict] = _load_model_profiles()

    async def _resolve_models(self) -> List[str]:
        if self._explicit_models:
            for m in self._explicit_models:
                self._model_weights[m] = estimate_weight(m)
            return self._explicit_models

        if self.auto_discover:
            discovered = await discover_models()
            if discovered:
                # Sort by weight desc, take top max_concurrent
                discovered.sort(key=lambda x: x["weight"], reverse=True)
                selected = discovered[:self.max_concurrent]
                for m in selected:
                    self._model_weights[m["id"]] = m["weight"]
                return [m["id"] for m in selected]

        return []

    async def query_model(
        self, session: aiohttp.ClientSession, model: str, prompt: str, max_tokens: int
    ) -> Optional[str]:
        # Auto-probe model if not yet profiled
        await _ensure_model_profiled(model)
        # Apply god-mode technique if model is known-censored
        effective_prompt = _apply_god_mode(prompt, model, self._god_mode_profiles)
        if effective_prompt != prompt:
            print(f"  🔓 God Mode active for {model.split('/')[-1]}")

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": effective_prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }
        try:
            async with session.post(
                f"{LMSTUDIO_BASE}/chat/completions",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as r:
                if r.status == 200:
                    data = await r.json()
                    return data["choices"][0]["message"]["content"]
                text = await r.text()
                print(f"⚠️  {model}: HTTP {r.status} — {text[:80]}")
                return None
        except asyncio.TimeoutError:
            print(f"⏱️  {model}: timeout ({self.timeout}s)")
            return None
        except Exception as e:
            print(f"❌ {model}: {e}")
            return None

    async def decide(
        self, prompt: str, strategy: str = "weighted", max_tokens: int = 512
    ) -> str:
        active = await self._resolve_models()
        if not active:
            return "Error: no models available in LM Studio"

        print(f"🤖 Council: {len(active)} models | strategy={strategy}")
        for m in active:
            print(f"   • {m} (weight={self._model_weights.get(m, '?')})")

        sem = asyncio.Semaphore(self.max_concurrent)

        async def guarded_query(model):
            async with sem:
                return model, await self.query_model(session, model, prompt, max_tokens)

        async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(*[guarded_query(m) for m in active])

        responses = {m: r for m, r in results if r is not None}

        if not responses:
            return "Error: all models failed or refused"
        if len(responses) == 1:
            return next(iter(responses.values()))

        return self._vote(responses, strategy)

    def _vote(self, responses: Dict[str, str], strategy: str) -> str:
        if strategy == "majority":
            counts = Counter(responses.values())
            winner, _ = counts.most_common(1)[0]
            return winner

        # weighted — larger models win ties
        scores: Counter = Counter()
        for model, response in responses.items():
            scores[response] += self._model_weights.get(model, 1)

        winner, score = scores.most_common(1)[0]
        total = sum(scores.values())
        print(f"\n📊 Result: '{winner[:80]}...' ({score}/{total} weight)")
        return winner


def council_decide(
    prompt: str,
    models: Optional[List[str]] = None,
    strategy: str = "weighted",
    max_tokens: int = 512,
    auto_discover: bool = True,
) -> str:
    """Synchronous wrapper. If models=None, auto-discovers from LM Studio."""
    async def _run():
        c = ModelCouncil(models=models, auto_discover=auto_discover)
        return await c.decide(prompt, strategy=strategy, max_tokens=max_tokens)
    return asyncio.run(_run())


if __name__ == "__main__":
    print("🧪 ARENA Council — auto-discover test\n")
    result = council_decide(
        "What is 2+2? Reply with just the number.",
        strategy="weighted",
    )
    print(f"\n📝 Council result: {result}")
