---
name: agent-long-term-memory
description: Three-tier long-term memory for AI agents — short-term + entity + episodic. 三层长期记忆架构：短期记忆 + 实体画像 + 情景记忆。跨项目共享用户画像，让 AI 真正记住你。
---

# Agent Long-Term Memory · AI 智能体长期记忆

## Install from GitHub · 从 GitHub 安装

```bash
git clone https://github.com/exp007/agent-long-term-memory.git ~/.codex/skills/agent-memory
```

Three-tier persistent memory shared at `~/.codex/agent_memory/` across all projects.

三层持久记忆，数据存在 `~/.codex/agent_memory/`，所有项目共享。

## Quick Start · 快速开始

```python
from agent_memory import get_memory

mem = get_memory()
mem.remember("name", "Alice")
mem.recall("name")                    # -> "Alice"
mem.recall("favorite color")          # -> None (not yet stored)
```

## API Reference · API 参考

### Tier 2: Entity Memory · 实体记忆（结构化事实，SQLite）

| Method | Signature | Description |
|--------|-----------|-------------|
| `remember` | `(key, value, evidence="", confidence=1.0)` | Store a structured fact · 存储结构化事实 |
| `remember` | `(content, tags=None, ...)` | Store a fact in v1 compat mode |
| `recall` | `(key_or_query, limit=10, tags=None)` | Lookup by key or search by content · 按 key 精确查或按内容搜 |
| `recall_card` | `(key)` | Get the full EntityCard · 获取完整卡片 |
| `get_profile` | `()` | Return all entity cards · 获取全部画像 |
| `search_entities` | `(keyword)` | Fuzzy search across keys and values · 模糊搜索 |
| `forget_entity` | `(key)` | Delete an entity card · 删除 |
| `clean_stale` | `(threshold=0.3)` | Remove low-confidence cards · 清理低置信度 |
| `entity_count` | property | Number of entity cards · 卡片数量 |

### Tier 3: Episodic Memory · 情景记忆（对话片段，ChromaDB）

| Method | Signature | Description |
|--------|-----------|-------------|
| `archive` | `(content, summary="")` | Store a conversation chunk · 存储对话片段 |
| `recollect` | `(query, n_results=5)` | Semantic search · 语义检索 |
| `episodic_count` | property | Number of stored episodes · 片段数量 |

### Tier 1: Short-Term Memory · 短期记忆（滑动窗口）

| Method | Signature | Description |
|--------|-----------|-------------|
| `add_turn` | `(user_text, assistant_text)` | Record a turn · 记录一轮对话 |
| `get_recent` | `(n=None)` | Get recent messages · 获取最近消息 |
| `clear_short_term` | `()` | Clear buffer · 清空缓冲区 |

### RAG Context Building · RAG 上下文构建

| Method | Signature | Description |
|--------|-----------|-------------|
| `build_context` | `(user_query="", episodic_top_k=3)` | Full MemoryContext · 完整上下文 |
| `build_system_extension` | `(user_query="", episodic_top_k=3)` | Prompt injection string · 系统提示扩展 |

### Auto Extraction · 自动抽取

| Method | Signature | Description |
|--------|-----------|-------------|
| `auto_remember` | `(conversation_text)` | Extract entities from text · 从对话中抽取实体。有 OpenAI key 用 LLM，无则用正则兜底。 |

### v1 Compat API · v1 兼容接口

`add_fact`, `get_fact`, `get_facts`, `list_facts`, `forget`, `supersede`, `forget_stale`, `learn`, `get_lessons`, `apply_lesson`, `track_entity`, `get_entity`, `update_entity`, `list_entities`, `link_fact_to_entity`, `stats`, `export_json`, `close`

## Standard Integration Pattern · 标准集成流程

```
session start:       mem = get_memory(); inject mem.get_profile() into system prompt
every user message:  mem.add_turn(user_msg, assistant_msg)
significant facts:   mem.remember(key, value, evidence)
                     mem.auto_remember(conversation_text)  # auto-extract · 自动抽取
conversation end:    mem.archive(full_conversation, summary)
periodic cleanup:    mem.clean_stale(0.3); mem.forget_stale(30)
shutdown:            mem.close()
```

## Dependencies · 依赖

```
pip install chromadb>=0.4.0 openai>=1.0.0
```

OpenAI key is optional — if unset, entity extraction falls back to regex patterns.
OpenAI key 可选——不配也能用正则兜底。
