# M-A3 多Agent记忆层架构设计

> 跨 Agent 知识共享与协同记忆系统 | agent-cluster/memory/

---

## 一、设计目标

| 目标 | 实现方式 |
|------|---------|
| 会话记忆同步 | SessionSync + JSONL 事件日志 |
| Agent 私有记忆隔离 | PrivateMemory + SQLite scope 隔离 |
| 共享知识池 | SharedKnowledgePool + 权限矩阵 |
| 持久化存储检索 | PersistentStore + FTS5 全文索引 |

---

## 二、架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    外部调用方（Agent / Orchestrator）           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│              MemoryRouter（统一入口/路由层）                     │
│  · 自动 scope 判断   · 权限校验   · 路由分发                   │
└───────┬─────────────────┬──────────────────┬────────────────┘
        │                 │                  │
        ▼                 ▼                  ▼
┌───────────────┐ ┌─────────────────┐ ┌────────────────────┐
│ PrivateMemory │ │SharedKnowledgePool│ │   SessionSync      │
│ (Agent私有隔离)│ │  (跨Agent共享)   │ │  (会话同步+事件流)   │
└───────┬───────┘ └────────┬────────┘ └────────┬─────────────┘
        │                  │                   │
        ▼                  ▼                   ▼
┌──────────────────────────────────────────────────────────────┐
│                 PersistentStore（SQLite 持久化）                │
│  ┌──────────────────┐  ┌──────────────────────────────────┐ │
│  │  WAL 模式高并发   │  │  FTS5 全文搜索索引                 │ │
│  │  乐观锁版本控制   │  │  软删除 + 自动清理触发器            │ │
│  └──────────────────┘  └──────────────────────────────────┘ │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ memory.db     │  │sessions.db   │  │session_events.jsonl│  │
│  │ (记忆主库)    │  │ (会话元数据) │  │ (事件流日志)       │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                  MemoryIndex（检索增强层）                      │
│  · 多信号加权重排   · 相似记忆发现   · 热门标签   · 知识图谱   │
└──────────────────────────────────────────────────────────────┘
```

---

## 三、三层记忆作用域

### 3.1 Private（私有记忆）
- 每个 Agent 独立的存储空间
- 权限：`agent_id == self`（仅自己可读/写）
- 内容：个人偏好、专用知识、提炼规则、任务中间状态
- TTL：由重要性自动决定（CRITICAL=1年，EPHEMERAL=1小时）

### 3.2 Shared（共享知识池）
- 所有 Agent 可读，授权 Agent 可写
- 权限矩阵：
  ```
  orchestrator  → 可写全部
  admin         → 可写全部
  其他Agent     → 仅可读
  ```
- 池子类型：
  - `shared_facts` - 共享事实（库存状态、汇率等）
  - `collaboration_artifacts` - 协作成果（分析报告、决策文档）
  - `org_knowledge` - 组织知识（政策、业务规则）
  - `global_rules` - 全局协作协议

### 3.3 Session（会话记忆）
- 仅当前会话参与者可见
- 会话结束后 24 小时自动过期
- 内容：事件流、中间结果共享、决策广播

---

## 四、文件结构

```
agent-cluster/memory/
├── __init__.py              # 包导出
├── memory_core.py           # 核心数据模型（MemoryEntry, Query, Result）
├── persistent_store.py      # SQLite 持久化（WAL + FTS5 + 触发器）
├── private_memory.py        # Agent 私有记忆（隔离读写）
├── shared_knowledge.py      # 共享知识池（权限矩阵）
├── session_sync.py          # 会话同步（事件流 + 快照）
├── memory_index.py          # 全文检索（加权重排 + 知识图谱）
├── memory_router.py          # 统一路由入口
├── memory_api.py             # FastAPI REST 接口（可选）
├── memory_integration.py    # 集成胶水（Agent记忆胶水/会话恢复/协同）
└── demo.py                   # 使用演示
```

---

## 五、核心接口

### 5.1 统一写入 `MemoryRouter.memorize()`
```python
entry_id = mr.memorize(
    content="SKU001 库存预警：仅剩 50 件",
    agent_id="inventory",
    scope=MemoryScope.SHARED,          # 或 "private" / "session" / "auto"
    memory_type=MemoryType.FACT,
    importance=MemoryImportance.HIGH,
    tags=["inventory", "alert"],
    related_agent_ids=["finance", "procurement"],
)
```

### 5.2 统一查询 `MemoryRouter.recall()`
```python
result = mr.recall(
    agent_id="finance",
    query_text="库存",
    scope="shared",
    limit=20,
)
for entry in result.entries:
    print(entry.content)
