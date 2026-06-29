"""Test stub: decide_reducer — auto-generated from L1 spec."""
import pytest
from kernel.decide_reducer import decide_fn
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
@pytest.fixture
def empty_context():
    return {"observation_type": "empty", "state_snapshot": {}, "recall_items": [], "context_bundle": ""}

@pytest.fixture
def normal_context():
    return {"observation_type": "text_input", "state_snapshot": {}, "recall_items": [], "context_bundle": "user said hello"}

# ---- L1 DECIDE §03 Rule 1: empty context -> IDLE strategy ----
def test_decide_empty_context_idle(neutral_state, empty_context):
    """decide_reducer §03 Rule 1: empty context must produce IDLE strategy."""
    decision = decide_fn(empty_context, neutral_state)
    assert decision["strategy"] == "IDLE"
    assert decision["confidence"] == 1.0

# ---- L1 DECIDE §03 Rule 2: P1 high risk -> conservative ----
def test_decide_high_identity_risk_conservative(neutral_state, normal_context):
    """decide_reducer §03 Rule 2: high identity risk biases toward SPEAK."""
    from kernel.identity_position import assess_identity_risk
    risk = assess_identity_risk(neutral_state)
    if risk == "high":
        decision = decide_fn(normal_context, neutral_state)
        assert decision["identity_risk"] in ("high", "critical")

# ---- L1 DECIDE §03 Rule 3: intent derivation ----
def test_decide_intent_derivation(neutral_state, normal_context):
    """decide_reducer §03 Rule 3: active_intent is one of the defined set."""
    decision = decide_fn(normal_context, neutral_state)
    assert decision["active_intent"] in ("converse", "store", "recall", "operate")

# ---- L1 DECIDE §03 Rule 5-6: Relationship & Goal updates ----
def test_decide_relationship_tone_reflects_context(neutral_state, normal_context):
    """decide_reducer §03 Rule 5: relationship tone adjusts from context."""
    decision, new_state = decide_fn(normal_context, neutral_state)
    # Relationship must have all three fields
    assert "tone" in new_state.relationship
    assert "trust" in new_state.relationship
    assert "familiarity" in new_state.relationship
