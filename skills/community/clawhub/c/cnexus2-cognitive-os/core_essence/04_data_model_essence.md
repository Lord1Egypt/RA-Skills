# 04_data_model_essence — 数据模型核心

## 一、等式

```
System Memory = Block + State + Trace
```

Block、State、Trace 是系统的三种基本数据类型。每种类型有各自的结构和语义。

## 二、Block（记忆块）

### 2.1 定义

Block 是系统记忆的基本存储单元。每一条 Block 包含一段独立内容及其元数据。

### 2.2 结构

| 字段 | 类型 | 值域 | 语义 |
|------|------|------|------|
| ID | string | UUID | 唯一标识符 |
| Label | string | persona / emotion / intent / belief / narrative / episodic / archival / reflective | 类型标签 |
| Content | string | — | 记忆内容 |
| Importance | float | [0.0, 1.0] | 重要性 |
| DecayRate | float | [0.0, 0.05] | 衰减率 |
| CreatedAt | int | unix timestamp | 创建时间 |
| UpdatedAt | int | unix timestamp | 最后更新时间 |
| Version | int | ≥ 1 | 版本号 |

### 2.3 8 种 Block 类型

| Label | 语义 | 数量约束 |
|-------|------|---------|
| persona | 人格自我，系统核心身份 | 始终唯一 |
| emotion | 情感状态，当前轮情感快照 | 仅最新一条活跃 |
| intent | 目标动机，当前与近期目标 | 1-3 条活跃 |
| belief | 信念，多个信念并存 | 无上限 |
| narrative | 叙事，故事线摘要 | 无上限 |
| episodic | 事件，交互事件记录 | 无上限 |
| archival | 长期事实，低频高价值事实 | 无上限 |
| reflective | 反思，自省输出 | 无上限 |

### 2.4 不变量

- persona label 的 Block 全程存在且唯一
- emotion label 的 Block 只保留最新一条
- DecayRate = 0.0 的 Block 不衰减

## 三、State（认知状态）

### 3.1 定义

State 是系统在任意时刻的当前认知状态。它不是 Block（不存储在 Block store 中），而是作为一个单独的状态实体维护。

### 3.2 结构

State 包含四个维度和一个迭代元信息：

**1. Emotion（情感状态）**

| 分量 | 值域 | 语义 |
|------|------|------|
| valence | [-1.0, 1.0] | 情感效价，从负面到正面 |
| arousal | [0.0, 1.0] | 唤醒度，从平静到激动 |
| dominance | [0.0, 1.0] | 支配度，从被动到主动 |

**2. Relationship（关系状态）**

| 分量 | 值域 | 语义 |
|------|------|------|
| tone | [-1.0, 1.0] | 关系语调，从敌对到友好 |
| trust | [0.0, 1.0] | 信任度，从怀疑到信赖 |
| familiarity | [0.0, 1.0] | 熟悉度，从陌生到熟悉 |

**3. Goal（目标状态）**

| 分量 | 类型 | 语义 |
|------|------|------|
| current | string | 当前活跃目标 |
| progress | [0.0, 1.0] | 目标完成程度 |

**4. Attention（注意力状态）**

| 分量 | 类型 | 语义 |
|------|------|------|
| focus | string | 当前关注焦点 |
| level | [0.0, 1.0] | 注意力水平 |

**5. Meta（迭代元信息）**

| 分量 | 类型 | 语义 |
|------|------|------|
| session_count | int | 会话计数 |
| total_interactions | int | 总交互次数计数 |

### 3.3 不变量

- Emotion 的三个分量不能同时为 0（系统不存在"无情"状态）
- Trust 和 familiarity 只上升不下降（除非极端事件）
- Valence 的变化幅度有上界（上界值属于 L1 执行约束，不在 L0 定义）
- State 每轮必须推进（至少 total_interactions 递增）

## 四、Trace（溯源轨迹）

### 4.1 定义

Trace 是系统每个操作的不可变记录。它不存储原始数据，只存储操作摘要。

### 4.2 结构

| 字段 | 类型 | 值域 | 语义 |
|------|------|------|------|
| TraceID | string | UUID | 唯一标识 |
| Timestamp | int | unix timestamp | 操作发生时间 |
| Operation | string | observe / cognize / decide / speak / store / reflect | 操作名称 |
| Status | string | success / failed / degraded | 操作状态 |
| Component | string | — | 组件名称 |
| DurationMs | int | ≥ 0 | 操作耗时 |
| Error | string | — | 失败时的错误信息 |

### 4.3 不变量

- Trace 是 append-only（不可修改已有 trace）
- Trace 不包含原始交互内容（只记 metadata）
- Trace 的保留数量有限制，超出后循环覆盖

## 五、三元组关系

- **Block** 存储"过去"——系统经历过的所有可召回的记忆
- **State** 存储"现在"——系统的当前状态
- **Trace** 存储"过程"——系统如何从一个状态到另一个状态的轨迹

Block 与 State 通过 Trace 关联：每一条 trace 记录了一个操作前后的 state 变化，以及操作中涉及到的 block。

## 六、不在本文件范围内

| 概念 | 所属层级 |
|------|---------|
| 存储实现（文件 / LanceDB / 内存） | L1 runtime_spec |
| 读写 / 缓存 / 降级策略 | L1 runtime_spec |
| 衰减 / 淘汰算法 | L1 runtime_spec |
| 存储目录结构 | L1 runtime_spec |
| Trace 的循环覆盖规则 | L1 runtime_spec |
| Block 上限（当前 10,000 条） | L1 runtime_spec |
