# 系统总控章节路由

## 1. 当前路由模型

`dimens-system-orchestrator` 不再路由到多个业务顶层技能。当前路由模型是：

```text
系统级需求
  -> dimens-system-orchestrator 拆模块、排顺序、识别风险
  -> dimens-manager 对应业务章节落地
  -> dimens-sdk 仅在需要开发者集成时进入
```

顶层技能只保留：

| 顶层技能 | 职责 |
| --- | --- |
| `dimens-system-orchestrator` | 系统级拆解与编排 |
| `dimens-manager` | 项目内业务操作与排查 |
| `dimens-sdk` | SDK 与集成代码 |

## 2. `dimens-manager` 章节路由表

| 用户意图 / 系统阶段 | 路由章节 | 说明 |
| --- | --- | --- |
| API Key、Secret、token、第三方登录 | `dimens-manager/references/key-auth/overview.md` | Key 只是登录方式扩展，权限仍继承绑定用户 |
| 团队、成员、部门、租户隔离、项目链接解析 | `dimens-manager/references/team/overview.md` | 所有资源操作前先稳定 `teamId / projectId` |
| 创建项目、项目初始化、目录、文档 | `dimens-manager/references/project/overview.md` | 项目是表格、文档、报表的容器 |
| 建表、字段、视图、行数据、关联、筛选 | `dimens-manager/references/table/overview.md` | 系统数据模型主链 |
| 角色、项目权限、表列行权限、ACL、公开访问 | `dimens-manager/references/permission/overview.md` | 涉及可见性和协同时必须前置 |
| 审批、自动化、AI 分析、模型路由 | `dimens-manager/references/workflow/overview.md` | 区分团队工作流定义、项目挂载和运行调用 |
| 审批工作流自动生成 | `dimens-manager/references/workflow/references/approval-generation.md` | 生成 `pluginType=approval` 草案和落地计划，不等同于画布 |
| 报表、图表、参数联动、数据源查询 | `dimens-manager/references/report/overview.md` | 创建组件前必须先走报表预检链 |
| 业务场景画布、审批工作流画布、流程图、思维导图 | `references/business-canvas-flow.md` -> `dimens-manager/references/canvas/overview.md` -> `dimens-manager/references/canvas/references/generation-guide.md` | 生成 `nodes/edges` 并保存画布版本，不等同于可执行工作流 |
| PPT 画布、演示稿画布、幻灯片画布 | `dimens-manager/references/canvas/overview.md` -> `dimens-manager/references/canvas/references/generation-guide.md#8-ppt--演示稿画布规则` | 16:9，一页一个 `SECTION` 分区，所有内容放在对应分区内 |
| Node.js、Web、BFF、移动端接入 | `dimens-sdk/SKILL.md` | 只有开发者集成问题才进入 SDK |

## 3. 默认路由顺序

系统总控先按 `references/scenario-taxonomy.md` 归类为“项目梳理 / 新建项目 / 修改项目内数据 / 查询 / 分类路由”之一，再进入下面资源章节。场景分类负责判断任务形态，资源章节负责落地细节。

### 3.1 从零创建系统

1. `dimens-manager/references/key-auth/overview.md`
2. `dimens-manager/references/team/overview.md`
3. `dimens-manager/references/project/overview.md`
4. `dimens-manager/references/table/overview.md`
5. 如果存在流程、审批或多角色协作，追加 `references/business-canvas-flow.md` 和 `dimens-manager/references/canvas/overview.md`
6. 按需追加 `permission / workflow / report`
7. 如果要写代码接入，再追加 `dimens-sdk/SKILL.md`

### 3.2 已有项目链接

1. 解析链接中的 `teamId / projectId / sheetId / viewId`。
2. 进入 `dimens-manager/references/team/overview.md` 校准上下文。
3. 根据资源类型进入 `project / table / permission / workflow / report` 章节。
4. 后续命令显式携带解析出的 ID，避免上下文漂移。

### 3.3 只问具体资源

如果用户已经明确只问某个资源，不要强行展开完整系统设计：

| 明确资源 | 直接章节 |
| --- | --- |
| Key / token | `key-auth` |
| teamId / projectId | `team` |
| 项目 / 文档 / 菜单 | `project` |
| 表 / 字段 / 行 / 视图 | `table` |
| 角色 / 权限 / ACL | `permission` |
| 工作流 / AI / 模型 | `workflow` |
| 报表 / 图表 / 数据源 | `report` |
| 画布 / 白板 / 流程图 / 思维导图 / PPT / 演示稿 / 幻灯片 | `dimens-manager/references/canvas/overview.md` |
| 业务场景画布 / 审批工作流画布 | `references/business-canvas-flow.md`，再进入 `dimens-manager/references/canvas/overview.md` |

## 4. 章节依赖关系

- `team` 通常先于所有资源章节，因为上下文不稳会导致所有命令落错项目。
- `project` 通常先于 `table`，因为表、文档、报表都挂在项目下。
- `table` 通常先于 `workflow` 和 `report`，因为流程触发和报表数据源都依赖业务对象。
- `canvas` 可以在方案表达阶段提前生成，但如果要执行自动化，仍要回到 `workflow` 创建真实可执行流。
- 审批工作流画布和可执行审批工作流必须拆开：前者路由到 `dimens-manager/references/canvas/overview.md`，后者路由到 `workflow/references/approval-generation.md`。
- `permission` 不是最后补丁，只要用户提到可见范围、公开访问、部门隔离、只看自己，就要提前设计。
- `sdk` 不替代业务章节；SDK 只是接入方式，业务规则仍以 `dimens-manager` 为准。

## 5. 输出路由时的最低要求

输出路由不能只说“去看 manager”，必须具体到章节路径，例如：

```text
下一步建议进入：
1. dimens-manager/references/team/overview.md
2. dimens-manager/references/project/overview.md
3. dimens-manager/references/table/overview.md
```

如果涉及命令落地，还要同时引用：

- `references/command-mapping.md`
- `dimens-manager` 对应章节下的 `references/*.md`

## 6. 常见错误

| 错误 | 修正 |
| --- | --- |
| 仍写 `dimens-table`、`dimens-permission` 作为顶层技能 | 改成 `dimens-manager/references/table/overview.md`、`dimens-manager/references/permission/overview.md` |
| 只路由到 `dimens-manager`，不说章节 | 必须给出具体业务域章节 |
| 系统需求直接进入 `table` | 先由总控拆项目、文档、报表、权限边界 |
| SDK 问题混到 manager | 开发者集成进入 `dimens-sdk`，业务规则再回 manager |
