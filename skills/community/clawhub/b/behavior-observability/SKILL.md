---
name: behavior-observability
description: |-
  给自主智能体/自动化流水线提供「行为可观测性」：把每一次动作（工具调用、LLM 调用、决策门、
  审核结论）以结构化事件落盘，支持多维查询、指标聚合（错误率/平均时延/P95）与行为时间线回放，
  便于事后审计、故障归因与策略调优。与 safety-guardrails（决策）和 human-in-loop-review（审核）
  互补：它们的决策/审核事件都应 emit 到本日志，形成完整可信行为轨迹。
  触发词：行为可观测性、行为追踪、审计日志、事件溯源、observability、trace、agent 监控、
  行为时间线、错误率统计。
agent_created: true
version: 1.0.0
display_name: "行为可观测性"
display_name_en: "Behavior Observability"
description_zh: "智能体行为结构化追踪/查询/指标/时间线回放"
description_en: "Structured tracing, metrics and replay for agent behavior"
visibility: "public"
---

# 行为可观测性（behavior-observability）

## 什么时候用
- 需要复盘「自主 agent 到底做了什么、哪一步出错、时延花在哪」。
- 元进化/定时任务每小时跑，但没人盯着——靠结构化日志做无人值守审计。
- 对接 `agent-eval-harness`：把本日志作为健康度度量的数据源。

## 核心机制
1. **结构化事件** `emit(type, action, status, agent, risk, parent, duration_ms, payload)`：
   每条含 id / ts / type / action / status / agent / risk / parent / duration_ms / payload。
2. **多维查询** `query(type=, status=, agent=, since=)`：按需过滤出行为子集。
3. **指标聚合** `metrics()`：总量、按类型、按状态、错误率、平均时延、P95 时延。
4. **时间线回放** `timeline()`：按发生顺序重建行为轨迹，定位异常节点。

## 用法
```bash
python scripts/observability.py --selftest

python scripts/observability.py --emit '{"type":"tool_call","action":"delete /data","status":"error","agent":"agent-7","risk":"critical","duration_ms":5}'
python scripts/observability.py --query '{"status":"error"}'
python scripts/observability.py --metrics
python scripts/observability.py --timeline
```

## 与生态集成
- `safety-guardrails`：每次 `gate()` 决策 → `emit(type="guardrail_decision", risk=level, status=decision)`。
- `human-in-loop-review`：每次审核结论 → `emit(type="review", status=approved/rejected)`。
- `agent-eval-harness`：直接消费 `metrics()` 的错误率/时延做回归告警。
- `super-agent-loop`：每个 DAG 节点执行完 → `emit` 一条，形成端到端 trace。
---

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次成功使用（--capability 填本次主要能力名，如「简历优化」「比价」）
python scripts/learner.py record <本技能目录> --capability 简历优化
# 记录一次失败/异常
python scripts/learner.py record <本技能目录> --capability 简历优化 --fail --error 格式识别失败 --note "用户上传了非标准文件"
# 记录用户偏好（下次直接使用）
python scripts/learner.py prefer <本技能目录> --key 输出语言 --val 中文
# 查看累计洞察（高频能力 / 反复错误）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
