# 02_identity_correction — 身份修正器规格

**层级：L2（稳定性控制层）**
**输入源：** DriftAssertionResult（来自 01_drift_detection.md）+ L0 attractor

---

## 一、职责

身份修正器在收到 corrective_signal（needs_correction = true）时执行。

**修正动作必须是单向收敛的。** 修正将系统状态拉向 attractor 的目标点，不能远离。

## 二、修正的规则

### 2.1 修正路径的选择

根据 triggered_ids（触发异常的断言 ID）选择修正路径：

| 触发断言 ID | 修正路径 | 动作 |
|------------|---------|------|
| L0-01, L0-02 | structural_fix | 恢复 Block 唯一性（删除多余） |
| L0-03, L0-04 | attractor_pull | 增加 attractor 牵引力，强制维度回到下限以上 |
| L0-05 | emotion_reset | 重置 Emotion 三通道到中性状态 (0.0, 0.5, 0.5) |
| L1-03 | continuous_oscillation_dampening | 降低 State.Emotion 的变化灵敏度（通过 L1 调整 update 的步长上限） |
| L1-04 | trust_reinforcement | 修正 trust 到上一轮快照值，标记异常 |
| L1-05 | goal_unstuck | 强制推进/progress 到下一个阶段 |
| 多条同时触发 | composite_repair | 按 severity 从高到低依次执行 |

### 2.2 单向收敛保证

```
修正规则必须满足：
  修正前与 attractor_target 的距离：D_before
  修正后与 attractor_target 的距离：D_after
  保证：D_after < D_before（严格收敛）
```

**验证方法：** 每次修正后，比较 attractor 三个维度的前后位置。如果任何维度远离目标点，则该修正违反单向收敛规则。

### 2.3 修正不可引发二次震荡

```
修正动作的限制：
  修正只修改 L0 定义的问题 block
  修正不修改 State.Emotion 或 State.Attention 的当前值（emotion_reset 除外）
  修正不修改 State.Relationship（trust_reinforcement 除外，但它只回退，不改变方向）
  修正不主动调用外部推理引擎
```

**如果修正本身引发了新的震荡信号**——令修正器立即停止当前修正路径，将本次修正标记为 failed，通知恢复触发器。

### 2.4 Attractor 牵引力计算

```
当触发 attractor_pull（L0-03 或 L0-04 失败）时：
  牵引力方向 = attractor_target - current_position
  牵引力大小 = min(1.0, distance / 恢复步数)
  
  其中恢复步数 = 默认 3 轮（渐进修复，不拉满）
  
  修正后的位置：
    corrected_position = current + pull_force × 恢复步数
    (始终 clamp 在 [0,1]³ 和强制下限以上)
```

## 三、修正结果的结构

```
CorrectionResult(iteration t) = {
  triggered: bool,              # 是否执行了修正
  correction_path: str,         # 上述 2.1 中的路径名
  before: {honesty, stability, continuity},  # 修正前的身份位置（数值化后）
  after: {honesty, stability, continuity},   # 修正后的身份位置（数值化后）
  convergence_proven: bool,     # D_after < D_before 是否成立
  reentrant_oscillation: bool,  # 修正是否引发二次震荡
  status: str,                  # "success" / "failed" / "partial"
  anomaly_signal: StatusAnomalySignal or None,  # 如果修正失败，交给恢复触发器
}
```

## 四、不在本文件范围内

| 概念 | 所属位置 |
|------|---------|
| 身份位置的数值化映射规则 | L1 identity_position 的实现 |
| attractor_target 的具体坐标 | L0 01_identity_attractor.md |
| 修正失败后的恢复触发的执行 | 03_recovery_triggers.md |
| 降级策略 | 04_degradation_policy.md |
