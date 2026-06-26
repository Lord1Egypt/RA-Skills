# Migration Guide / 迁移指南

## From Project Lifecycle Navigator / 从项目生命周期导航助手迁移

Move project intake, MVP planning, code-review upgrade, and realignment rules into:

迁移项目启动、MVP 规划、代码审查升级和校准规则到：

```text
modules/project-lifecycle.md
```

## From Daily Workflow / 从 Daily Workflow 迁移

Map legacy files:

旧文件映射：

```text
PROJECT_TARGET.md  -> TARGET.md
PROJECT_STATUS.md  -> STATUS.md
COMPLETED_JOBS.md  -> COMPLETED.md
PENDING_JOBS.md    -> PENDING.md
NEXT_STEPS.md      -> NEXT_ACTIONS.md
SCHEDULE.md        -> NEXT_ACTIONS.md compatibility alias
```

## From Web Search Rules / 从 Web Search Rules 迁移

The old web-only workflow becomes Knowledge Intake Governance.

旧版仅网页搜索流程升级为知识库资料接入治理。

Legacy config paths:

旧配置路径：

```text
~/.workbuddy/skills/web-search-rules/config.json
~/.workbuddy/skills/web-search-rules-en/config.json
~/.skill-config/web-search-rules-en/config.json
```

New recommended config path:

新推荐配置路径：

```text
~/.skill-config/ai-workflow-os/knowledge-intake/config.json
```

Do not delete old configurations automatically. Compare and migrate with user confirmation.

不要自动删除旧配置。先比较，再经用户确认后迁移。
