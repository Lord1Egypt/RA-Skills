# 🧠 anamnesis-hub

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-anamnesis--hub-blue)](https://clawhub.ai/victorqr/anamnesis-hub)

**Three-tier memory architecture for OpenClaw AI agents.**  
Persistent, automated, cross-device memory that never forgets.

---

## 中文简介

**anamnesis-hub** 是一套面向 OpenClaw AI Agent 的**四层记忆架构**，解决跨会话的"AI 失忆"问题：

| 层级 | 功能 | 技术栈 |
|------|------|--------|
| **L0** 运行时检索 | 语义 + BM25 混合搜索，实时注入上下文 | memory-core + Ollama bge-m3 + SQLite-vec |
| **L0** 云召回 *可选* | 多设备记忆同步，跨实例共享 | MemOS Cloud 插件 |
| **L0** 主动召回 | 回复前 sub-agent 搜索相关记忆 | Active Memory 插件（内置） |
| **L1** 工作记忆 | 按日归档的 Markdown 日志，人工可编辑 | `memory/YYYY-MM-DD.md` |
| **L2a** 索引层 | 双向索引 ←→ ARCHIVE.md，零污染 ~90行 | `MEMORY.md`（只读基底） |
| **L2b** 档案层 | 详细记录含反向引用 ← MEMORY.md:XX | `ARCHIVE.md`（~220行，历史垃圾已清理） |
| **L2c** 知识图谱 | 结构化 entity/key/value，精确查找 + 热度追踪 | `facts.sqlite` |

**自动化管线**：Dreaming（每日 UTC 03:00）→ 三方同步（18:00/20:00/22:00）→ auto-memory v3（两阶段管道：ARCHIVE.md 归档 → MEMORY.md 摘要）→ session-extract（扫描会话JSONL → MemOS提取 → .learnings/ + memory/）。

### 附赠技能
- **cross-platform-writer** — 跨平台文本写入，自动处理编码/BOM/CRLF
- **auto-memory** — 对话记忆自动提取 (v3: 两阶段管道 + SHA-256 去重)
- **seed-facts-db** — 从 ARCHIVE.md 初始化结构化知识图谱

一行命令部署：`bash scripts/auto-setup.sh`

---

## One-Command Setup

```bash
# Clone and run
git clone https://github.com/VictorQR/anamnesis-hub.git
cd anamnesis-hub
bash scripts/auto-setup.sh
```

The interactive script handles everything:

| Step | What it does | Toggle |
|------|-------------|--------|
| ✅ | Install **Ollama** (standard or Intel) | `--skip-ollama` |
| ✅ | Download **bge-m3** embedding model | — |
| ✅ | **Plugin conflict check** (auto-detect subconscious-personality-guardian) | — |
| ✅ | Install **memory-core** plugin | — |
| ✅ | Configure **openclaw.json** with optimized defaults | Auto-insert on confirm |
| ✅ | Install **MemOS Cloud** (*optional*) with full recommended config | `--skip-memos` |
| ✅ | Create `memory/` directory | — |
| ✅ | Set up **Dreaming cron** (03:00 UTC) | — |

```bash
# Preview mode
bash scripts/auto-setup.sh --dry-run

# Skip Ollama (already installed)
bash scripts/auto-setup.sh --skip-ollama

# Skip MemOS Cloud
bash scripts/auto-setup.sh --skip-memos
```

---

## Architecture

| Tier | Layer | Technology | Purpose |
|------|-------|-----------|---------|
| **L0** | Runtime Retrieval | memory-core + Ollama bge-m3 + SQLite-vec | Real-time semantic + BM25 hybrid search |
| **L0** | Cloud Recall | MemOS Cloud plugin (*optional*) | Cross-device memory capture & recall |
| **L1** | Working Memory | `memory/YYYY-MM-DD.md` | Daily summaries, notes, decisions |
| **L2a** | Long-term Index | `MEMORY.md` (~90 lines, 0% pollution) | Bidirectional index → ARCHIVE.md |
| **L2b** | Detailed Archive | `ARCHIVE.md` (~220 lines) | Full records with ← MEMORY.md:XX references |
| **L2c** | Structured KB | `facts.sqlite` (entity/key/value) | Precise lookup + activation/decay |

### Automated Pipelines

| Pipeline | Schedule | Job |
|----------|----------|-----|
| **Dreaming** | 03:00 UTC daily | Scan logs → DeepSeek analysis → promote to L2 |
| **Three-Way Sync** | 18:00 / 20:00 / 22:00 CST (*optional*) | Cloud ↔ Markdown ↔ Vector alignment |
| **auto-memory v3** | 18:30 / 22:30 CST | Stage 1: ARCHIVE.md (SHA-256 dedup) → Stage 2: MEMORY.md (summary) |
| **session-extract** | 22:00 CST | Scan session JSONL → MemOS extractor/reranker → `.learnings/` + `memory/` (two-pass) |
| **Wiki Compilation** | 04:00 UTC daily (*optional*) | Entity extraction → wiki vault pages |

---

## Installation via ClawHub

```bash
openclaw skills install victorqr/anamnesis-hub
```

This loads the SKILL.md into your agent's context so it knows how to set up and maintain the memory system.

---

## Prerequisites

- [OpenClaw](https://openclaw.ai) >= 3.x
- Node.js >= 18
- Internet connection (for Ollama download and bge-m3 model)

---

## Skill Structure

```
anamnesis-hub/
├── SKILL.md                          # Main skill entry (loaded into agent context)
├── anamnesis-hub.skill                # Packaged .skill distribution file
├── scripts/
│   └── auto-setup.sh                  # One-command interactive setup script
├── references/
│   ├── INDEX.md                      # 📌 文档入口索引
│   ├── architecture.md                # 四层架构设计、插件配置、协同流程
│   ├── setup-guide.md                 # 环境配置、手动安装步骤、cron 设置
│   ├── memory-directory.md           # memory/ 目录结构、状态文件、LCM 机制
│   ├── sync-api.md                   # MemOS Cloud API 参考
│   ├── scripts-reference.md         # 所有脚本统一说明（用途、cron、依赖）
│   ├── pipeline-stages.md            # 日终管线 6 阶段详解
│   ├── candidates-review.md          # P3 记忆候选审核机制
│   └── upgrade-reset.md              # 升级路径、重置流程、卸载步骤
└── README.md                         # This file
```

👉 **完整文档请查阅 `references/INDEX.md`**

---

## How It Works

1. **Every conversation** is automatically indexed into the vector database
2. **Each session** retrieves relevant context via semantic + BM25 hybrid search
3. **Daily** the Dreaming pipeline analyzes logs and promotes insights to long-term memory
4. **Tri-hourly** (*optional*) the three-way sync keeps cloud, local files, and vector store aligned
5. **The Agent** never starts from scratch — it remembers you across sessions

---

## License

MIT — free to use, modify, and redistribute.

---

## Author

**VictorQR** — Open source OpenClaw memory infrastructure
