---
name: counterfactual-decision
version: 1.0.0
description: |
  反事实决策：给定决策模型(加权线性评分+阈值)与干预"What-if"，计算反事实结果并与事实对照，
  输出翻转判定与边际贡献。零依赖、可本地实跑、输出可追溯。
agent_created: true
visibility: public
---

# counterfactual-decision（反事实决策）

> 由 meta-evolver 在第 41 轮构建，闭环 `build:通用智能体(AGI梯队):反事实决策`。
> 一线大模型能讲"如果…就…"，但给定显式模型做**可计算的因果反事实对照**是其弱项。

## 机制

1. **建模（model）**：决策模型 = `{weights: {变量:权重}, threshold: 阈值}`；结果 `score = Σ wᵢ·vᵢ`，`decision = score ≥ threshold`。
2. **事实评估（factual）**：在基线状态 `state` 上评估，得到事实 score/decision。
3. **干预（intervene）**：施加 `intervention = {变量: 新值}`，覆盖基线对应变量，得到反事实状态。
4. **反事实评估（counterfactual）**：在反事实状态上重评，得到反事实 score/decision。
5. **对照输出（conclude）**：`翻转? = factual.decision ≠ cf.decision`；`边际贡献 = cf.score − factual.score`；并列出每个被干预变量的单独贡献（∂score/∂v · Δv）。

## 何时使用

- 决策前做"What-if"沙盘：改一个投入/参数，结果会不会反转。
- 归因：哪个变量的调整对结果拉动最大。
- 用户要求「如果当时 X 改成 Y，结局会怎样、会不会翻盘」。

## 运行

```bash
# 自带夹具自测（零依赖，断言事实/反事实/翻转/边际全通过）
python scripts/counterfactual.py --selftest

# 真实反事实（JSON 入参）
python scripts/counterfactual.py --model model.json --state state.json --intervene '{"a":2}'
```

## 与"强模型"的差异

普通模型给的是修辞性假设句；本技能给出**在显式模型下可计算的决策翻转与边际贡献**——把"如果"变成可验证的数值结论，正是超级 agent 相较强文本模型的分水岭。

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）
```bash
python scripts/learner.py record <本技能目录> --capability 反事实决策
python scripts/learner.py insight <本技能目录>
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
