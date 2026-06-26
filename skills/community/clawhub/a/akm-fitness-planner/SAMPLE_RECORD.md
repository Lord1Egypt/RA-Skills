<!--
文件：SAMPLE_RECORD.md
核心功能：提供 AKM Fitness 的英文脱敏样本，展示输入快照、结构化记录、决策输出与变化原因。
输入：真实健身使用记录的轻脱敏重写版。
输出：供 GitHub、ClawHub 或审阅者快速理解 Fitness skill 工作流的公开样本。
-->

# Fitness Sample Record

## Input Snapshot

- Primary goals: reduce body fat while preserving upper-body strength and lower-back safety
- Physical limits: no spinal compression tolerance, avoid aggravating lumbar instability
- Equipment reality: commercial gym available, but no guarantee of open squat rack at peak hours
- Time budget: 45 minutes hard cap
- Recovery state: slept poorly, mild fatigue, no acute joint pain
- Recent context: previous session already used heavy pushing volume

## Structured Record

```yaml
Profile:
  GoalPriority:
    1: fat-loss adherence
    2: strength retention
    3: low-risk lower-body stimulus
  BodyConstraints:
    - lumbar instability history
    - avoid high spinal loading
    - avoid fatigue-driven technical breakdown
  EquipmentContext:
    - cable stack
    - dumbbells
    - leg press
    - no rack dependency
  TimeBudget:
    session_cap_minutes: 45
  RecoveryState:
    sleep: below baseline
    systemic_fatigue: mild
    acute_pain: none
  RecentLoad:
    previous_session_bias: upper-body pushing
    lower_body_readiness: usable but not ideal for axial loading
```

## Decision Output

```yaml
StateJudgment: constrained-but-trainable
PrimaryDecision: run a low-spinal-load lower-body and trunk-stability session instead of a heavy squat-centered day
DecisionConfidence: medium
Plan:
  - leg press: moderate load, controlled tempo, 3 working sets
  - dumbbell Romanian deadlift: light technique sets only if lumbar response stays stable
  - split squat or step-up: unilateral volume without axial loading
  - cable anti-rotation core work
  - stop if lumbar stability drops or fatigue rises sharply
RiskNotes:
  - poor sleep lowers tolerance for high-skill heavy loading
  - rack-dependent plans create avoidable execution friction today
NonNegotiables:
  - no barbell back squat
  - no maximal loading
  - no plan extension beyond 45 minutes
MissingInputs: []
```

## Why This Output Changed

The decision did not start from a generic "leg day" template.
It changed because the valid action space was narrowed by four concrete factors:

1. lower-back constraints removed heavy spinal loading
2. poor recovery reduced tolerance for high-skill intensity
3. time cap ruled out complex multi-block programming
4. equipment uncertainty made rack-dependent planning fragile

The result is still a training decision, but it is profile-first rather than template-first.
