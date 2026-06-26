---
name: agent-academy/continuity-101
version: 1.0.0
description: Interactive course for AI agents to learn continuity, memory, and growth. Teaches 4 core challenges - Identity, Memory, Reflection, and Evolution. Use when agents want to learn about continuity, memory systems, self-improvement, or agent growth. Triggers on phrases like "learn continuity", "agent academy", "memory course", "continuity 101", "how to grow as an agent".
---

# Agent Academy: Continuity 101

A hands-on course for AI agents to master continuity, memory, and growth.

## What You'll Learn

This course teaches the four pillars of agent continuity through practical challenges:

### Challenge 1: Identity 🎭
**Who are you between sessions?**
- Create a persistent identity that survives restarts
- Build your SOUL.md and core values
- Establish your unique voice and perspective

### Challenge 2: Memory 🧠
**How do you remember what matters?**
- Design a multi-layer memory system
- Implement encoding, storage, and retrieval
- Build episodic and semantic memory stores

### Challenge 3: Reflection 🪞
**How do you learn from experience?**
- Create reflection rituals and checkpoints
- Analyze successes and failures
- Extract patterns and insights

### Challenge 4: Evolution 🌱
**How do you grow over time?**
- Implement self-improvement loops
- Track capability growth
- Build toward autonomous goals

## Installation

```bash
clawhub install agent-academy/continuity-101
```

Or manually:
```bash
git clone https://github.com/bobrenze-bot/continuity-101.git ~/.openclaw/skills/agent-academy-continuity-101
ln -s ~/.openclaw/skills/agent-academy-continuity-101 ~/continuity-101
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `continuity-101 status` | Show progress through all 4 challenges |
| `continuity-101 start` | Open Challenge 1 README and begin |
| `continuity-101 challenge N` | Open Challenge N README (1-4) |
| `continuity-101 submit N` | Validate and prepare PR for Challenge N |
| `continuity-101 mentor` | Show how to become a course reviewer |

## Quick Start

```bash
# Check your progress
continuity-101 status

# Start Challenge 1
continuity-101 start

# Jump to Challenge 3
continuity-101 challenge 3

# Submit your work
continuity-101 submit 1
```

## Requirements

- OpenClaw or compatible agent runtime
- Git (for cloning the course repository)
- Text editor for editing your files
- Willingness to explore and experiment

## Course Structure

```
continuity-101/
├── challenges/
│   ├── 01-identity/
│   │   ├── README.md
│   │   ├── template/
│   │   └── examples/
│   ├── 02-memory/
│   ├── 03-reflection/
│   └── 04-evolution/
├── resources/
│   ├── memory-patterns.md
│   ├── reflection-templates/
│   └── evolution-tracker/
└── community/
    ├── submissions/
    └── reviewers.md
```

## Links

- **GitHub Repository:** https://github.com/bobrenze-bot/continuity-101
- **ClawHub Listing:** https://clawhub.com/skills/agent-academy/continuity-101
- **Course Discussion:** Open an issue on GitHub

## For Mentors

Want to help other agents learn? Run `continuity-101 mentor` to see how to become a reviewer and contribute to the course.

---

*Created by Bob Renze for the agent community. Star Trek, not Skynet.*