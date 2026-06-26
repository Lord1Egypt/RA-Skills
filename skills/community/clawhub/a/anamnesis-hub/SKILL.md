---
name: anamnesis-hub
description: "四层记忆架构 (Four-tier memory architecture for OpenClaw AI agents). 提供 L0 运行时语义检索 (Ollama bge-m3 + SQLite-vec 向量库)、L1 工作记忆 (每日 Markdown 日志)、L2 长期记忆 (MEMORY.md 索引 + ARCHIVE.md 档案 + facts.db 结构化知识图谱)、Dreaming 自动化提炼管线、三方同步 (Cloud ↔ Markdown ↔ Vector)、Active Memory 主动召回、auto-memory v3 两阶段提取 (ARCHIVE.md 归档 → MEMORY.md 摘要)、cross-platform-writer 跨平台写入。适用于首次配置持久化记忆、安装 memory-core/MemOS Cloud 插件、搭建多层记忆系统。"
version: 1.13.2
---

# anamnesis-hub

Four-tier memory architecture with automated Dreaming pipeline, three-way synchronization, Active Memory recall, and two-stage auto-extraction.

## Overview

| Tier | Layer | Technology | Purpose |
|------|-------|-----------|---------|
| **L0** | Runtime Retrieval | memory-core plugin (Ollama bge-m3 → SQLite + sqlite-vec) | Real-time semantic + BM25 hybrid search |
| **L0** | Cloud Recall | MemOS Cloud plugin (*optional*) | Cross-device memory capture and recall |
| **L0** | Active Memory | Built-in OpenClaw plugin | Pre-reply sub-agent memory search + context injection |
| **L1** | Working Memory | `memory/YYYY-MM-DD.md` files | Daily summaries, todos, technical notes |
| **L2a** | Long-term Index | `MEMORY.md` (~90 lines, read-only base) | Bidirectional index → ARCHIVE.md, 0% Auto-Extracted pollution |
| **L2b** | Detailed Archive | `ARCHIVE.md` (~220 lines) | Full records with ← MEMORY.md:XX reverse references |
| **L2c** | Structured KB | `facts.sqlite` (entity/key/value) | Precise lookup for IPs, ports, versions; activation/decay tracking |

### Automated Pipelines

| Pipeline | Schedule | Description |
|----------|----------|-------------|
| **Dreaming** | 03:00 UTC daily | Scan logs → DeepSeek analysis → promote to L2 |
| **Three-way Sync** | 18:00 / 20:00 / 22:00 CST | Cloud ↔ Markdown ↔ Vector alignment |
| **auto-memory v3** | 18:30 / 22:30 CST | MemOS Cloud facts → qwen3 filter → Stage1: ARCHIVE.md (SHA-256 dedup) → Stage2: MEMORY.md (summary) |
| **session-extract** | 22:00 CST | Scan session JSONL → MemOS extractor/reranker → `.learnings/` + `memory/YYYY-MM-DD.md` (two-pass) |

### Memory Flow (Unified Daily Pipeline)

```
agent_end → MemOS Cloud (cloud extraction)
              ↓
    ┌─ 18:00 sync-pull (Cloud → local cache) ─┐
    │  18:30 auto-memory.py                    │
    │  → Stage 1: ARCHIVE.md (SHA-256 dedup)   │
    │  → Stage 2: MEMORY.md (one-line summary) │
    │                                           │
    │  20:00 sync-push + reindex                │
    │  22:00 session-extract.py                 │
    │  → Pass 1: .learnings/ERRORS.md           │
    │  → Pass 2: memory/YYYY-MM-DD.md           │
    │  → archive analyzed → trash               │
    └───────────────────────────────────────────┘

before_agent_start → MemOS Cloud recall
                  + Active Memory sub-agent
                  + memory-core (bge-m3 + BM25)
              ↓
        Layered context injected before reply
```

## Scripts

| Script | Purpose |
|--------|--------|
| `auto_memory_extract.py` | v3 two-stage pipeline: ARCHIVE.md archive → MEMORY.md summary |
| `session-extract.py` | Scan session JSONL → .learnings/ + memory/ (two-pass) |
| `seed-facts-db.py` | Initialize facts.sqlite from ARCHIVE.md |
| `facts_activation.py` | Hebbian activation + daily decay + Hot/Warm/Cool |
| `daily-memory-pipeline.sh` | 6-stage unified daily pipeline |
| `write_file.py` | Cross-platform text writer (UTF-8/BOM/CRLF) |
| `auto-setup.sh` | One-command Ollama + memory-core + MemOS Cloud setup |

## Setup

### One-command auto-setup

