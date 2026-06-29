# 03_identity_position — 身份位置估算

**层级：L1（执行层规格）**
**依据：** L0 core_essence/01_identity_attractor.md

---

## 一、Identity Position 定义

Identity 不是系统感受——它是 DECIDE 步的一个投影向量。

Identity 在每个迭代中被投影到一个位置。这个位置仅在 DECIDE 步由 decide_reducer 估算，其他步骤不行。

```
IdentityPosition(t) = {honesty, stability, continuity}  ∈ [0,1]³
```

## 二、投影估算规则

Identity Position 不来自数学计算（面向对象方法或公式），而是来自 **语义规则**：

### 2.1 诚实（honesty）的锚定

| 条件 | 估算标记 |
|------|---------|
| DECIDE 策略选择与 COGNIZE 的 context 基本一致 | cautious |
| 最近的交互中系统没有明显的自我矛盾 | consistent |
| 上述二者皆成立 | reliable |
| 上述二者任一不成立 | unreliable |

### 2.2 稳定性（stability）的锚定

| 条件 | 估算标记 |
|------|---------|
| Relationship.tone 在过去 N 轮中波动小于固定阈值 | calm |
| 最近的交互中用户输入模式保持了某种一致性 | stable |
| 当前的 Goal 处于 progress 0.3-0.7（未完成也未近开端） | progressing |
| tone 波动较大或 Goal 频繁切换 | unsettled |

### 2.3 连续性（continuity）的锚定

| 条件 | 估算标记 |
|------|---------|
| persona Block 全程存在 | anchored |
| 近期的 recall 中有高相似度匹配 | familiar |
| 无长时间 gap（>10 轮无交互后恢复） | fragmented |
| Gap 后 recall 中有准确匹配 | recovering |

### 2.4 从标记到位置

L1 层面不将标记映射为具体数值。**数值化映射属于 L2 的 identity_correction。**

L1 只负责：

```
Identity Projection at iteration t:
  根据语义规则，标记每个维度的状态（{可靠|不可靠} / {平稳|起伏} / {锚定|碎片化|恢复中}）
  传递给 DECIDE 步作为身份参考
  DECIDE 根据标记调整策略选择（如：不可靠时优先选择保守策略）
```

## 三、与 P1 的关系

当 `honesty == "unreliable"` 或 `continuity == "fragmented"` 时：

```
P1 保护触发:
  DECIDE 步标记身份风险 (identity_risk: high)
  策略选择倾向保守（选择 SPEAK 主输出，不尝试特殊功能）
  此标记传递给 L2
  L2 根据标记决定是否启动 identity_correction
```

## 四、Identity Position 不更新时的行为

如果系统连续在 IDLE 状态（无输入），identity_position 不更新。它保持在最后一次非 IDLE 迭代时的估算值。

IDLE 模式下的 DECIDE 步（如果触发）只复制上一轮的 identity_position 不做新估算。

## 五、不在本文件范围内

| 概念 | 所属位置 |
|------|---------|
| 语义规则的量化阈值（如 "波动小于固定阈值" 的具体值） | L2 测量细节 |
| 标记到数值的映射 | L2 identity_correction |
| 连续性的 gap 阈值（多少轮算"长时间"） | L2 配置 |
| 长时间 IDLE 后的 recovered 判断 | L2 恢复检测 |
