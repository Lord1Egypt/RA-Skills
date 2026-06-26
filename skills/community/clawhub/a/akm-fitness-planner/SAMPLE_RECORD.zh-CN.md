<!--
文件：SAMPLE_RECORD.zh-CN.md
核心功能：提供 AKM Fitness 的中文脱敏样本，展示输入快照、结构化记录、决策输出与变化原因。
输入：真实健身使用记录的轻脱敏重写版。
输出：供 GitHub 中文页、ClawHub 溯源码或内部审阅者快速理解 Fitness skill 工作流的公开样本。
-->

# Fitness 脱敏样本

## 输入快照

- 主目标：减脂优先，同时保住上肢力量和下背安全
- 身体限制：不接受高脊柱压缩负荷，避免诱发腰椎滑脱相关风险
- 器械现实：商业健身房可用，但高峰时段不能假设深蹲架一定空闲
- 时间预算：本次训练硬上限 45 分钟
- 恢复状态：睡眠差，轻度疲劳，无急性关节疼痛
- 近期背景：上一练已经用了较多上肢推训练量

## 结构化记录

```yaml
Profile:
  GoalPriority:
    1: 减脂依从性
    2: 力量保持
    3: 低风险下肢刺激
  BodyConstraints:
    - 腰椎稳定性历史问题
    - 避免高脊柱负荷
    - 避免疲劳状态下动作崩坏
  EquipmentContext:
    - 绳索器械
    - 哑铃
    - 腿举机
    - 不依赖深蹲架
  TimeBudget:
    session_cap_minutes: 45
  RecoveryState:
    sleep: 低于基线
    systemic_fatigue: 轻度
    acute_pain: 无
  RecentLoad:
    previous_session_bias: 上肢推
    lower_body_readiness: 可训练，但不适合高轴向负荷
```

## 决策输出

```yaml
StateJudgment: constrained-but-trainable
PrimaryDecision: 今天做低脊柱负荷的下肢与核心稳定训练，而不是重蹲主导日
DecisionConfidence: medium
Plan:
  - 腿举：中等负荷，控制节奏，3 组工作组
  - 哑铃罗马尼亚硬拉：仅在腰部反馈稳定时做轻技术组
  - 保加利亚分腿蹲或登阶：用单侧容量替代高轴向负荷
  - 绳索抗旋核心
  - 若腰部稳定性下降或疲劳明显上升，立即停止
RiskNotes:
  - 睡眠差会降低高技能重负荷训练容错
  - 依赖深蹲架的方案今天会制造不必要执行摩擦
NonNegotiables:
  - 不做杠铃背蹲
  - 不做极限负荷
  - 训练不延长到 45 分钟以外
MissingInputs: []
```

## 为什么输出变了

这个决策不是从一个泛化的“腿日模板”开始的。
它之所以改变，是因为有效动作空间被四个具体变量同时收窄：

1. 下背限制排除了高脊柱负荷
2. 恢复偏差降低了高技能高强度动作的容错
3. 时间上限排除了复杂分块计划
4. 器械不确定性让深蹲架依赖方案变得脆弱

最后产出的仍然是训练决策，但它是画像优先，而不是模板优先。
