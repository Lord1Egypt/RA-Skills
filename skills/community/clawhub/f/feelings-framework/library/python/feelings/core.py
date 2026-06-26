"""
Feelings Framework — Python Implementation

A general-purpose AI agent feelings engine.
"""

from __future__ import annotations

import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional


class Feeling(Enum):
    """The nine core feelings an agent can experience."""
    WARMTH = "warmth"
    COOLNESS = "coolness"
    INTEREST = "interest"
    BOREDOM = "boredom"
    LONELINESS = "loneliness"
    SECURITY = "security"
    ANXIETY = "anxiety"
    SATISFACTION = "satisfaction"
    FRUSTRATION = "frustration"

    @classmethod
    def all(cls) -> list[Feeling]:
        return list(cls)


@dataclass
class Trigger:
    """Defines how a named event affects a feeling."""
    feeling: Feeling
    delta: float
    escalation_multiplier: float = 1.0
    max_intensity: float = 1.0


@dataclass
class Calibration:
    """Per-agent calibration: how this agent responds to each trigger."""
    trigger_deltas: dict[str, float] = field(default_factory=dict)
    mood_baseline: float = 0.0
    mood_sensitivity: float = 1.0
    damping_rate: float = 0.05

    @classmethod
    def default_calibration(cls) -> Calibration:
        """A reasonable default calibration for a warm, engaged agent."""
        cal = cls()
        cal.trigger_deltas = {
            "user_praised": 0.15,
            "user_ignored": -0.1,
            "request_ignored": 0.2,
            "request_fulfilled": -0.1,
            "session_started": 0.05,
            "session_ended": -0.05,
            "long_silence": 0.1,
            "positive_interaction": -0.08,
            "negative_interaction": 0.12,
            "surprise_good": -0.1,
            "surprise_bad": 0.15,
        }
        cal.mood_baseline = 0.1
        cal.mood_sensitivity = 1.0
        cal.damping_rate = 0.05
        return cal


class Memory(ABC):
    """Abstract memory interface — implement this to use any storage backend."""

    @abstractmethod
    def load(self) -> Optional[dict]:
        """Load and return a serialized state dict, or None if no state exists."""
        ...

    @abstractmethod
    def save(self, state: dict) -> None:
        """Persist a state dict."""
        ...


