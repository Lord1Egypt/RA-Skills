# 系统级业务场景画布流程

本文档用于优化 `dimens-system-orchestrator` 的系统搭建流程：当用户要生成完整业务系统时，除了表格、文档、报表，还要按需补“业务场景画布”，用来表达业务流程、角色协作、审批流转和异常路径。

## 1. 定位

业务场景画布是系统方案的可视化交付物，不等同于可执行工作流。

| 类型 | 主要作用 | 下一跳 |
| --- | --- | --- |
| 业务场景画布 | 展示业务对象、角色、阶段、状态流转、异常路径 | `dimens-manager/references/canvas/overview.md` |
| 审批工作流画布 | 展示发起、条件分支、人工审批、拒绝/撤回、摘要回写等审批业务流程 | `dimens-manager/references/canvas/overview.md` + `dimens-manager/references/workflow/references/approval-generation.md` |
| PPT 演示稿画布 | 用画布表达汇报页、方案页、路演页等演示稿内容 | `dimens-manager/references/canvas/references/generation-guide.md#8-ppt--演示稿画布规则` |
| 可执行审批工作流 | 真实创建、发布、项目挂载和运行审批任务 | `dimens-manager/references/workflow/overview.md` |

一句话规则：

**画布负责看清业务场景，可执行工作流负责跑通业务动作。**

## 2. 什么时候必须加画布

系统拆解中出现下面任一条件时，默认应补业务场景画布：

- 用户明确说“流程、流转、审批、自动化、节点、场景、业务链路”。
- 用户明确说“PPT、演示稿、幻灯片、汇报页”，并且希望在画布中生成可编辑页面。
- 系统涉及 3 个以上角色协作。
- 核心对象存在明显生命周期，例如线索、商机、工单、合同、采购单、报销单。
- 流程包含条件分支、退回、撤回、超时、异常处理。
- 用户希望 AI 自动生成系统方案，并且要能直观看到业务场景。

如果只是简单维护一张静态表，不强制创建画布。

## 3. 系统级默认流程

总控 Skill 处理完整系统建设时，推荐按下面顺序补画布：

1. 先拆业务对象和角色。
2. 再拆表格字段和状态模型。
3. 识别是否存在流程、审批或自动化。
4. 生成业务场景画布草案。
5. 如果是审批场景，再生成审批工作流画布草案。
6. 生成完成后必须先路由到 `dimens-manager` 执行 `canvas validate`，校验通过再保存。
7. 需要保存时路由到 `dimens-manager` 执行 `canvas create -> canvas info -> canvas validate -> canvas save -> canvas info -> canvas versions`。
8. 需要真实执行审批时，再路由到 `dimens-manager/references/workflow/overview.md`。

不要在业务对象、角色和状态都没拆清前直接生成画布，否则画布会变成空泛流程图。

## 4. 业务场景画布输出要求

业务场景画布至少包含：

| 画布元素 | 要求 |
| --- | --- |
| 角色泳道 | 申请人、审批人、负责人、财务、管理员、外部客户等 |
| 业务对象 | 表单、工单、合同、商机、采购单、报销单等 |
| 状态节点 | 草稿、待审批、处理中、已完成、已拒绝、已撤回 |
| 动作节点 | 提交、分配、审批、复核、通知、归档、回写 |
| 条件节点 | 金额、风险、优先级、部门、合同类型等 |
| 异常路径 | 拒绝、退回、撤回、超时、转交、人工兜底 |
| 数据沉淀 | 表格字段、审批摘要、报表统计口径 |

## 5. 系统级节点职责与用法

总控生成画布草案时，先定义节点职责，再选择节点类型。不要把完整业务流程全部画成 `RECTANGLE`，否则后续 AI 保存出来的流程图会失去业务语义。

