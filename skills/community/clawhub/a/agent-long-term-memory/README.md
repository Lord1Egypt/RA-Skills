# Agent Long-Term Memory · AI 智能体长期记忆

[![GitHub stars](https://img.shields.io/github/stars/exp007/agent-long-term-memory?style=flat)](https://github.com/exp007/agent-long-term-memory/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/exp007/agent-long-term-memory?style=flat)](https://github.com/exp007/agent-long-term-memory/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-6e4af0.svg)](https://codex.app)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/exp007/agent-long-term-memory/pulls)
[![pip install](https://img.shields.io/badge/pip-install-blue.svg)](https://pypi.org)

**Three-tier long-term memory architecture for AI agents.**

A local-first memory system inspired by human cognition: short-term (recent conversation), structured entity memory (facts like name, preferences, fears), and episodic memory (fuzzy semantic recall). Stores to `~/.codex/agent_memory/`, shared across all projects. Zero cloud dependency.

**三层长期记忆架构**——短期记忆（连贯对话）、实体画像记忆（结构化事实，如姓名/偏好/恐惧）、长期情景记忆（模糊语义召回）。本地存储、跨项目共享，零外部服务依赖。

## Installation · 安装

### Method 1: pip install from GitHub · pip 安装（推荐）

```bash
pip install git+https://github.com/exp007/agent-long-term-memory.git
`

### Method 2: Git clone + pip · 本地开发

```bash
git clone https://github.com/exp007/agent-long-term-memory.git
cd agent-long-term-memory
pip install -e .
`

### Method 3: As a Codex Skill · 作为 Codex 技能

```bash
git clone https://github.com/exp007/agent-long-term-memory.git ~/.codex/skills/agent-memory
`

Then any Codex project can call rom agent_memory import get_memory.

### Method 4: Single-file copy · 复制单文件

Copy src/memory.py into your project and import directly. Only requires chromadb and openai.

### Prerequisites · 前置依赖

- Python 3.10+
- chromadb>=0.4.0 (for Tier 3 episodic memory)
- openai>=1.0.0 (optional — entity auto-extraction; regex fallback if unavailable)

---

## Architecture · 架构

```
+------------------+    +----------------------+    +------------------------+
|  Short-Term      |    |  Entity Memory       |    |  Episodic Memory       |
|  Ring Buffer     |    |  SQLite / Archive    |    |  ChromaDB / Vectors    |
|  短期记忆         |    |  实体画像记忆         |    |  长期情景记忆           |
+--------+---------+    +----------+-----------+    +-----------+------------+
         |                         |                            |
         +-------------------------+----------------------------+
                                   |
                        +----------v-----------+
                        |  Central Processing  |
                        |  中枢处理            |
                        |  = System Prompt     |
                        |  + Entity Cards      |
                        |  + Retrieved Episodes|
                        |  + Recent Messages   |
                        +----------------------+
```

**Tier 1** keeps the last N rounds verbatim for conversational coherence.  
**Tier 2** stores structured facts (name, preferences, fears) in SQLite — precision recall that never fails.  
**Tier 3** embeds conversation chunks into ChromaDB for fuzzy semantic search.  

**第一层**保留最近N轮对话原貌，确保连贯性。  
**第二层**将结构化事实存入 SQLite（如"怕狗""喜欢电影"），精准查档不会出错。  
**第三层**将对话片段向量化存入 ChromaDB，通过语义检索做模糊召回。

## Quick Start · 快速开始

```bash
pip install chromadb openai
git clone https://github.com/exp007/agent-long-term-memory.git
cd agent-long-term-memory
```

```python
from agent_memory import get_memory

mem = get_memory()  # singleton, data at ~/.codex/agent_memory/
                    # 单例模式，数据存在 ~/.codex/agent_memory/

# Tier 2 — structured facts · 结构化事实
mem.remember("name", "Alice")
mem.remember("fear", "dogs", evidence="chased as child", confidence=0.95)
mem.recall("name")   # -> "Alice"

# Tier 3 — episodic memory · 情景记忆
mem.archive("Discussed AI safety concerns")
mem.recollect("AI safety")  # -> matching episodes

# Tier 1 — short-term · 短期记忆
mem.add_turn("What is my name?", "Your name is Alice!")

# RAG — assemble context for LLM prompt · 组装上下文
extension = mem.build_system_extension("What do you know about me?")
# -> "=== User Profile ===\n- name: Alice\n- fear: dogs (conf: 0.95)\n..."
```

**No cloud, no API keys required.** OpenAI key is optional — entity extraction falls back to regex patterns.
## Use Cases · 使用场景

| Scenario | How AgentMemory helps |
|----------|-----------------------|
| AI Companion · AI 陪伴角色 | 第100轮对话精准记得第1轮的细节 |
| Coding Assistant · 编码助手 | 跨项目记住偏好、项目结构、常用模式 |
| Customer Support · 客服机器人 | 结构化存储客户画像，跨 session 精准应答 |
| Personal Knowledge Base · 个人知识库 | 对话片段向量化，随时语义检索 |

## vs. Alternatives · 与同类项目对比

| Feature | AgentMemory | Mem0 | Letta/MemGPT | LangChain Memory |
|---------|------------|------|--------------|------------------|
| Local-first · 本地优先 | Yes | Cloud API | Heavy | Framework-only |
| Three-tier arch · 三层架构 | Yes | No | Partial | No |
| Zero services · 零服务依赖 | Yes | No | No | N/A |
| Codex Skill | Yes | No | No | No |
| Cross-project · 跨项目共享 | Yes | No | No | No |
| ~700 lines · ~700行代码 | Yes | 50k+ | 100k+ | N/A |

AgentMemory is for people who want a simple, inspectable, local memory layer — not a platform.

## API Reference · API 参考

### Tier 2: Entity Memory · 实体记忆

```python
mem.remember(key, value, evidence="", confidence=1.0)  # store fact · 存储事实
mem.recall(key_or_query, limit=10, tags=None)           # lookup · 精确查询
mem.recall_card(key)                                     # full card · 完整卡片
mem.get_profile()                                        # all cards · 所有画像
mem.search_entities(keyword)                             # fuzzy search · 模糊搜索
mem.forget_entity(key)                                   # delete · 删除
mem.clean_stale(threshold=0.3)                           # remove low-confidence · 清理低置信度
```

### Tier 3: Episodic Memory · 情景记忆

```python
mem.archive(content, summary="")   # store chunk · 存储片段
mem.recollect(query, n_results=5)  # semantic search · 语义检索
```

### Tier 1: Short-Term Memory · 短期记忆

```python
mem.add_turn(user_text, assistant_text)  # record turn · 记录对话
mem.get_recent(n=None)                   # recent messages · 最近消息
mem.clear_short_term()                   # reset · 清空
```

### RAG Context · RAG 上下文

```python
mem.build_context(user_query="", episodic_top_k=3)        # full MemoryContext
mem.build_system_extension(user_query="", episodic_top_k=3) # prompt injection string
```

### Auto-Extraction · 自动抽取

```python
mem.auto_remember(conversation_text)
# Uses GPT-4o-mini if OPENAI_API_KEY is set; regex fallback otherwise.
# 有 OpenAI key 就用 LLM 抽取，没有就用正则兜底。
```

### v1 Compat API · v1 兼容接口

Facts/Lessons/Tracked Entities — `add_fact`, `get_fact`, `supersede`, `learn`, `get_lessons`, `track_entity`, `get_entity`, `list_entities`, `stats`, `export_json`, `close`.

## As a Codex Skill · 作为 Codex 技能

Drop-in [Codex](https://codex.app) skill. Install once, available everywhere.

一键安装，全局可用：

```python
from agent_memory import get_memory
mem = get_memory()
system_prompt += mem.build_system_extension(user_query)
```

## Configuration · 配置

| Env var · 环境变量 | Default | Description |
|---------|---------|-------------|
| `OPENAI_API_KEY` | (none) | LLM-based entity extraction · LLM实体抽取 |

```python
# Custom storage · 自定义路径
mem = AgentMemory(data_dir="./my-data")
```

## Tests · 测试

```bash
pip install chromadb openai
python tests/test_memory.py
```
## Contributing · 参与贡献

PRs welcome! Here's how to get involved:

1. [Open an issue](https://github.com/exp007/agent-long-term-memory/issues) — discuss bugs, features, or ideas
2. Fork the repo, create a feature branch (git checkout -b feat/my-feature)
3. Make your changes, add tests if applicable
4. Submit a Pull Request with a clear description

### Roadmap · 路线图

- [ ] Built-in forget/decay mechanism · 内置遗忘机制
- [ ] Multi-user entity isolation · 多用户实体隔离
- [ ] Context window auto-optimization · 上下文窗口自动优化
- [ ] Web dashboard for memory inspection · 记忆检查面板
- [ ] Export to Markdown for human review · 导出可读格式


## License · 许可

MIT — use it, fork it, ship it.

---

*Built for agents that remember. · 为有记忆的智能体而建。*
