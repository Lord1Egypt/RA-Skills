---
name: "deer-flow"
description: "Open-source super agent harness orchestrating sub-agents, memory & sandboxes for deep research & extended tasks with extensible skills"
---

# DeerFlow — Super Agent Harness (OpenClaw)

DeerFlow (Deep Exploration and Efficient Research Flow) is an open-source super agent harness that orchestrates sub-agents, memory, and sandboxes to do almost anything — powered by extensible skills.

**Source:** `C:\Users\Harry\Downloads\deer-flow\`
**Original:** https://github.com/bytedance/deer-flow
**License:** MIT

本技能基於 GitHub 上的 [bytedance/deer-flow](https://github.com/bytedance/deer-flow) 修改與封裝。

## Overview

DeerFlow 2.0 is a ground-up rewrite by ByteDance Volcengine for orchestrating complex AI agent workflows:

- **Sub-agent orchestration** — spawn and coordinate specialized sub-agents
- **Persistent memory** — maintain context and knowledge across sessions
- **Sandboxed execution** — safe code and tool execution
- **Extensible skills** — pluggable skill architecture
- **Deep research** — automated multi-step research pipelines

## Structure

```
deer-flow/
├── backend/           # Python backend (FastAPI)
├── frontend/          # Web UI
├── skills/            # Extensible skill definitions
├── scripts/           # Utility scripts
├── contracts/         # API contracts
├── docker/            # Docker configuration
├── docs/              # Documentation
└── tests/             # Test suite
```

## Usage in OpenClaw

When the user asks about deep research agents, multi-step agent workflows, or sub-agent orchestration:
1. Reference DeerFlow's skill architecture for extensibility patterns
2. Use the sub-agent spawning patterns documented in the project
3. Consult `docs/` for architecture and deployment

## Quick Install

```bash
cd C:\Users\Harry\Downloads\deer-flow
make install   # or follow Install.md
```