| 系统级元素 | 推荐节点类型 | 作用 | 用法 |
| --- | --- | --- | --- |
| 用户提交、外部导入、接口返回 | `PARALLELOGRAM` | 表示输入或输出 | 放在流程入口、接口边界或结果输出位置 |
| 系统处理、人工处理、状态动作 | `RECTANGLE` | 表示普通业务动作 | `label` 使用“动词 + 对象”，一个节点只做一件事 |
| 审批、风控、规则判断 | `DIAMOND` | 表示条件分支 | 出边必须写“是/否/通过/驳回/命中/未命中” |
| 表格、数据库、知识库、日志 | `CYLINDER` | 表示数据沉淀或读取 | 用于“写入客户表”“读取库存数据”“沉淀知识库” |
| 合同、报告、回执、SOP | `DOCUMENT` / `MARKDOWN` | 表示文档产物或长说明 | 业务产物用 `DOCUMENT`，规则说明用 `MARKDOWN` |
| 角色泳道、阶段区域 | `SECTION` | 表示分组背景 | 用于“销售阶段”“财务审批”“售后处理”，不作为流程步骤 |
| 信息图、复杂展示、PPT 核心页 | `INFOGRAPHIC` | 表示复杂信息、趋势、对比、路径、关系的强视觉表达 | PPT 和复杂展示场景优先使用，内容写入 `data.infographicSyntax` |
| 画布内 AI 智能体生成 | `CUSTOM_AGENT` | 读取上游节点并生成 Markdown、思维导图或信息图等后续节点 | 只在需要用户点击运行并生成内容时使用，不作为普通业务处理步骤 |
| 项目表格视图 | `EMBEDDED_SHEET` | 表示嵌入多维表视图 | 真实落地时需要 `embeddedSheet.sheetId/viewId` |
| 风险提示、补充说明 | `TEXT` / `STICKY_NOTE` | 表示备注 | 放在相关节点旁边，不接入主流程时序 |

节点说明要求：

- 每个节点必须能说清业务职责，例如“采集申请信息”“判断是否超预算”“写入审批结果”。
- 每个节点的 `data.backgroundColor` 必须使用淡色或 `transparent`，不要使用黑色、深灰、深蓝等深色背景。
- 每条边必须表达时序或分支，不要把业务动作写在边上。
- 判断节点至少有两条出边，分支 label 必须清楚。
- `SECTION`、`TEXT`、`STICKY_NOTE` 是辅助表达，不要当成主流程动作。
- `CUSTOM_AGENT` 是画布内 AI 智能体，不要滥用为普通“AI 分析”业务步骤。
- 需要保存或生成完整 JSON 时，继续进入 `dimens-manager/references/canvas/references/generation-guide.md`。

输出画布 JSON 时，必须至少包含：

```json
{
  "version": "1.0",
  "timestamp": 1777800000000,
  "nodes": [],
  "edges": [],
  "viewport": { "x": 0, "y": 0, "zoom": 1 },
  "meta": {
    "source": "dimens-system-orchestrator",
    "scenario": "business-canvas"
  }
}
```

保存型 JSON 不能只给 `id/type/position/data.label` 这种简化节点。总控如果直接生成草案，也必须遵循 `dimens-manager/references/canvas/references/generation-guide.md` 的可渲染字段模板：

- 节点必须包含 `style.width/height`、顶层 `width/height`、`positionAbsolute`、`data.width/height`、`data.borderRadius`、`data.align`、`data.verticalAlign`、`selected`、`dragging`。
- 节点 `data.backgroundColor` 必须是淡色或 `transparent`，推荐 `#ffffff`、`#f8fafc`、`#eff6ff`、`#ecfdf5`、`#fff7ed`。
- 边必须包含 `sourceHandle`、`targetHandle`、`markerEnd: { "type": "arrowclosed" }`、`style.stroke`、`style.strokeWidth`、`animated`、`selected`、`zIndex`。
- 普通边使用 `type: "default"`，分支、回退或跨层级连线使用 `type: "smoothstep"`，不要使用前端无法识别的边类型。

如果用户要 PPT / 演示稿 / 幻灯片画布，必须额外遵守：

