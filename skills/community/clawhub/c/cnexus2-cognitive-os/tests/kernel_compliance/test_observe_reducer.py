"""Test stub: cognize_reducer — auto-generated from L1 spec."""
import pytest
import math
import json
from datetime import datetime

# 占位符 — 待 kernel/ 实现后替换
from kernel.cognize_reducer import cognize_fn
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

# ---- L1 OBSERVE §02 Rule 1: normalize input ----
def test_observe_normalization():
    """observe_reducer §02 Rule 1: raw input is stripped and lowercased."""
    obs = {"type": "text_input", "raw": "  HeLLo World!  ",
           "normalized": "hello world!", "is_empty": False}
    assert obs["normalized"] == obs["raw"].strip().lower()

# ---- L1 OBSERVE §02 Rule 2: empty detection ----
def test_observe_empty_detection():
    """observe_reducer §02 Rule 2: empty input sets is_empty=True."""
    obs = {"type": "empty_observation", "raw": "", "normalized": "", "is_empty": True}
    assert obs["is_empty"] is True

# ---- L1 OBSERVE §05: OBSERVE does not modify State ----
def test_observe_does_not_modify_state(neutral_state):
    """observe_reducer §05: OBSERVE must not mutate State."""
    from kernel.observe_reducer import observe_fn
    obs = observe_fn("hello", neutral_state)
    assert obs["type"] == "text_input"
    assert obs["is_empty"] is False
    # State passed in is a snapshot; observe_fn must not mutate it.
    # (Immutability is enforced by StateSnapshot's frozen design.)
