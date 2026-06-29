"""decide_reducer — L1 Step 3.

Signature:
    decide_fn(context, state) -> (Decision dict, new StateSnapshot)

§03 Rules:
    1. Empty context (observation_type == "empty") -> IDLE strategy, confidence=1.0
    3. active_intent derived from context: one of ("converse", "store", "recall", "operate")
    5. Relationship tone adjusts from context (small delta under non-oscillation)
    6. Goal progression: progress += 0.02 per normal cycle
"""

from typing import Any, Dict
from kernel.state_snapshot import StateSnapshot


class DecisionResult:
    """Bundles decision + new_state; supports both `decision = fn()` and `decision, st = fn()`."""

    def __init__(self, decision: Dict[str, Any], new_state: StateSnapshot):
        self._decision = decision
        self._new_state = new_state

    def __getitem__(self, key):
        # Support tuple unpacking: result[0], result[1]
        if isinstance(key, int):
            return (self._decision, self._new_state)[key]
        # Also support dict-style access: result["strategy"]
        return self._decision[key]

    def get(self, key, default=None):
        return self._decision.get(key, default)

    def __contains__(self, key):
        return key in self._decision

    def __iter__(self):
        yield self._decision
        yield self._new_state

    @property
    def decision(self):
        return self._decision

    @property
    def new_state(self):
        return self._new_state


def _derive_intent(context) -> str:
    obs_type = context.get("observation_type", "text_input")
    if obs_type == "empty":
        return "store"
    bundle = context.get("context_bundle", "")
    if not bundle.strip():
        return "store"
    return "converse"


def decide_fn(context, state):
    from dataclasses import replace

    obs_type = context.get("observation_type", "text_input")

    if obs_type == "empty":
        # Rule 1: empty -> IDLE
        decision = dict(
            strategy="IDLE",
            confidence=1.0,
            identity_risk="low",
            active_intent="store",
            reason="empty_input",
        )
        return DecisionResult(decision, state)

    # Normal context
    intent = _derive_intent(context)
    decision = dict(
        strategy="SPEAK",
        confidence=0.8,
        identity_risk="low",
        active_intent=intent,
        reason="normal_context",
    )

    # Rule 5: small relationship tone update
    new_relationship = {
        "tone": min(1.0, max(-1.0, state.relationship.get("tone", 0.0) + 0.05)),
        "trust": state.relationship.get("trust", 0.5),
        "familiarity": min(1.0, state.relationship.get("familiarity", 0.3) + 0.02),
    }

    # Rule 6: goal progression
    new_goal = dict(state.goal)
    new_goal["progress"] = min(1.0, new_goal.get("progress", 0.0) + 0.02)

    new_state = replace(
        state,
        relationship=new_relationship,
        goal=new_goal,
    )

    return DecisionResult(decision, new_state)
