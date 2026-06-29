"""CNexusOSKernel — Pure Facade & Lifecycle Router (Phase 4).

This file replaces the monolithic 874-line kernel with a routing facade.
It performs exactly three duties:

1. Environment init: mount BlockStore, StateSnapshot, L2/L3 hooks
2. Pipeline routing: OBSERVE -> COGNIZE -> DECIDE -> SPEAK -> STORE -> REFLECT
3. Inline L2 interception: drift_assertion_matrix checks after each step

All reducer logic is delegated to pure functions in src/kernel/.
"""

import os
import json
import hashlib
import time as _time
from collections import defaultdict, deque
from dataclasses import asdict
from typing import Any, Dict, List, Optional

from kernel.state_snapshot import StateSnapshot, EmotionSnapshot
from kernel.block_store import BlockStore
from kernel.observe_reducer import observe_fn
from kernel.cognize_reducer import cognize_fn
from kernel.decide_reducer import decide_fn
from kernel.speak_reducer import speak_fn
from kernel.store_reducer import store_fn
from kernel.reflect_reducer import reflect_fn
from kernel.identity_position import assess_identity_risk, evaluate_recovery, can_rearm
from kernel.l2_degradation_policy import apply_degradation

# ──────────────────────────────────────────────────────────────────────
# L2 Drift Assertions (inline monitors)
# ──────────────────────────────────────────────────────────────────────
_L0_ASSERTIONS: List[callable] = []
_L1_ASSERTIONS: List[callable] = []


def _register_drift_assertions():
    """Register L0/L1 invariants as callable checks."""
    if _L0_ASSERTIONS:
        return  # already registered

    # L0-01: At most one persona block in store
    def l0_01_persona_unique(store: BlockStore) -> bool:
        return len(store.get_persona()) <= 1

    # L0-02: At most one emotion block in store
    def l0_02_emotion_unique(store: BlockStore) -> bool:
        return len(store.get_emotion()) <= 1

    # L0-05: Non-zero emotion val/arousal/dominance (at least one NE zero)
    EPSILON = 1e-5
    def l0_05_emotion_nonzero(state: StateSnapshot) -> bool:
        e = state.emotion
        return not (abs(e.val) < EPSILON and abs(e.arousal - 0.5) < EPSILON
                    and abs(e.dominance - 0.5) < EPSILON)

    _L0_ASSERTIONS.extend([
        ("L0-01", l0_01_persona_unique),
        ("L0-02", l0_02_emotion_unique),
        ("L0-05", l0_05_emotion_nonzero),
    ])

    # L1-01: Single oscillation records to history
    def l1_01_oscillation_recorded(trace: List[Dict]) -> bool:
        return any(t.get("oscillation") for t in trace[-3:])

    # L1-03: Consecutive oscillation triggers anomaly signal
    def l1_03_consecutive_oscillation(trace: List[Dict]) -> bool:
        recent = [t.get("oscillation", False) for t in trace[-3:]]
        return sum(1 for o in recent if o) < 3  # haven't triggered REFUGE yet

    _L1_ASSERTIONS.extend([
        ("L1-01", l1_01_oscillation_recorded),
        ("L1-03", l1_03_consecutive_oscillation),
    ])


def _run_drift_checks(state: StateSnapshot, store: BlockStore,
                       trace: List[Dict]) -> List[Dict]:
    """Run all registered drift assertions. Returns list of failures."""
    results = []
    for name, check in _L0_ASSERTIONS:
        passed = check(store) if "store" in check.__code__.co_varnames else check(state)
        results.append({"assertion": name, "passed": passed})
    for name, check in _L1_ASSERTIONS:
        passed = check(trace) if "trace" in check.__code__.co_varnames else check(state)
        results.append({"assertion": name, "passed": passed})
    return results


