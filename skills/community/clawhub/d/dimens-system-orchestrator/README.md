# dimens-system-orchestrator

`dimens-system-orchestrator` 是维表智联的系统级总控技能，用于把“生成一个 XX 系统 / 平台 / 管理应用”这类需求先拆成项目、目录、表格、文档、报表、业务场景画布、权限、工作流和对接模块，再路由到 `dimens-manager` 的具体业务章节。

当前顶层技能体系已经收敛为 3 个：

| 顶层技能 | 职责 |
| --- | --- |
| `dimens-system-orchestrator` | 系统级拆解、执行顺序、章节路由 |
| `dimens-manager` | 项目内业务管理：Key、团队、项目、表格、权限、工作流、报表 |
| `dimens-sdk` | SDK、Node.js、Web、BFF、移动端集成 |

## 适用场景

优先使用本技能的典型问题：

- “帮我生成一个客户管理系统”
- “帮我搭一个售后管理平台”
- “做一个项目管理系统，需要表格、报表、业务流程画布和权限”
- “生成一个审批系统，要能体现审批工作流画布”
- “基于这个项目链接，帮我规划业务系统”

不适合使用本技能的情况：

- 只问单个 CLI 命令：直接进入 `dimens-manager` 对应章节。
- 只问 SDK 代码：直接进入 `dimens-sdk`。
- 只修一个具体表字段：直接进入 `dimens-manager/references/table/overview.md`。

## 默认工作流

1. 判断是否为系统级需求。
2. 解析或确认 `teamId / projectId / baseUrl`。
3. 先拆项目资源：目录、表格、文档、报表、业务场景画布。
4. 再拆数据模型：表、字段、关联、示例数据、查询案例。
5. 如果涉及流程、审批或多角色协作，补业务场景画布；审批场景补审批工作流画布。
6. 按需补权限、工作流、外部对接。
7. 输出 `dimens-manager` 章节路由和执行顺序。
8. 用户确认后再进入具体命令或落地步骤。
9. 执行后必须回查：`project info` 验证上传 URL 写回，`sheet tree` 验证目录归位，报表链路至少跑到 `query-widget` 或 `query`。

## `dimens-manager` 章节入口

| 场景 | 章节入口 |
| --- | --- |
| Key 鉴权、第三方接入 | `dimens-manager/references/key-auth/overview.md` |
| 团队、成员、项目上下文 | `dimens-manager/references/team/overview.md` |
| 项目创建、初始化、文档资源 | `dimens-manager/references/project/overview.md` |
| 表、字段、视图、行数据 | `dimens-manager/references/table/overview.md` |
| 角色、权限、行级策略 | `dimens-manager/references/permission/overview.md` |
| 工作流、AI、模型路由 | `dimens-manager/references/workflow/overview.md` |
| 报表、组件、查询链 | `dimens-manager/references/report/overview.md` |
| 业务场景画布、审批工作流画布 | `dimens-manager/references/canvas/overview.md`、`dimens-manager/references/canvas/references/generation-guide.md` |

## 核心原则

- 先方案，后执行。
- 系统搭建不要只建表，默认考虑表格、文档、报表。
- 涉及流程或审批的系统，默认补业务场景画布；画布用于表达场景，不替代真实工作流。
- 表格建模必须细到字段类型、关联、候选项、示例数据和视图。
- 权限不是最后补丁，涉及角色、公开访问、部门可见、行级控制时要前置设计。
- 报表不要直接从 `widget-add` 开始，先走 `report create -> preview -> widget-add -> query-widget -> query`。
- 修改数据必须先读取当前数据，再分析修改，再提交更新。
- 创建目录不会自动移动已有菜单；新资源用 `--folder-id`，已有资源用 `sheet update --folder-id`，最后用 `sheet tree` 验证。
- SVG 封面/图标默认生成 `250x150px`、淡色背景、轻量动态效果的 SVG；必须保留 `.svg` 扩展名，上传后还要把返回 `url` 写回项目或文档。

## 参考资料

- `references/scenario-taxonomy.md`
- `references/system-decomposition.md`
- `references/business-canvas-flow.md`
- `references/skill-routing.md`
- `references/interface-navigation.md`
- `references/command-mapping.md`
- `references/examples.md`
