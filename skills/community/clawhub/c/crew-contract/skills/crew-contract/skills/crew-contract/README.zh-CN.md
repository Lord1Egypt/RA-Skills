# Crew Contract — Main–Sub Delegation（主-子分工）

*主代理是指挥，不亲自演奏每个乐器。通用方法层 skill（适配任意 agent 框架）：主代理把握目标/约束/证据/最终判断，有界子代理执行嘈杂工作，独立评审为实质改动把关——内置模型无关的路线卡选择机制。*

[[English](README.md)] | 中文

## 为什么需要

多代理协作的失败方式是可预测的：评审者对同家族产物更宽容（实测家族偏差 3.4–8.4pp）、无协调并行把错误放大至 17.2×、编排成本约 15× 对话 token、子代理被截断即丢失工作。Crew Contract 把**证据支持的做法**写成规则——同样重要的是，明确什么时候**不该**编排。

## 你得到什么

- **五个有界角色**（勘察 / 调研 / 执行 / 测试 / 评审），职责严格分离——评审永远是全新独立上下文；代理不自审、不 commit。
- **派单契约 + 可复制 brief 模板**——自包含派单、预算/停止纪律、歧义契约（`assumptions / needs_input / default_if_forced / blocking_level`）、SAVE-EARLY 落盘韧性。
- **路线卡式模型选择**——不写死任何模型名：候选 = 运行时 provider 清单 ∩ 你的模型政策；执行槽与评审槽开工前定好，按判据选（执行=便宜+缓存亲和；评审=政策允许时跨家族）。
- **证据支撑的护栏**——准入闸门（满足 ≥2 条才编排：可并行 / 单上下文装不下 / 价值覆盖成本）、按缓存→路由→effort 排序的成本杠杆、验证优先级（确定性检查 > 弱验证者 > LLM 裁判）、可选 manifest 断点协议。
- **诚实的局限**——评审独立性是部分的、depth-1 子代理不能提问、无断点续跑；一律列为未解问题，只写缓解不宣称解决。

## 安装

```bash
npx skills add mfang0126/crew-contract   # 适配 77+ 种 agent CLI
```

或 clone 仓库后让你的 agent 技能加载器指向该目录。Hermes Agent 也可从仓库路径安装。

## 60 秒了解方法

1. 判断：小任务 → 只在主线做（skill 内含"不编排"判据）。
2. 选路线：回答路线卡提问（执行槽 + 评审槽），或复用仍然匹配的路线卡。
3. 派发自包含 brief（附模板）——每个可写区域只归一个 worker，先只读勘察。
4. 用最小决定性测试验证；评审深度随风险分级。
5. 主代理亲自回读 diff/产物后才声明完成。

## 证据要点

| 结论 | 来源 |
|---|---|
| 可并行任务 +81% / 严格顺序 −39…−70%；有编排者错误放大 17.2× → 4.4× | [Google 代理规模研究](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/) |
| 多代理 ≈15× 对话 token | [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system) |
| 7 个 SOTA 多代理系统失败率 41–86.7%；"该问不问"占失败 6.8% | [MAST, arXiv:2503.13657](https://arxiv.org/abs/2503.13657) |
| 评审家族偏差 3.4–8.4pp（不含自审情形） | [arXiv:2508.06709](https://arxiv.org/abs/2508.06709)、[arXiv:2609.17857](https://arxiv.org/abs/2609.17857) |
| 长上下文退化在完美检索下依然存在（13.9–85%） | [arXiv:2510.05381](https://arxiv.org/abs/2510.05381) |

完整"规则 → 来源"映射：[`references/evidence-index.md`](references/evidence-index.md)。

## 仓库结构

```
SKILL.md                          # 方法层（框架无关）
references/
  child-brief-template.md         # 可复制派单模板
  evidence-index.md               # 规则 → 公开来源
  hermes-mechanics.md             # Hermes Agent 适配示例
```

## 许可

MIT。欢迎提 issue / 反馈。
