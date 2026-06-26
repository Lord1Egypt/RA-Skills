---
name: dimens-system-orchestrator
slug: dimens-system-orchestrator
description: 用于维表智联系统级方案拆解与执行编排，适合“生成一个客户管理系统/平台”这类完整业务系统搭建需求。
version: 1.0.1
author: 方块智联工作室
tags: [orchestrator, system-design, routing, planning, dimens-cli]
---

# 系统级总控技能（dimens-system-orchestrator）

适用产品：

- 产品名称：`维表智联`
- 开发方：`方块智联工作室`
- 官网：[https://dimens.bintelai.com/](https://dimens.bintelai.com/)

## 执行前必读

- ✅ 当前技能只负责系统级拆解、执行顺序、章节路由和风险提示。
- ✅ 项目内业务操作统一进入 `dimens-manager`。
- ✅ SDK、HTTP、Web、BFF、Node.js、移动端接入统一进入 `dimens-sdk`。
- ✅ 只要 `dimens-cli` 已覆盖对应能力，方案和执行步骤优先推荐 `dimens-cli` 命令行；不要把自定义 URL、手动打开页面链接或绕过 CLI 的 HTTP 地址当成首选解决方案。
- ✅ 真实执行项目前，必须先用 `dimens-cli auth api-key-login` 通过 API Key / API Secret 换 token；URL 只能解析 `teamId/projectId/sheetId/viewId`，不能替代登录。
- ✅ Windows 下生成中文方案、Markdown、JSON、画布 JSON 或文档文件时，必须遵守 `../windows-utf8.md`，统一 UTF-8 写入并读回检查，避免中文变成 `??`。
- ✅ 默认节奏是“先方案，后执行”；系统边界没拆清前不要直接给创建命令。
- ✅ 项目资源默认按“四类交付物”理解：表格、文档、报表、业务场景画布。
- ✅ 涉及流程、审批、自动化或多角色协作的系统，默认补业务场景画布；审批场景额外补审批工作流画布。
- ✅ 更新类操作统一遵循“先读取当前数据 -> 分析并修改目标字段 -> 再提交更新”。

## 职责边界

| 问题类型 | 应使用技能 |
| --- | --- |
| 完整系统、平台、管理应用的规划和拆解 | `dimens-system-orchestrator` |
| 项目内资源创建、配置、更新、排查 | `dimens-manager` |
| 画布、流程图、思维导图、PPT 画布、AI 一键生成画布 | `dimens-manager/references/canvas/overview.md` |
| SDK、HTTP API、Web/BFF/Node.js/移动端接入 | `dimens-sdk` |

## 快速路由表

| 阶段 | 章节入口 | 作用 |
| --- | --- | --- |
| 认证阶段 | `dimens-manager/references/key-auth/overview.md` | API Key / Secret 换 token、第三方接入、登录边界 |
| 上下文阶段 | `dimens-manager/references/team/overview.md` | 确认 `teamId / projectId`、成员、租户隔离、资源归属 |
| 项目阶段 | `dimens-manager/references/project/overview.md` | 创建项目、项目菜单、文档资源、初始化主链 |
| 建模阶段 | `dimens-manager/references/table/overview.md` | 表、字段、视图、行数据、relation、筛选查询 |
| 权限阶段 | `dimens-manager/references/permission/overview.md` | 角色、项目权限、表/列/行权限、ACL、公开访问 |
| 工作流阶段 | `dimens-manager/references/workflow/overview.md` | 工作流定义、项目挂载、运行调用、模型配置 |
| 报表阶段 | `dimens-manager/references/report/overview.md` | 报表、组件、参数联动、数据源查询 |
| 画布阶段 | `dimens-manager/references/canvas/overview.md` | 画布资源、AI 生成图数据、版本和组件资源 |
| 业务场景画布阶段 | `references/business-canvas-flow.md` | 系统级业务流程、审批流转、角色协作和异常路径表达 |

## 默认处理顺序

1. 先按 `references/scenario-taxonomy.md` 判断属于项目梳理、新建项目、修改项目内数据、查询还是分类路由。
2. 判断只是方案输出，还是要真实执行查询、创建或修改。
3. 如果要真实执行，先按 `references/auth-prerequisite.md` 完成 `auth api-key-login`，不要用 URL 替代 token。
4. 识别系统定位：系统名称、核心目标、主要使用者。
5. 归一化上下文：解析或确认 `teamId / projectId / baseUrl`。
6. 设计项目容器：项目名称、目录结构、菜单入口、文档、报表与业务场景画布。
7. 拆核心对象：主对象、从对象、生命周期状态、对象关系。
8. 设计多表模型：表、字段类型、候选项、relation、默认视图、示例数据。
9. 设计查询与视图：常用筛选、列表视图、统计口径、报表数据源。
10. 如存在流程、审批、自动化或多角色协作，补业务场景画布；审批系统额外补审批工作流画布。
11. 按需补权限、工作流、报表、画布和外部对接。
12. 最后给出下一步进入 `dimens-manager` 的具体章节路径。

## 系统级画布说明

系统总控遇到完整业务系统、审批系统、售后系统、CRM、项目管理平台等需求时，不能只拆表格和权限，还要判断是否需要业务场景画布。画布的目标是让用户看清“谁在什么阶段做什么、数据如何流转、异常如何处理”，不是替代真实可执行工作流。

画布节点职责必须在系统方案阶段先拆清：

| 节点职责 | 推荐节点类型 | 系统级用法 |
| --- | --- | --- |
| 表单提交、导入、上传、外部返回 | `PARALLELOGRAM` | 表达数据从用户、接口或文件进入系统 |
| 普通动作、系统处理、人工处理 | `RECTANGLE` | 表达一个明确业务动作，不要把多个动作塞进一个节点 |
| 条件判断、审批分支、风控命中 | `DIAMOND` | 表达“是否...”类判断，分支边必须标注“是/否/通过/驳回” |
| 多维表、数据库、知识库、日志沉淀 | `CYLINDER` | 表达数据被读取、写入或沉淀 |
| 合同、报告、SOP、知识条目 | `DOCUMENT` / `MARKDOWN` | 表达文档产物或较长说明 |
| 阶段、泳道、业务域分组 | `SECTION` | 包裹同一阶段或同一角色的一组节点，不作为流程动作 |
| 信息图、复杂展示、PPT 核心页 | `INFOGRAPHIC` | 表达复杂信息、指标趋势、方案对比、流程概览、系统关系，PPT 场景要优先善用 |
| 画布内 AI 智能体生成 | `CUSTOM_AGENT` | 只在需要用户点击运行并生成后续节点时使用，不作为普通业务处理步骤 |
| 嵌入业务表视图 | `EMBEDDED_SHEET` | 展示项目内表格视图，真实落地时需要 `sheetId/viewId` |

系统级输出只负责说明“需要什么画布、画布表达哪些角色/对象/状态/异常、节点职责如何拆”。落地保存和节点字段细节进入：

1. `references/business-canvas-flow.md`
2. `dimens-manager/references/canvas/overview.md`
3. `dimens-manager/references/canvas/references/generation-guide.md`

如果系统总控直接输出画布 JSON 草案，不能只给 `id/type/position/data.label`。保存型 JSON 必须继续采用 `dimens-manager` 的可渲染字段模板：顶层包含 `version/timestamp`，节点包含 `style.width/height`、顶层 `width/height`、`positionAbsolute`、`data.width/height`、`data.align/verticalAlign`，边包含 `sourceHandle/targetHandle`、`markerEnd`、`style.stroke/style.strokeWidth`，边类型使用 `default` 或 `smoothstep`。

如果用户要创建 PPT、演示稿或幻灯片画布，必须路由到 `dimens-manager/references/canvas/references/generation-guide.md#8-ppt--演示稿画布规则`。PPT 画布要求 `16:9`，最外层是一组 `SECTION` 页面分区，一页 PPT 对应一个分区，所有页面内容都必须放在所属分区内。

PPT 或复杂展示场景必须优先考虑 `INFOGRAPHIC` 信息图节点。凡是方案亮点、路径拆解、趋势、对比、SWOT、象限、系统关系、流程概览等需要强视觉表达的信息，优先用 `INFOGRAPHIC`，并在 `data.infographicSyntax` 中写 AntV Infographic DSL。

## 执行完成判定

执行类任务不能只看“命令返回 success”。至少按下表回查后，才能说“系统初始化完成 / OK”：

| 动作 | 必做验证 | 不通过时 |
| --- | --- | --- |
| SVG 封面/图标上传 | 确认 SVG 为 `250x150px`、淡色背景、动态效果，文件保留 `.svg`，类型是 `image/svg+xml`，并拿到 `url` | 重新按“先读 -> 合并 URL -> update”执行 |
| 项目封面/图标写回 | `project info` 回查目标字段是否已经是上传后的 `url` | 重新按“先读 -> 合并 URL -> update”执行 |
| 创建目录 | 记录返回的目录 `sheetId`，后续子资源显式使用 `--folder-id` | 不要假设其他菜单自动进入目录 |
| 移动已有菜单资源 | 执行 `sheet update RESOURCE_ID --folder-id FOLDER_ID` 后再 `sheet tree` | 未归位则继续修正 `folderId` |
| 创建表格 | `sheet info`、`view list`、`column list` 回查结构 | 缺视图或字段时回到 table 章节补齐 |
| 创建报表 | `report create -> preview -> widget-add -> query-widget -> query` 至少跑通预检链 | 报表只是空壳，不能算完成 |
| 创建画布 | `canvas create -> canvas info -> canvas save` 至少跑通保存链路 | 画布只是空壳或版本未写入，不能算 AI 生成画布完成 |

如果用户让“直接创建一套系统”，最后输出必须包含：已创建资源 ID、目录归位结果、上传 URL 写回结果、报表预检结果、下一步风险。

## 链接输入规则

| 链接形态 | 解析结果 | 下一步 |
| --- | --- | --- |
| `https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/` | `teamId`、`projectId` | 进入团队与项目章节 |
| `https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/SHEET_ID?view=VIEW_ID` | `teamId`、`projectId`、`sheetId`、`viewId` | 如果是表格页面，进入表格章节；如果是在线文档页面，先把 `sheetId` 当菜单资源 ID，优先走 `doc info --sheet-id SHEET_ID` 取真实 `documentId` |

链接只能解析上下文，不能获取 token。只要后续要执行 CLI 查询、创建或修改，必须先按 `references/auth-prerequisite.md` 使用 API Key / API Secret 登录。

## 高风险跑偏点

- 不要在 Windows 下用 `cmd echo`、默认重定向或未指定编码的 PowerShell 写中文正文；生成系统方案、画布 JSON、Markdown 文档时都必须按 UTF-8 写入。
- 不要把维表页面 URL 当成认证凭据；URL 不能换 token，真实执行前必须先 `dimens-cli auth api-key-login`。
- 不要把系统需求收缩成“只建几张表”。
- 不要跳过文档和报表资源。
- 不要在建模没明确前直接执行命令。
- 不要把权限、公开访问、部门隔离当成最后补丁。
- 不要以为“创建目录”会自动移动其他菜单；创建子资源必须带 `--folder-id`，已有资源必须再执行 `sheet update --folder-id`。
- 不要把 SVG 封面当普通文件上传；封面默认规格是 `250x150px`、淡色背景、动态效果，文件名必须保留 `.svg`，上传 MIME 应为 `image/svg+xml`。
- 不要让报表直接从 `widget-add` 开始；固定预检链是 `report create -> report preview -> report widget-add -> report query-widget -> report query`。
- 不要把画布流程图当成可执行工作流；可执行工作流还需要工作流定义、发布和项目挂载。
- 不要只给审批工作流画布就声称审批能力完成；画布只表达业务场景，真实审批还要走工作流定义、发布、项目挂载和运行验证。
- 不要把 SDK 接入问题混入系统拆解；代码接入交给 `dimens-sdk`。
- 不要在没有 `sheet tree`、`project info`、报表 query 等回查证据时宣称“完成”。
- 不要把文档页面链接里的 `sh_xxx` 误当成 `documentId`；在线文档页面 URL 默认先产出 `sheetId`，需要先通过 `getBySheetId` 或 `doc info --sheet-id` 换出真实 `documentId`。

## 常见错误与修正

| 错误 | 修正 |
| --- | --- |
| 一个完整系统需求直接落到单个表 | 先拆项目、目录、表格、文档、报表和权限边界 |
| 方案还没确认就开始执行 | 先输出模块方案，再等用户确认或明确授权执行 |
| 只写“去 manager 看” | 必须给出具体章节路径 |
| 报表创建后找不到 `reportId` | 说明当前 `report create` 返回的 `reportId` 等于菜单资源 `sheetId` |
| 用户给了 URL 就直接执行命令 | URL 只能解析上下文，先用 API Key / Secret 执行 `auth api-key-login` 换 token |
| 创建了目录但菜单没进去 | 对新建资源用 `sheet create --folder-id`，对已建资源用 `sheet update --folder-id` |
| SVG 上传后无法作为图片使用 | 生成 `250x150px` 淡色动态 SVG，保留 `.svg` 扩展名并走 `upload file`，确认上传类型是 `image/svg+xml` |
| 业务流程只写成文字，没有画布 | 按 `references/business-canvas-flow.md` 生成业务场景画布，再路由到 `dimens-manager` 保存 |
| 审批画布被当成真实审批流 | 明确区分审批工作流画布和可执行审批工作流，后者继续进入 `workflow/approval-generation.md` |

## 参考文档

- `../windows-utf8.md`
- `references/auth-prerequisite.md`
- `references/scenario-taxonomy.md`
- `references/system-decomposition.md`
- `references/business-canvas-flow.md`
- `references/skill-routing.md`
- `references/interface-navigation.md`
- `references/command-mapping.md`
- `references/examples.md`
