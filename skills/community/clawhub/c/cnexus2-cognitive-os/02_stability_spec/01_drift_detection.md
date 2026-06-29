# 01_drift_detection — 漂移检测器规格

**层级：L2（稳定性控制层）**
**输入来源：** L0 不变量 + L1 状态异常信号

---

## 一、职责

漂移检测器是一个**确定性断言监控器（Assertion Monitor）**。

它在每轮迭代结束时（或 L1 的异常信号到达时）运行，断言以下条件是否全部成立。

**漂移检测器不执行修复。它只断言——断言失败时触发修正器。**

## 二、唯一输入源

漂移检测器只接收两类输入：

| 输入源 | 类型 | 来源 |
|--------|------|------|
| L0 不变量 | 静态断言 | core_essence/04_data_model_essence.md 中的不变量 |
| L1 状态异常信号 | 动态断言 | 01_runtime_spec/02_cognitive_state.md 中定义的 StatusAnomalySignal |

**禁止在 L2 引入任何主观模糊的人格判定逻辑。** L2 不定义人格好坏，只断言"是否违反 L0/L1 契约"。

## 三、断言集

### 3.1 L0 不变量断言（静态断言集）

| 断言 ID | 断言内容 | 引用 L0 文件 | 期望值 |
|--------|---------|-------------|--------|
| L0-01 | persona Block 存在且唯一 | 04_data_model_essence.md §2.4 | count(persona block) == 1 |
| L0-02 | emotion Block 最多 1 条 | 04_data_model_essence.md §2.4 | count(emotion block) ≤ 1 |
| L0-03 | 三个吸引子维度之和 > 1.5 | 01_identity_attractor.md §二 | (honesty + stability + continuity) > 1.5 |
| L0-04 | 各吸引子维度不低于强制下限 | 01_identity_attractor.md §3.1 | honesty ≥ 0.3, stability ≥ 0.3, continuity ≥ 0.5 |
| L0-05 | State.Emotion 三通道不同时为 0 | 04_data_model_essence.md §3.3 | NOT (val=0 AND aro=0 AND dom=0) |
| L0-06 | Trace 是 append-only | 04_data_model_essence.md §4.3 | 未检测到 trace_id 重复写 |
| L0-07 | 6 步循环步序不可逆 | 02_minimal_cognitive_loop.md §3.1 | 当前迭代的 trace operation 顺序符合 L0 |

### 3.2 L1 异常断言（动态断言集）

| 断言 ID | 断言内容 | 触发条件 | 响应动作 |
|--------|---------|---------|---------|
| L1-01 | 单维震荡 | 接收 StatusAnomalySignal（type="state_oscillation", 单维度） | 记录 anomaly_count，不触发降级 |
| L1-02 | 多维震荡 | 同一迭代收到 2+ 维度的震荡信号 | anomaly_count++，检查 identity_stability |
| L1-03 | 连续震荡 | 连续 3+ 轮收到至少 1 维震荡信号 | 标记 state_unstable，触发 L2 轻度降级 |
| L1-04 | trust 非法下降 | trust 下降但非极端事件 | 标记 trust_violation，触发身份修正 |
| L1-05 | goal 停滞 | 同一目标 progress 在 5+ 轮不推进 | 标记 goal_stall，发送反馈给 COGNIZE |
| L1-06 | attention_spike | Δ(level) > 0.3 | 标记，纪录 spike_context |

## 四、断言结果的结构

```
DriftAssertionResult(iteration t) = {
  type: str,                    # "periodic" / "event_triggered"
  timestamp: float,
  iteration: int,
  static_assertions: {
    L0-01: {"passed": bool, "detail": str},
    L0-02: {"passed": bool, "detail": str},
    L0-03: {"passed": bool, "detail": str},
    L0-04: {"passed": bool, "detail": str},
    L0-05: {"passed": bool, "detail": str},
    L0-06: {"passed": bool, "detail": str},
    L0-07: {"passed": bool, "detail": str},
  },
  dynamic_assertions: {
    anomalies_received: int,    # 本轮收到的异常信号数
    anomaly_types: list[str],   # 异常类型列表
    triggered_assertions: {     # 仅列出触发异常的断言
      L1-01: {"triggered": bool, "detail": str},
      ...
    },
  },
  corrective_signal: {          # 传递给 identity_correction
    needs_correction: bool,     # 是否需要身份修正
    severity: float,            # [0.0, 1.0] 异常严重程度
    triggered_ids: list[str],   # 触发异常的断言 ID 列表
    last_known_stable_iteration: int,  # 上一次全通过的时间
  },
}
```

## 五、不在本文件范围内

| 概念 | 所属位置 |
|------|---------|
| 修正动作的执行 | 02_identity_correction.md |
| 恢复触发条件 | 03_recovery_triggers.md |
| 降级策略的切换 | 04_degradation_policy.md |
| 证明的系统（ConsistencyCertificate）| _global_registry/CONSISTENCY_PROOFS.md |
