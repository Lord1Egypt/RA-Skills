"""cognize_reducer — L1 Step 2.

Signature:
    cognize_fn(obs, state, recall_items, **kwargs) -> ContextResult

Returns a ContextResult with:
    - .emotion (emotion changes from delta mapping)
    - .attention (attention level changes)
    - .context (namedtuple with state_snapshot, recall_items, context_bundle)

§02 Rules:
    1. Empty observation -> no state update (emotion, attention unchanged)
    2. |Δ(val)| <= 0.35, |Δ(arousal)| <= 0.30, |Δ(dominance)| <= 0.25
    3. |Δ(attention.level)| <= 0.30
    4. Oscillation detection (structural for now)
    5. P1 identity protection (structural for now)
"""

from typing import Any, Dict, List, NamedTuple
from dataclasses import replace
from kernel.state_snapshot import StateSnapshot, EmotionSnapshot


# Delta bounds from L1 spec
_DELTA_VAL_MAX = 0.35
_DELTA_AROUSAL_MAX = 0.30
_DELTA_DOMINANCE_MAX = 0.25
_DELTA_ATTENTION_MAX = 0.30


class CognizeContext(NamedTuple):
    """Context produced by COGNIZE for downstream steps."""
    state_snapshot: Dict[str, Any]
    recall_items: List[Any]
    context_bundle: str


class ContextResult:
    """Holds both the state snapshot AND the context bundle.
    Provides .context access for test compliance.
    Supports .emotion, .attention for direct state access.
    """

    def __init__(self, new_state: StateSnapshot, context: CognizeContext):
        self._state = new_state
        self._context = context

    @property
    def context(self) -> CognizeContext:
        return self._context

    @property
    def emotion(self) -> EmotionSnapshot:
        return self._state.emotion

    @property
    def attention(self) -> Dict[str, Any]:
        return self._state.attention

    @property
    def state(self) -> StateSnapshot:
        return self._state

    # Dict-like access for state fields
    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        return getattr(self._state, name)


def _compute_emotion_delta(obs: Dict[str, Any], state: StateSnapshot) -> Dict[str, float]:
    """Compute emotion changes from observation."""
    raw = obs.get("normalized", "")
    is_empty = obs.get("is_empty", True)

    if is_empty:
        return {"val": 0.0, "arousal": 0.0, "dominance": 0.0}

    # Simple positive/negative sentiment mapping
    negative_words = {"hate", "angry", "sad", "bad", "terrible", "awful", "worst",
                      "angry", "ugly", "stupid", "powerless"}
    positive_words = {"love", "happy", "good", "great", "fine", "nice",
                      "beautiful", "wonderful", "excellent"}

    words = set(raw.lower().split())
    neg_count = sum(1 for w in words if w in negative_words)
    pos_count = sum(1 for w in words if w in positive_words)

    val_delta = 0.0
    arousal_delta = 0.0
    dominance_delta = 0.0

    if neg_count > 0:
        val_delta = -min(_DELTA_VAL_MAX, neg_count * 0.15)
        arousal_delta = min(_DELTA_AROUSAL_MAX, neg_count * 0.12)
        dominance_delta = -min(_DELTA_DOMINANCE_MAX, neg_count * 0.10)
    elif pos_count > 0:
        val_delta = min(_DELTA_VAL_MAX, pos_count * 0.12)
        arousal_delta = min(_DELTA_AROUSAL_MAX, pos_count * 0.10)
        dominance_delta = min(_DELTA_DOMINANCE_MAX, pos_count * 0.08)
    elif len(raw) > 200:
        # Long input raises attention but not much emotion
        arousal_delta = 0.10
        dominance_delta = -0.05

    return {"val": val_delta, "arousal": arousal_delta, "dominance": dominance_delta}


def _compute_attention_delta(obs: Dict[str, Any]) -> float:
    """Compute attention level change from observation length."""
    raw = obs.get("normalized", "")
    is_empty = obs.get("is_empty", True)
    if is_empty:
        return 0.0

    length = len(raw)
    if length > 300:
        return _DELTA_ATTENTION_MAX
    elif length > 100:
        return 0.20
    elif length > 20:
        return 0.10
    return 0.05


def cognize_fn(obs, state, recall_items, **kwargs):
    is_empty = obs.get("is_empty", True)

    if is_empty:
        # Rule 1: empty -> no change
        delta_e = {"val": 0.0, "arousal": 0.0, "dominance": 0.0}
        delta_att = 0.0
    else:
        delta_e = _compute_emotion_delta(obs, state)
        delta_att = _compute_attention_delta(obs)

    # Clamp: ensure delta doesn't exceed bounds
    delta_v = max(-_DELTA_VAL_MAX, min(_DELTA_VAL_MAX, delta_e["val"]))
    delta_a = max(-_DELTA_AROUSAL_MAX, min(_DELTA_AROUSAL_MAX, delta_e["arousal"]))
    delta_d = max(-_DELTA_DOMINANCE_MAX, min(_DELTA_DOMINANCE_MAX, delta_e["dominance"]))
    delta_att = max(-_DELTA_ATTENTION_MAX, min(_DELTA_ATTENTION_MAX, delta_att))

    # Compute new state
    new_emotion = EmotionSnapshot(
        val=max(-1.0, min(1.0, state.emotion.val + delta_v)),
        arousal=max(0.0, min(1.0, state.emotion.arousal + delta_a)),
        dominance=max(0.0, min(1.0, state.emotion.dominance + delta_d)),
    )
    new_attention = dict(state.attention)
    new_attention["level"] = max(0.0, min(1.0, new_attention["level"] + delta_att))

    new_state = replace(state, emotion=new_emotion, attention=new_attention)

    # Build context bundle
    context_bundle = obs.get("normalized", "")
    context = CognizeContext(
        state_snapshot={
            "emotion": {"val": new_emotion.val, "arousal": new_emotion.arousal, "dominance": new_emotion.dominance},
            "relationship": new_state.relationship,
            "goal": new_state.goal,
            "attention": new_attention,
        },
        recall_items=recall_items,
        context_bundle=context_bundle,
    )

    return ContextResult(new_state, context)
