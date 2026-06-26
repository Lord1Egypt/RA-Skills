# Roundtable Adapter Guide

> **Version**: 0.2.0 | **Date**: 2026-05-26

Roundtable adapters let you plug any agent framework into the roundtable discussion engine. Implement three methods, register, done.

## Quick Start (10 lines)

```python
from roundtable.adapters.simple import SimpleAdapter

adapter = SimpleAdapter(
    name="Alice",
    role="engineer",
    avatar="👩‍💻",
    title="技术总监",
    speak_fn=lambda ctx: f"I think {ctx['topic']} needs a microservice architecture.",
)
```

That's it. Pass the adapter to `RoundtableCore` and it handles the rest.

## Interface

All adapters subclass `RoundtableAdapter` from `roundtable.adapters.base`:

```python
from abc import ABC, abstractmethod
from typing import Any

class RoundtableAdapter(ABC):
    @abstractmethod
    def get_persona(self) -> dict[str, Any]:
        """Return {name, role, avatar?, title?, description?}"""
        ...

    @abstractmethod
    async def speak(self, context: dict[str, Any]) -> str:
        """Generate speech from context. Return Markdown string.
        
        context keys:
            topic       — discussion topic
            history     — list of all prior speeches
            round       — current round number (1-indexed)
            findings    — consensus/disagreement points so far
            participants — all participant personas
        """
        ...

    @abstractmethod
    async def listen(self, speech: dict[str, Any]) -> dict[str, Any] | None:
        """React to another agent's speech. Return None for no reaction.
        
        speech keys:
            speaker  — speaker name
            content  — speech content
            round    — round number
        """
        ...
```

Optional hooks (override if needed):

```python
    def on_round_start(self, round_num: int) -> None:
        """Called at the start of each round. No-op by default."""

    def on_discussion_end(self, conclusion: str) -> None:
        """Called when the discussion ends. No-op by default."""
```

## Lifecycle

```
__init__()           → adapter created (one per discussion)
get_persona()        → metadata collected before first turn
  ┌─ round N ──────────────────────────────┐
  │  on_round_start(N)                     │
  │  speak(context) → for agent A          │
  │  listen(speech) → for agents B, C, ... │
  │  speak(context) → for agent B          │
  │  listen(speech) → for agents A, C, ... │
  │  ...                                   │
  └────────────────────────────────────────┘
on_discussion_end(conclusion) → cleanup
```

## Registration

Register custom adapters before creating a discussion:

```python
import roundtable
from roundtable.adapters.base import RoundtableAdapter

class MyLangChainAdapter(RoundtableAdapter):
    def __init__(self, llm, persona):
        self._llm = llm
        self._persona = persona

    def get_persona(self):
        return self._persona

    async def speak(self, context):
        prompt = f"Topic: {context['topic']}\nHistory: {context['history']}"
        return await self._llm.ainvoke(prompt)

    async def listen(self, speech):
        return None

# Register
roundtable.register_adapter("langchain", MyLangChainAdapter)

# Use via CLI: roundtable run --adapter langchain ...
```

Query registered adapters:

```python
roundtable.list_adapters()   # {"langchain": <class>, "simple": <class>}
roundtable.get_adapter("langchain")  # <class MyLangChainAdapter>
```

## Built-in Adapters

| Adapter | Module | Description |
|---------|--------|-------------|
| `SimpleAdapter` | `roundtable.adapters.simple` | Callable-based, zero deps |
| Hermes adapter | `roundtable.adapters.hermes` | Integrated with Hermes Agent (auto-registered) |

## Error Handling

| Scenario | Behavior |
|----------|----------|
| `speak()` raises | Agent marked `error`, skipped this round, discussion continues |
| `listen()` raises | Reaction silently dropped |
| `speak()` exceeds 60s | Timeout enforced by core, agent skipped |
| Mixed adapters | Same discussion can use different adapters per participant |

## Persona Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | ✅ | str | Display name |
| `role` | ✅ | str | Role identifier (e.g. "engineer") |
| `avatar` | ❌ | str | Emoji or image URL |
| `title` | ❌ | str | Role title (e.g. "技术总监") |
| `description` | ❌ | str | Role description for info card |

## Examples

### Minimal (pure function)

```python
from roundtable.adapters.simple import SimpleAdapter

def alice_speak(ctx):
    return f"Round {ctx['round']}: I believe we should prioritize {ctx['topic']}."

adapter = SimpleAdapter(name="Alice", role="pm", avatar="👩", speak_fn=alice_speak)
```

### With reactions

```python
def bob_listen(speech):
    if "microservice" in speech.get("content", "").lower():
        return {"reaction": "agree", "note": "Strong +1 on microservices"}
    return None

adapter = SimpleAdapter(
    name="Bob", role="engineer", avatar="👨‍💻",
    speak_fn=lambda ctx: "Architecture is key.",
    listen_fn=bob_listen,
)
```

### Async with external API

```python
import httpx

async def gpt_speak(ctx):
    async with httpx.AsyncClient() as client:
        resp = await client.post("https://api.openai.com/v1/chat/completions", ...)
        return resp.json()["choices"][0]["message"]["content"]

adapter = SimpleAdapter(name="GPT", role="analyst", avatar="🧠", speak_fn=gpt_speak)
```
