# dimens-manager

`dimens-manager` 是维表智联业务管理统一技能，用于承载项目内的认证、团队上下文、项目初始化、表格建模、权限、工作流、报表和画布等业务落地细节。

## 定位

当前技能整合自以下旧技能：

- `dimens-manager/references/key-auth/overview.md`
- `dimens-manager/references/team/overview.md`
- `dimens-manager/references/project/overview.md`
- `dimens-manager/references/table/overview.md`
- `dimens-manager/references/permission/overview.md`
- `dimens-manager/references/workflow/overview.md`
- `dimens-manager/references/report/overview.md`
- `dimens-manager/references/canvas/overview.md`

系统级拆解仍由 `dimens-system-orchestrator` 负责，SDK 与开发者接入仍由 `dimens-sdk` 负责。

## 目录

| 目录 | 来源 | 用途 |
| --- | --- | --- |
| `references/key-auth/` | `dimens-manager/references/key-auth/overview.md` | Key 鉴权、第三方接入、登录 token 边界 |
| `references/team/` | `dimens-manager/references/team/overview.md` | 团队、成员、项目上下文与租户隔离 |
| `references/project/` | `dimens-manager/references/project/overview.md` | 项目创建、初始化、菜单与文档主链 |
| `references/table/` | `dimens-manager/references/table/overview.md` | 表、字段、视图、行、relation 和筛选 |
| `references/permission/` | `dimens-manager/references/permission/overview.md` | 角色、项目权限、资源权限、行级策略 |
| `references/workflow/` | `dimens-manager/references/workflow/overview.md` | 工作流定义、项目挂载、运行与模型边界 |
| `references/report/` | `dimens-manager/references/report/overview.md` | 报表、组件、参数、数据源与查询 |
| `references/canvas/` | `dimens-manager/references/canvas/overview.md` | 画布资源、AI 生成画布、版本与组件资源市场 |

## 工作流补充

审批工作流 AI 自动生成归入 `references/workflow/references/approval-generation.md`，不新增顶层 Skill。它负责把业务描述转换为审批蓝图、`pluginType=approval` 的工作流 JSON 草案和项目落地计划。
