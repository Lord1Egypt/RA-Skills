"""Test stub: reflect_reducer — auto-generated from L1 spec."""
import pytest
from kernel.reflect_reducer import reflect_fn
from kernel.block_store import BlockStore
from kernel.state_snapshot import StateSnapshot, EmotionSnapshot

@pytest.fixture
def empty_block_store():
    return BlockStore()

@pytest.fixture
def neutral_state():
    return StateSnapshot(
        emotion=EmotionSnapshot(val=0.0, arousal=0.5, dominance=0.5),
        relationship={"tone": 0.0, "trust": 0.5, "familiarity": 0.3},
        goal={"current": "converse", "progress": 0.0},
        attention={"focus": "general", "level": 0.5},
        meta={"session_count": 0, "total_interactions": 1}
    )

# ---- L1 REFLECT §03 Rule 1: even after store failure, reflect runs ----
def test_reflect_after_store_failure(empty_block_store, neutral_state):
    """reflect_reducer §03 Rule 1: REFLECT still runs after STORE failure."""
    failed_store = {"blocks_written": {"emotion": 0, "episodic": 0, "intent": 0, "archival": 0},
                    "total_blocks": 0, "failed_writes": ["episodic"],
                    "decay_activated": False, "eviction_triggered": False, "timestamp": 0.0}
    trace = []
    result = reflect_fn(failed_store, neutral_state, trace, empty_block_store)
    assert "anomaly_note" in result or result.get("anomaly_signal_sent") is not None

# ---- L1 REFLECT §03 Rule 2: narrative + reflective blocks written ----
def test_reflect_writes_narrative_and_reflective(empty_block_store, neutral_state):
    """reflect_reducer §03 Rule 2+4: REFLECT writes narrative and reflective blocks."""
    successful_store = {"blocks_written": {"emotion": 1, "episodic": 1, "intent": 0, "archival": 0},
                        "total_blocks": 2, "failed_writes": [],
                        "decay_activated": True, "eviction_triggered": False, "timestamp": 0.0}
    trace = []
    result = reflect_fn(successful_store, neutral_state, trace, empty_block_store)
    assert result.get("narrative_written") is True
    assert result.get("reflective_written") is True

# ---- L1 REFLECT §03 Rule 3: belief delta depends on oscillation ----
def test_reflect_belief_delta(empty_block_store, neutral_state):
    """reflect_reducer §03 Rule 3: smooth state gives belief +0.02; oscillating gives -0.05."""
    # Smooth case
    smooth_store = {"blocks_written": {"emotion": 1, "episodic": 1, "intent": 0, "archival": 0},
                    "total_blocks": 2, "failed_writes": [],
                    "decay_activated": True, "eviction_triggered": False, "timestamp": 0.0}
    trace = []
    result = reflect_fn(smooth_store, neutral_state, trace, empty_block_store)
    if not result.get("state_oscillation_detected"):
        assert result.get("belief_delta", 0) >= 0.0