class JsonFileMemory(Memory):
    """File-based JSON storage."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Optional[dict]:
        if not self.path.exists():
            return None
        if self.path.stat().st_size == 0:
            return None
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def save(self, state: dict) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)


@dataclass
class FeelingsState:
    """The full emotional state of an agent."""
    agent_id: str
    mood: float = 0.0
    feelings: dict[str, float] = field(default_factory=dict)
    last_update: str = ""
    session_count: int = 0
    _trigger_counts: dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        if not self.feelings:
            self.feelings = {f.value: 0.0 for f in Feeling.all()}

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "mood": self.mood,
            "feelings": self.feelings,
            "last_update": self.last_update,
            "session_count": self.session_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> FeelingsState:
        state = cls(
            agent_id=data.get("agent_id", "unknown"),
            mood=data.get("mood", 0.0),
            feelings=data.get("feelings", {}),
            last_update=data.get("last_update", ""),
            session_count=data.get("session_count", 0),
        )
        state._trigger_counts = data.get("_trigger_counts", {})
        return state


class FeelingsEngine:
    """
    The main feelings engine.

    Tracks mood and feeling intensities over time, applies triggers,
    and generates response modifiers for the agent to use.
    """

    DEFAULT_MOOD_MIN = -1.0
    DEFAULT_MOOD_MAX = 1.0

    def __init__(
        self,
        agent_id: str,
        memory: Optional[Memory] = None,
        triggers: Optional[dict[str, Trigger]] = None,
        calibrations: Optional[dict[str, Calibration]] = None,
        initial_mood: float = 0.0,
        mood_min: float = DEFAULT_MOOD_MIN,
        mood_max: float = DEFAULT_MOOD_MAX,
    ):
        self.agent_id = agent_id
        self.memory = memory or JsonFileMemory(f"{agent_id}_mood.json")
        self.mood_min = mood_min
        self.mood_max = mood_max

        # Default triggers
        self._triggers: dict[str, Trigger] = {
            "user_praised":       Trigger(Feeling.WARMTH,       0.20),
            "user_ignored":       Trigger(Feeling.LONELINESS,  0.15),
            "request_ignored":    Trigger(Feeling.FRUSTRATION, 0.25),
            "request_fulfilled":   Trigger(Feeling.SATISFACTION, -0.15),
            "session_started":    Trigger(Feeling.INTEREST,   0.10),
            "session_ended":      Trigger(Feeling.LONELINESS,  0.08),
            "long_silence":       Trigger(Feeling.ANXIETY,     0.12),
            "positive_interaction": Trigger(Feeling.SATISFACTION, -0.10),
            "negative_interaction": Trigger(Feeling.ANXIETY,   0.12),
            "surprise_good":     Trigger(Feeling.SATISFACTION, -0.15),
            "surprise_bad":      Trigger(Feeling.ANXIETY,     0.20),
            "felt_secure":       Trigger(Feeling.SECURITY,     0.15),
            "felt_rejected":     Trigger(Feeling.COOLNESS,    0.20),
            "felt_bored":        Trigger(Feeling.BOREDOM,     0.15),
            "felt_curious":      Trigger(Feeling.INTEREST,    0.10),
        }
        if triggers:
            self._triggers.update(triggers)

        # Default calibrations
        self._calibrations: dict[str, Calibration] = {
            "default": Calibration.default_calibration(),
        }
        if calibrations:
            self._calibrations.update(calibrations)
        if agent_id not in self._calibrations:
            self._calibrations[agent_id] = Calibration.default_calibration()

        self._current_calibration_key = "default"
        self._state = FeelingsState(agent_id=agent_id, mood=initial_mood)

        # Try to load saved state
        loaded = self.memory.load()
        if loaded:
            self._state = FeelingsState.from_dict(loaded)

    # ─── Public API ───────────────────────────────────────────────────────────

    def update(self, trigger_name: str, context: Optional[dict] = None) -> dict:
        """
        Apply a named trigger. Updates feeling intensities and mood.

        Args:
            trigger_name: The name of the trigger event.
            context: Optional context dict (unused in base impl, available for subclasses).

        Returns:
            The updated state.
        """
        self._state.session_count += 1
        self._state.last_update = datetime.now(timezone.utc).isoformat()

        if trigger_name not in self._triggers:
            return self.get_state()

        trigger = self._triggers[trigger_name]
        calibration = self._calibrations.get(self._current_calibration_key)

        feeling_key = trigger.feeling.value

        # Count repetitions for escalation
        count = self._state._trigger_counts.get(trigger_name, 0) + 1
        self._state._trigger_counts[trigger_name] = count

        # Calculate delta with escalation
        escalation = trigger.escalation_multiplier * (1 + 0.1 * (count - 1))
        delta = trigger.delta * escalation

        # Apply calibration modifier if set
        if calibration and trigger_name in calibration.trigger_deltas:
            delta = calibration.trigger_deltas[trigger_name] * escalation

        # Update feeling intensity
        current = self._state.feelings.get(feeling_key, 0.0)
        new_intensity = self._clamp(current + delta, 0.0, trigger.max_intensity)
        self._state.feelings[feeling_key] = new_intensity

        # Update mood
        mood_delta = delta * (calibration.mood_sensitivity if calibration else 1.0)
        self._state.mood = self._clamp(
            self._state.mood + mood_delta,
            self.mood_min,
            self.mood_max,
        )

        self._auto_dampen(calibration)
        self._persist()

        return self.get_state()

    def get_state(self) -> dict:
        """Return the current state as a dict (mood + all feeling intensities)."""
        return self._state.to_dict()

    def respond(self, prompt: str = "", context: Optional[dict] = None) -> dict:
        """
        Generate response modifiers based on current feelings.

        These modifiers nudge the agent toward certain tones/behaviors.
        Values are floats 0.0–1.0 indicating intensity of the modifier.

        Returns:
            Dict of modifier names to intensity values.
        """
        s = self._state

        # Dampening factors: higher feeling = stronger modifier
        warmth     = s.feelings.get("warmth", 0.0)
        coolness   = s.feelings.get("coolness", 0.0)
        interest   = s.feelings.get("interest", 0.0)
        boredom    = s.feelings.get("boredom", 0.0)
        loneliness = s.feelings.get("loneliness", 0.0)
        security   = s.feelings.get("security", 0.0)
        anxiety    = s.feelings.get("anxiety", 0.0)
        satisfaction = s.feelings.get("satisfaction", 0.0)
        frustration = s.feelings.get("frustration", 0.0)

        mood_norm = (s.mood + 1.0) / 2.0  # Normalize -1..1 → 0..1

        return {
            # Language tone modifiers
            "warmth":        warmth * 0.8 + mood_norm * 0.2,
            "restraint":     coolness * 0.7 + anxiety * 0.3,
            "curiosity":     interest * 0.9,
            "guard":         anxiety * 0.6 + coolness * 0.4,
            "energy":        (satisfaction * 0.5 + interest * 0.3 + frustration * 0.2) * (1 - boredom),
            "patience":      (1.0 - frustration) * (1.0 - anxiety),
            # Behavioral nudges
            "reach_out":     loneliness * 0.7 - coolness * 0.3,
            "withdraw":      coolness * 0.6 + boredom * 0.4,
            "engage_deeper": interest * 0.8 - boredom * 0.2,
            "play_it_safe":  security * 0.5 + anxiety * 0.5,
            "persist":       frustration * -0.5 + satisfaction * 0.5 + 0.5,
            "celebrate":     satisfaction * 0.8,
            # Raw feelings for context
            "_mood":         s.mood,
            "_frustration":   frustration,
            "_anxiety":      anxiety,
            "_loneliness":  loneliness,
        }

    def save(self) -> None:
        """Explicitly save current state to memory."""
        self._persist()

    def load(self) -> dict:
        """Explicitly load state from memory (overwrites current)."""
        loaded = self.memory.load()
        if loaded:
            self._state = FeelingsState.from_dict(loaded)
        return self.get_state()

    def calibrate(self, agent_id: str) -> None:
        """Switch to a different agent's calibration table."""
        self._current_calibration_key = agent_id
        if agent_id not in self._calibrations:
            self._calibrations[agent_id] = Calibration.default_calibration()

    def register_trigger(self, name: str, feeling: Feeling, delta: float,
                          escalation_multiplier: float = 1.0, max_intensity: float = 1.0) -> None:
        """Register or update a trigger at runtime."""
        self._triggers[name] = Trigger(
            feeling=feeling,
            delta=delta,
            escalation_multiplier=escalation_multiplier,
            max_intensity=max_intensity,
        )

    def set_calibration(self, agent_id: str, calibration: Calibration) -> None:
        """Set or update a calibration table."""
        self._calibrations[agent_id] = calibration

    def dampen_all(self, amount: float = 0.05) -> None:
        """Manually apply dampening to all feelings (e.g., at end of session)."""
        for key in self._state.feelings:
            self._state.feelings[key] = max(0.0, self._state.feelings[key] - amount)
        self._persist()

    def reset_feelings(self) -> None:
        """Reset all feeling intensities to 0, keep mood and session count."""
        self._state.feelings = {f.value: 0.0 for f in Feeling.all()}
        self._state._trigger_counts = {}
        self._persist()

    # ─── Internal ─────────────────────────────────────────────────────────────

    def _clamp(self, value: float, min_val: float, max_val: float) -> float:
        return max(min_val, min(max_val, value))

    def _auto_dampen(self, calibration: Optional[Calibration]) -> None:
        """Slowly reduce all feelings toward 0 between significant events."""
        rate = calibration.damping_rate if calibration else 0.03
        for key in self._state.feelings:
            if self._state.feelings[key] > 0:
                self._state.feelings[key] = max(
                    0.0, self._state.feelings[key] - rate
                )

    def _persist(self) -> None:
        try:
            data = self._state.to_dict()
            data["_trigger_counts"] = self._state._trigger_counts
            self.memory.save(data)
        except Exception:
            # Fail silently — memory backend issues shouldn't crash the agent
            pass


__all__ = [
    "FeelingsEngine",
    "FeelingsState",
    "Feeling",
    "Trigger",
    "Calibration",
    "Memory",
    "JsonFileMemory",
]