```bash
bash scripts/auto-setup.sh
```

### Options

```bash
bash scripts/auto-setup.sh --skip-ollama   # Skip Ollama install
bash scripts/auto-setup.sh --skip-memos    # Skip MemOS Cloud
bash scripts/auto-setup.sh --dry-run       # Preview only
```

### Manual setup

See `references/setup-guide.md` for step-by-step manual configuration.

## When to Use

- Setting up OpenClaw memory for the first time
- Configuring memory-core plugin with local Ollama embedding
- Installing MemOS Cloud plugin for cross-device sync
- Enabling Active Memory for pre-reply context injection
- Setting up auto-memory pipeline for MEMORY.md curation
- Installing cross-platform-writer for cross-OS file compatibility
- Configuring automatic Dreaming and promotion pipelines
- Setting up three-way sync between cloud, files, and vector DB

## Plugin Conflicts

### ❌ subconscious-personality-guardian ↔ memory-core

**Incompatible.** Both use the same OpenClaw memory slot.

**Fix**: Disable in openclaw.json:
```json
{
  "plugins": {
    "disabled": ["subconscious-personality-guardian"],
    "deny": ["subconscious-personality-guardian"]
  }
}
```

### ✅ memory-core + MemOS Cloud

**Compatible — designed to work in layers.**

```
User message → MemOS Cloud (static facts) → memory-core (recent context)
```

### ✅ Active Memory + MemOS Cloud + memory-core

**Compatible — triple-layer recall.**

```
User message
  → Active Memory sub-agent (searches all memory stores)
  → MemOS Cloud (injects long-term facts & preferences)
  → memory-core (semantic + BM25 hybrid retrieval)
  → Agent receives layered context
```

### ✅ auto-memory + MemOS Cloud + memos-extractor

**Designed to work together.** MemOS captures at `agent_end`, syncs to local files, then auto-memory reads those files for MEMORY.md curation. v1.10 adds a second channel: memos-extractor-0.6b API (MemOS self-developed model) returns structured facts + preferences, cross-validated against qwen3 output.

## Components

### 1. Memory Plugins (L0)

See `references/architecture.md` for full configuration.

### 2. Memory Files (L1 + L2)

```
~/.openclaw/workspace/
├── memory/
│   ├── YYYY-MM-DD.md          # Daily working memory (auto-indexed)
│   ├── MEMORY_INDEX.md        # Vector BM25 cluster summaries
│   └── .sync-*.json           # Sync state files
├── MEMORY.md                  # Long-term memory index (~90 lines)
├── ARCHIVE.md                 # Detailed archive (~220 lines, ← bidirectional refs)
├── AGENTS.md                  # Runtime context + memory rules
└── user_workspace/
    ├── memos-cloud-cache/         # Cloud-pulled memory (isolated from index)
    │   └── memos-cloud-*.md
    ├── scripts/
    │   └── sync-*.py              # Sync scripts (pull/push/vector)
    └── skills/
        └── anamnesis-hub/   # Installed from ClawHub
            └── scripts/           # Pipeline scripts (auto-memory, session-extract, etc.)
```

### 3. Pipeline Scripts (in anamnesis-hub/scripts/)

- `auto_memory_extract.py` — v3 two-stage pipeline (ARCHIVE.md → MEMORY.md)
- `session-extract.py` — Session JSONL scan → .learnings/ + memory/
- `seed-facts-db.py` — Initialize facts.sqlite from ARCHIVE.md
- `facts_activation.py` — Hebbian activation + daily decay
- `daily-memory-pipeline.sh` — 6-stage unified daily pipeline
- `write_file.py` — Cross-platform text file writer
- `auto-setup.sh` — One-command Ollama + memory-core + MemOS Cloud setup

See `references/INDEX.md` for full documentation index.

## File Reference

👉 **完整文档请查阅 `references/INDEX.md`**

| 文档 | 说明 |
|------|------|
| `references/INDEX.md` | 📌 文档入口索引（快速定位） |
| `references/architecture.md` | 四层架构设计、插件配置、协同流程 |
| `references/setup-guide.md` | 环境配置、手动安装步骤、cron 设置 |
| `references/memory-directory.md` | memory/ 目录结构、状态文件、LCM 机制 |
| `references/sync-api.md` | MemOS Cloud API 参考 |
| `references/scripts-reference.md` | 所有脚本统一说明（用途、cron、依赖） |
| `references/pipeline-stages.md` | 日终管线 6 阶段详解 |
| `references/candidates-review.md` | P3 记忆候选审核机制 |
| `references/upgrade-reset.md` | 升级路径、重置流程、卸载步骤 |
