# Migration From The Monolithic v1 Design / 从 v1 单体设计迁移

Version 2.0 changes `ai-workflow-os` from a duplicated all-in-one controller into a router. Keep specialist skills independently installable and authoritative. Do not copy their complete state machines back into this package.

2.0 版本把 `ai-workflow-os` 从重复实现全部能力的单体控制器改为路由器。专门 Skill 保持独立安装和权威性，不要再把它们的完整状态机复制回本包。

## Lifecycle / 项目生命周期

Route project discovery, MVP planning, realignment, repository-wide review, latest-delivery review, and target rebaseline to `project-lifecycle-navigator`. Use `modules/project-lifecycle.md` only as a reduced-fidelity fallback.

把项目发现、MVP 规划、中期校准、全项目审查、最新交付审查和目标重基线路由到 `project-lifecycle-navigator`。只有专门 Skill 不可用时才使用回退模块。

## Formal Governance And Coding / 正式治理与编码

Route persistent targets, Work Orders, Controller/QA state, and acceptance to `cms-project-governance`. Route authorized coding and coding-loop evidence to `agent-loop-engineering`.

持久目标、Work Order、Controller/QA 状态和验收交给 `cms-project-governance`；授权编码和编码循环证据交给 `agent-loop-engineering`。

## Project Memory / 项目记忆

Keep `daily-workflow` authoritative for explicit checkpoint, wrap-up, and handoff memory. Reuse existing project-owned files; do not create a parallel `Docs/` schema.

明确由 `daily-workflow` 管理 checkpoint、收工和交接记忆。复用项目已有文件，不创建平行 `Docs/` 体系。

Legacy mappings remain read-only until confirmed:

```text
PROJECT_TARGET.md  -> TARGET.md
PROJECT_STATUS.md  -> STATUS.md
COMPLETED_JOBS.md  -> COMPLETED.md
PENDING_JOBS.md    -> PENDING.md
NEXT_STEPS.md      -> NEXT_ACTIONS.md
SCHEDULE.md        -> NEXT_ACTIONS.md compatibility alias
```

## Research Intake / 研究入库

Keep `web-search-rules` authoritative for web research, source rules, claim evidence, staging, archive, and audit. Use the bundled intake module only for reduced-fidelity fallback.

由 `web-search-rules` 权威管理网页研究、来源规则、主张证据、暂存、归档和审计。本包入库模块只作为降级回退。

Legacy configuration paths may be inspected for migration, but do not delete or modify them automatically:

```text
~/.workbuddy/skills/web-search-rules/config.json
~/.workbuddy/skills/web-search-rules-en/config.json
~/.skill-config/web-search-rules-en/config.json
```

## One-Writer Migration / 单写入者迁移

Before updating any state:

1. inventory current and legacy files;
2. assign one owner to each fact and state machine;
3. show conflicts and proposed mappings;
4. copy first and validate;
5. retain source history unless the user separately authorizes cleanup.
