# 03_recovery_triggers — 恢复触发器规格

**层级：L2（稳定性控制层）**
**输入源：** CorrectionResult（失败时）+ DriftAssertionResult

---

## 一、职责

恢复触发器在修正动作失败（CorrectionResult.status == "failed"）或检测到持续性结构问题时执行。

**恢复触发器的输出是降级信号**，它决定系统进入哪个降级级别，以及何时重新激活（Re-arm）回到正常模式。

## 二、触发条件

| 触发条件 | 信号源 | 严重程度 |
|---------|--------|---------|
| 修正失败—二次震荡 | CorrectionResult.reentrant_oscillation == true | 0.7 |
| 修正失败—收敛性证明失败 | CorrectionResult.convergence_proven == false | 0.8 |
| 连续震荡 > 5 轮 | DriftAssertionResult 的 anomaly_count 累计 | 0.6 |
| L0-01 永久断裂（persona 丢失） | 断言持续 false 超过 3 轮 | 1.0（最高） |
| L1-01 持续 10+ 轮且无收敛 | 动态断言持续异常 | 0.5 |

## 三、恢复路径

### 3.1 REFUGE 模式（最高级别恢复）

```
触发条件：触发条件中任意一个 >= 0.7 严重程度，或 persona 丢失

REFUGE 模式行为：
  - 冻结当前 State（不写入新的 emotion/goal/relationship/attention）
  - 新输入仍然 OBSERVE + STOREl（L0 不变量要求）
  - COGNIZE 执行最简版本（不更新 State 维度）
  - DECIDE 始终选择 "REPAIR"
  - SPEAK 输出固定响应（L3 降级：固定文本）
  - REFLECT 跳过
  - 系统状态标记为 "REFUGING"

REFUGE 模式退出条件：
  - L0 断言集全部通过（01_drift_detection.md §3.1）
  - 至少 2 轮迭代无新异常信号
  - 通过后重新激活（Re-arm），回到正常循环
```

REFUGE 模式的最短持续时间为 **3 轮迭代**（防抖动）。

### 3.2 降级路径选择

```
根据严重程度选择降级路径：
  ≤ 0.3: 无降级（只标记）
  0.4-0.5: L1 降级（精度降低）
  0.6-0.7: L2 降级（REFUGE 模式候选）
  ≥ 0.8: L3 降级（REFUGE 模式激活）
  1.0: 结构冻结—保留 persona 和 archival Block，其余全部归档
```

### 3.3 重新激活（Re-arm）条件

```
从降级状态回到正常状态的重新激活必须满足：

  1. 当前降级级别生效 ≥ 3 轮（防抖动）
  2. DriftAssertionResult 连续 2 轮全部 passed
  3. CorrectionResult 连续 2 轮没有 triggered
  
  满足以上三条后：
    降级级别下调一级（L3→L2→L1→L0）
    每级至少保持 1 轮观察期（确认稳定性）
```

## 四、恢复触发器的输出

```
RecoveryTrigger(t) = {
  triggered: bool,              # 是否触发恢复
  trigger_reason: str,          # 触发条件名称
  severity: float,              # [0.0, 1.0]
  degradation_level: str,       # "L0" / "L1" / "L2" / "L3"
  refu时: bool,                 # 是否进入 REFUGE
  refuge_exit_iteration: int or None,  # REFUGE 预计退出时间
  rearm_conditions_met: bool,   # 重新激活的条件是否达标
  timestamp: float,
}
```

## 五、防抖动

```
不可在 < 3 轮内反复触发降级-升级-降级（间歇性抖动）

防抖动规则：
  1. 进入新降级级别后至少保持 3 轮
  2. 3 轮内即使条件满足也不升级
  3. 降级到升级的路径中每级保持 1 轮观察期
```
