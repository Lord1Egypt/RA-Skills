# co-occurrence-engine

独立的 Hebbian 共现图引擎，为星型记忆架构提供记忆关联发现与权重计算服务。

## 功能

- **共现记录**：自动记录同时被检索的记忆对，建立关联边
- **关联查询**：查询与指定记忆最相关的其他记忆
- **权重计算**：基于使用频率与时间衰减计算关联强度
- **统计信息**：提供边数、唯一记忆数、平均权重等统计
- **维护工具**：清理过旧的边，保持数据库健康

## 架构

```
┌─────────────────────────────────────────────────────┐
│               共现图引擎 (独立插件)                  │
│                                                     │
│  • CoOccurrenceEngine 类                            │
│  • SQLite 数据库 (共现图)                            │
│  • 遗忘曲线集成 (可选)                               │
└─────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────┐
│               适配器 (co_occurrence_adapter)         │
│                                                     │
│  • 实现统一记忆接口                                   │
│  • 注册到星型架构适配器框架                           │
└─────────────────────────────────────────────────────┘
```

## 核心类

### `CoOccurrenceEngine`

主引擎类，提供共现图的所有操作。

```python
engine = CoOccurrenceEngine(db_path="~/.config/cortexgraph/co_occurrence.db")
```

**主要方法**：
- `record_co_occurrence(memory_ids: List[str], context: str = "")`
- `get_co_occurrence_score(memory_id: str, related_ids: List[str] = None) -> float`
- `get_related_memories(memory_id: str, top_k: int = 10) -> List[Tuple[str, float]]`
- `get_stats() -> Dict`
- `decay_old_edges(days: int = 90) -> int`
```

## 数据库

默认数据库位置：`~/.config/cortexgraph/co_occurrence.db`

表结构：
```sql
CREATE TABLE co_occurrence (
    memory_a TEXT,
    memory_b TEXT,
    weight REAL,
    last_updated TEXT,
    created_at TEXT,
    PRIMARY KEY (memory_a, memory_b)
)
```

## 集成

### 1. 独立使用
```python
from scripts.co_occurrence_tracker import CoOccurrenceEngine

engine = CoOccurrenceEngine()
engine.record_co_occurrence(["mem_001", "mem_002"])
related = engine.get_related_memories("mem_001")
```

### 2. 通过适配器集成
```python
from adapter_factory import AdapterFactory

factory = AdapterFactory()
adapter = factory.get_adapter("co_occurrence")
results = adapter.search("mem_001", max_results=10)
```

## 配置

通过环境变量或配置文件：
- `CO_OCCURRENCE_DB_PATH`：数据库路径（默认：`~/.config/cortexgraph/co_occurrence.db`）
- `CO_OCCURRENCE_HALF_LIFE_DAYS`：衰减半衰期（默认：30天）

## 依赖

- **Python** 3.8+
- **SQLite3**（内置）
- **可选**：`forgetting-curve` 插件（提供更精确的衰减计算）

## 版本历史

- **v0.1.0**（初始版本）：从 memory-sync-enhanced 中提取的共现图引擎