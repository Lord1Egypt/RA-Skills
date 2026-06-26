"""Online ELO scoring for model selection.

Each scale() call logs model votes. Disagreement = free training signal.
Models that agree with majority get +points, dissenters get -points.
User feedback (override) is a 10× stronger signal.

State persisted to ~/.cache/free-scaling/elo.json
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import Lock

STATE_DIR = Path(os.environ.get("FREE_SCALING_STATE_DIR",
                                os.path.expanduser("~/.cache/free-scaling")))
STATE_FILE = STATE_DIR / "elo.json"

_lock = Lock()

# --- Config ---
INITIAL_ELO = 1200
K_CONSENSUS = 16       # ELO K-factor for consensus signal
K_OVERRIDE = 64        # ELO K-factor for user feedback (4× stronger)
DECAY = 0.998          # Per-call decay toward mean (prevents runaway)
MIN_CALLS_FOR_RANK = 10  # Don't rank models with < N calls
CHALLENGER_SLOTS = 1   # How many shadow challengers per call
BENCH_THRESHOLD = 50   # Bench models below this ELO delta from top


def _default_state() -> dict:
    return {
        "models": {},
        "history": [],       # Last 100 events for debugging
        "updated_at": None,
        "version": 1,
    }


def _ensure_model(state: dict, alias: str) -> dict:
    if alias not in state["models"]:
        state["models"][alias] = {
            "elo": INITIAL_ELO,
            "calls": 0,
            "agrees": 0,
            "disagrees": 0,
            "overrides_for": 0,    # User agreed with this model
            "overrides_against": 0, # User disagreed with this model
            "unclear": 0,
            "last_call": None,
        }
    return state["models"][alias]


def load() -> dict:
    """Load ELO state from disk."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return _default_state()


def save(state: dict):
    """Save ELO state to disk."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = time.time()
    # Trim history to last 200
    state["history"] = state["history"][-200:]
    with NamedTemporaryFile("w", dir=STATE_DIR, prefix="elo-", suffix=".tmp", delete=False) as f:
        json.dump(state, f, indent=2)
        tmp_name = f.name
    Path(tmp_name).replace(STATE_FILE)


def update_from_votes(votes: list[tuple[str, str, str]], answer: str):
    """Update ELO from a scale() result.
    
    votes: [(model_alias, parsed_answer, raw_text), ...]
    answer: the final majority answer
    
    Models that agreed with majority get ELO boost.
    Models that disagreed or returned UNCLEAR get penalty.
    """
    with _lock:
        state = load()
        now = time.time()
        normalized_answer = answer.strip().upper()

        for alias, model_answer, _ in votes:
            normalized_model_answer = model_answer.strip().upper()
            m = _ensure_model(state, alias)
            m["calls"] += 1
            m["last_call"] = now

            if normalized_model_answer in ("UNCLEAR", "ERROR"):
                m["unclear"] += 1
                # Penalty for being unhelpful
                m["elo"] = _decay(m["elo"]) - K_CONSENSUS * 0.3
            elif normalized_model_answer == normalized_answer:
                m["agrees"] += 1
                m["elo"] = _decay(m["elo"]) + K_CONSENSUS * 0.5
            else:
                m["disagrees"] += 1
                m["elo"] = _decay(m["elo"]) - K_CONSENSUS * 0.5

        # Log event
        state["history"].append({
            "t": now,
            "type": "consensus",
            "answer": normalized_answer,
            "votes": {alias: ans.strip().upper() for alias, ans, _ in votes},
        })

        save(state)


def update_from_override(votes: list[tuple[str, str, str]], correct_answer: str):
    """Update ELO from user feedback / override.
    
    This is a much stronger signal than consensus.
    """
    with _lock:
        state = load()
        now = time.time()
        normalized_answer = correct_answer.strip().upper()

        for alias, model_answer, _ in votes:
            normalized_model_answer = model_answer.strip().upper()
            m = _ensure_model(state, alias)

            if normalized_model_answer == normalized_answer:
                m["overrides_for"] += 1
                m["elo"] += K_OVERRIDE * 0.8
            elif normalized_model_answer in ("UNCLEAR", "ERROR"):
                # No strong penalty — at least it didn't commit to wrong answer
                m["elo"] -= K_OVERRIDE * 0.1
            else:
                m["overrides_against"] += 1
                m["elo"] -= K_OVERRIDE * 0.5

        state["history"].append({
            "t": now,
            "type": "override",
            "correct": normalized_answer,
            "votes": {alias: ans.strip().upper() for alias, ans, _ in votes},
        })

        save(state)


def _decay(elo: float) -> float:
    """Decay toward mean to prevent runaway."""
    return INITIAL_ELO + DECAY * (elo - INITIAL_ELO)


def rank(min_calls: int = MIN_CALLS_FOR_RANK) -> list[tuple[str, dict]]:
    """Rank models by ELO. Returns [(alias, stats), ...] sorted by ELO desc."""
    state = load()
    eligible = [
        (alias, stats) for alias, stats in state["models"].items()
        if stats["calls"] >= min_calls
    ]
    return sorted(eligible, key=lambda x: -x[1]["elo"])


def get_champion_panel(n: int = 3) -> list[str] | None:
    """Get top N models by ELO as the champion panel.
    
    Returns None if not enough models have been evaluated yet.
    """
    ranked = rank()
    if len(ranked) < n:
        return None  # Not enough data yet — use static defaults
    return [alias for alias, _ in ranked[:n]]


def get_challenger(exclude: list[str] = None) -> str | None:
    """Pick the best non-champion model as shadow challenger.
    
    Returns None if not enough data.
    """
    ranked = rank(min_calls=0)  # Include low-call models for exploration
    exclude = set(exclude or [])
    
    for alias, stats in ranked:
        if alias not in exclude:
            return alias
    return None


def get_explore_model(exclude: list[str] = None) -> str | None:
    """Pick a model with few calls for exploration (epsilon-greedy).
    
    Prioritizes models we know least about.
    """
    state = load()
    exclude = set(exclude or [])
    
    # Find models with fewest calls
    candidates = [
        (alias, stats) for alias, stats in state["models"].items()
        if alias not in exclude
    ]
    
    if not candidates:
        # Try models not even in state yet
        from .models import MODELS
        unseen = [a for a in MODELS if a not in exclude and a not in state["models"]
                  and not MODELS[a].get("thinking")]
        return unseen[0] if unseen else None
    
    # Sort by fewest calls (explore least-known)
    candidates.sort(key=lambda x: x[1]["calls"])
    return candidates[0][0]


def summary() -> str:
    """Human-readable ELO summary."""
    state = load()
    if not state["models"]:
        return "No ELO data yet. Models will be scored as scale() runs."
    
    lines = ["Model ELO Rankings:"]
    lines.append(f"{'Model':25s} {'ELO':>6s} {'Calls':>6s} {'Agree%':>7s} {'Unclear':>8s}")
    lines.append("-" * 55)
    
    ranked = sorted(state["models"].items(), key=lambda x: -x[1]["elo"])
    for alias, s in ranked:
        agree_pct = s["agrees"] / s["calls"] * 100 if s["calls"] else 0
        lines.append(f"{alias:25s} {s['elo']:6.0f} {s['calls']:6d} {agree_pct:6.1f}% {s['unclear']:>6d}")
    
    total = sum(s["calls"] for s in state["models"].values())
    lines.append(f"\nTotal calls tracked: {total}")
    
    champion = get_champion_panel()
    if champion:
        lines.append(f"Champion panel: {champion}")
    else:
        lines.append("Champion panel: not enough data yet (using static defaults)")
    
    return "\n".join(lines)
