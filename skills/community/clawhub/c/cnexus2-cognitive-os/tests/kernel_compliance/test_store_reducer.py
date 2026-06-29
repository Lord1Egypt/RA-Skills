"""Test stub: store_reducer — auto-generated from L1 spec."""
import pytest
from kernel.store_reducer import store_fn
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

# ---- L1 STORE §03 Rule 2: at least emotion + episodic blocks per cycle ----
def test_store_writes_at_least_two_blocks(empty_block_store, neutral_state):
    """store_reducer §03 Rule 2: each cycle writes emotion + episodic."""
    response = {"text": "hello", "inference_type": "llm", "confidence": 0.9, "latency_ms": 100, "metadata": {}}
    result = store_fn(response, neutral_state, {"iteration": 1}, empty_block_store)
    assert result["blocks_written"].get("emotion", 0) >= 1
    assert result["blocks_written"].get("episodic", 0) >= 1

# ---- L1 STORE §03 Rule 3: emotion block is overwritten ----
def test_emotion_block_overwrite(empty_block_store, neutral_state):
    """store_reducer §03 Rule 3: emotion block overwrites (keeps only one)."""
    response = {"text": "a", "inference_type": "llm", "confidence": 0.9, "latency_ms": 50, "metadata": {}}
    store_fn(response, neutral_state, {"iteration": 1}, empty_block_store)
    store_fn(response, neutral_state, {"iteration": 2}, empty_block_store)
    emotion_blocks = [b for b in empty_block_store.blocks if b["label"] == "emotion"]
    assert len(emotion_blocks) <= 1

# ---- L1 STORE §03 Rule 8: batch write ----
def test_store_batch_write(empty_block_store, neutral_state):
    """store_reducer §03 Rule 8: batch write — single block failure doesn't stop others."""
    response = {"text": "hello", "inference_type": "llm", "confidence": 0.9, "latency_ms": 100, "metadata": {}}
    result = store_fn(response, neutral_state, {"iteration": 1}, empty_block_store)
    assert isinstance(result["blocks_written"], dict)
    assert isinstance(result["failed_writes"], list)
    assert result["total_blocks"] >= 2
