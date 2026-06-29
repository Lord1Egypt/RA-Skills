---
name: agent-openclaw-memory
description: "OpenClaw Agent 自进化记忆系统。零 token 成本运行、Obsidian vault 实时同步、向量检索、自愈健康监控、自动归档/分类/清理，不需要人工干预。Self-evolving memory system for OpenClaw agents."
---

# OpenClaw Agent 自进化记忆系统

> **OpenClaw Agent 的自进化记忆系统。**
>
> 零 token 成本运行 — 脚本自动压缩/索引/检索，不烧 Agent token。Obsidian vault 实时同步 — 知识库自动进入 Agent 记忆。自进化 — 执行模式自动提炼为规则，记忆越用越聪明。自愈 — 出错自动修复，不需要人管。
>
> **Self-evolving memory system for OpenClaw Agent.**
>
> Zero-token operation — scripts handle compression/indexing/search, no Agent tokens burned. Obsidian vault real-time sync — knowledge base auto-enters Agent memory. Self-evolving — execution patterns auto-distilled into rules, memory gets smarter over time. Self-healing — errors auto-fixed, no human intervention.

## 关键词 / Keywords

自进化记忆、零 token、本地知识库、自动记忆管理、长期记忆、向量检索、Obsidian vault、Qdrant、embedding、agent memory、自愈监控、自动维护、DAG 调度、抗体自愈、概念聚合、记忆蒸馏、健康检查

self-evolving memory, zero token, local knowledge base, auto memory management, long-term memory, vector search, Obsidian vault, Qdrant, embedding, agent memory, self-healing, auto maintenance, DAG scheduler, antibody healing, concept consolidation, memory distillation, health monitoring

---

## 中文

### 这是什么

一个 OpenClaw 的记忆增强技能。解决了三个问题：

1. **Vault 内容进不了记忆** — 你用 Obsidian 记了大量笔记，但 Agent 的 `memory_search` 搜不到
2. **会话记忆丢失** — 工具调用、决策、发现等有价值信息，对话结束就没了
3. **记忆系统维护成本高** — 向量库、嵌入服务、同步链路，哪个断了都不知道

### 为什么用脚本而不是纯 prompt

ClawHub 上大部分记忆技能是纯 SKILL.md — 用 prompt 教 Agent 自己写文件、grep 搜索、手动整理。问题：

- **Token 成本高**：Agent 每次存/搜/整理都要读写文件，100 条记忆整理一次烧 50K token
- **不靠谱**：Agent 可能忘记写、分类错、不去重，全靠“自觉”
- **不自动**：不聊天时什么都不发生，要用户手动提醒整理

本技能用 30 个 Python 脚本替代 Agent 的手动操作：

| 操作 | 纯 prompt 方案 | 本技能 |
|------|---------------|--------|
| 存一条记忆 | Agent 读+写+分类 ≈ 2000 token | compress.py **0 token** |
| 搜一条记忆 | grep 返回原始文本 ≈ 1000+ token | memory_search 返回 3 条 ≈ 300 token |
| 整理 100 条 | Agent 全读再分类 ≈ 50000 token | heartbeat 自动跑 **0 token** |
| 文件膨胀 | token 线性增长 | token 不变（脚本扛） |

### 自进化自动管理

装好后完全自动运行，不需要人工干预：

- **每 45 分钟**：heartbeat 自动执行 15 个维护任务（vault 同步、记忆压缩、健康检查、断链修复…）
- **每 6 小时**：重型维护（概念聚合、记忆蒸馏、项目 Profile 重建）
- **实时**：vault 文件变化 → 自动检测 → 自动同步到向量库
- **自愈**：错误模式自动提取为抗体规则，下次遇到同类错误自动修复
- **自进化**：执行模式自动压缩为规则，高频观察自动晋升为知识

你不需要提醒 Agent “该整理了”，不需要手动清理过期文件，不需要检查向量库是否同步。脚本按时间表自动跑，出问题自动修。

### 安装

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/yxyujian98-png/vault-memory-system.git
cd openclaw-memory-system
pip install -r requirements.txt
docker-compose up -d
python scripts/setup.py --vault-dir /path/to/vault
```

### 前置条件

| 组件 | 必需 | 说明 |
|------|:----:|------|
| Python 3.10+ | ✅ | 脚本运行环境 |
| Qdrant | ✅ | 向量数据库 |
| 嵌入服务 | ✅ | LM Studio / Ollama / OpenAI 兼容 |
| Obsidian Vault | ✅ | Markdown 知识库 |
| LLM API | 可选 | 高重要性记忆才需要 |

### 运行时数据流

```
┌─────────────────────────────────────────────────────┐
│                Layer 1: OpenClaw 内置                 │
│                                                     │
│  session-memory hook → memory/YYYY-MM-DD-HHMM.md   │
│  memory-compact hook → compaction 前提取记忆          │
│  memory-extract hook → /new、/reset 时提取           │
│                       ↓                             │
│  memory_search ← SQLite (FTS5 + sqlite-vec + 混合)  │
└─────────────────────────────────────────────────────┘
         │ sync_vault_memory.py
         ↓
