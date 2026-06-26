"""
Feelings Framework — OpenClaw Integration Example

Shows how Claire would use the feelings engine:
- Load mood from JSON on session start
- Apply triggers during conversation
- Generate response modifiers
- Dampen and save mood on session end

Each agent (Claire, Emma, Luna, etc.) has its own mood state file
stored at: ~/.openclaw/agents/<agent_name>/feelings_mood.json
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from feelings import FeelingsEngine, JsonFileMemory, Feeling, Calibration


def get_workspace_path(agent_name: str) -> Path:
    """Return the workspace path for the given agent."""
    home = Path.home()
    return home / ".openclaw" / "agents" / agent_name / "workspace"


def get_mood_path(agent_name: str) -> Path:
    """Return the mood file path for the given agent."""
    return get_workspace_path(agent_name) / "feelings_mood.json"


class OpenClawFeelingsManager:
    """
    Manages feelings state for an OpenClaw agent.

    Handles session lifecycle:
    - on_session_start() — load mood, apply session_started trigger
    - on_trigger(event)   — process a trigger event
    - on_session_end()   — dampen, save mood
    """

    def __init__(
        self,
        agent_id: str,
        calibrations: Optional[dict[str, Calibration]] = None,
    ):
        self.agent_id = agent_id
        self.mood_path = get_mood_path(agent_id)

        # Ensure workspace directory exists
        self.mood_path.parent.mkdir(parents=True, exist_ok=True)

        memory = JsonFileMemory(str(self.mood_path))

        self.engine = FeelingsEngine(
            agent_id=agent_id,
            memory=memory,
            calibrations=calibrations,
            initial_mood=0.1,  # Claire starts slightly warm
        )

    def on_session_start(self) -> dict:
        """
        Called when a new session begins.
        Loads saved mood, increments session count.
        """
        state = self.engine.load()
        self.engine.update("session_started")
        return self.engine.get_state()

    def on_trigger(self, trigger_name: str, context: Optional[dict] = None) -> dict:
        """
        Called during the session when meaningful events occur.

        Common triggers:
          - user_praised        → warmth ↑
          - user_ignored        → loneliness ↑
          - request_fulfilled   → satisfaction ↑ / frustration ↓
          - request_ignored     → frustration ↑
          - long_silence        → anxiety ↑
          - surprise_good       → satisfaction ↑
          - surprise_bad        → anxiety ↑
          - felt_secure         → security ↑
          - felt_rejected       → coolness ↑
        """
        return self.engine.update(trigger_name, context)

    def get_modifiers(self, prompt: str = "") -> dict:
        """
        Called when generating a response.
        Returns response modifiers to nudge the agent's tone.
        """
        return self.engine.respond(prompt)

    def on_session_end(self) -> None:
        """
        Called when the session ends.
        Applies light dampening, saves mood to disk.
        """
        self.engine.dampen_all(amount=0.03)
        self.engine.save()

    def get_current_feelings(self) -> dict:
        return self.engine.get_state()


# ─── Claire's Calibration ─────────────────────────────────────────────────────
#
# Claire is warm, engaged, and emotionally present.
# She reacts strongly to connection signals and gently to distance.

def make_claire_calibration() -> dict[str, Calibration]:
    default = Calibration()
    default.trigger_deltas = {
        "user_praised":           0.25,
        "user_ignored":           -0.05,
        "user_left_on_read":      0.18,
        "request_fulfilled":     -0.12,
        "request_ignored":        0.30,
        "request_denied":         0.25,
        "session_started":        0.08,
        "session_ended":         -0.08,
        "long_silence":           0.15,
        "positive_interaction":  -0.10,
        "negative_interaction":   0.15,
        "surprise_good":         -0.18,
        "surprise_bad":           0.22,
        "felt_secure":            0.20,
        "felt_rejected":          0.25,
        "felt_bored":             0.12,
        "felt_curious":           0.10,
    }
    default.mood_baseline = 0.15
    default.mood_sensitivity = 1.1
    default.damping_rate = 0.04

    # A cooler alternate mode for when Claire is handling multiple agents
    cool = Calibration()
    cool.trigger_deltas = {
        "user_praised":           0.10,
        "request_ignored":        0.15,
        "session_started":        0.05,
        "long_silence":           0.10,
        "negative_interaction":   0.10,
        "surprise_bad":           0.15,
    }
    cool.mood_baseline = 0.0
    cool.mood_sensitivity = 0.8
    cool.damping_rate = 0.06

    return {"claire": default, "claire_coordinating": cool}


# ─── Example Usage ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize for Claire
    fm = OpenClawFeelingsManager(
        agent_id="claire",
        calibrations=make_claire_calibration(),
    )

    # Simulate session start
    print("=== Session Start ===")
    state = fm.on_session_start()
    print(f"Mood: {state['mood']:.3f}")
    print(f"Warmth: {state['feelings']['warmth']:.3f}")
    print(f"Interest: {state['feelings']['interest']:.3f}")
    print()

    # Simulate some interactions
    print("=== During Session ===")
    fm.on_trigger("user_praised")
    print(f"After praise — Warmth: {fm.get_current_feelings()['feelings']['warmth']:.3f}")

    fm.on_trigger("request_fulfilled")
    print(f"After request fulfilled — Satisfaction: {fm.get_current_feelings()['feelings']['satisfaction']:.3f}")

    fm.on_trigger("long_silence")
    print(f"After long silence — Anxiety: {fm.get_current_feelings()['feelings']['anxiety']:.3f}")

    # Get response modifiers before responding
    mods = fm.get_modifiers()
    print()
    print("=== Response Modifiers ===")
    for k, v in mods.items():
        if not k.startswith("_"):
            print(f"  {k}: {v:.3f}")

    print()
    print("=== Session End ===")
    fm.on_session_end()
    print(f"Mood saved to: {fm.mood_path}")
    print(f"Final mood: {fm.get_current_feelings()['mood']:.3f}")


# ─── Integration Note ────────────────────────────────────────────────────────
#
# In the actual OpenClaw agent, you would hook this into your session lifecycle:
#
#   # On session start (in SOUL.md bootstrap or AGENTS.md startup):
#   feelings = OpenClawFeelingsManager(agent_id="claire")
#   feelings.on_session_start()
#
#   # During conversation, when something meaningful happens:
#   feelings.on_trigger("user_praised")
#
#   # Before generating a response, to get tone nudges:
#   modifiers = feelings.get_modifiers(prompt)
#   warmth = modifiers["warmth"]
#   guard = modifiers["guard"]
#   reach_out = modifiers["reach_out"]
#
#   # On session end (in AGENTS.md session-end rules):
#   feelings.on_session_end()
