# OpenClaw Agent 记忆系统 / OpenClaw Agent Memory System

> **让 OpenClaw Agent 拥有持久记忆。**
>
> 自动同步 Obsidian 知识库 → Agent 可搜索。会话观察零成本压缩 → 不丢失。向量库 + 嵌入服务 + 同步链路 → 自动健康监控。
>
> **Give your OpenClaw Agent persistent memory.**
>
> Auto-sync Obsidian vault → searchable by Agent. Zero-LLM compression of session observations → nothing lost. Vector DB + embedding service + sync chain → self-healing health monitoring.

---

## 中文

### 它解决什么问题

你用 Obsidian 记了大量笔记，但 OpenClaw Agent 的 `memory_search` 搜不到。
你和 Agent 聊了半天，做了很多决策和发现，对话结束就丢了。
你的 Qdrant 向量库、LM Studio 嵌入服务、vault 同步链路，哪个断了都不知道。

这个技能把这三件事自动化了。

### 快速开始

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/yxyujian98-png/openclaw-agent-memory.git
cd openclaw-memory-system
pip install -r requirements.txt
docker-compose up -d                              # 启动 Qdrant
python scripts/setup.py --vault-dir /path/to/vault  # 7 步自动配置
# 按 setup.py 输出的指引配置 hooks 和 cron
```

### 前置条件

| 组件 | 必需 | 说明 |
|------|:----:|------|
| Python 3.10+ | ✅ | 脚本运行环境 |
| Qdrant | ✅ | 向量数据库，`docker-compose up -d` 一行启动 |
| 嵌入服务 | ✅ | LM Studio / Ollama / 任何 OpenAI 兼容 embedding 端点 |
| Obsidian Vault | ✅ | 你的 Markdown 知识库 |
| LLM API | 可选 | 只有高重要性记忆才需要（DeepSeek / OpenAI 等） |

### 配置

安装向导会自动创建 `scripts/config.json`，你也可以手动编辑：

```json
{
  "vault_dir": "/path/to/your/vault",
  "llm": {
    "baseUrl": "https://api.deepseek.com/v1",
    "apiKey": "你的 API Key",
    "model": "deepseek-chat"
  },
  "embedder": {
    "baseUrl": "http://localhost:1234/v1",
    "apiKey": "你的嵌入服务 Key",
    "model": "text-embedding-nomic-embed-text-v1.5",
    "embeddingDims": 768
  },
  "qdrant": {
    "host": "localhost",
    "port": 6333,
    "collection": "knowledge_base"
  },
  "sync_dirs": ["01-日记", "02-知识", "04-教训", "07-项目"]
}
```

### 它做了什么

```
你的 Obsidian Vault                          OpenClaw memory_search
  ├── 01-日记/     ── sync_vault_memory.py ──→  memory/*.md (SQLite)
  ├── 02-知识/     ── vault_to_qdrant.py   ──→  Qdrant (向量库)
  ├── 04-教训/
  └── 07-项目/

Agent 工具调用     ── observe.py + compress.py ──→ Qdrant (结构化观察)

每 45 分钟自动：vault 健康检查 → 增量同步 → 记忆压缩 → 健康报告
```

### 核心设计

- **零 LLM 成本**：compress.py 用规则驱动把工具调用结构化为类型/概念/重要性，不调 LLM
- **三级嵌入降级**：LM Studio → 本地 ONNX → numpy 哈希，嵌入服务挂了也能跑
- **版本追踪**：Qdrant 向量带 version/is_latest/supersedes，知识演化不冲突
- **PRISM 意图路由**：根据查询意图自动选择最优检索策略
- **抗体自愈**：错误模式自动提取为抗体规则，下次遇到同类错误自动匹配修复

### 脚本一览

#### 核心管线

| 脚本 | Token | 功能 |
|------|:-----:|------|
| `shared_config.py` | 0 | 集中配置（环境变量 > config.json > 默认值） |
| `qdrant_utils.py` | 0 | Qdrant 增删改查 |
| `embedder.py` | 0 | 三级降级嵌入 + LRU 缓存 |
| `compress.py` | 0 | 零 LLM 观察结构化 |
| `observe.py` | 0 | 工具调用观察队列 |
| `sync_vault_memory.py` | 0 | vault → memory/ 增量同步 |
| `vault_to_qdrant.py` | 0 | vault → Qdrant 向量同步 |
| `extract_memories.py` | 按需 | 会话压缩 + 概念聚合 + 蒸馏 |
| `unified_memory.py` | 按需 | Mem0 + Qdrant 统一搜索 |

#### 健康与维护

| 脚本 | 功能 |
|------|------|
| `vault_guardian.py` | vault 健康 + 过时检测 + 增量同步 |
| `memory_health.py` | 4 链路健康检查 |
| `lmstudio_guardian.py` | 嵌入服务健康 + 降级模式 |
| `maintenance_orchestrator.py` | DAG 任务调度器 |
| `setup.py` | 7 步安装向导 |

#### 辅助脚本

| 脚本 | 功能 |
|------|------|
| `vault_watcher.py` | vault 文件变化监听 |
| `vault_maintainer.py` | vault 自动修复 |
| `process_inbox.py` | 收件箱自动分类 |
| `auto_link_vault.py` | 补全 [[wiki 链接]] |
| `compress_to_rule.py` | 执行模式 → 抗体/规则提取 |
| `session_cleaner.py` | 过期文件清理 |
| `health_check_v2.py` | 抗体健康巡检 |
| `context_snapshot.py` | compaction 前上下文备份 |

### 排障

```bash
python scripts/memory_health.py        # 完整健康检查
python scripts/shared_config.py        # 检查配置
openclaw memory status                 # OpenClaw 索引状态
openclaw hooks list                    # Hook 状态
openclaw cron list                     # Cron 任务状态
```

---

## English

### What problem does it solve

You have extensive notes in Obsidian, but OpenClaw Agent's `memory_search` can't find them.
You had hours of conversations with decisions and discoveries, but they're lost when the session ends.
Your Qdrant vector DB, LM Studio embedding service, or vault sync chain — you don't know which one broke.

This skill automates all three.

### Quick Start

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/yxyujian98-png/openclaw-agent-memory.git
cd openclaw-memory-system
pip install -r requirements.txt
docker-compose up -d                              # Start Qdrant
python scripts/setup.py --vault-dir /path/to/vault  # 7-step auto setup
# Follow setup.py output to configure hooks and cron
```

### Prerequisites

| Component | Required | Description |
|-----------|:--------:|-------------|
| Python 3.10+ | ✅ | Script runtime |
| Qdrant | ✅ | Vector database, `docker-compose up -d` to start |
| Embedding server | ✅ | LM Studio / Ollama / any OpenAI-compatible embedding endpoint |
| Obsidian Vault | ✅ | Your Markdown knowledge base |
| LLM API | Optional | Only for high-importance memories (DeepSeek / OpenAI etc.) |

### Configuration

Setup wizard auto-creates `scripts/config.json`, or edit manually:

```json
{
  "vault_dir": "/path/to/your/vault",
  "llm": {
    "baseUrl": "https://api.deepseek.com/v1",
    "apiKey": "your-api-key",
    "model": "deepseek-chat"
  },
  "embedder": {
    "baseUrl": "http://localhost:1234/v1",
    "apiKey": "your-embedding-key",
    "model": "text-embedding-nomic-embed-text-v1.5",
    "embeddingDims": 768
  },
  "qdrant": {
    "host": "localhost",
    "port": 6333,
    "collection": "knowledge_base"
  },
  "sync_dirs": ["01-日记", "02-知识", "04-教训", "07-项目"]
}
```

### What it does

```
Your Obsidian Vault                          OpenClaw memory_search
  ├── 01-日记/     ── sync_vault_memory.py ──→  memory/*.md (SQLite)
  ├── 02-知识/     ── vault_to_qdrant.py   ──→  Qdrant (vector DB)
  ├── 04-教训/
  └── 07-项目/

Agent tool calls   ── observe.py + compress.py ──→ Qdrant (structured observations)

Every 45 minutes: vault health check → incremental sync → memory compression → health report
```

### Core design

- **Zero LLM cost**: compress.py structures tool calls into type/concepts/importance using rules, no LLM calls
- **3-level embedding fallback**: LM Studio → local ONNX → numpy hash, works even when embedding server is down
- **Version tracking**: Qdrant vectors carry version/is_latest/supersedes, no knowledge evolution conflicts
- **PRISM intent routing**: auto-selects optimal search strategy based on query intent
- **Antibody self-healing**: error patterns auto-extracted as antibody rules, matched for auto-fix next time

### Scripts

#### Core pipeline

| Script | Token | Function |
|--------|:-----:|----------|
| `shared_config.py` | 0 | Centralized config (env > config.json > defaults) |
| `qdrant_utils.py` | 0 | Qdrant CRUD |
| `embedder.py` | 0 | 3-level embedding fallback + LRU cache |
| `compress.py` | 0 | Zero-LLM observation structuring |
| `observe.py` | 0 | Tool call observation queue |
| `sync_vault_memory.py` | 0 | vault → memory/ incremental sync |
| `vault_to_qdrant.py` | 0 | vault → Qdrant vector sync |
| `extract_memories.py` | On demand | Session compression + concept consolidation + distillation |
| `unified_memory.py` | On demand | Mem0 + Qdrant unified search |

#### Health & maintenance

| Script | Function |
|--------|----------|
| `vault_guardian.py` | Vault health + stale detection + incremental sync |
| `memory_health.py` | 4-chain health check |
| `lmstudio_guardian.py` | Embedding server health + degraded mode |
| `maintenance_orchestrator.py` | DAG task scheduler |
| `setup.py` | 7-step setup wizard |

#### Auxiliary scripts

| Script | Function |
|--------|----------|
| `vault_watcher.py` | Vault file change listener |
| `vault_maintainer.py` | Vault auto-repair |
| `process_inbox.py` | Inbox auto-categorization |
| `auto_link_vault.py` | Auto-complete [[wiki links]] |
| `compress_to_rule.py` | Execution patterns → antibody/rule extraction |
| `session_cleaner.py` | Expired file cleanup |
| `health_check_v2.py` | Antibody health patrol |
| `context_snapshot.py` | Pre-compaction context backup |

### Troubleshooting

```bash
python scripts/memory_health.py        # Full health check
python scripts/shared_config.py        # Check config
openclaw memory status                 # OpenClaw index status
openclaw hooks list                    # Hook status
openclaw cron list                     # Cron job status
```

---

## License

MIT
