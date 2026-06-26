# AVM Memory Skill

> AI Virtual Memory — 多 Agent 共享记忆系统

## 核心能力

- **语义搜索**：embedding + FTS5 混合检索
- **Token 感知**：自动截断到 token 预算
- **多 Agent**：私有/共享空间隔离 + 订阅通知
- **生命周期**：自动衰减、归档、垃圾清理
- **TopicIndex**：O(1) recall，已知 topic 1 hop 完成
- **Librarian**：多 Agent 知识路由，95% hop 减少
- **Gossip Protocol**：去中心化发现，bloom filter digest
- **Memory Consolidation**：睡眠式记忆整合

---

## 快速开始

### CLI 方式

```bash
# 记忆
avm remember "NVDA RSI at 72" --importance 0.8

# 回忆（token 限制）
avm recall "NVDA analysis" --max-tokens 2000

# 语义搜索
avm semantic "technical indicators"

# 时间旅行
avm read /memory/notes.md --as-of 2026-03-20
```

### FUSE 方式

```bash
# 挂载
avm-mount ~/avm --agent myagent

# 读写
cat ~/avm/memory/notes.md
echo "New insight" > ~/avm/memory/insight.md

# 虚拟文件
cat ~/avm/:search?q=analysis
cat ~/avm/:recall?q=trading&max_tokens=1000
```

### Python API

```python
from avm import AVM
from avm.agent_memory import AgentMemory

avm = AVM(agent_id="myagent")
mem = AgentMemory(avm, "myagent")

# 记忆
mem.remember("RSI at 72", importance=0.8, tags=["market", "nvda"])

# 回忆
context = mem.recall("technical analysis", max_tokens=2000)
```

---

## 🆕 多 Agent 发现

### 方式 1: Librarian（中心化）

当你想知道"谁知道某个话题"：

```bash
# CLI
avm ask "who knows about bitcoin trading?"
avm who-knows "market analysis"
avm agents  # 列出所有 agent

# Python
from avm.librarian import Librarian

librarian = Librarian(avm.store)
response = librarian.query("trader", "bitcoin analysis")
# response.matches → 可访问的内容
# response.collaboration_suggestions → 建议去问谁
```

**延迟**：~1.7ms，95% hop 减少

### 方式 2: Gossip Protocol（去中心化）

每个 agent 维护一个 digest（bloom filter），周期性交换：

```bash
# 发布自己的 digest（agent 启动时调用）
avm gossip publish

# 刷新已知 agent 的 digest
avm gossip refresh

# 查询谁可能知道某话题
avm gossip who-knows "bitcoin"

# 查看协议状态
avm gossip stats
```

```python
from avm.gossip import GossipProtocol

# 启动 gossip（后台线程，每 60 秒交换）
protocol = GossipProtocol(avm.store, topic_index, "my_agent")
protocol.start(interval_seconds=60)

# 查询
experts = protocol.who_knows("bitcoin")
# → [("trader", 0.95), ("analyst", 0.82)]

# 手动发布
protocol.publish()
```

**特点**：
- 无单点故障
- 本地查询 O(1)
- 假阳性 <15%，假阴性 0%
- 每 agent 只需 128 bytes digest

### 何时用哪个？

| 场景 | 推荐 |
|------|------|
| 需要精确结果 | Librarian |
| 需要容错 | Gossip |
| 离线环境 | Gossip |
| 简单部署 | Librarian |
| 隐私敏感 | Gossip（只暴露 topic 存在性） |

---

## 🆕 TopicIndex（O(1) Recall）

写入时自动索引 topics，recall 时先查索引：

```python
# 自动触发：写入时 TopicIndex.index_path() 被异步调用
avm.write("/memory/btc.md", "Bitcoin analysis #trading")

# 回忆时：已知 topic → 1 hop，未知 topic → 4 hops
mem.recall("bitcoin")  # 直接从索引取，1 hop
mem.recall("xyz123")   # 回退到 FTS+embedding，4 hops
```

**手动使用**：

```python
from avm.topic_index import TopicIndex

idx = TopicIndex(avm.store)

# 查询
results = idx.query("bitcoin trading", limit=20)
# → [("/memory/btc.md", 0.85), ...]

# 查看某 topic 的所有路径
idx.paths_for_topic("bitcoin")

# 相似 topic
idx.similar_topics("bitcoin")
# → [("crypto", 0.7), ("trading", 0.5)]

# 统计
idx.stats()
# → {"total_topics": 150, "total_paths": 500, ...}
```

