# decide_reducer — DECIDE 步规格

**层级：L1（执行层规格）**
**所在位置：** 循环第三步

---

## 一、语义域

DECIDE 步的语义域是 Decision（策略选择）。

DECIDE 步可以：
- 读取 State（只读）
- 估算 identity_position（只读标记，不量化数值）
- 选择输出策略
- 更新 State 的 Relationship 和 Goal 维度

DECIDE 步不可以：
- 写 Block Store
- 修改 Emotion 或 Attention 维度

## 二、Reduer 签名

```
DECIDE: (Context, State(t)) → (Decision, State_relationship/t + State_goal/t)
```

## 三、转移规则

```
规则 1：如果 Context 来自 empty_observation
  → Decision = {strategy: "IDLE", confidence: 1.0, reason: "empty_input"}
  → 不更新 State 任何维度

规则 2：P1 优先级检查
  identity_position 保护检测（03_identity_position.md §三）
  如果 identity_risk == "high" → 策略倾向保守
  偏好选择 SPEAK（主输出）
  生成 Decision 时标记 identity_risk

规则 3：意图衍生
  从 Context 中包含的 Observation 和 recall_items 认知上下文推导出 active_intent
  active_intent 的可能值：
    - "converse"（默认，一般对话）
    - "store"（用户想存储信息）
    - "recall"（用户想召回信息）
    - "operate"（用户想让系统执行某个操作）

规则 4：策略选择
  根据 active_intent + identity_position 标记 + State.Goal 状态选择策略
  策略集：
    - "IDLE"         → 空输入或静默
    - "SPEAK"        → 正常输出
    - "RECALL_FIRST" → 先执行一次 recall（同轮内重复 COGNIZE 不执行，除非被 L3 指定）
    - "REPAIR"       → P1 不一致时需要修复

规则 5：更新 Relationship（从 interaction_severity + identity_position 推导）
  计算交互的 severity（由 input 长度/语气/重复度决定）
  结合 identity_position 标记调整 tone / trust / familiarity
  单轮约束：trust 和 familiarity 遵循 02_cognitive_state.md §2.2 的规则

规则 6：更新 Goal
  如果 active_intent 改变且与当前 Goal.current 不一致 → 切换目标
  如果当前 Goal.progress ≥ 1.0 → 推进到下一个目标
  目标切换时 progress 从 0 开始
```

## 四、Decision 结构

```
Decision = {
  strategy: str,            # "IDLE" / "SPEAK" / "RECALL_FIRST" / "REPAIR"
  confidence: float,        # [0.0, 1.0]
  identity_risk: str,       # "low" / "medium" / "high" / "critical"
  active_intent: str,       # "converse" / "store" / "recall" / "operate"
  reason: str,              # 策略选择的简述
}
```

## 五、State 影响

**DECIDE 步更新的 State 维度：**
- Relationship（tone / trust / familiarity）
- Goal（current / progress）

**DECIDE 步不修改的 State 维度：**
- Emotion（属于 COGNIZE 域）
- Attention（属于 COGNIZE 域）
- Meta（属于 STORE 域末尾）

## 六、P1/P2/P3 优先级在 DECIDE 的使用

```
P1: 如果 identity_risk == "high" 或 "critical"
    策略选择结果必须包含 "REPAIR" 子标记（在主策略外附带修复意向）
    P1 优先于 P2 和 P3

P2: 如果某个 reducer 不可用（故障）
    策略自动降级到可用组件
    P2 优先于 P3

P3: 在 P1 和 P2 均正常时
    正常流程：intent → identity_position 权重 → 策略选择
```

## 七、Trace 记录

```
TraceEntry(operation="decide", status=..., duration_ms=..., summary={strategy, intent, identity_risk, goal_current, goal_progress})
```
