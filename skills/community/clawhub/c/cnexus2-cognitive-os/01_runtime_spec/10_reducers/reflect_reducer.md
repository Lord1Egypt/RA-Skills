# reflect_reducer — REFLECT 步规格

**层级：L1（执行层规格）**
**所在位置：** 循环第六步（最后一步）

---

## 一、语义域

REFLECT 步的语义域是 Narrative + Belief Delta + Self-model 调优。

REFLECT 步评估本轮迭代对系统自身状态的影响，调整 State 中的元认知维度。

REFLECT 步是不影响本轮响应的循环步骤（REFLECT 可缺失——L0 不变量）。

REFLECT 步不可以：
- 写 Block Store（narrative / reflective Block 除外）
- 修改 Emotion / Relationship / Goal / Attention 等核心维度
- 调外部推理引擎

## 二、Reduer 签名

```
REFLECT: (StoreResult, State(t+), Trace of this iteration) → (ReflectResult, State_meta微调)
```

## 三、转移规则

```
规则 1：如果本轮 STORE 步 failed
  → REFLECT 仍然执行（不影响反思）
  → ReflectResult 中记录 anomaly_note

规则 2：Narrative 合成
  收集本轮迭代的摘要：
  - OBSERVE 的 type
  - COGNIZE 的 intent + recall_count
  - DECIDE 的 strategy + identity_risk
  - SPEAK 的 inference_type + token_count
  - STORE 的 blocks_written
  将上述信息合成为一个 narrative 条目的内容
  写入 Block Store（label = "narrative", decay_rate = 0.08）

规则 3：Belief 调整
  回顾本轮 trace，评估 recall 的有效性和 State 变化的稳定性
  如果本轮平稳（无震荡信号 → State.Emotion 的所有分量变化均在 L1 约束内）
    → belief 维持或微增（+0.02，始终 ≤ 1.0）
  如果本轮发生震荡
    → belief 衰减（−0.05，始终 ≥ 0.0）
  如果 belief 衰减幅度 |Δ| > 0.10
    → 生成误差信号传递给 L2

规则 4：reflective Block 写入
  label = "reflective", content = 本轮自省摘要
  decay_rate = 0.15
  写入 Block Store

规则 5：State 微调
  REFLECT 步修改的 State 内容只限于 meta 中与 self-model 相关的追踪字段
  （如果有条件提供）
  不修改 Emotion/Relationship/Goal/Attention 四个主维度
```

## 四、ReflectResult 结构

```
ReflectResult = {
  narrative_written: bool,         # 是否写入了 narrative Block
  reflective_written: bool,        # 是否写入了 reflective Block
  belief_delta: float,             # belief 变化值
  belief_after: float,             # 调整后的 belief 值
  state_oscillation_detected: bool,# 本轮是否检测到 State 异常
  anomaly_signal_sent: bool,       # 是否向 L2 发送异常信号
  iteration: int,                  # 迭代号
  timestamp: float,
}
```

## 五、State 影响

**REFLECT 步修改的 State 内容：**
- Meta 中 self-model 追踪字段（如果有）
- 不影响 Emotion / Relationship / Goal / Attention

## 六、缺失时的行为

如果 REFLECT 步因任何原因未执行（REFLECT_SKIPPED 错误）：

```
下一轮 REFLECT 步尝试补偿：
  如果上一轮 narrative 未写入 → 本轮写入 (narrative of (prev + current))
  如果上一轮 reflective 未写入 → 本轮可同时写入
```

但 State 的 belief 调整不补偿——缺失的那轮 belief 不做回顾性修复。

## 七、Trace 记录

```
TraceEntry(operation="reflect", status=..., duration_ms=..., summary={narrative, belief_delta, oscillation_flag})
```