┌─────────────────────────────────────────────────────┐
│                Layer 2: 自定义脚本                     │
│                                                     │
│  Cron 每 45 分钟 → orchestrator --light --parallel  │
│    → vault_guardian / extract_memories / memory_health│
│    → 12 个任务按 DAG 拓扑并行执行                      │
│                                                     │
│  Qdrant (knowledge_base)                            │
│    → vault 分块 / 工具观察 / 融合概念                  │
└─────────────────────────────────────────────────────┘
```

### 核心设计

- **零 LLM 成本**：compress.py 纯规则驱动
- **三级嵌入降级**：LM Studio → ONNX → numpy 哈希
- **版本追踪**：version / is_latest / supersedes
- **PRISM 意图路由**：事实型 / 过程型 / 反思型 / 时序型
- **抗体自愈**：错误模式 → 自动修复规则

---

## English

### What is this

An OpenClaw memory enhancement skill. Solves three problems:

1. **Vault content not in memory** — You have extensive Obsidian notes, but Agent's `memory_search` can't find them
2. **Session memory lost** — Tool calls, decisions, discoveries — all gone when session ends
3. **Memory system maintenance costly** — Vector DB, embedding service, sync chain — which one broke?

### Why scripts instead of pure prompt

Most memory skills on ClawHub are pure SKILL.md — they teach the Agent to write files, grep search, and organize manually. Problems:

- **High token cost**: Agent reads/writes files for every store/search/organize. Organizing 100 memories costs ~50K tokens
- **Unreliable**: Agent may forget to write, misclassify, skip dedup — depends on "self-discipline"
- **Not automatic**: Nothing happens when you're not chatting. User must manually remind Agent to organize

This skill replaces manual Agent operations with 30 Python scripts:

| Operation | Pure prompt approach | This skill |
|-----------|---------------------|------------|
| Store one memory | Agent read+write+classify ≈ 2000 tokens | compress.py **0 tokens** |
| Search one memory | grep returns raw text ≈ 1000+ tokens | memory_search returns 3 results ≈ 300 tokens |
| Organize 100 items | Agent reads all then classifies ≈ 50K tokens | heartbeat auto-runs **0 tokens** |
| File growth | tokens scale linearly | tokens stay flat (scripts handle it) |

### Self-evolving automatic management

Runs fully automatic after installation. No human intervention needed:

- **Every 45 minutes**: heartbeat runs 15 maintenance tasks (vault sync, memory compression, health check, broken link repair…)
- **Every 6 hours**: heavy maintenance (concept consolidation, memory distillation, project profile rebuild)
- **Real-time**: vault file changes → auto-detected → auto-synced to vector DB
- **Self-healing**: error patterns auto-extracted as antibody rules, auto-fix on next occurrence
- **Self-evolving**: execution patterns auto-compressed into rules, frequent observations auto-promoted to knowledge

You don't need to remind Agent “time to organize”. Don't need to manually clean expired files. Don't need to check if vector DB is synced. Scripts run on schedule, fix problems automatically.

### Installation

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/yxyujian98-png/vault-memory-system.git
cd openclaw-memory-system
pip install -r requirements.txt
docker-compose up -d
python scripts/setup.py --vault-dir /path/to/vault
```

### Prerequisites

| Component | Required | Description |
|-----------|:--------:|-------------|
| Python 3.10+ | ✅ | Script runtime |
| Qdrant | ✅ | Vector database |
| Embedding server | ✅ | LM Studio / Ollama / OpenAI-compatible |
| Obsidian Vault | ✅ | Markdown knowledge base |
| LLM API | Optional | Only for high-importance memories |

### Runtime data flow

```
┌─────────────────────────────────────────────────────┐
│                Layer 1: OpenClaw Built-in            │
│                                                     │
│  session-memory hook → memory/YYYY-MM-DD-HHMM.md   │
│  memory-compact hook → extract before compaction    │
│  memory-extract hook → extract on /new, /reset      │
│                       ↓                             │
│  memory_search ← SQLite (FTS5 + sqlite-vec + hybrid)│
└─────────────────────────────────────────────────────┘
         │ sync_vault_memory.py
         ↓
┌─────────────────────────────────────────────────────┐
│                Layer 2: Custom Scripts               │
│                                                     │
│  Cron every 45m → orchestrator --light --parallel   │
│    → vault_guardian / extract_memories / memory_health│
│    → 15 tasks in DAG topological parallel           │
│                                                     │
│  Qdrant (knowledge_base)                            │
│    → vault chunks / tool observations / fused concepts│
└─────────────────────────────────────────────────────┘
```

### Core design

- **Zero LLM cost**: compress.py is purely rule-driven
- **3-level embedding fallback**: LM Studio → ONNX → numpy hash
- **Version tracking**: version / is_latest / supersedes
- **PRISM intent routing**: factual / procedural / reflective / recency
- **Antibody self-healing**: error patterns → auto-fix rules

---

## License

MIT
