"""store_reducer — L1 Step 5.

Signature:
    store_fn(response, state, iteration_meta, block_store) -> StoreResult

§03 Rules:
    2. Each cycle writes at least emotion + episodic blocks
    3. emotion block is overwritten (only one at any time)
    8. Batch write: single block failure doesn't stop others
"""

from typing import Any, Dict
from kernel.block_store import BlockStore
from kernel.state_snapshot import StateSnapshot


def _make_emotion_block(state: StateSnapshot) -> Dict[str, Any]:
    return {
        "label": "emotion",
        "block_id": "e:cycle",
        "data": {
            "val": state.emotion.val,
            "arousal": state.emotion.arousal,
            "dominance": state.emotion.dominance,
        },
        "importance": 0.5,
        "timestamp": 0.0,
    }


def _make_episodic_block(response: Dict[str, Any], iteration_meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "label": "episodic",
        "block_id": f"ep:it{iteration_meta.get('iteration', 0)}",
        "data": {
            "response_text": response.get("text", ""),
            "inference_type": response.get("inference_type", "unknown"),
        },
        "importance": 0.3,
        "timestamp": 0.0,
    }


def store_fn(response, state, iteration_meta, block_store):
    blocks_written = {"emotion": 0, "episodic": 0, "intent": 0, "archival": 0}
    failed_writes = []

    # Write emotion block (overwrite)
    try:
        block_store.replace_emotion(_make_emotion_block(state))
        blocks_written["emotion"] = 1
    except Exception as e:
        failed_writes.append({"label": "emotion", "error": str(e)})

    # Write episodic block (append)
    try:
        block_store.add(_make_episodic_block(response, iteration_meta))
        blocks_written["episodic"] = 1
    except Exception as e:
        failed_writes.append({"label": "episodic", "error": str(e)})

    return dict(
        blocks_written=blocks_written,
        total_blocks=block_store.count,
        failed_writes=failed_writes,
        decay_activated=False,
        eviction_triggered=False,
        timestamp=0.0,
    )
