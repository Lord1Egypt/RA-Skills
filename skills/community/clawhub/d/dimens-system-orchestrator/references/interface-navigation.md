# 总控到接口资料导航

## 1. 使用目的

系统级拆解完成后，AI 需要知道下一步去哪里看真实命令、接口级资料和业务章节。当前顶层技能已收敛为：

- `dimens-system-orchestrator`
- `dimens-manager`
- `dimens-sdk`

因此导航不再指向旧业务顶层技能，而是指向 `dimens-manager/references/<业务域>/`。

## 2. 总控内部资料

| 文档 | 用途 |
| --- | --- |
| `system-decomposition.md` | 系统模块拆解方法 |
| `business-canvas-flow.md` | 业务场景画布与审批工作流画布的系统级流程 |
| `skill-routing.md` | 顶层技能与 `dimens-manager` 章节路由 |
| `command-mapping.md` | 系统建设步骤到 CLI 命令的映射 |
| `examples.md` | 系统级需求输出案例 |

## 3. 业务章节资料落点

| 业务域 | 入口 | 常用扩展资料 |
| --- | --- | --- |
| Key 鉴权 | `dimens-manager/references/key-auth/overview.md` | `dimens-manager/references/key-auth/references/login-flow.md`、`examples.md` |
| 团队上下文 | `dimens-manager/references/team/overview.md` | `context-sources.md`、`isolation.md`、`project-entry.md` |
| 项目初始化 | `dimens-manager/references/project/overview.md` | `bootstrap-flow.md`、`doc-richtext-guidelines.md`、`examples.md` |
| 多维表格 | `dimens-manager/references/table/overview.md` | `build-flow.md`、`field-design-patterns.md`、`row-filters.md` |
| 权限 | `dimens-manager/references/permission/overview.md` | `command-mapping.md`、`matrix.md`、`scenario-routing.md` |
| 工作流 | `dimens-manager/references/workflow/overview.md` | `project-binding.md`、`model-routing.md`、`usage.md` |
| 业务场景画布 | `dimens-manager/references/canvas/overview.md` | `dimens-manager/references/canvas/overview.md`、`business-canvas-flow.md` |
| 报表 | `dimens-manager/references/report/overview.md` | `usage.md`、`recharts-widget-guide.md`、`examples.md` |

## 4. SDK 资料落点

如果用户要写代码接入，而不是只用 CLI 管理项目资源，进入：

- `dimens-sdk/SKILL.md`
- `dimens-sdk/references/examples.md`
- `dimens-sdk/references/web-examples.md`
- `dimens-sdk/references/table-examples.md`
- `dimens-sdk/references/report-examples.md`

## 5. 链接解析后的导航

项目链接：

```text
https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/
```

默认导航：

1. `dimens-manager/references/team/overview.md`
2. `dimens-manager/references/project/overview.md`
3. 按用户目标进入 `table / permission / workflow / report`

表格链接：

```text
https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/SHEET_ID?view=VIEW_ID
```

默认导航：

1. `dimens-manager/references/team/overview.md`
2. `dimens-manager/references/table/overview.md`
3. `dimens-manager/references/table/references/row-filters.md` 或字段/视图相关资料

## 6. 不要这样导航

| 错误导航 | 正确导航 |
| --- | --- |
| `dimens-table` | `dimens-manager/references/table/overview.md` |
| `dimens-permission` | `dimens-manager/references/permission/overview.md` |
| `dimens-project` | `dimens-manager/references/project/overview.md` |
| `dimens-report` | `dimens-manager/references/report/overview.md` |
| “去 manager 看看” | 给出具体 manager 章节路径 |
