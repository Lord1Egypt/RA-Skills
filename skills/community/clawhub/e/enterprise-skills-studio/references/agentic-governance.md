# Agentic AI 治理（管一支 Agent 队伍）

> 与 `references/process-systems.md` 的分工：**process-systems 讲"单个技能/工作流怎么做"**（连接器/状态机/事务安全/HITL），本篇讲"怎么治理一批 Agent/技能组成的体系"——评估、护栏、可观测、责任归属、人机协同。前者是 construction，后者是 governance。

## 一、为什么 Agentic 需要专门治理

- Agent 会**自主串联多步、调用工具、写外部系统**，失败的爆炸半径远大于单次问答。
- 概率性 LLM + 确定性系统的接缝处最易出事（幻觉、越权、不可逆写）。
- 一个 Agent 出错能牵连整条业务流程 → 必须有"队伍级"护栏与责任链。

## 二、五大治理支柱

| 支柱 | 要点 | 落地检查 |
|------|------|----------|
| **评估 Evaluation** | 上线前离线评测 + 回归基线 + 基准集；每次改 prompt/模型都重跑 | 有评测套件（`scripts/eval_gen.py`）吗？改动能回归吗？ |
| **护栏 Guardrails** | 权限边界、确定性边界、敏感动作升级、拒绝/兜底路径 | 写动作有确认门吗？越界能拒吗？ |
| **可观测 Observability** | 结构化日志、trace、指标、审计链；出错可回溯 | 每次调用有 trace id + 前后值吗？ |
| **责任归属 Accountability** | 谁对 Agent 决策负责（owner/业务方/平台）；事故复盘 | 每个技能有 owner 吗？事故有复盘吗？ |
| **人机协同 HITL** | 何时升人力、升级路径、人在环确认点 | 高风险步骤有 human gate 吗？ |

## 三、Agentic 成熟度（接 `scripts/maturity_assess.py` 的 agentic 维度）

0. 无 Agentic，全是单轮问答
1. 有少量脚本化 Agent，但无评测/无护栏
2. 关键 Agent 有评测 + 人工确认门 + 基础日志
3. 评测自动化 + 护栏体系 + 可观测 + 职责分离
4. 评估/护栏/可观测/责任闭环，事故可自愈式复盘

## 四、治理自审清单

- [ ] 每个 Agent/技能有 owner 与责任链？
- [ ] 上线前有评测套件且改动能回归？
- [ ] 敏感/写动作有 guardrail 与 human gate？
- [ ] 调用有 trace + 审计链，出错可回溯？
- [ ] 越界/异常有明确的拒绝与兜底路径？
- [ ] 事故有复盘并回流到 Evolution Log？
