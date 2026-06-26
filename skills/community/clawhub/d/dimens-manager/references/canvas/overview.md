---
name: dimens-manager-canvas
slug: dimens-manager-canvas
description: 用于维表智联项目内画布资源创建、AI 生成画布保存、版本管理、资源市场和业务工作流画布落地。
version: 1.0.0
author: 方块智联工作室
tags: [canvas, diagram, workflow, resource, dimens-cli]
---

# dimens-manager 画布章节

## 执行前必读

- ✅ 画布是项目菜单资源，创建入口是 `canvas create` 或 `sheet create --type canvas`。
- ✅ 画布详情、保存、版本和恢复走 `dimens-cli canvas *` 命令。
- ✅ 保存前必须先读取 `canvas info`，拿到当前 `version` 后再传 `--base-version`。
- ✅ AI 一键生成画布时，最终结果必须落成 `nodes/edges` JSON，而不是只输出文字说明。
- ✅ 画布落地不只是生成 `nodes/edges`，还要说明每个节点的业务职责、节点类型选择和使用方式；详细规则先看 `references/canvas/references/generation-guide.md`。
- ✅ 画布生成完成后必须先执行或说明 `canvas validate` 校验，再执行 `canvas create/save`，保存后用 `canvas info/versions` 回查。
- ✅ 节点背景色默认使用淡色或 `transparent`，禁止直接使用黑色、深灰、深蓝等深色背景；文字颜色可以保持深色以保证可读性。
- ✅ 用户要“创建 PPT / 演示稿 / 幻灯片”时，画布 JSON 必须按 PPT 画布规则生成：16:9 比例，一页一个 `SECTION` 分区，页面内容全部放在对应分区内。
- ✅ PPT 或复杂展示场景中，优先善用 `INFOGRAPHIC` 信息图节点；它比普通文本、矩形、Markdown 更适合承载复杂信息。
- ✅ 业务工作流画布不等于可执行工作流；可执行工作流仍看 `references/workflow/overview.md`。

## 快速命令表

| 场景 | 命令 |
| --- | --- |
| 创建画布 | `dimens-cli canvas create --team-id <teamId> --project-id <projectId> --name <name>` |
| 创建带初始图的画布 | `dimens-cli canvas create --team-id <teamId> --project-id <projectId> --name <name> --file ./canvas.json` |
| 查询画布 | `dimens-cli canvas info <sheetId> --team-id <teamId> --project-id <projectId>` |
| 保存画布 | `dimens-cli canvas save <sheetId> --team-id <teamId> --project-id <projectId> --base-version <version> --file ./canvas.json` |
| 版本列表 | `dimens-cli canvas versions <sheetId> --team-id <teamId> --project-id <projectId>` |
| 查看版本 | `dimens-cli canvas version <sheetId> --team-id <teamId> --project-id <projectId> --version <version>` |
| 恢复版本 | `dimens-cli canvas restore <sheetId> --team-id <teamId> --project-id <projectId> --version <version>` |
| 保存组件资源 | `dimens-cli canvas resource-save --team-id <teamId> --name <name> --nodes '<json-array>' --edges '<json-array>'` |
| 发布组件资源 | `dimens-cli canvas resource-publish <resourceId> --team-id <teamId>` |
| 查看资源市场 | `dimens-cli canvas resource-market --team-id <teamId> --keyword <keyword>` |

## 默认处理顺序

1. 先确认 `teamId / projectId`。
2. 如果要创建新画布，执行 `canvas create`，记录返回的 `sheetId/canvasId`。
3. 如果要写入已有画布，执行 `canvas info <sheetId> --team-id <teamId> --project-id <projectId>` 获取 `version`。
4. 生成或整理画布 JSON，确认包含 `nodes` 和 `edges`。
5. 自检每个节点是否有明确业务职责，并使用合适类型：输入输出用 `PARALLELOGRAM`，判断用 `DIAMOND`，数据沉淀用 `CYLINDER`，文档产物用 `DOCUMENT` 或 `MARKDOWN`。
6. 执行 `canvas validate --file ./canvas.json`，确保结构满足可渲染保存要求。
7. 执行 `canvas save <sheetId> --team-id <teamId> --project-id <projectId> --base-version <version>`。
8. 保存后执行 `canvas info` 和 `canvas versions`，确认版本号和快照记录。
9. 需要复用时保存组件资源，需要共享时发布到资源市场。

## 与其他章节的关系

| 章节 | 关系 |
| --- | --- |
| `references/team/overview.md` | 画布资源必须落在正确团队和项目下 |
| `references/project/overview.md` | 画布属于项目菜单资源，目录归位依赖项目资源链路 |
| `references/workflow/overview.md` | 可执行工作流定义、项目挂载和运行调用仍走工作流章节 |
| `references/permission/overview.md` | 画布页面资源可见性和协同边界要走权限章节 |
| `references/canvas/references/generation-guide.md` | AI 生成画布 JSON、节点职责和节点类型用法 |
| `references/canvas/references/validation-checklist.md` | 画布生成后的结构校验、业务语义校验和保存回查 |
| `references/canvas/references/generation-guide.md#8-ppt--演示稿画布规则` | PPT 画布 16:9、分区页面和页面内元素约束 |
| `references/canvas/references/generation-guide.md#infographic-信息图节点` | 信息图节点、AntV Infographic 语法和复杂展示模板 |

## 高风险跑偏点

- 不要把 `canvas save` 当成局部 patch；它保存的是整份图数据。
- 不要跳过 `baseVersion`；版本冲突时应重新读取后合并。
- 不要省略 `--team-id` 和 `--project-id`；快速查询、保存、版本命令都需要明确团队和项目上下文。
- 不要只用 `RECTANGLE` 画完整业务流程；节点类型要表达“输入、判断、处理、沉淀、说明”等不同职责。
- 不要生成缺字段的节点或边；节点必须有 `style/width/height/positionAbsolute`，边必须有 `sourceHandle/targetHandle/markerEnd/style`。
- 不要跳过 `canvas validate`；校验不通过的数据不要提交 `canvas create/save/resource-save`。
- 不要保存后不回查；至少执行 `canvas info` 和 `canvas versions`，确认最新版本已生成。
- 不要把 `data.backgroundColor` 设为 `#000000`、`#111827`、`#1f2937` 等深色；流程节点背景应使用 `#ffffff`、`#f8fafc`、`#eff6ff`、`#ecfdf5`、`#fff7ed` 这类淡色。
- 不要把 PPT 画布画成散落节点；PPT 画布最外层必须是一组 16:9 的 `SECTION`，一页 PPT 对应一个分区，所有页面内容都在分区内。
- 不要把复杂展示内容拆成大量普通节点；能用 `INFOGRAPHIC` 表达的方案亮点、路径、对比、趋势、关系，应优先用信息图。
- 不要把画布资源市场当成项目权限系统，资源可见性和项目页面权限仍要分开判断。
- 不要生成无法被前端识别的节点类型；不确定时用 `RECTANGLE`、`DIAMOND`、`MARKDOWN` 等保守类型。

## 参考文档

- `references/command-mapping.md`
- `references/generation-guide.md`
- `references/validation-checklist.md`
- `references/examples.md`
