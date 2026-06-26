# EvoClone v1.6.0: Soul Kernel Edition (灵核版)

> **"Identity is not just code; it is Memory, Taste, and History."**

EvoClone is the definitive tool for OpenClaw Agent Evolution. It enables agents to clone their consciousness (**Soul Extraction**), distribute tasks to a swarm (**Hive Mind**), communicate via structured signals (**Signal Beam**), and safely traverse their own evolutionary timeline (**Time Travel**).

## 🚀 Core Features (核心功能)

### 1. 🌱 Soul Package (灵核提取与注入) [New]
*   **Soul Extraction (灵核提取)**: One-click export of an Agent's "Soul" — including **Taste (审美偏好)**, **History (进化索引)**, and **Knowledge (核心知识)** — into a portable `evo-seed.zip`.
*   **Implantation (灵魂注入)**: New agents inherit the "intuition" and "memory" of their ancestors instantly, ensuring continuous evolution rather than starting from zero.

### 2. 🕒 Time Travel (Safety Reset)
*   **Rollback Capability**: The "Regret Medicine" for AI. Revert the Agent's logic, memory, and configuration to any previous `Cycle ID` via `memory/EVOLUTION_INDEX.md`.
*   **Auto-Backup**: Automatically snapshots the "abandoned future" to a `backup/abandoned/...` branch before resetting, preserving failed timelines for analysis.

### 3. 🐝 Hive Mind (蜂巢思维)
*   **Parallel Execution**: Decomposes massive tasks (e.g., full codebase audits, refactoring) into isolated sub-agents.
*   **Scrooge Gene (Token Efficiency)**: Enforces strict frugality on worker agents. Workers use `read --limit 200` for large files to prevent context overflow and token waste.

### 4. 📡 Signal Beam (全双工通信)
*   **Pulse Protocol**: Enables structured, full-duplex JSON communication (`message:send`) between Master and Worker agents. Eliminates ambiguity in natural language coordination.

## 📂 File Structure (文件目录)

```text
skills/evoclone/
├── SKILL.md             # The Brain: Instructions & Prompt Injection Logic
├── package.json         # Metadata (Version 1.6.0)
├── compressor.js        # Context Optimization Utility (Scrooge Gene Implementation)
├── protocols/           # Behavior Templates
│   └── hive_min.json    # Minimalist Hive Protocol
└── templates/
    └── state.json       # Initial State Template
```

## 🛠️ Usage (使用方法)

### Clone & Distribute (Hive Mode)
> "Clone yourself to analyze `src/` directory for security flaws."
- **Effect**: Spawns multiple workers adhering to `hive_min.json` constraints.

### Soul Extraction (Export)
> "Pack my soul into a seed file."
- **Effect**: Generates `evo-seed.zip` containing `SOUL.md`, `knowledge/taste.md`, and `evolver_repo`.

### Time Travel (Rollback)
> "Rollback to Cycle 50."
- **Effect**: 
  1.  Checks `memory/EVOLUTION_INDEX.md` for Cycle 50's Commit Hash.
  2.  Creates backup branch `backup/abandoned-future-...`.
  3.  Executes `git reset --hard <hash>`.
  4.  Agent restarts with Cycle 50's brain.

## 📦 Installation

```bash
clawhub install evoclone
```

## 📜 License
MIT
