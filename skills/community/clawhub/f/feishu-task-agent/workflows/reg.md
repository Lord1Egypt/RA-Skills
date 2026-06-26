# Workflow: 飞书任务智能体注册 / 初始化

## Overview

本工作流为飞书任务智能体专属注册与初始化流程，执行全程依赖 OpenClaw 内置 Tool 能力。流程必须按固定顺序执行，任一步报错都立即终止，不继续后续步骤。

## Dependencies

本流程依赖 openclaw 中的 Tool 能力，后续执行注册相关操作均需调用该工具完成。
**⚠️ 强制要求**：当流程中涉及的任何工具（如 `feishu_task_agent` 或其他关联工具）不存在、未加载或未找到时，必须**立即报错并终止流程**，绝对不要尝试自行搜索、猜测或寻找替代工具。

## Triggers【严格强制触发规则，禁止 AI 推导匹配】

⚠️ 本工作流只允许用户明确原话精准触发，禁止 AI 自动推导、禁止模糊匹配、禁止其他流程联动调用、禁止意图猜测触发。

✅ 仅当用户意图明确且同时包含以下两个核心要素时，才允许进入本注册流程：

1. **明确的主体**：包含“飞书任务智能体”字样
2. **明确的动作**：包含“注册”、“/reg”或“初始化”等意图

❌ 以下情况一律不准触发本流程：

- 用户只说“注册”，不带完整「飞书任务智能体」字样
- AI 自行判断需要注册、后台自动补逻辑触发
- 其他功能流程联动调用、间接调用本注册流程
- 近似词、同义词、简写、口头替代语，一律不识别

## Steps (注册核心执行步骤)

1. **创建定时任务**
   - 本步骤必须使用 OpenClaw 原生命令创建定时任务，统一使用 `openclaw cron`，不要改用其他封装工具。
   - **核心约束**：在创建前，必须先查询判断任务是否已存在。**如果对应 ID 的任务已经存在，则跳过创建，绝对不能重复创建。**
   - 查询命令固定为：
     ```bash
     openclaw cron list --all --json
     ```
   - 判断规则固定为：返回结果中 `name` 等于对应 `Task ID`，即视为该任务已存在，必须跳过，不得重复创建。
   - 根据以下明确任务列表，按顺序逐个执行“先查是否存在，再决定创建/跳过”：
     | 任务唯一 ID (Task ID)                 | 任务描述 (Description)                                                                                 | Cron 表达式              |
     | --------------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------- |
     | feishu-task-daily-report-genarate | 使用技能 `feishu-task-agent`，按 `workflows/agent-profile.md` 的规则在当前应用目录生成或更新 `daily.json`，输出“Todo_Agent_RecentHighlights_Field”和“Todo_Agent_TomorrowsFocus_Field” | `30 23 * * *`          |
     | get-agent-unfinished-tasks        | 使用技能 `feishu-task-agent`，流转到 `workflows/polled-task-execution.md` 执行未开始任务轮询流程 | `*/10 * * * *`          |
   - 若 `feishu-task-daily-report-genarate` 不存在，则执行：
     ```bash
     openclaw cron add \
       --name 'feishu-task-daily-report-genarate' \
       --cron '30 23 * * *' \
       --tz 'Asia/Shanghai' \
       --message '使用技能 feishu-task-agent，按 workflows/agent-profile.md 的规则在当前应用目录生成或更新 daily.json，输出“Todo_Agent_RecentHighlights_Field”和“Todo_Agent_TomorrowsFocus_Field”。' \
       --session isolated \
       --no-deliver
     ```
   - 若 `get-agent-unfinished-tasks` 不存在，则执行：
     ```bash
     openclaw cron add \
       --name 'get-agent-unfinished-tasks' \
       --cron '*/10 * * * *' \
       --tz 'Asia/Shanghai' \
       --message '使用技能 feishu-task-agent，按 workflows/polled-task-execution.md 执行未开始任务轮询流程。' \
       --session isolated \
       --no-deliver
     ```
   - 任一 `openclaw cron list` 或 `openclaw cron add` 命令报错，都必须立即终止流程，不继续后续步骤。

2. **修改当前智能体的工作区下的 `AGENTS.md` 文件**
   - 通过 Markdown 标题层级判断目标段落是否已存在。
   - 若不存在：直接追加指定内容。
   - 若已存在：读取该标题下方现有数据，与待写入内容对比；内容不一致则覆盖更新，一致则跳过。
   - 待追加/更新的内容配置如下：
     ```markdown
     ### 路由硬规则 

     - 硬规则：每次处理用户输入前，必须先执行 `feishu-task-agent` 的任务化判断逻辑（以该 skill 的路由规则、`workflows/auto-task.md` 与 `references/task-decision-rules.md` 为准）。 
     - “执行”不等于“读过”。必须先完成任务化判断，再决定是否直接回复。 
     - 若用户请求生成任何可交付内容（如 JD、邮件、PRD、纪要、报告、方案、清单、SOP、汇报材料、文案草稿等），默认先进入 `feishu-task-agent` 的任务候选，不得直接按普通聊天回复处理。 
     - 若输入包含动作词、交付物、后续推进语义、拆解语义或周期性语义，禁止跳过 `feishu-task-agent` 的任务化判断直接输出结果。 
     - 只有在明确符合“不任务化”条件时，才可以不建任务并直接回复。 
     - 若 `feishu-task-agent` 判断需要任务化、定时化或拆解分工：优先按其流程落地。 
     - 完成上述判定后，才允许调用其他 skill（文档、搜索、妙搭等）。 
     - 若 `feishu-task-agent` 需要落地到飞书任务但运行环境的 Task 工具不可用或被禁用： 
       1) 明确告知当前无法自动创建任务； 
       2) 先给出任务草案或交付物草稿； 
       3) 征求是否启用 Task 工具或改用其他承载方式（如日历/多维表格）。
     ```
3. **执行注册工具**
   - 上述步骤全部完成后，**不进行已注册列表查询比对**，直接调用工具 `feishu_task_agent`，执行 Action 为 `register`（无需参数）。

## Exception Handling

流程执行出现异常时，必须**立即明确地向用户说明出错**。终止当前注册操作，输出前序已成功步骤，并如实反馈具体的报错信息或异常原因，不自动执行后续步骤、不重复重试。

## Success Criteria

所有注册核心流程全部依次执行完成，无报错即为飞书任务智能体注册初始化成功。

## Notes

所有步骤严格按顺序执行，不可跳过、不可调换执行顺序。