```

### 5.3 Agent 记忆胶水 `AgentMemoryGlue`
```python
glue = AgentMemoryGlue("inventory")

# 装饰器：自动记忆任务结果
@glue.memorize_outcome
def query_inventory(sku):
    return db.query(sku)

# 快捷方法
glue.remember_preference("优先仓库", "华东")
glue.remember_knowledge("爆款规则：日销 > 30 件需补货")
glue.remember_rule("安全水位 = 3天 × 日均销量")

# 跨Agent同步
glue.share_with(
    content="库存预警：SKU001 仅剩 50 件",
    target_agent_ids=["procurement", "finance"],
)
```

### 5.4 会话恢复 `SessionRecovery`
```python
recovery = SessionRecovery("inventory")

# 保存检查点
recovery.save_checkpoint(session_id, task_state={"step": 2, "data": result})

# 加载检查点
state = recovery.load_checkpoint(session_id)
```

### 5.5 协同记忆 `CollaborationMemory`
```python
collab = CollaborationMemory("orchestrator")

# 启动协作
session_id = collab.start_collaboration(
    task_id="月度报告",
    participants=["finance", "procurement", "sales"],
)

# 记录决策（自动提议为全局规则）
collab.record_collaboration_decision(
    session_id=session_id,
    decision="毛利率目标 35%",
    decided_by="finance",
)
```

---

## 六、权限矩阵

| 操作 | Agent自身 | 其他Agent | Orchestrator |
|------|----------|----------|-------------|
| 读私有记忆 | ✅ | ❌ | ✅ |
| 写私有记忆 | ✅ | ❌ | ❌ |
| 读共享知识 | ✅ | ✅ | ✅ |
| 写共享知识 | ❌ | ❌ | ✅ |
| 读会话记忆 | ✅（参与者）| ✅（参与者）| ✅ |
| 写会话记忆 | ✅（参与者）| ✅（参与者）| ✅ |
| 删除他人共享 | ❌ | ❌ | ✅ |

---

## 七、生命周期管理

```
记忆创建 → 访问计数 → TTL 倒计时
                            ↓
    ┌── 重要性 ≥ HIGH ──→ 保留长期
    │
    └── 重要性 < HIGH ──→ TTL 到期 ──→ 软删除 ──→ FTS触发器自动清理
                                                    │
                                            ┌── 超过30天 ──→ 最终删除
                                            └── 30天内 ──→ 可恢复
```

---

## 八、FastAPI 启动方式

```python
from agent_cluster.memory.api import create_api
from agent_cluster.memory import MemoryRouter

router = MemoryRouter()
app = create_api(router)

# uvicorn.run(app, host="0.0.0.0", port=8081)
```

API 端点：
- `POST /memory/memorize` - 存储记忆
- `POST /memory/recall` - 查询记忆
- `POST /knowledge/publish` - 发布共享知识
- `POST /session/create` - 创建协作会话
- `POST /sync` - 跨Agent知识同步
- `GET /context/{agent_id}` - 构建Agent上下文

---

## 九、集成现有系统

### 9.1 Orchestrator 集成
```python
from agent_cluster.memory.memory_integration import OrchestratorMemoryMixin

class Orchestrator(OrchestratorMemoryMixin, BaseOrchestrator):
    def on_task_complete(self, task, result, agent_id):
        self.memorize_task_outcome(
            task=task.description,
            agent_id=agent_id,
            outcome=str(result),
            success=result.status == "success",
        )
```

### 9.2 专业 Agent 集成
```python
from agent_cluster.memory.memory_integration import AgentMemoryGlue

class InventoryAgent:
    def __init__(self):
        self.memory = AgentMemoryGlue("inventory")
    
    def query(self, sku):
        result = self._query_db(sku)
        self.memory.remember_task("query_inventory", str(result), True)
        return result
```

---

## 十、性能特性

| 特性 | 实现 |
|------|------|
| 高并发写入 | SQLite WAL 模式 |
| 全文检索 | FTS5（支持前缀匹配） |
| 检索加速 | 重要性加权重排 |
| 连接复用 | 单例连接池 |
| 内存效率 | SessionContext 按需加载 |
| 数据安全 | 软删除 + 乐观锁 |
