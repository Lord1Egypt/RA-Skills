# Team Charter Template

# 团队宪章

> **使用说明**: 填写以下各节，删除所有注释后保存为 `.claude/teams/<team_name>/team_charter.md`

## Team Name

**团队名称**: `<team_name>`

<!-- 团队唯一标识名，建议使用英文，如 ldd_research -->

## Mission

<!-- 团队总体任务场景与长远目标，1-3 句话 -->

```
在此描述团队的核心使命...
```

## Roles

<!-- 列出所有角色，明确指定一个为 team-leader -->

| # | 角色名 | 职责 | agent_type |
|---|--------|------|------------|
| 1 | `team-leader` | 任务分发、进度跟踪、冲突解决 | `team-leader` |
| 2 | `<role_2_name>` | `<职责描述>` | `<role_2_name>` |
| 3 | `<role_3_name>` | `<职责描述>` | `<role_3_name>` |

> **注意**: `type` 字段必须与 `name` 保持一致。

## Workflow

<!-- 定义角色间协作流，格式：谁 → 谁 → 何时触发 -->

```
team-leader → <executor> : 任务分发后
<executor> → team-leader : 任务完成提交时
<role_a> → <role_b> : <触发时机>
```

## Created / Updated

- **创建日期**: `2026-XX-XX`
- **最后更新**: `2026-XX-XX`