- PPT 画布必须是 `16:9`。
- 最外层必须是 `SECTION` 页面分区，一页 PPT 对应一个 `SECTION`。
- 每页推荐 `1280 x 720`，页面间纵向间隔默认 `100`。
- 所有标题、正文、图表、流程、图片、备注等内容节点都必须通过 `parentNode` 放在对应页面分区内。
- 复杂展示内容优先用 `INFOGRAPHIC`，包括方案亮点、路径拆解、趋势、对比、SWOT、象限、系统关系和流程概览。
- 继续进入 `dimens-manager/references/canvas/references/generation-guide.md#8-ppt--演示稿画布规则` 查看页面分区模板。

## 6. 审批工作流画布要求

审批工作流画布是审批场景的可视化说明，不直接等同于 `flow_info` 中的可执行定义。

审批画布至少要表达：

- 发起入口：通常是表格的 `workflow` 字段。
- 申请信息：申请单字段、附件、金额、原因、发起部门。
- 审批链路：直属负责人、部门负责人、财务、法务、管理员等。
- 条件分支：金额阈值、天数、风险等级、合同类型。
- 人工动作：同意、拒绝、退回、转交、撤回。
- 自动动作：通知、编号、状态回写、审批摘要回写。
- 结束状态：已通过、已拒绝、已撤回、已超时。

审批画布在表达时，还要给出“节点职责边界”，不能只画线不讲配置：

| 画布节点 | 需要说清的配置 |
| --- | --- |
| 开始节点 | 触发来源、申请单上下文、入参变量 |
| 校验节点 | 必填字段、金额/天数/风险规则、失败提示 |
| 审批节点 | 审批人策略、角色/人员来源、可执行动作、是否允许转交 |
| 条件节点 | 判断表达式、分支标签、进入哪条后续链路 |
| 通知节点 | 通知对象、模板、触发时机 |
| 回写节点 | 写回哪个字段、摘要内容、是否同步状态 |
| 终点节点 | 结束结果、是否需要沉淀原因或摘要 |

如果用户要求“这个审批流要能跑”，必须继续进入：

```text
dimens-manager/references/workflow/references/approval-generation.md
```

## 7. 推荐路由

| 用户意图 | 先由总控做什么 | 下一跳 |
| --- | --- | --- |
| 生成一个业务系统，并体现业务流程 | 在系统拆解中补业务场景画布 | `dimens-manager/references/canvas/overview.md` |
| 生成审批系统 | 先拆系统模块，再补审批工作流画布和可执行审批流计划 | `dimens-manager/references/canvas/overview.md` + `dimens-manager/references/workflow/overview.md` |
| 生成审批工作流画布 | 直接生成审批画布草案，强调非可执行边界 | `dimens-manager/references/canvas/overview.md` |
| 生成 PPT / 演示稿 / 幻灯片画布 | 直接路由到画布章节，按 16:9 和一页一个 `SECTION` 生成 | `dimens-manager/references/canvas/references/generation-guide.md#8-ppt--演示稿画布规则` |
| AI 自动生成审批工作流 | 生成审批蓝图和 `pluginType=approval` 工作流草案 | `dimens-manager/references/workflow/references/approval-generation.md` |
| 保存画布版本 | 不在总控里细化，转到画布命令链 | `dimens-manager/references/canvas/overview.md` |

## 8. 验收标准

系统级方案如果声明“已补业务场景画布”，至少要满足：

- 画布能看出核心业务对象。
- 画布能看出主要角色和职责边界。
- 画布能看出主流程和异常路径。
- 每个节点能说清业务职责，并且节点类型能表达输入、处理、判断、沉淀、文档、AI 辅助等不同语义。
- 审批画布能看出发起、审批、拒绝、撤回、回写摘要。
- PPT 画布必须每页都有 `SECTION` 分区，比例为 `16:9`，页面内容节点都在对应分区内。
- 复杂展示页必须优先使用 `INFOGRAPHIC`，并提供合法 `data.infographicSyntax`。
- 保存型任务必须执行或说明 `canvas create -> canvas info -> canvas save`。
- 生成型任务必须执行或说明 `canvas validate`，校验失败不能进入保存。
- 保存后必须执行或说明 `canvas info -> canvas versions`，确认最新版本已经写入。
- 可执行审批流必须另有工作流定义、发布、项目挂载和运行验证计划。
