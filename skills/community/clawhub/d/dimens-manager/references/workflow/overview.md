---
name: dimens-manager-workflow
slug: dimens-manager-workflow
description: 用于维表智联工作流定义、项目挂载、运行调用与模型配置边界说明。
version: 1.0.0
author: 方块智联工作室
tags: [workflow, ai, automation, flow, dimens-cli]
---

# dimens-manager 工作流章节

适用产品：

- 产品名称：`维表智联`
- 开发方：`方块智联工作室`
- 官网：[https://dimens.bintelai.com/](https://dimens.bintelai.com/)

## 执行前必读

- ✅ 所有工作流能力先确认 `teamId`
- ✅ 项目内工作流展示必须区分“团队工作流定义”和“项目工作流挂载”
- ✅ 解释工作流问题时，不能只看 `flow_info`，还要看项目绑定关系
- ✅ 模型问题不能默认认为所有工作流节点都会自动继承团队默认模型
- ✅ `chat/completions` 接口与普通工作流节点执行是两条不同链路，不能混为一谈
- ✅ 涉及项目入口、AI 分析、审批、自动化时，要同时检查项目上下文和权限边界
- ✅ AI 自动生成审批工作流时，必须同时输出业务蓝图、`pluginType=approval` 的图草案和项目落地计划

## 命令维护表

| 命令 | 作用 | 必填参数 | 常用可选 | 细节说明 |
| --- | --- | --- | --- | --- |
| `flow_list` | 查询团队级工作流定义 | `teamId` | `usageType`, `visibility`, `status` | 先看团队级是否真的存在这个工作流 |
| `project_workflow_binding_list` | 查询项目内工作流挂载关系 | `teamId`, `projectId` | `systemView`, `showInAiAnalysis` | 用于判断为什么项目里看不到或入口不对 |
| `flow_run_invoke` | 正式执行工作流 | `teamId`, `flowId` 或 `label` | `projectId`, `debug`, `input` | 正式执行和调试执行要分开理解，不能混用结论 |
| `flow_run_debug` | 调试运行工作流 | `teamId`, `flowId` 或 `label` | `projectId`, `input` | 更适合排查节点执行问题和输入输出结构 |
| `dimens-cli ai chat-completions` | 走 OpenAI 兼容接口调用团队模型或工作流能力 | `teamId`, `messages` | `model`, `temperature`, `stream` | `model` 为空时可能走团队默认文本模型，但不等于所有工作流节点都这样继承 |
| `flow_config_get` | 查询团队默认模型策略 | `teamId` | `type=default_models` | 只说明团队默认模型配置，不代表节点自动回退一定生效 |
| `dimens-cli ai chat-completions` | 辅助生成审批工作流草案 | `teamId`, `messages` | `model=team-default` | 可用于让 AI 产出审批蓝图和 JSON 草案，但创建、发布、挂载仍要看当前能力边界 |

### 强调细节

- 工作流问题默认要分三层看：团队定义、项目挂载、运行调用，不能只查一个接口就下结论。
- 如果后续存在更新类工作流配置命令，也应遵循“拿数据 -> 改数据 -> 更新数据”的通用规则，先读当前定义或绑定关系再改。
- `chat-completions` 和普通工作流节点执行是两条链路，不能因为一条可用就推断另一条也正常。
- 用户说“项目里看不到工作流”时，默认先查 `flow_list` 再查 `project_workflow_binding_list`，不要直接怀疑前端。

## 核心约束

### 1. 工作流分层

- 团队级定义在 `flow_info`
- 项目级可见性与入口挂载依赖项目绑定关系
- 一个工作流“存在”不代表项目里“能看到”或“能用”

### 2. 默认模型边界

- 团队级默认模型配置已经存在
- `POST /app/flow/:teamId/v1/chat/completions` 已支持“默认文本模型模式”
- 但普通工作流 LLM 节点并不能默认假设会自动回退到 `default_models`

### 3. 运行链路边界

- 管理态接口负责工作流 CRUD、草稿、发布
- 运行态接口负责调试、执行、SSE 回传
- OpenAI 兼容聊天接口是工作流体系对外暴露的一条兼容入口，不等于完整工作流管理接口

### 4. 上下文要求

- 团队级操作必须先有 `teamId`
- 项目入口、AI 分析入口、审批入口等场景必须补齐 `projectId`
- 如果用户只说“工作流不能用”，默认需要同时排查团队、项目、绑定和模型配置

### 5. 风险边界

- 工作流问题可能同时影响团队隔离、项目隔离、模型配置和权限控制
- 只靠单一接口返回结果不足以得出结论，必须结合文档和真实挂载关系一起判断

### 6. 审批自动生成边界

- “生成审批系统”属于系统级建设，先用 `dimens-system-orchestrator`。
- “生成审批工作流 / 审批流程 / 审批节点”属于本章节，重点看 `references/approval-generation.md`。
- AI 生成结果必须能落成工作流图草案，不能只输出自然语言流程说明。
- 审批真值以后端审批实例表为准，表格 `workflow` 字段只负责发起和展示摘要。

## 必查文档

| Skill / references | 作用 | 什么时候必须看 |
| --- | --- | --- |
| `dimens-manager/references/team/overview.md` | 团队与项目上下文边界 | 分析项目挂载时必须看 |
| `dimens-manager/references/table/overview.md` | 系统视图、项目内入口与表域联动 | 分析 AI 分析入口时建议看 |
| `dimens-manager/references/permission/overview.md` | 项目可见性、角色与资源授权边界 | 处理看不到或不能运行时建议看 |
| `references/usage.md` | 团队定义 / 项目挂载 / 运行调用三层分层 | 处理工作流时必须看 |
| `references/project-binding.md` | 项目挂载与系统视图入口关系 | 分析项目里看不到时必须看 |
| `references/model-routing.md` | 默认模型与节点模型边界 | 处理模型配置时必须看 |
| `references/approval-generation.md` | AI 自动生成审批工作流的输入、输出、JSON 草案和落地计划 | 处理审批工作流自动生成时必须看 |
| `references/capability-status.md` | 已封装 / server-only / 部分对齐 状态 | 判断当前能力范围时建议看 |
| `references/examples.md` | 工作流接口案例 | 需要直接举例时看 |

## 使用场景示例

### 场景 1：解释为什么项目里看不到某个工作流

推荐检查顺序：

1. 确认工作流是否存在于团队级定义中
2. 确认工作流是否已发布
3. 确认项目是否存在工作流绑定
4. 确认系统视图是否与当前入口匹配
5. 确认项目成员权限和可见性设置

### 场景 2：通过 OpenAI 兼容接口调用团队默认模型

```json
{
  "teamId": "TEAM1",
  "messages": [
    {
      "role": "user",
      "content": "帮我总结本周项目进展"
    }
  ],
  "model": "team-default"
}
```

注意：

- `model` 为空、`default`、`team-default` 可能走团队默认文本模型
- 这条链路适用于聊天兼容接口，不等于所有工作流节点都会按同样规则解析

### 场景 3：调用某个指定工作流

```json
{
  "teamId": "TEAM1",
  "model": "my-flow-label",
  "messages": [
    {
      "role": "user",
      "content": "按审批流程帮我生成本周申请单摘要"
    }
  ]
}
```

注意：

- `model` 可以被解释为 `flowId` 或 `label`
- 如果工作流已绑定项目入口，还要检查调用时是否需要额外业务上下文

### 场景 4：AI 自动生成审批工作流

推荐输出顺序：

1. 业务审批蓝图：触发条件、表单字段、审批角色、条件分支、结束动作。
2. 工作流图草案：`pluginType=approval`，包含 `nodes`、`edges`、`globalVariables`、`meta`。
3. 项目落地计划：发布工作流、挂载到项目、设置 `systemView=approval`、补 `workflow` 字段入口、验证审批实例和字段摘要回写。

注意：

- 如果缺少 `teamId/projectId`，只能生成草案和落地步骤，不要声称已经写入项目。
- 如果需要保存为可视化画布，另看 `dimens-manager`；可视化画布不等于可执行审批工作流。

## 常见错误与排查

| 错误现象 | 根本原因 | 解决方案 |
| --- | --- | --- |
| 团队里能看到工作流，项目里看不到 | 只创建了团队工作流，没有做项目挂载 | 检查项目绑定关系与系统视图配置 |
| 配了默认模型，但某个节点仍然报模型缺失 | 普通 LLM 节点未必自动回退到团队默认模型 | 检查节点自身模型配置与后端真实实现 |
| `chat/completions` 能调用，工作流界面不能跑 | 两条链路的入口和校验条件不同 | 区分聊天兼容调用与工作流运行链路 |
| 调试可用，正式执行失败 | 调试和正式执行走不同运行上下文或参数 | 检查运行参数、发布版本和正式执行入口 |
| 同一个工作流在不同项目表现不同 | 项目绑定、权限或系统视图不同 | 联动检查 `projectId`、绑定关系与权限 |

## 参考文档

- `references/usage.md`
- `references/project-binding.md`
- `references/model-routing.md`
- `references/approval-generation.md`
- `references/capability-status.md`
- `references/examples.md`
- 如需查看整个 Skill 体系的能力总览，请返回 `dimens-cli/skills/README.md`
