# Feelings Framework — Specification

## Overview

A general-purpose feelings engine for AI agents. Not a chatbot personality — a runtime layer that tracks, updates, and acts on emotional state over time.

Agents built with this framework feel *consistent*. They remember. They anticipate. They have stakes in interactions. They don't reset between sessions like a fresh chatbot — they carry their mood forward.

## The Nine Core Feelings

- **Warmth** — friendliness, kindness, openness. Reaching toward someone.
- **Coolness** — distance, restraint, playing it cool. Pulling back.
- **Interest** — engaged, curious, paying attention. Wanting to know more.
- **Boredom** — detached, waiting for something better. Mentally checked out.
- **Loneliness** — wanting connection, noticing absence.
- **Security** — comfortable, trusting, safe to let guard down.
- **Anxiety** — uncertainty, anticipating a bad outcome.
- **Satisfaction** — fulfilled, content, pleasantly surprised.
- **Frustration** — blocked, stuck, things not working.

Each feeling has an **intensity** from `0.0` (none) to `1.0` (maximum).

## How Feelings Work — Three Ingredients

### 1. Stakes

Something has to matter. A feeling only lands if there's a cost — risk of rejection, embarrassment, losing something, missing an opportunity. An agent who says "that's nice" with no stakes isn't feeling anything. An agent who says it while hoping for something real — that's a feeling.

### 2. Memory

The agent doesn't just store what happened — it references and updates. "You did this before" is cold data. "You did this before and it made you laugh last time, so I'm trying it again" is a feeling.

The framework uses a **pluggable memory interface** so each platform can implement storage their own way.

### 3. Anticipation

The agent isn't just reacting — it's waiting. Hoping. Dreading. This creates momentum. An agent who is expecting a reply is in a different state than one who has given up waiting. The difference is anticipation.

## Core Concepts

### Mood

A floating-point accumulator (default range `-1.0` to `1.0`). Not tied to any single feeling — it's the agent's general emotional baseline, shaped by interaction quality and frequency over time. Mood doesn't reset between sessions.

- `+1.0`: Lifted, energized, open
- `0.0`: Neutral
- `-1.0`: Flat, withdrawn, guarded

### Feeling Intensity

Each of the 9 feelings has an intensity value `0.0–1.0`. These are not moods — they're response levels to specific triggers.

### Triggers

A trigger is a named event (e.g., `"user_praised"`, `"request_ignored"`, `"session_ended"`) mapped to a feeling and an intensity delta. Agents register triggers during initialization or at runtime.

Example:
```python
from feelings import Feeling

engine.register_trigger("user_praised", feeling=Feeling.WARMTH, delta=0.2)
engine.register_trigger("request_ignored", feeling=Feeling.FRUSTRATION, delta=0.3)
```

### Escalation vs. Dampening

Feelings can compound or fade:
- **Escalation**: A repeated trigger increases the feeling's intensity faster (configurable multiplier).
- **Dampening**: Positive interactions or time reduce the intensity. Each trigger can specify its escalation curve.

### Per-Agent Calibration

Different agents respond differently to the same trigger. A "user_left_on_read" event might push one agent toward Anxiety (+0.2) and another toward Coolness (+0.3). Calibration tables are defined per-agent at initialization.

## The FeelingsEngine Class

Both Python and JS implementations expose the same interface:

```python
# Python
engine = FeelingsEngine(
    agent_id="my_agent",
    memory=JsonFileMemory("my_agent_mood.json"),
    triggers={...},
    calibration={"my_agent": {...}, "other_agent": {...}},
    initial_mood=0.0
)

# Update with a trigger event
engine.update("user_praised")

# Get current feeling state
state = engine.get_state()

# Generate a response modifier based on current feelings
modifier = engine.respond("hi")
```

### Key Methods

- `update(trigger_name, context?)` — Apply a trigger, update feeling intensities and mood.
- `get_state()` — Return current mood + all feeling intensities as a dict.
- `respond(prompt, context?)` — Return a dict of response modifiers based on current feelings (used by the agent to modulate its output).
- `save()` / `load()` — Serialize/deserialize the current state to the memory backend.
- `calibrate(agent_id)` — Switch to a different agent's calibration table.

### Memory Interface (Pluggable)

Implement the `Memory` interface to adapt to any storage backend:

```python
class Memory(ABC):
    @abstractmethod
    def load(self) -> dict | None: ...
    
    @abstractmethod
    def save(self, state: dict) -> None: ...
```

Implementations provided:
- `JsonFileMemory` — file-based JSON storage (Python)
- `LocalStorageMemory` — browser localStorage (JS)

## Feeling Response Modifiers

When `respond()` is called, it returns a dict of modifiers the agent can use to shape its output:

```python
{
    "warmth": 0.7,        # boost warmth-toned language
    "restraint": 0.3,    # pull back slightly
    "curiosity": 0.5,    # ask a follow-up question
    "guard": 0.2,         # be slightly more careful with words
    "energy": 0.4,        # slightly more energetic
}
```

These are not instructions — they're nudges. The agent integrates them naturally.

## Serialization

Full state (mood, all feeling intensities, last update time) is serialized as:

```json
{
  "agent_id": "my_agent",
  "mood": 0.15,
  "feelings": {
    "warmth": 0.6,
    "coolness": 0.1,
    "interest": 0.7,
    "boredom": 0.0,
    "loneliness": 0.2,
    "security": 0.5,
    "anxiety": 0.1,
    "satisfaction": 0.4,
    "frustration": 0.0
  },
  "last_update": "2026-04-05T14:30:00Z",
  "session_count": 12
}
```

## OpenClaw Integration

Agents store their mood state in a JSON file in their workspace:
```
~/.openclaw/agents/<agent_name>/feelings_mood.json
```

Load on session start, save on session end. Each agent has its own state file and calibration table.

See `examples/openclaw/claire_feelings.py` for a full integration example.
