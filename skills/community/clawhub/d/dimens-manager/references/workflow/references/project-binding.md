# dimens-manager 工作流章节 项目挂载分层

本文档专门收口“团队定义 vs 项目挂载 vs 系统视图入口”，避免把这部分规则散落在 `usage.md` 和 `examples.md`。

## 1. 三层对象与职责

| 层级 | 主要对象 | 回答的问题 | 典型字段 |
| --- | --- | --- | --- |
| 团队定义层 | `flow_info` | 团队里有哪些工作流、是否发布、标签是什么 | `id`, `label`, `name`, `status`, `usageType` |
| 项目挂载层 | `mul_project_workflow_binding`（文档中也常写 `project_workflow_binding`） | 某个项目到底挂了哪些工作流、挂到哪个入口 | `projectId`, `workflowId`, `systemView`, `showInAiAnalysis` |
| 系统视图入口层 | AI 分析 / 审批 / 自动化 | 最终用户在具体入口看到什么 | `systemView` 与入口路由约定 |

结论：工作流“在团队存在”不等于“在项目可见”。

## 2. 标准判断顺序

遇到“项目里看不到工作流”时，默认按下面顺序判断：

1. 先确认团队定义层是否存在该工作流（`teamId`）。
2. 再确认该工作流是否处于可执行状态（已发布、未禁用）。
3. 再确认项目挂载层是否存在绑定关系（`projectId + workflowId`）。
4. 再确认绑定项的 `systemView` 是否与当前业务入口一致。
5. 最后再看项目权限与可见性是否允许当前用户看到该入口。

## 3. 上下文最小集合

不同问题的最小上下文如下：

| 问题类型 | 最小上下文 |
| --- | --- |
| 团队工作流查询 | `teamId` |
| 项目工作流可见性 | `teamId + projectId` |
| 入口级可见性（AI 分析/审批/自动化） | `teamId + projectId + systemView` |
| 运行失败排查 | `teamId + flowId/label (+ projectId)` |

如果只有 `teamId`，最多只能判断“团队里有没有”，不能直接判断“项目里为什么没有”。

## 4. 与其他 references 的关系

- 业务层解释优先看 `usage.md`。
- 接口参数与请求案例看 `examples.md`。
- 模型解析与默认模型边界看 `model-routing.md`。
- CLI 已封装与 server-only 边界看 `capability-status.md`。
