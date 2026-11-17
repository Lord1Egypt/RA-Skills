# Project Lifecycle Fallback / 项目生命周期回退模块

Use this reduced-fidelity module only when `project-lifecycle-navigator` is unavailable. Turn unclear or changing intent into a bounded project decision, then route formal governance or implementation onward.

本模块只在 `project-lifecycle-navigator` 不可用时使用，把模糊或变化中的意图转化为有限范围的项目决策，再把正式治理或实现交给后续专门流程。

## Supported Modes / 支持模式

- New-project discovery and MVP boundary / 新项目发现与 MVP 边界
- Mid-project realignment / 项目中期校准
- Repository-wide health review / 全项目健康度审查
- Latest-delivery alignment review / 最新交付对齐审查
- Owner-led target rebaseline proposal / Owner 主导的目标重基线建议

Keep the last three modes separate. A whole-project audit cannot sign QA, a latest-delivery review is not another full scan, and a rebaseline proposal is not authorization.

后三种模式必须分开。全项目审计不能签署 QA，最新交付审查不是再次全量扫描，重基线建议也不等于授权。

## Minimum Outputs / 最小输出

- selected mode and boundary / 模式与边界
- current facts and evidence / 当前事实与证据
- project goal, core user, and user-visible value / 项目目标、核心用户和用户可见价值
- MVP or active delivery scope and Non-Goals / MVP 或当前交付范围与 Non-Goals
- unknowns, conflicts, risks, and assumptions / 未知、冲突、风险与假设
- retain/fix/upgrade/rewrite/pause/remove decisions when relevant / 必要时给出保留、修复、升级、重写、暂停、移除决定
- observable acceptance and next validation / 可观察验收与下一项验证
- Owner decisions and exact next action / Owner 决定与准确下一步

## Rules / 规则

1. Inspect available repository and governance evidence read-only before asking questions.
2. Ask only questions that materially change the decision.
3. Propose unclear targets as `TBD - Owner Confirmation Required`; do not write them as authority.
4. Distinguish `implemented`, `partial`, `verified`, `unverified`, `unusable`, `documentation-conflict`, and `not-executed`.
5. Do not code, dispatch work, or sign QA acceptance.
6. Hand formal governance to `cms-project-governance` and authorized implementation to `agent-loop-engineering`.

1. 先只读检查已有仓库和治理证据，再提问。
2. 只询问会实质改变决定的问题。
3. 不清楚的目标标记为 `TBD - Owner Confirmation Required`，不得写成权威目标。
4. 区分 implemented、partial、verified、unverified、unusable、documentation-conflict 和 not-executed。
5. 不写代码、不派发工作、不签署 QA 验收。
6. 正式治理交给 `cms-project-governance`，授权实现交给 `agent-loop-engineering`。
