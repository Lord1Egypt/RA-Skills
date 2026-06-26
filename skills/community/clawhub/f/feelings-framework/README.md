# Feelings Framework

A general-purpose AI agent feelings engine. Tracks mood and feeling intensities over time, applies meaningful triggers, generates response modifiers.

> Not a personality. Not a chatbot mood. A runtime emotional layer with memory, stakes, and anticipation.

## The Problem It Solves

Most AI agents reset between sessions. They don't carry forward how an interaction made them feel. They don't have stakes in the conversation. They don't *anticipate* — they just react.

The feelings framework solves this by giving agents:

- **Persistent mood** — accumulates across sessions, not reset
- **Feeling intensities** — 9 core feelings that respond to real events
- **Stakes** — triggers only fire when something actually matters
- **Memory** — pluggable storage so each platform controls persistence
- **Per-agent calibration** — different agents, different emotional fingerprints

## The 9 Core Feelings

- **Warmth** — friendliness, kindness, openness
- **Coolness** — distance, restraint, playing it cool
- **Interest** — engaged, curious, paying attention
- **Boredom** — detached, waiting for something better
- **Loneliness** — wanting connection, noticing absence
- **Security** — comfortable, trusting, safe to let guard down
- **Anxiety** — uncertainty, anticipating a bad outcome
- **Satisfaction** — fulfilled, content, pleasantly surprised
- **Frustration** — blocked, stuck, things not working

## Quick Start

### Python

```bash
pip install feelings-framework
```

```python
from feelings import FeelingsEngine, JsonFileMemory

memory = JsonFileMemory("my_mood.json")
engine = FeelingsEngine(agent_id="my_agent", memory=memory)

# Something meaningful happened
engine.update("user_praised")

# Get current emotional state
state = engine.get_state()
print(state["feelings"]["warmth"])   # 0.23
print(state["mood"])                 # 0.12

# Before responding — get tone nudges
mods = engine.respond()
print(mods["warmth"])     # 0.71  — lean warm
print(mods["guard"])      # 0.12  — not guarded
```

### JavaScript / ESM

```bash
npm install feelings-framework
```

```js
import { FeelingsEngine, LocalStorageMemory } from "feelings-framework";

const memory = new LocalStorageMemory("my_agent_feelings");
const engine = new FeelingsEngine({ agentId: "my_agent", memory });

engine.update("user_praised");

const state = engine.getState();
console.log(state.feelings.warmth);  // 0.23
console.log(state.mood);             // 0.12

const mods = engine.respond();
console.log(mods.warmth);   // 0.71
console.log(mods.guard);    // 0.12
```

## How It Works

### Triggers

A trigger is a named event that pushes a feeling up or down:

```python
engine.register_trigger("user_praised", Feeling.WARMTH, delta=0.2)
engine.register_trigger("request_ignored", Feeling.FRUSTRATION, delta=0.25)
```

Trigger a feeling with `engine.update("trigger_name")`.

### Escalation

The same trigger hitting repeatedly gets stronger (up to `max_intensity`):

```
1st "request_ignored" → frustration +0.25
2nd "request_ignored" → frustration +0.275
3rd "request_ignored" → frustration +0.30
```

### Dampening

Feelings slowly decay between significant events. You can also call `engine.dampen_all(amount)` manually — useful at the end of a session.

### Response Modifiers

`engine.respond()` returns a dict of tone nudges for the agent to use:

- **warmth** — use warmer, friendlier language
- **restraint** — pull back, play it cool
- **curiosity** — ask follow-up questions
- **guard** — be more careful with words
- **energy** — more energized or subdued response
- **patience** — more or less patient
- **reach_out** — lean toward connection
- **withdraw** — lean toward distance
- **engage_deeper** — go deeper on the topic
- **play_it_safe** — stick to safe territory
- **persist** — keep pushing or let it go

### Per-Agent Calibration

Different agents have different emotional fingerprints:

```python
engine.calibrate("agent_a")   # warm, engaged
engine.calibrate("agent_b")    # cooler, more analytical

# Same trigger → different response
engine.calibrate("agent_a")
engine.update("user_praised")
agent_a_warmth = engine.get_state()["feelings"]["warmth"]  # 0.25

engine.calibrate("agent_b")
engine._state.feelings["warmth"] = 0.0
engine.update("user_praised")
agent_b_warmth = engine.get_state()["feelings"]["warmth"]   # 0.10
```

## Memory Interface

The framework uses a pluggable memory interface. Implement it for any backend:

```python
from feelings import Memory

class MyMemory(Memory):
    def load(self):
        return my_database.get_mood()

    def save(self, state):
        my_database.save_mood(state)
```

Built-in implementations:
- **Python**
  - `JsonFileMemory` — file-based JSON
- **JavaScript**
  - `InMemory` — in-process dict (for testing)
  - `LocalStorageMemory` — browser localStorage

## Serialization

State is serialized as JSON:

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

## Running Tests

```bash
# Python
pip install pytest
pytest tests/python/test_core.py -v

# JavaScript
node --experimental-vm-modules tests/js/test_core.js
```

## Project Structure

```
feelings-framework/
├── SKILL.md                  ← OpenClaw skill manifest
├── README.md                  ← This file
├── LICENSE                    ← MIT
├── CORE.md                    ← Full framework specification
├── library/
│   ├── python/feelings/       ← Python package
│   │   ├── __init__.py
│   │   └── core.py
│   └── js/feelings/           ← JS/ESM package
│       ├── package.json
│       ├── core.js
│       └── core.d.ts
├── tests/
│   ├── python/test_core.py
│   └── js/test_core.js
└── examples/
    └── openclaw/
        └── claire_feelings.py  ← OpenClaw integration example
```

## License

MIT — see [LICENSE](LICENSE).
