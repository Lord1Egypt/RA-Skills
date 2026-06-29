# CONSISTENCY_PROOFS — L2 一致性证明系统

## 职责

本文件定义系统一致性证明的三种证明类型。证明在每轮迭代结束时生成，由 L2 漂移检测器触发。

证明是为了回答一个问题：**"系统现在是否一致？"**

---

## 一、证明 1：State Consistency Theorem（状态一致性定理）

### 声明

```
∀ t: State(t+1) = f(State(t), OBSERVE(t), recall_items(t))
```

### 含义

- State 不凭空生成
- State 不回应 OBSERVE（OBSERVE 只产 Observation，不写 State）
- State 不跨步跳跃（只更新于 COGNIZE 和 DECIDE 步，不被 SPEAK/STORE/REFLECT 直接修改）

### 证明方法

| 条件 | 检测方法 | 所属文件 |
|------|---------|---------|
| State(t+1) 依赖 State(t) | 检查 COGNIZE 步的输入是否包含上一轮 | 02_stability_spec/01_drift_detection.md |
| State 不被 SPEAK 修改 | 检查 SPEAK 步的 trace 不包含 State 更新操作 | 01_drift_detection L0-07 |
| State 只在 COGNIZE 和 DECIDE 步更新 | 检查各步 Trace 的 operation 与 State 更新字段的映射 | L1 各 reducer 规格 |
| State 所有字段值在 L0 定义的值域内 | 检查 emotion/relationship/goal/attention 各分量 | L0-05, L0-03, L0-04 |

### 证明格式

```
StateConsistency(t) = {
  "theorem": "State(t+1) = f(State(t), OBSERVE(t), recall_items(t))",
  "verification": {
    "state_dependency": {"passed": bool, "details": ""},
    "no_illegal_writes": {"passed": bool, "details": ""},
    "state_boundaries": {"passed": bool, "details": ""}
  },
  "passed": bool,
  "timestamp": float,
  "iteration": int
}
```

---

## 二、证明 2：Loop Soundness Theorem（循环健全性定理）

### 声明

```
∀ t: exists next_step(t)
  next_step(t) ∈ {OBSERVE, COGNIZE, DECIDE, SPEAK, STORE, REFLECT}
  next_step(t) != current_step(t)
```

### 含义

- 在每轮迭代中，6 步按序执行
- 不存在 reorder
- 不存在 implicit step（6 步之外的隐藏步骤）
- 降级路径不引入新步骤

### 证明方法

| 条件 | 检测方法 | 所属文件 |
|------|---------|---------|
| 每一步有合法 successor | 检查本步 trace 的下一个操作 | 01_drift_detection L0-07 |
| 不存在 reorder | 检查 trace 操作序与 L0 定义的 6 步序列一致 | 01_drift_detection L0-07 |
| 不存在 implicit step | 检查 trace 中 operation 字段只含 6 种之一 | 01_drift_detection L0-07 |
| 降级路径中新步骤 | 检查降级路径中各 step 仍属于 6 种之一 | 02_stability_spec/04_degradation_policy |

### 证明格式

```
LoopSoundness(t) = {
  "theorem": "∀ t: exists valid next_step(t)",
  "verification": {
    "step_succession": {"passed": bool, "details": ""},
    "no_reorder": {"passed": bool, "details": ""},
    "no_implicit_step": {"passed": bool, "details": ""},
    "degradation_no_new_step": {"passed": bool, "details": ""}
  },
  "passed": bool,
  "timestamp": float,
  "iteration": int
}
```

---

## 三、证明 3：Identity Stability Theorem（身份稳定性定理）

### 声明

```
∀ t: ||Identity(t+1) - Identity(t)||_∞ ≤ ε (其中 ε = 0.1)
```

Identity(t) = {honesty, stability, continuity} ∈ [0,1]³
||·||_∞ = max 范数（三维的最大变化值）

### 证明方法

| 条件 | 检测方法 | 所属文件 |
|------|---------|---------|
| 单轮变化 ≤ 0.1 | 检查 identity 各维度的前后差值 | 02_stability_spec/01_drift_detection |
| 无 runaway drift | 连续 N 轮漂移方向是否一致 | 01_drift_detection L1-03 |
| 不低于强制下限 | 检查各维度值 | L0-03, L0-04 |

### 证明格式

```
IdentityStability(t) = {
  "theorem": "||Identity(t+1) - Identity(t)||_∞ ≤ ε",
  "verification": {
    "per_dim_change": {
      "honesty": {"delta": 0.0, "passed": bool},
      "stability": {"delta": 0.0, "passed": bool},
      "continuity": {"delta": 0.0, "passed": bool}
    },
    "no_runaway": {"passed": bool, "details": ""},
    "above_threshold": {"passed": bool, "details": ""}
  },
  "passed": bool,
  "timestamp": float,
  "iteration": int
}
```

---

## 四、证明聚合

三种证明在每轮迭代结束时聚合为一个 **ConsistencyCertificate**：

```
ConsistencyCertificate(t) = {
  "iteration": int,
  "certification": {
    "state_consistency": bool,
    "loop_soundness": bool,
    "identity_stability": bool
  },
  "all_passed": bool,
  "broken_since": int or None,
  "timestamp": float
}
```

## 五、证明的监控和触发

| 证明失败 | 触发 | 说明 |
|---------|------|------|
| StateConsistency(t) = false | LEAK detection | 可能 L1 越界写 State |
| LoopSoundness(t) = false | ENTROPY detection | 可能 loop 结构被修改 |
| IdentityStability(t) = false | identity drift 检测 | 可能 attractor 失效 |
| 连续 5 轮 all_passed = false | 结构冻结 | 02_stability_spec/03_recovery_triggers.md |

## 六、不在本文件内

| 内容 | 所属位置 |
|------|---------|
| 检测器的具体实现细节 | 02_stability_spec/01_drift_detection.md |
| 修复流程 | 02_stability_spec/02_identity_correction.md |
| 恢复触发和防抖动 | 02_stability_spec/03_recovery_triggers.md |
| 降级策略 | 02_stability_spec/04_degradation_policy.md |
| Type System | GLOBAL_SEMANTIC_REGISTRY.md |
