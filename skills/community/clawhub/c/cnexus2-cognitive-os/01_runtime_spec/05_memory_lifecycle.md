# 05_memory_lifecycle — Block 生命周期规范

**层级：L1（执行层规格）**
**依据：** L0 core_essence/04_data_model_essence.md §二

---

## 一、Block 存在周期

每个 Block 从创建到淘汰经历三个阶段：

```
ACTIVE → STALE → ARCHIVE → DISCARDED
                 ↓
              REACTIVATE（如果被高 importance recall 命中）
```

| 阶段 | Importance 区间 | 行为 |
|------|----------------|------|
| ACTIVE | ≥ 0.40 | 正常参与 recall |
| STALE | [0.20, 0.40) | 低频 recall 可命中 |
| ARCHIVE | [0.05, 0.20) | 仅精确匹配可命中，不参与语义召回 |
| DISCARDED | < 0.05 | 从 store 中移除（不可恢复） |

每个阶段的边界值不可由 L1 修改（属于 L2 或 L3 的可调参数区域）。

## 二、衰减规则

### 2.1 衰减触发条件

```
如果 Block.decay_rate > 0.0，则每轮迭代（iteration）执行衰减：
  importance(t+1) = importance(t) × (1 − decay_rate)

如果 Block.decay_rate = 0.0，则永不衰减。
```

**DecayRate = 0.0 的 Block 类型：**

| Block 类型 | 默认 decay_rate | 备注 |
|-----------|----------------|------|
| persona | 0.0 | 核心身份——永不衰减 |
| archival | 0.01 | 长期事实——极慢衰减 |
| emotion | 0.30 | 情感快照——快速淘汰，仅留最新一条 |
| intent | 0.15 | 目标——中等衰减 |
| belief | 0.05 | 信念——慢衰减 |
| narrative | 0.08 | 叙事——中慢衰减 |
| episodic | 0.20 | 事件——中等快速衰减 |
| reflective | 0.15 | 反思——中等衰减 |

**DecayRate 不可为负。** Block 不可自增 importance。

### 2.2 特殊规则：recall 后的重要性修正

当 Block 被 recall_items 命中时（其 block_id 出现在 L1/L2/L3 任一召回层的结果中），该 Block 的 importance 获得临时补偿：

```
如果 Block 本轮被 recall 命中：
  importance = importance + 0.02
  上限 clamp at 1.0
```

这是唯一一个能阻止衰减的机制。不存在"手动提升"路径。

## 三、淘汰规则

### 3.1 触发淘汰的条件

存储空间受限。当以下条件之一满足时，触发淘汰流程：

```
条件 A：Block Store 中的 Block 数量 ≥ 10,000 条
条件 B：内存使用超过预设上限（具体量由 L2 定义）
```

### 3.2 淘汰策略

```
1. 筛选所有 DISCARDED (importance < 0.05) 的 Block → 优先移除
2. 如果 DISCARDED 移除后仍超上限：
   从 ARCHIVE (importance < 0.20) 中按 importance 升序淘汰
3. 淘汰到上限的 80%（8,000 条）为止
```

### 3.3 不可淘汰的 Block

以下 Block 即使 importance 很低也不淘汰：

```
- persona label 的 Block（唯一、永久存在）
- 当前迭代内新创建的 Block（防止刚存即删）
- 被 L3 标记为 protected 的 Block
```

## 四、合并规则

### 4.1 合并触发条件

相临迭代中产生的连续 episodic Block 在以下条件同时满足时可以合并：

```
条件 1：两条 Block 的 label 均为 "episodic"
条件 2：两条 Block 的创建时间差 ≤ 5 轮迭代
条件 3：两条 Block 的 importance 差值 ≤ 0.15
条件 4：合并后的 content 不超过 800 字符
```

### 4.2 合并的调和规则

```
合并后的 Block：
  content = 第一条的摘要 + " → " + 第二条的摘要
  importance = max(重要性_1, 重要性_2) × 1.05  # 轻微加成，上限 clamp 1.0
  decay_rate = 两种 decay_rate 的调和平均值
  created_at = 两条中较早的时间戳
  version = 两条版本号的 max + 1
```

**不变量保护：合并不覆盖 persona / emotion / archival 等非 episodic label 的 Block。**

### 4.3 信念合并（belief）

两个 belief Block 在不可调和时，遵循以下优先级：

```
如果 belief_1.content 和 belief_2.content 相互矛盾：
  保留信任度高的 belief（比较的是 trust 分量，非 importance）
  被覆盖的 belief 不删除，降为 importance × 0.5
```

> 这里的"信任度"指 Block 自身携带的 belief_weight，即 L0 中定义的 belief Block 的 importance 字段。两个 belief 在 content 冲突时，信任度高的胜出，另一条的 importance 腰斩。

### 4.4 叙事合并（narrative）

narrative Block 合并必须保留时间线完整性：

```
合并后的 narrative content 格式：
  [time_range: t_start→t_end] {key_event_1} → {key_event_2} → ...
```

narrative 合并不降级 importance（叙事价值不因合并而降低）。

## 五、STORE 步执行逻辑

### 5.1 各 Block 类型的写入规则

| 类型 | 写入时机 | 写入数量 |
|------|---------|---------|
| persona | 系统初始化时写入一次 | 1 条 |
| emotion | 每轮 COGNIZE 后覆盖写入 | 覆盖写最新一条 |
| intent | DECIDE 步检测到新 intent 时写入 | 1-3 条 |
| belief | REFLECT 步中 belief_delta 触发 | 不定期 |
| narrative | 每轮 REFLECT 步后 | 同轮不超过 1 条 |
| episodic | 每轮 STORE 步 | 1 条 |
| archival | DEPECIDE 步或 L3 反馈中鉴定为高价值 | 1 条 |
| reflective | REFLECT 步 | 1 条 |

**每轮至少写入 1 条 Block（emotion 或 episodic）。** 不能有干环。

### 5.2 Block 的上限

全局 Block 数上限 10,000 条（此值可由 L2 或 L3 调整）。超过即触发淘汰流程。

## 六、不在本文件范围内

| 概念 | 所属位置 |
|------|---------|
| Block 的物理存储实现 | 实现层 |
| 10,000 条上限的调整机制 | L2 降级策略 |
| 运行时 importance 的衰减调度器 | L2 监控 |
| 合并的精确语法解析 | L1 store_reducer |
