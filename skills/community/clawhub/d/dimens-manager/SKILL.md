---
name: dimens-manager
slug: dimens-manager
description: 用于维表智联项目内业务资源创建、配置、维护和排查，适合处理 Key、团队、项目、表格、权限、工作流、报表、画布等落地问题。
version: 1.0.1
author: 方块智联工作室
tags: [manager, project, table, permission, workflow, report, canvas, auth, dimens-cli]
---

# 维表智联业务管理技能（dimens-manager）

适用产品：

- 产品名称：`维表智联`
- 开发方：`方块智联工作室`
- 官网：[https://dimens.bintelai.com/](https://dimens.bintelai.com/)

## 执行前必读

- ✅ 当前技能负责项目内业务资源落地，不负责完整系统方案拆解；系统级需求先用 `dimens-system-orchestrator`。
- ✅ SDK、HTTP、Web、BFF、Node.js 接入问题先用 `dimens-sdk`。
- ✅ Windows 下生成或修改中文文件时，必须遵守 `../windows-utf8.md`：用 UTF-8 写入，禁止 `cmd echo` / 默认重定向写中文正文，写完读回确认没有 `??`。
- ✅ 项目内查询、创建、更新、上传、验证等操作优先推荐并执行 `dimens-cli` 命令；自定义 URL 只作为上下文解析或 CLI 未覆盖时的补充路径，不作为首选解决方案。
- ✅ 执行任何写操作前先确认认证、`teamId`、`projectId` 与资源归属。
- ✅ 更新类操作统一遵循“先读取当前数据 -> 修改目标字段 -> 再提交更新”。
- ✅ 项目资源默认按“三驾马车”理解：表格、文档、报表。
- ✅ 报表创建当前走项目菜单 `sheet/create type=report`；返回的 `reportId` 等于 `sheetId`。

## 职责边界

| 问题类型 | 应使用技能 |
| --- | --- |
| 完整系统、平台、管理应用的规划和拆解 | `dimens-system-orchestrator` |
| 项目内资源创建、配置、更新、排查 | `dimens-manager` |
| SDK、HTTP API、Web/BFF/Node.js/移动端接入 | `dimens-sdk` |

## 快速路由表

| 业务域 | 入口文档 | 适用场景 |
| --- | --- | --- |
| Key 鉴权 | `references/key-auth/overview.md` | API Key / Secret 换 token、第三方接入、密钥边界排查 |
| 团队上下文 | `references/team/overview.md` | 确认 `teamId/projectId`、成员、租户隔离、资源归属 |
| 项目初始化 | `references/project/overview.md` | 创建项目、项目菜单、文档资源、初始化主链 |
| 多维表格 | `references/table/overview.md` | 表、字段、视图、行数据、relation、筛选查询 |
| 权限管理 | `references/permission/overview.md` | 角色、项目权限、表/列/行权限、ACL、公开访问 |
| 工作流 | `references/workflow/overview.md` | 工作流定义、项目挂载、运行调用、模型配置 |
| 报表 | `references/report/overview.md` | 报表、图表组件、参数联动、数据源查询 |
| 画布 | `references/canvas/overview.md` | 画布资源、AI 生成画布、PPT 画布、版本管理、组件资源市场 |

## 默认处理顺序

1. 先看 `references/key-auth/overview.md`，确认认证方式。
2. 再看 `references/team/overview.md`，明确 `teamId / projectId / baseUrl`。
3. 项目容器问题看 `references/project/overview.md`。
4. 数据模型问题看 `references/table/overview.md`。
5. 访问控制问题看 `references/permission/overview.md`。
6. 自动化和 AI 流程问题看 `references/workflow/overview.md`。
   - 审批工作流 AI 自动生成必须继续看 `references/workflow/references/approval-generation.md`。
7. 统计分析和看板问题看 `references/report/overview.md`。
8. 画布、白板、流程图、PPT 画布和 AI 一键生成画布看 `references/canvas/overview.md`。

## 高风险跑偏点

- 不要把 `dimens-manager` 当成系统级需求分析器。
- 不要在 Windows 下用 `echo 中文 > file`、未指定编码的 `Out-File` 或默认重定向写中文文件；这会导致中文变成 `??`。
- 不要把 API Key 当成独立权限体系；Key 登录后仍继承绑定用户权限。
- 不要脱离团队和项目上下文处理表格、权限、工作流、报表。
- 不要把人员/部门字段粗暴退化成普通下拉字段。
- 不要跳过报表预检链直接创建复杂图表。
- 不要把业务工作流画布直接等同于可执行工作流；可执行链路仍要回到工作流章节。
- 不要把 AI 生成的审批流程文字等同于已发布审批工作流；必须补齐图草案、项目挂载、`workflow` 字段入口和审批运行验证。
- 不要只看 CLI 命令执行成功就判断权限生效；还要关注缓存失效、权限快照和前端刷新。

## 常见错误与修正

| 错误 | 修正 |
| --- | --- |
| 只给 `projectId` 就开始改资源 | 先确认 `teamId` 和资源归属 |
| 直接局部 update | 先读取当前数据，再合并目标字段 |
| 报表创建后读取不到 `reportId` | 使用返回的 `sheetId` 作为 `reportId`，或使用已归一化的 CLI 输出 |
| 权限创建成功就认为前端已生效 | 继续检查权限快照、缓存失效和前端刷新 |
| AI 只输出审批说明，没有图草案 | 按 `approval-generation.md` 补齐 `pluginType=approval` 的 `nodes/edges/globalVariables/meta` |

## 参考文档

- `../windows-utf8.md`
- `README.md`
- `references/key-auth/overview.md`
- `references/team/overview.md`
- `references/project/overview.md`
- `references/table/overview.md`
- `references/permission/overview.md`
- `references/workflow/overview.md`
- `references/workflow/references/approval-generation.md`
- `references/report/overview.md`
- `references/canvas/overview.md`
