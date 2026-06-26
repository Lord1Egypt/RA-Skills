# Feelings Framework — OpenClaw Skill

## What It Does

The **feelings-framework** skill gives your OpenClaw agent a persistent emotional layer. It tracks mood and feeling intensities over time, applies meaningful triggers, and generates response modifiers you can use to shape how the agent sounds.

This isn't personality acting — it's runtime emotional state that carries across sessions.

## When It Activates

- When you want agents to have consistent emotional memory
- When interactions should feel like they *matter* (stakes, anticipation, recall)
- When you want different agents to respond differently to the same event

## How to Use

### 1. Install

The library is included in this skill. Import from the local path:

```python
import sys
sys.path.insert(0, "/path/to/feelings-framework/library/python")

from feelings import FeelingsEngine, JsonFileMemory
```

Or pip install if published:

```bash
pip install feelings-framework
```

### 2. Initialize per agent

Each agent gets its own `FeelingsEngine` instance with its own mood file:

```python
from feelings import FeelingsEngine, JsonFileMemory, Calibration

memory = JsonFileMemory("feelings_mood.json")

engine = FeelingsEngine(
    agent_id="my_agent",
    memory=memory,
    calibrations={"my_agent": my_calibration},
    initial_mood=0.1,
)
```

### 3. Session lifecycle

```python
# On session start
state = engine.load()
engine.update("session_started")

# During session — fire meaningful triggers
engine.update("user_praised")      # warmth ↑
engine.update("request_ignored")   # frustration ↑
engine.update("surprise_bad")      # anxiety ↑

# Before generating a response
mods = engine.respond()
# mods["warmth"]      → use more warm, friendly language
# mods["guard"]       → be more careful with words
# mods["reach_out"]   → lean toward connection

# On session end
engine.dampen_all(amount=0.03)
engine.save()
```

### 4. Per-agent calibration

Different agents can use different calibration tables:

```python
engine.calibrate("agent_a")   # warm, engaged
engine.calibrate("agent_b")   # cooler, more restrained
```

## Key Concepts

- **Mood** — general emotional baseline (-1 to +1), accumulates over time
- **Feeling intensity** — per-feeling 0.0–1.0, driven by triggers
- **Triggers** — named events mapped to feelings + deltas
- **Calibration** — per-agent trigger overrides
- **Escalation** — repeated triggers hit harder (up to a max)
- **Dampening** — feelings slowly decay between significant events
- **Response modifiers** — nudges for tone/language based on current state

## The 9 Feelings

Warmth · Coolness · Interest · Boredom · Loneliness · Security · Anxiety · Satisfaction · Frustration

## OpenClaw-Specific Notes

- Mood files for OpenClaw agents live at: `~/.openclaw/agents/<agent_name>/feelings_mood.json`
- See `examples/openclaw/claire_feelings.py` for a full integration example
- The example shows how to hook into OpenClaw session lifecycle (start/end)

## File Structure

```
feelings-framework/
├── CORE.md                    ← Full framework specification
├── library/python/feelings/    ← Python package
├── library/js/feelings/       ← JS/ESM package
├── tests/python/              ← Python tests
├── tests/js/                  ← JS tests
└── examples/openclaw/         ← OpenClaw integration example
```
