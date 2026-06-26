# Dreaming 蒸馏引擎 P0 优化 — 使用说明

## 交付物

| 文件 | 说明 |
|------|------|
| `agent-cluster/memory/immediate_skill_hook.py` | 即时 Skill 生成钩子 |
| `agent-cluster/memory/fts_search.py` | FTS5 全文检索增强层 |
| `agent-cluster/memory/tests/test_immediate_skill_hook.py` | 单元测试（22 tests） |
| `agent-cluster/memory/tests/test_fts_search.py` | 单元测试（27 tests） |

## P0-1：即时 Skill 生成钩子

### 核心机制

任务完成后立即触发，置信度分流：

```
task_result
  → extract_skill_candidate()    LLM提取（失败→规则兜底）
  → confidence >= 0.8  → write_skill_document()   直接写盘
  → confidence 0.5-0.8 → add_to_dreaming_queue()  入梦境队列
  → confidence < 0.5  → discard
```

### 快速使用

```python
from memory.immediate_skill_hook import create_hook

# 创建钩子
hook = create_hook(agent_id="agent-001")

# 在任务执行完成后调用
task_result = await agent.execute(task)
await hook.after_task_complete(task_result)
```

### 高级配置

```python
from memory.immediate_skill_hook import ImmediateSkillHook

hook = ImmediateSkillHook(
    agent_id="agent-001",
    skills_dir="data/skills",           # Skill 文档输出目录
    dream_queue_path="data/dream_queue.jsonl",  # 梦境队列路径
    llm_callable=my_llm_func,          # LLM 提取函数（可选）
    persist_to_memory=True,            # 同步写入记忆系统（供 FTS 检索）
)

# 自定义置信度阈值
hook.HIGH_CONFIDENCE_THRESHOLD = 0.85
hook.MEDIUM_CONFIDENCE_THRESHOLD = 0.6
```

### LLM 提取器（可选）

```python
def my_llm(query: str) -> str:
    """你的 LLM 接口，返回 JSON 字符串"""
    return llm_client.chat([{"role": "user", "content": query}])

hook = ImmediateSkillHook(llm_callable=my_llm)
```

### Skill 文档格式（agentskills.io 兼容）

```markdown
# Fix_SSL_Error

> Fix Python SSL certificate verification error

## Metadata
- **Version**: `1.0.0`
- **Confidence**: `0.92` (LLM structured extraction)
- **Extracted at**: 2026-04-16T00:00:00+00:00
- **Source task**: `task-001`

## Triggers
- `how to fix`

## Actions
1. Update certificates
2. Set REQUESTS_CA_BUNDLE environment variable
```

---

## P0-2：FTS5 全文检索层

### 核心能力

- **纯 FTS5 BM25 排序**：零外部依赖，直接利用 SQLite 内置 BM25
- **snippet 高亮**：`【关键词】` 风格（MaxHermes 同款）
- **过滤**：scope、memory_type、importance、agent_id
- **分页**：offset/limit
- **去重**：按 entry_id 自动去重
- **混合搜索**：可注入语义函数，融合 BM25 + 语义分

### 快速使用

```python
from memory.fts_search import create_searcher

# 纯 FTS5 搜索（推荐，无外部依赖）
searcher = create_searcher()
result = searcher.search("python ssl error", limit=10)

for hit in result.hits:
    print(hit.snippet)   # 【SSL】certificate...
    print(hit.bm25_score)
```

### 过滤与分页

```python
result = searcher.search(
    "deployment",
    scopes=["shared"],              # 作用域过滤
    memory_types=["procedure"],     # 记忆类型过滤
    min_importance=4,               # 最低重要性
    agent_id="agent-001",           # 指定 Agent
    limit=5,
    offset=10,                      # 第二页
)
```

### 混合搜索

```python
from memory.fts_search import HybridSearcher

def my_embedding(query: str, texts: list[str]) -> list[float]:
    """你的 embedding 服务，返回 0-1 相似度分数列表"""
    return embedding_client.similarity(query, texts)

searcher = HybridSearcher()
result = searcher.search(
    "async task handling",
    mode="keyword_first",           # keyword_first | semantic_first | pure_fts
    semantic_weight=0.4,            # 语义权重（0=纯关键词）
    semantic_func=my_embedding,
    limit=10,
)
```

### HybridSearcher 三种模式

| 模式 | 说明 |
|------|------|
| `pure_fts` | 纯 FTS5 BM25，无外部依赖（默认） |
| `keyword_first` | FTS5 为主排序，语义作 boost |
| `semantic_first` | 语义相似度为主，FTS5 候选兜底 |

### snippet 高亮说明

SQLite snippet() 默认返回 `...<b>term</b>...`，本模块使用 `【term】` 风格：

```python
result = searcher.search("ssl", highlight_open="【", highlight_close="】")
# → "【SSL】certificate verify failed"
```

### 获取 Skill 候选（Dreaming 引擎用）

```python
from memory.fts_search import FTS5Searcher

searcher = FTS5Searcher()
skill_candidates = searcher.get_skill_candidates(limit=20)
# → [SearchHit(entry_id=..., is_skill_candidate=True, ...)]
```

---

## 测试运行

```bash
# 运行全部测试
cd agent-cluster
pytest memory/tests/ -v

# 分别运行
pytest memory/tests/test_immediate_skill_hook.py -v
pytest memory/tests/test_fts_search.py -v
```

---

## 与现有系统集成

### 集成 immediate_skill_hook 到 Agent

```python
from memory.immediate_skill_hook import create_hook

hook = create_hook(agent_id="agent-001")

async def run_task(task):
    result = await agent.execute(task)
    # 任务完成后立即触发 Skill 提炼
    await hook.after_task_complete(result)
    return result
```

### 集成 fts_search 到 Dreaming 引擎

```python
from memory.fts_search import create_searcher

searcher = create_searcher()

# Dreaming 引擎召回相关记忆（无需 recall signal）
related = searcher.search(
    query="previous error patterns",
    memory_types=["procedure", "episode"],
    min_importance=3,
    limit=5,
)
```

### 在 memory_api.py 中启用 FTS5 增强

```python
from memory.fts_search import create_searcher

# 在 FastAPI 路由中使用
@router.get("/search")
async def search_memories(q: str, limit: int = 10):
    searcher = create_searcher()
    result = searcher.search(q, limit=limit)
    return result.to_dict()
```
