# OpenCode 免费模型路由策略

> 沉淀日期：2026-03-28
> 适用对象：使用 OpenCode 作为执行后端的自我进化智能体

## 核心结论

如果目标是在免费模型里兼顾稳定性、推理能力和长上下文，推荐长期只保留 3 个主力模型：

1. `opencode/minimax-m2.5-free` — 默认执行型主力
2. `opencode/mimo-v2-pro-free` — 复杂规划/评审型主力
3. `opencode/nemotron-3-super-free` — 长上下文研究/总结型主力

另外两个模型只在特定场景使用：

1. `opencode/mimo-v2-omni-free` — 有截图、图片、音频、视频等多模态输入时再用
2. `opencode/big-pickle` — 实验型备用模型，不作为默认生产选择

## 模型定位

### 1. MiniMax M2.5 Free

- 定位：免费主力 coding/agent 模型
- 适合：读代码、改代码、落文件、写报告、执行任务
- 不适合：特别长的研究型总结，或重推理的方案选择

### 2. MiMo V2 Pro Free

- 定位：复杂推理与规划模型
- 适合：拆解复杂任务、制定计划、做评审、处理老板建议
- 不适合：大量日常小修改都默认用它，性价比不高

### 3. Nemotron 3 Super Free

- 定位：长上下文研究总结模型
- 适合：读很多文档、很多知识文件后再压缩总结
- 不适合：高频执行型工作默认使用

### 4. MiMo V2 Omni Free

- 定位：多模态模型
- 适合：有截图、界面、图表、音频、视频输入的任务
- 不适合：纯文本/纯代码为主的常规 agent 工作

### 5. Big Pickle

- 定位：实验型模型
- 适合：尝鲜、做备用实验
- 不适合：作为创建者或调度系统的默认模型

## 对 evo-skill-creator 的命令路由建议

| 命令 | 首选模型 | 原因 | 备用 |
|------|----------|------|------|
| `go` | `opencode/minimax-m2.5-free` | 偏执行，要求稳、综合能力强 | 超复杂新角色设计可先用 `opencode/mimo-v2-pro-free` 出方案 |
| `learn` | `opencode/nemotron-3-super-free` | 要读较多资料并沉淀知识 | 主题偏框架设计时可换 `opencode/mimo-v2-pro-free` |
| `scan` | `opencode/nemotron-3-super-free` | 广度扫描后再压缩总结 | 轻量扫描可退回 `opencode/minimax-m2.5-free` |
| `plan` | `opencode/mimo-v2-pro-free` | 任务拆解、排序、取舍最吃推理 | 依赖超长上下文时可换 `opencode/nemotron-3-super-free` |
| `review` | `opencode/mimo-v2-pro-free` | 差距分析、优先级判断、方案输出 | 材料很长时可换 `opencode/nemotron-3-super-free` |
| `suggest` | `opencode/mimo-v2-pro-free` | 需要先表达立场，再对比老板建议后下结论 | 建议很具体、偏执行时可换 `opencode/minimax-m2.5-free` |
| `status` | `opencode/minimax-m2.5-free` | 轻量读取和汇总，不值得上重模型 | 无 |

## 创建新角色时的执行后端选择建议

创建新智能体时，应该明确询问用户采用哪种执行策略：

1. `Claude`：如果用户更看重高质量推理、成熟的权限/工具生态
2. `OpenCode`：如果用户希望优先使用免费模型或已有 OpenCode 工作流
3. `混合路由`：如果不同命令对执行器和模型要求差异明显

如果用户选择 `OpenCode` 或 `混合路由`，至少还要进一步确认：

1. 默认模型是什么
2. 哪些命令需要单独覆盖模型
3. 是否有命令需要单独限制/放开工具

## 对 scheduler 配置的启示

调度配置不应只停留在 agent 级别的单一 `executor` 和 `model`。

更理想的结构是：

1. `agent` 级别定义默认 `executor`、默认 `model`、默认 `tools`
2. `schedules` 中每个命令可按需覆盖 `executor`、`model`、`tools`

这样才能实现：

1. `go` 用 `MiniMax`
2. `plan/review/suggest` 用 `MiMo V2 Pro`
3. `learn/scan` 用 `Nemotron`
4. 特定任务单独限制工具权限

## 当前建议

在 scheduler 尚未支持命令级覆盖前：

1. 先为每个角色设一个主力默认模型
2. 把命令级路由策略写入设计文档或知识库
3. 将命令级 `executor/model/tools` 覆盖能力列为 scheduler 的优先改进项
