"""
Feelings Framework — Python Package

A general-purpose AI agent feelings engine.

Usage:
    from feelings import FeelingsEngine, JsonFileMemory, Feeling

    memory = JsonFileMemory("my_mood.json")
    engine = FeelingsEngine(agent_id="my_agent", memory=memory)

    engine.update("user_praised")
    state = engine.get_state()
    modifiers = engine.respond()
"""

from feelings.core import (
    FeelingsEngine,
    FeelingsState,
    Feeling,
    Trigger,
    Calibration,
    Memory,
    JsonFileMemory,
)

__version__ = "1.0.0"
__all__ = [
    "FeelingsEngine",
    "FeelingsState",
    "Feeling",
    "Trigger",
    "Calibration",
    "Memory",
    "JsonFileMemory",
    "__version__",
]
