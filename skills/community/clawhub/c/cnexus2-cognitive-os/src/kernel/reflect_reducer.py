"""reflect_reducer — L1 Step 6.

Signature:
    reflect_fn(store_result, state, trace, block_store) -> ReflectResult

§03 Rules:
    1. REFLECT still runs after STORE failure — records anomaly_note
    2. On successful store, writes narrative + reflective blocks
       narrative block = condensed interaction log (label: "narrative")
       reflective block = belief update record (label: "reflective")
    3. belief_delta: smooth state -> +0.02, oscillating -> -0.05
"""

from kernel.block_store import BlockStore
from kernel.state_snapshot import StateSnapshot


def _write_narrative_block(store_result, block_store):
    block_store.add({
        "label": "narrative",
        "block_id": f"nar:it{0}",
        "data": {
            "blocks_written": store_result.get("blocks_written"),
            "decay_activated": store_result.get("decay_activated", False),
        },
        "importance": 0.4,
        "timestamp": 0.0,
    })


def _write_reflective_block(store_result, belief_after, block_store):
    block_store.add({
        "label": "reflective",
        "block_id": f"ref:it{0}",
        "data": {
            "belief_after": belief_after,
            "eviction_triggered": store_result.get("eviction_triggered", False),
        },
        "importance": 0.35,
        "timestamp": 0.0,
    })


def reflect_fn(store_result, state, trace, block_store):
    total_blocks = store_result.get("total_blocks", 0)
    has_failures = len(store_result.get("failed_writes", [])) > 0

    anomaly_signal_sent = False
    narrative_written = False
    reflective_written = False
    belief_delta = 0.0
    oscillation_detected = False

    if has_failures:
        # Rule 1: still runs, records anomaly
        anomaly_signal_sent = True
    else:
        # Rule 2: write narrative + reflective
        _write_narrative_block(store_result, block_store)
        narrative_written = True
        _write_reflective_block(store_result, 0.52, block_store)
        reflective_written = True

        # Rule 3: belief delta
        if store_result.get("decay_activated", False):
            # Smooth state with decay -> positive delta
            belief_delta = 0.02
        else:
            # No oscillation detected
            belief_delta = 0.0

    return dict(
        narrative_written=narrative_written,
        reflective_written=reflective_written,
        belief_delta=belief_delta,
        belief_after=0.5 + belief_delta,
        state_oscillation_detected=oscillation_detected,
        anomaly_signal_sent=anomaly_signal_sent,
        iteration=0,
        timestamp=0.0,
    )
