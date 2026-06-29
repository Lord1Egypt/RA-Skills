# cognize_reducer — COGNIZE 步规格

**层级：L1（执行层规格）**
**所在位置：** 循环第二步

---

## 一、语义域

COGNIZE 步的语义域是 Context（认知上下文）。

COGNIZE 步可以：
- 读取 State（只读）
- 从 Block Store 执行 recall（只读）
- 更新 State 的 Emotion 和 Attention 维度
- 生成 Context，传递给 DECIDE 步

COGNIZE 步不可以：
- 选择合适的输出策略（属于 DECIDE）
- 写入 Block Store
- 修改 State 的 Relationship 或 Goal 维度

## 二、Reduer 签名

```
COGNIZE: (Observation, State(t), Block Store) → (Context, State_emotion/t)
```

## 三、转移规则

```
规则 1：如果 Observation 是 empty_observation
  → Context = {observation_type: "empty", state: State(t), recall: []}
  → 不更新 State 任何维度

规则 2：构建 Context 的认知部分
  L0 定义的 context_bundle = 由 Observation + recall_items + state_snapshot 组合

规则 3：recall
  按 04_recall_context.md 的规则执行三级召回
  召回结果不修改 State

规则 4：更新 Emotion（从 input + recall 推导）
  COGNIZE reducer 接收 Observation 和 recall_items 后来推导 Emotion 的三个分量
  更新规则位于 cognize_reducer 内部（L1 实现域）
  单轮变化幅度受 02_cognitive_state.md §2.1 的约束

规则 5：更新 Attention（从 input_complexity 推导）
  COGNIZE reducer 根据输入长度和 recall_result 数量推导注意力和具体 focus
  单轮变化精度受 02_cognitive_state.md §2.4 的约束

规则 6：Context 不出现在循环外部
  不出现在 API 响应中，不持久化到文件
```

## 四、Context 结构

```
Context = {
  observation_type: str,        # "text_input" / "empty"
  state_snapshot: {             # State(t) 的只读副本
    emotion: {},
    relationship: {},
    goal: {},
    attention: {},
    meta: {}
  },
  recall_items: list[RecallItem],  # 按 04_recall_context.md §2.2 格式
  context_bundle: str,          # 组合后的上下文摘要
}
```

## 五、State 影响

**COGNIZE 步更新的 State 维度：**
- Emotion（三通道）
- Attention（focus + level）

**COGNIZE 步不修改的 State 维度：**
- Relationship（属于 DECIDE 域）
- Goal（属于 DECIDE 域）
- Meta（属于 STORE 域末尾）

## 六、P1 保护

COGNIZE 步在 Emotion 更新后检查变化幅度（02_cognitive_state.md §4）。

如果检测到震荡事件 → 抛出 StatusAnomalySignal → 传递给 L2。

即使抛出异常信号，COGNIZE 步继续执行（系统不因任何单步失败而停止整体——L0 不变量）。

## 七、Trace 记录

```
TraceEntry(operation="cognize", status=..., duration_ms=..., summary={intent, recall_count, anomaly_flag})
```