# ──────────────────────────────────────────────────────────────────────
# CNexusOSKernel — Pure Facade
# ──────────────────────────────────────────────────────────────────────
class CNexusOSKernel:
    """Cognitive Loop Kernel — Pure Routing Facade.

    Lifecycle:
        boot() -> run(input_text) -> shutdown()
    """

    def __init__(self):
        # Core data
        self.block_store: BlockStore = BlockStore()
        self.state: StateSnapshot = StateSnapshot()
        self.trace: List[Dict] = deque(maxlen=100) if hasattr(deque, 'maxlen') else []
        self.running: bool = False

        # Degradation level
        self.degradation_level: str = "L0"
        self.anomaly_history: List[Dict] = []
        self.iterations_in_level: int = 0

        # L2 state
        self.in_refuge: bool = False
        self.iterations_in_refuge: int = 0

        # Stats
        self.session_count: int = 0
        self.total_interactions: int = 0

        # Register drift assertions once
        _register_drift_assertions()

    def _get_iteration_meta(self) -> Dict:
        return {
            "iteration": self.total_interactions,
            "session_count": self.session_count,
            "degradation_level": self.degradation_level,
        }

    # ──────────────────────────────────────────────────────────────
    # 6-Step Pipeline (Pure Routing)
    # ──────────────────────────────────────────────────────────────
    def run(self, input_text: str) -> Dict:
        """Execute one full cognitive loop cycle.

        Returns:
            Dict with keys: response, state, trace_update, drift_results
        """
        iteration_meta = self._get_iteration_meta()

        # --- Step 1: OBSERVE ---
        obs = observe_fn(input_text, self.state)
        has_input = not obs.get("is_empty", True)

        # --- Step 2: COGNIZE ---
        recall_items = []  # simplified; recall_context integration deferred
        context_result = cognize_fn(obs, self.state, recall_items)
        self.state = context_result.state  # update state snapshot

        # --- Step 3: DECIDE ---
        decision, self.state = decide_fn(
            context_result.context._asdict() if hasattr(context_result.context, '_asdict')
            else {"observation_type": obs["type"], "state_snapshot": {},
                  "recall_items": recall_items, "context_bundle": obs.get("normalized", "")},
            self.state,
        )

        # --- Step 4: SPEAK ---
        response = speak_fn(decision, context_result.context._asdict()
                            if hasattr(context_result.context, '_asdict') else {},
                            self.state, degradation_level=self.degradation_level)

        # --- Step 5: STORE ---
        store_result = store_fn(response, self.state, iteration_meta, self.block_store)

        # --- Step 6: REFLECT ---
        reflect_result = reflect_fn(store_result, self.state,
                                     list(self.trace)[-5:] if hasattr(self.trace, '__iter__') else [],
                                     self.block_store)

        # --- L2 Drift Checks ---
        drift_results = _run_drift_checks(self.state, self.block_store,
                                           list(self.trace) if hasattr(self.trace, '__iter__') else [])
        failures = [r for r in drift_results if not r["passed"]]

        if failures:
            # Record anomaly
            self.anomaly_history.append({"count": len(failures), "drift_results": drift_results})
            self.iterations_in_level += 1

            # Assess if escalation needed
            if len(self.anomaly_history) >= 2:
                anomaly_count = sum(a["count"] for a in self.anomaly_history[-3:])
                if anomaly_count >= 3:
                    # Escalate degradation
                    levels = ["L0", "L1", "L2", "L3"]
                    if self.degradation_level != "L3":
                        self.degradation_level = levels[min(levels.index(self.degradation_level) + 1, 3)]
                    if self.degradation_level == "L3":
                        self.in_refuge = True
        else:
            # No failures — potential rearm
            self.anomaly_history.append({"count": 0, "drift_results": drift_results})
            if self.degradation_level != "L0":
                self.iterations_in_level += 1
                if can_rearm(current_level=self.degradation_level,
                             anomaly_history=self.anomaly_history,
                             iterations_in_level=self.iterations_in_level):
                    levels = ["L0", "L1", "L2", "L3"]
                    idx = levels.index(self.degradation_level)
                    if idx > 0:
                        self.degradation_level = levels[idx - 1]
                        self.iterations_in_level = 0

        # --- Update meta ---
        self.total_interactions += 1
        self.trace.append({
            "iteration": self.total_interactions,
            "input": input_text,
            "emotion": {"val": self.state.emotion.val, "arousal": self.state.emotion.arousal,
                        "dominance": self.state.emotion.dominance},
            "oscillation": reflect_result.get("state_oscillation_detected", False),
            "drift_failures": len(failures),
        })

        return {
            "response": response,
            "state": {
                "emotion": {"val": self.state.emotion.val, "arousal": self.state.emotion.arousal,
                            "dominance": self.state.emotion.dominance},
                "relationship": self.state.relationship,
                "goal": self.state.goal,
                "attention": self.state.attention,
                "meta": {"session_count": self.session_count,
                         "total_interactions": self.total_interactions},
            },
            "store_result": store_result,
            "reflect_result": reflect_result,
            "drift_results": drift_results,
            "degradation_level": self.degradation_level,
            "in_refuge": self.in_refuge,
        }

    # ──────────────────────────────────────────────────────────────
    # Lifecycle methods
    # ──────────────────────────────────────────────────────────────
    def boot(self):
        """Initialize the kernel."""
        self.block_store = BlockStore()
        self.state = StateSnapshot()
        self.trace = []
        self.running = True
        self.degradation_level = "L0"
        self.anomaly_history = []
        self.iterations_in_level = 0
        self.in_refuge = False
        self.iterations_in_refuge = 0
        self.session_count = 0
        self.total_interactions = 0
        _register_drift_assertions()

    def status(self) -> Dict:
        """Return kernel status."""
        return {
            "running": self.running,
            "booted": self.running,
            "total_interactions": self.total_interactions,
            "session_count": self.session_count,
            "degradation_level": self.degradation_level,
            "in_refuge": self.in_refuge,
            "block_store_size": self.block_store.count,
            "emotion": {"val": self.state.emotion.val,
                        "arousal": self.state.emotion.arousal,
                        "dominance": self.state.emotion.dominance},
        }

    def memory_dump(self, limit: int = 10) -> List[Dict]:
        """Return recent blocks."""
        return self.block_store.blocks[-limit:]

    def reset(self):
        """Reset kernel to boot state."""
        self.boot()

    def shutdown(self):
        """Shutdown the kernel."""
        self.running = False

    # Legacy method for backward compatibility
    def handle_request(self, text: str) -> Dict:
        return self.run(text)
