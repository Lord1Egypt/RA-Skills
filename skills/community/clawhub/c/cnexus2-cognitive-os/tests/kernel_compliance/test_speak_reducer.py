"""Test stub: speak_reducer — auto-generated from L1 spec."""
import pytest
from kernel.speak_reducer import speak_fn
from kernel.state_snapshot import StateSnapshot, EmotionSnapshot

@pytest.fixture
def neutral_state():
    return StateSnapshot(
        emotion=EmotionSnapshot(val=0.0, arousal=0.5, dominance=0.5),
        relationship={"tone": 0.0, "trust": 0.5, "familiarity": 0.3},
        goal={"current": "converse", "progress": 0.0},
        attention={"focus": "general", "level": 0.5},
        meta={"session_count": 0, "total_interactions": 1}
    )

# ---- L1 SPEAK §03 Rule 1: IDLE strategy -> empty response ----
def test_speak_idle_returns_empty(neutral_state):
    """speak_reducer §03 Rule 1: IDLE decision yields empty text."""
    decision = {"strategy": "IDLE", "confidence": 1.0, "identity_risk": "low", "active_intent": "converse", "reason": "empty_input"}
    context = {"context_bundle": ""}
    response = speak_fn(decision, context, neutral_state)
    assert response["text"] == ""
    assert response["inference_type"] == "idle"

# ---- L1 SPEAK §03 Rule 2: SPEAK strategy calls inference ----
def test_speak_calls_inference(neutral_state):
    """speak_reducer §03 Rule 2: SPEAK decision triggers inference."""
    decision = {"strategy": "SPEAK", "confidence": 0.8, "identity_risk": "low", "active_intent": "converse", "reason": "normal"}
    context = {"context_bundle": "user said hello"}
    response = speak_fn(decision, context, neutral_state)
    assert isinstance(response["text"], str)

# ---- L1 SPEAK §05: SPEAK does not modify State ----
def test_speak_does_not_modify_state(neutral_state):
    """speak_reducer §05: SPEAK must not mutate State."""
    decision = {"strategy": "SPEAK", "confidence": 0.8, "identity_risk": "low", "active_intent": "converse", "reason": "normal"}
    context = {"context_bundle": "hello"}
    emotion_before = (neutral_state.emotion.val, neutral_state.emotion.arousal, neutral_state.emotion.dominance)
    response = speak_fn(decision, context, neutral_state)
    assert (neutral_state.emotion.val, neutral_state.emotion.arousal, neutral_state.emotion.dominance) == emotion_before

# ---- L1 SPEAK §03 Rule 4: degradation affects inference type ----
def test_speak_degradation_changes_inference(neutral_state):
    """speak_reducer §03 Rule 4: degradation_level affects inference_type."""
    decision = {"strategy": "SPEAK", "confidence": 0.8, "identity_risk": "low", "active_intent": "converse", "reason": "normal"}
    context = {"context_bundle": "hello"}
    response = speak_fn(decision, context, neutral_state, degradation_level="L2")
    assert response["inference_type"] in ("template", "fixed")