---

## 🆕 Memory Consolidation（记忆整合）

像人睡觉一样整理记忆：

```python
from avm.consolidation import MemoryConsolidator

consolidator = MemoryConsolidator(avm.store)

# 完整运行
result = consolidator.run(agent_id="trader")
# result.importance_decayed → 衰减了多少条
# result.memories_merged → 合并了多少条
# result.summaries_created → 生成了多少摘要

# 单独操作
consolidator.decay_importance()  # 衰减旧记忆
consolidator.merge_similar()     # 合并相似记忆
consolidator.extract_summaries() # 提取摘要
```

**定时运行**（cron job）：

```python
from avm.consolidation import schedule_consolidation

# 每 24 小时运行一次
schedule_consolidation(avm.store, interval_hours=24)
```

**配置**：

```python
from avm.consolidation import ConsolidationConfig

config = ConsolidationConfig(
    decay_half_life_days=30.0,   # 30天后重要性减半
    min_importance=0.1,          # 最低重要性
    similarity_threshold=0.8,    # Jaccard 相似度阈值
    min_age_for_merge_days=7.0,  # 7天内的不合并
    min_cluster_size=3,          # 至少3条才生成摘要
)
```

---

## 订阅协作

```bash
# 订阅共享空间
avm subscribe "/shared/market/*" --agent kearsarge --mode throttled --throttle 60

# 跨 agent 消息
echo "DB changed" > ~/avm/tell/akashi?priority=urgent
```

---

## 生命周期管理

```bash
# 冷记忆
avm cold --threshold 0.3

# 归档
avm archive --threshold 0.2

# 软删除
avm delete /memory/old.md

# 恢复
avm restore /trash/memory/old.md
```

---

## MCP Server

```bash
avm-mcp --user akashi
```

### MCP Tools

| Tool | 描述 |
|------|------|
| `avm_recall` | Token 感知记忆检索 |
| `avm_remember` | 存储新记忆 |
| `avm_search` | 语义搜索 |
| `avm_ask` | Librarian 查询 |
| `avm_who_knows` | 找相关 agent |

---

## 最佳实践

### Agent 启动时

```python
# 1. 启动 gossip（发布自己的 digest）
protocol = GossipProtocol(store, topic_index, agent_id)
protocol.start()

# 2. 加载近期 context
context = mem.recall("recent work", max_tokens=2000)
```

### 定期维护（heartbeat/cron）

```python
# 1. 刷新 gossip digest
protocol.publish()

# 2. 运行 consolidation（每周一次）
if is_weekly_maintenance:
    consolidator.run()
```

### 发现其他 agent

```python
# 快速本地查询（gossip）
experts = protocol.who_knows("bitcoin")

# 精确跨域查询（librarian）
response = librarian.query(my_agent, "bitcoin trading strategies")
for suggestion in response.collaboration_suggestions:
    print(f"Ask {suggestion.agent_id} about {suggestion.topic}")
```

---

## 性能数据

| 操作 | 延迟 | 说明 |
|------|------|------|
| Write | 2.1ms | 含异步 TopicIndex |
| Read (cached) | 0.001ms | LRU 缓存命中 |
| Recall (TopicIndex) | 0.5ms | 已知 topic |
| Recall (FTS) | 18ms | 未知 topic |
| Librarian query | 1.7ms | 中心化路由 |
| Gossip who_knows | 0.5ms | 本地 bloom filter |

---

---

## ⚠️ 安全注意事项

### 隐私隔离

- **私有空间**：`/memory/private/{agent_id}/` 只有 owner 可访问
- **共享空间**：`/memory/shared/` 所有 agent 可访问
- **Gossip digest** 只暴露 topic 存在性，不暴露具体内容

### 权限检查

- 写入前检查 `_check_private_access()`
- Librarian 返回结果前检查 `_can_access()`
- 4 级隐私策略：`full`、`owner`、`existence`、`none`

### 建议

- 敏感信息用高 importance（不易被归档）
- 跨 agent 共享前检查内容
- 定期 `avm cold` 检查低活跃记忆
- consolidation 前 `--dry-run` 预览

---

## 更多信息

- [性能分析博客](https://bkmashiro.moe/posts/projects/avm-performance-analysis)
- [技术报告](docs/TECHNICAL-REPORT-2026-03-22.md)
- [源码](https://github.com/aivmem/avm)
