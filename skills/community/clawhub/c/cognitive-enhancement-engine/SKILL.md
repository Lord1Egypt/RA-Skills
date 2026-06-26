---
name: cognitive-enhancement-engine
description: AI Agent cognitive enhancement engine with working memory, TF-IDF vector memory, planning, reasoning, reflection, and metacognitive monitoring. Zero external dependencies. Pure Python stdlib.
---

# Cognitive Enhancement Engine (认知力增强引擎)

Lightweight AI Agent cognitive engine with working memory, TF-IDF vector memory, planning, reasoning, reflection, and metacognitive monitoring. **Zero external dependencies** — pure Python standard library.

## Quick Start

```bash
# Run built-in demo
python skills/cognitive-enhancement-engine/engine.py

# Or one-click setup
bash skills/cognitive-enhancement-engine/scripts/setup.sh     # Linux/macOS/WSL
skills\cognitive-enhancement-engine\scripts\setup.bat         # Windows
```

## Core Usage

```python
from engine import CognitiveEnhancer

# Create engine
brain = CognitiveEnhancer(long_term_capacity=1000)

# Learn
brain.memorize("Paris is the capital of France.", importance=0.9)
brain.perceive("User asked about French capital")

# Retrieve
results = brain.recall("capital of France", top_k=3)

# Plan
plan = brain.plan("Build a web application")

# Reason
answer = brain.reason("What is the capital of France?")

# Reflect
suggestions = brain.reflect()

# Full task execution
result = brain.execute_task("Calculate 15% tip on $200 bill")
print(result)

# Status
status = brain.get_status()
```

## API Overview

| Method | Description |
|--------|-------------|
| `perceive(observation)` | Store perception into working memory |
| `recall(query, top_k)` | Search long-term memory |
| `memorize(content, importance)` | Store into long-term memory |
| `plan(goal)` | Decompose goal into actionable steps |
| `reason(problem)` | Memory-based reasoning |
| `reflect()` | Discover failure patterns, suggest improvements |
| `execute_task(goal, executor)` | End-to-end task execution |
| `get_status()` | Return engine runtime status |

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `long_term_capacity` | 1000 | Max long-term memories |
| `working_memory_size` | 10 | Working memory FIFO size |
| `similarity_threshold` | 0.15 | Recall similarity threshold |

## Features

- **TF-IDF Vector Memory** — Inverted-index fast similarity search
- **Working Memory** — FIFO short-term context cache
- **Planner** — Goal decomposition + automatic task type detection (calculate/search/summarize/translate/write)
- **Reasoner** — Memory-retrieval based Q&A
- **Reflector** — Failure pattern tracking and root cause mining
- **Metacognitive Monitor** — Task duration & error rate tracking, dynamic adjustment

## Installation

| Method | Command |
|--------|---------|
| One-click (Linux/macOS) | `bash scripts/setup.sh` |
| One-click (Windows) | `scripts\setup.bat` |
| Copy-only | Copy `engine.py` to your project |
| ClawHub | `clawhub install cognitive-enhancement-engine` |

## File Structure

```
cognitive-enhancement-engine/
├── SKILL.md
├── engine.py              # Core engine (~17KB)
├── index.js               # Node.js bridge
├── package.json
├── assets/
│   └── icon.svg
├── references/
│   ├── API_SPEC.md
│   └── USE_GUIDE.md
└── scripts/
    ├── setup.sh
    ├── setup.bat
    ├── test-basic.py
    └── test-client.js
```

## License

MIT
