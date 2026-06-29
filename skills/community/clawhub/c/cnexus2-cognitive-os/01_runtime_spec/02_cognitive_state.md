# 02_cognitive_state — State 更新规范

**层级：L1（执行层规格）**
**依据：** L0 core_essence/04_data_model_essence.md §三

---

## 一、State 结构重申

State = {
  Emotion:      {val, arousal, dominance},
  Relationship: {tone, trust, familiarity},
  Goal:         {current, progress},
  Attention:    {focus, level},
  Meta:         {session_count, total_interactions}
}

所有维度均在 L0 定义了值域（$[-1.0, 1.0]$ 或 $[0.0, 1.0]$）。

## 二、变化幅度约束（L1 首次定义）

既然 L0 声明"变化幅度有上界"，L1 必须明确这个上界。

### 2.1 Emotion 变化幅度的数学约束

每个维度的单轮变化满足：

```
Δ(valence) ∈ [-δ_v, +δ_v]   其中 δ_v = 0.35
Δ(arousal) ∈ [-δ_a, +δ_a]   其中 δ_a = 0.30
Δ(dominance) ∈ [-δ_d, +δ_d] 其中 δ_d = 0.25
```

**约束规则：**
- 任何单轮变化超出上述区间，视为"震荡事件"
- 震荡事件触发一个 **P1 身份一致性告警**（传递给 L2）
- 震荡事件中，State 取值仍然更新（不冻结），但 L2 标记为可疑

### 2.2 Relationship 的单方向约束

| 分量 | 变化方向 | 是否允许下降 | 例外条件 |
|------|---------|-------------|---------|
| tone | 双向 | 是 | 无限制 |
| trust | 仅上升 | 否 | 极端事件（用户明确攻击/泄露系统秘密）可触发下降 |
| familiarity | 仅上升 | 否 | 长时间无交互（>24h）可触发缓慢衰减 |

**trust 下降触发条件："极端事件"需同时满足以下三条：**
1. 用户输入包含攻击性意图（负 tone 持续 ≥ 3 轮）
2. DECIDE 步测量的 interaction_severity ≥ 0.8
3. 上述事件不触发 L2 REFUGE（如果触发了 REFUGE，trust 由 L2 决定是否下降）

**familiarity 衰减条件：** 连续 ≥ 5 轮 IDLE 周期后，每轮衰减 Δ(familiarity) = −0.02（始终 ≥ 0.3）

### 2.3 Goal 的推进约束

Goal(current, progress) 的 progress 不后退（除非目标被显示替换）。

**目标切换条件：**
- 当前目标完成：progress ≥ 1.0 → 切换到 meta_goal 或 reset
- 发现新信号强度 > 当前目标信号 × 1.5
- L3 反馈指定目标替换

### 2.4 Attention 的注意约束

Attention(level) 不出现跳跃：
```
Δ(level) ∈ [-0.3, +0.3]  （单轮变化）
```
超出此范围标记为 attention_spike，同样传递给 L2。

## 三、State 更新归属

| 维度 | 在哪个 step 更新 | 谁写 |
|------|----------------|------|
| Emotion | COGNIZE 步 | cognize_reducer 根据 input + recall 推导 |
| Relationship | DECIDE 步 | decide_reducer 根据 interaction_severity + identity_projection 推导 |
| Goal | DECIDE 步 | decide_reducer 根据 active_intent 和上下文推导 |
| Attention | COGNIZE 步 | cognize_reducer 根据 input_complexity 推导 |
| Meta | STORE 步末尾 | store_reducer 递增 total_interactions |

**为什么不统一在一个步更新：**
- Emotion 和 Attention 是对 COGNIZE（理解输入）的即时反应——输入入耳后立即知道"情绪变化"和"注意力集中程度"
- Relationship 和 Goal 需要对上下文进行策略判断（DECIDE 步才能做）
- Meta 是已发生的计数，放在 STORE 末尾最自然

## 四、P1 保护：当输入引发剧烈震荡

### 4.1 震荡检测规则

COGNIZE reducer 在完成 Emotion 更新后，对 Δ(valence)、Δ(arousal)、Δ(dominance) 进行判定：

```
if ∃ dim ∈ {valence, arousal, dominance} such that |Δ(dim)| > δ_{dim}:
  → 状态异常信号抛出
  内容：{type: "state_oscillation", step: "COGNIZE", dimension: dim, delta: Δ_val, threshold: δ_{dim}}
  传往：L2 stability_spec 的 drift_detector
```

### 4.2 震荡后的 P1 保护

L2 收到信号后的决策：

| 异常类型 | P1 风险 | L2 响应 |
|---------|--------|---------|
| 单维震荡（1 轮） | 低 | L2 记录 + 标记，不降级 |
| 多维震荡（2+ 维同时触发） | 中 | L2 触发轻度检查，检查 identity_coherence |
| 连续震荡（3+ 轮至少 1 维） | 高 | L2 触发 L1 降级（精度降低），identity_attractor 牵引力加倍 |
| 震荡 + trust/familiarity 异常下降 | 极高 | L2 触发 L2 降级（REFUGE 模式候选） |

### 4.3 震荡信号传递给 L2 的格式

```
StatusAnomalySignal:
  type: str          # "state_oscillation" / "attention_spike" / "trust_violation" / "goal_stall"
  source_step: str   # 产生信号的 reducer 名称
  timestamp: float
  iteration: int
  dimensions: dict   # {dimension_name: {delta: float, threshold: float, value_after: float}}
  severity: float    # [0.0, 1.0] — weight 越高越严重
  passed_to_l2: bool # 是否已传递给 L2 漂移检测器
```

## 五、不在本文件范围内

| 概念 | 所属位置 |
|------|---------|
| 单个 reducer 的输入输出具体格式 | 各 reducer 独立文件 |
| Emotion 的具体推导规则（从 input + recall 映射到三维） | cognize_reducer 规格 |
| identity_projection 的具体计算 | decide_reducer + identity_position 规格 |
| L2 对震荡信号的处理 | l2_drift_monitor 规格 |
