---
name: adsbrain-trace-error-locator
description: "AdsBrain / Codewiz Langfuse Trace 错误定位 Skill。用于用户提供 Langfuse trace 链接、trace_id、截图、现象描述、对错样例时，在 XRay/Langfuse 平台查询链路，定位错误发生的 observation/step/tool/model 位置，解释错误原因、责任归因和修复建议。触发词: trace定位、链路定位、Langfuse定位、平台搜索trace、定位出错位置、定位错误原因、找出哪一步错了、为什么多了澄清、为什么没调用工具、为什么调用错工具、为什么输出不符合预期、AdsBrain执行链路排查、Codewiz trace排查、xray trace排查。典型触发: \"帮我查这条 trace 为什么错\"、\"在平台搜索这条 trace 定位原因\"、\"这个对的时候和错的时候差异在哪里\"、\"多了澄清，帮我定位哪一步导致的\"、\"根据截图和 Langfuse 链路找问题\"。不应触发: 普通代码解释、非 AI/Agent 链路的 Java/RPC 性能排查。"
metadata:
  category: trace
  subcategory: adsbrain-debug
  platform: xray-langfuse
  depends_on: xray-ai-trace-analysis
  input: [langfuse_url, project_id, trace_id, timestamp, symptom, screenshot, expected_behavior, actual_behavior, object_id]
  output: [root_cause_report, faulty_observation, evidence, fix_suggestions]
---

# AdsBrain Trace 错误定位 Skill

这个 Skill 专门处理“有一个线上/平台现象，需要去 Langfuse/XRay 里搜索 trace，定位错误位置和原因”的问题。它不是泛泛做链路性能分析，而是要围绕用户给出的 **预期行为 vs 实际行为**，找到具体是哪一步模型决策、工具调用、Prompt 约束、payload 透传或前端交互导致了错误。

## 目标

当用户提供以下任一信息时，主动使用本 Skill：

- Langfuse/XRay Trace URL，例如 `https://xray-langfuse.devops.xiaohongshu.com/.../project/<project_id>/traces/<trace_id>?timestamp=...`
- `trace_id` / `project_id`
- 截图或文字现象，例如“对的时候是直接二次确认卡片，错的时候多了一次澄清”
- 对错样例，例如“这是对的时候 / 这是错的逻辑”
- 某个对象 ID、请求时间、会话信息，例如 `campaignId=205868099`、北京时间 `20:57`

默认输出必须简洁，固定包含以下内容：

1. **问题理解**：用 2～3 行说明“正确表现 / 实际错误 / 本次定位目标”。
2. **定位结论**：展示 trace、session、错误位置、责任归属和一句话根因。
3. **关键证据与解决建议**：最多列 3 条关键证据、3 条解决建议。

默认不要输出完整链路时间线、长表格、全部 observation、完整 input/output 或长篇责任边界。只有用户明确要求“详细展开 / 完整证据链 / 归档报告 / 输出完整链路时间线”时，才输出详细版报告。

无论简版还是详细版，都必须判断错误归属到哪个位置：`master agent`、`执行 agent`、`诊断 agent`、`规划 agent`、`盯盘 agent`、`前端/工程侧`、`Tool/RPC`、`平台/埋点`。不能只说“模型错了”。

## 信息抽取规则

### 1. 从 URL 抽取参数

如果用户给了 Langfuse URL，按以下规则解析：

- `project/<project_id>` 中的值作为 `project_id`
- `traces/<trace_id>` 中的值作为 `trace_id`
- URL query 中的 `timestamp` 可作为辅助时间点
- 若 URL 中包含 `sit`、用户提到测试环境/SIT，则后续请求追加 `--env sit`；否则默认生产环境

### 2. 没有 trace_id 时的搜索策略

如果用户只给了截图、对象 ID、时间或现象，没有给 trace_id：

1. 先确认是否已有保存的 `project_id`；没有则询问用户提供 Langfuse 项目 URL 或 project_id。
2. 将用户描述的北京时间转为 UTC。
3. 用 `xray-ai-trace-analysis` 的 query 能力搜索 observation，优先按以下线索组合查询：
   - `input` / `output` 包含计划 ID、广告主 ID、关键词，例如 `205868099`、`澄清`、`确认修改`、`计划出价`
   - `level=ERROR` 或 `level=WARNING`
   - `name` in `llm-stream`、`agent-step`、`router.execute`、`queryAdIndex`、`resolveAmbiguousAdIntent`、`updateCampaign`、`modifyCascade` 等
   - 按 `start_time desc` 排序
4. 汇总候选 trace，展示完整 `trace_id`、时间、name、level、关键 input/output，让用户选择；如果只有一个强匹配，可以直接进入深度分析。

> 查询时间范围不得超过 7 天；用户给的是北京时间时，必须转 UTC 后传入 `--from/--to`。

## 执行步骤

本 Skill 复用本地 `xray-ai-trace-analysis` 的脚本。默认路径：

```bash
python3 /Users/jialize/.codewiz/skills/xray-ai-trace-analysis/scripts/query_langfuse_trace.py
```

### Step 1：拉取 trace 数据

首次有 project_id 时保存：

```bash
python3 /Users/jialize/.codewiz/skills/xray-ai-trace-analysis/scripts/query_langfuse_trace.py --save_project_id <project_id> --trace_id <trace_id>
```

后续已保存 project_id 时：

```bash
python3 /Users/jialize/.codewiz/skills/xray-ai-trace-analysis/scripts/query_langfuse_trace.py --trace_id <trace_id>
```

若是 SIT：

```bash
python3 /Users/jialize/.codewiz/skills/xray-ai-trace-analysis/scripts/query_langfuse_trace.py --trace_id <trace_id> --env sit
```

数据产物：

- `/Users/jialize/.codewiz/skills/xray-ai-trace-analysis/tmp/langfuse_trace_prompt.txt`
- `/Users/jialize/.codewiz/skills/xray-ai-trace-analysis/tmp/langfuse_trace.json`

### Step 2：读取并重建执行时间线

必须读取 `langfuse_trace_prompt.txt` 和必要时的 `langfuse_trace.json`。

重点抽取：

- `trace_id`
- `total_duration_ms`
- 每个 observation 的：
  - `id`
  - `parent_observation_id`
  - `type`
  - `name`
  - `start_time/end_time`
  - `level/error_type/status_message`
  - `input/output`
  - `metadata.attributes`
  - `tool.call.id` / `tool.name`
  - `session.turn-id` / `session.position`（如果在 input 里能看到）

把链路重建为“用户输入 → 模型决策 → 工具调用 → 工具结果 → 模型输出”的时间线。

### Step 3：围绕现象做差异定位

不要只输出通用性能分析。必须基于用户给出的现象判断异常类型。

常见异常类型与定位方法：

#### A. 多了一次“澄清”

重点检查：

- 哪个 `llm-stream` 或 `agent-step` 的 output 生成了澄清文案/确认询问
- 模型 input 中是否缺少二次确认信号、execution_payload、对象 ID、目标值、投放形态
- system prompt 是否要求“模糊意图需反问”
- 是否错误调用了 `resolveAmbiguousAdIntent`
- tool 返回是否包含 `clarificationQuestion`
- 前端 payload 是否没有正确透传 `confirmation_signal` 或 `execution_payload`

判定范式：

- 如果 payload 已包含完整对象 ID + 目标值 + confirmation_signal，但模型仍澄清：优先判为 **模型遵循规则错误 / Prompt 冲突**。
- 如果 payload 缺字段导致模型澄清：优先判为 **上游/前端透传缺失**。
- 如果 tool 返回多个候选或归属不一致导致澄清：优先判为 **业务数据歧义**。

#### B. 没有调用应调用的 Tool

重点检查：

- 模型最后一个 tool-call 决策节点的 output
- available tools 中是否有目标 Tool
- system prompt 中是否把该场景排除
- 输入参数是否缺失必填字段
- 是否被二次确认门禁、创编资格门禁、风控规则提前拦截

#### C. 调错 Tool / 路由错误

重点检查：

- `queryAdIndex` 返回的 `creationType/platform/campaignType`
- 模型根据 `creationType` 选择的工具是否符合规则
- 是否出现“形态不匹配错误”后没有纠偏
- tool input 是否包含错误层级字段，例如计划口径出价却使用了单元级参数不完整的 Tool

#### D. 输出格式不符合预期

重点检查：

- 最后一轮 `llm-stream` output
- system prompt 中的输出约束
- 是否加载/遵循 response skill 或 confirmation skill
- 是否多输出 Markdown、解释文案、第二个 JSON

#### E. Tool/RPC 失败

重点检查：

- `level=ERROR` 节点
- Tool observation 的 `output`、`error_type`、`status_message`
- RPC 原始 `code/msg/requestId`
- 是否应该重试或纠偏但没有做

### Step 4：判断错误归属

必须把错误原因归属到一个或多个明确位置，并给出证据。优先级如下：

#### Agent 归属规则

| 归属位置 | 典型证据 | 说明 |
|---|---|---|
| `master agent` | 根路由、任务分发、选择子 agent 错误；未把用户真实意图传给子 agent | 例如本应交给执行 agent，却进入诊断/规划；或丢失上下文 |
| `规划 agent` | 规划方案、executionPayload、目标值、对象 ID、动作类型生成错误 | 例如把 `3.20` 错写成 `4.00`，或生成了错误 Tool/字段 |
| `执行 agent` | 已收到正确 executionPayload，但执行阶段澄清、调错 Tool、未按确认信号执行、输出格式错误 | 例如二次确认后仍澄清，或 `creationType` 路由错误 |
| `诊断 agent` | 诊断/归因/建议内容错误，导致后续采纳执行错误 | 例如诊断建议的出价、预算、原因不符合数据 |
| `盯盘 agent` | 盯盘建议、一键采纳 payload、watchdog_report 字段错误 | 例如按钮文案正确但 `payload.params.execution_payload` 错误 |
| `前端/工程侧` | 按钮点击、payload 透传、URL/session、卡片 schema、状态机、接口拼装错误 | 例如截图正确但 trace input 缺少 `confirmation_signal`；或前端把旧值/新值传错 |
| `Tool/RPC` | Tool input 正确但 Tool output/RPC 返回错误，或 Tool 内部转换/鉴权/单位换算错误 | 例如 `campaignDayBudget` 分/元转换错误，RPC 返回业务失败 |
| `平台/埋点` | trace 缺 observation、usage/session/user_id 缺失、input/output 不完整 | 影响定位准确性，但不一定是业务根因 |

#### 工程侧判定规则

当满足以下任一条件时，必须明确标记为 `前端/工程侧` 或 `Tool/RPC`，不要误判为 agent 推理问题：

- 用户截图/页面显示正确，但 trace 中 agent 收到的 input/payload 缺字段或值错误。
- 模型输出了正确 tool call，但实际 Tool observation 的 input 被改写。
- Tool 入参正确，但 RPC 返回错误或执行结果与入参不一致。
- session/trace 串联缺失导致无法追到上一轮确认卡片。
- 前端按钮点击后没有透传 `payload.params.confirmation_signal` 或 `payload.params.execution_payload`。

### Step 5：生成 Trace / Session 链接

如果用户提供了原始 Langfuse URL，最终报告直接保留原链接，并用 Markdown 超链接输出。

如果只有 `project_id` 和 `trace_id`，按以下格式生成 trace 链接，并以 `[trace_id](url)` 形式输出，确保可点击：

```text
https://xray-langfuse.devops.xiaohongshu.com/langfuse-microapp/project/<project_id>/traces/<trace_id>
```

如果从 observation 中提取到 `session_id`，最终报告必须展示完整 `session_id`，并尽量输出为可点击链接。

Session 链接格式优先使用：

```text
https://xray-langfuse.devops.xiaohongshu.com/langfuse-microapp/project/<project_id>/sessions/<url_encoded_session_id>
```

输出格式为 `[session_id](session_url)`。如果该 session URL 在当前平台不可用，再补充一句“如链接不可打开，可在 XRay/Langfuse 以 session_id 检索”。不要只输出纯文本 session_id。

### Step 6：证据引用要求

最终报告不能只给结论，必须列出证据。证据包括：

- Observation id
- 节点名/type
- 时间点
- input/output 中的关键片段
- tool arguments / tool result
- metadata 中关键字段

如果原始 input/output 太长，只摘关键字段，不要整段贴出。

## 报告格式

### 默认：简版报告

除非用户明确要求详细版，否则最终只按以下格式输出。字段尽量不要省略；没有数据时写“未提供/未检索到/需要补充”。

```markdown
# Trace 定位结论

## 1. 问题理解
- 现象：<用户描述的错误现象，一句话>
- 期望：<正确情况下应该怎样>
- 实际：<链路里实际发生了什么>

## 2. 定位结论
- Trace：[`<trace_id>`](<trace_url>)
- Session：[`<session_id>`](<session_url>)；没有则写未检索到
- 错误位置：<agent/tool/observation，精确到 observation id>
- 责任归属：<master agent / 执行 agent / 诊断 agent / 规划 agent / 盯盘 agent / 前端/工程侧 / Tool/RPC / 平台/埋点>
- 根因：<一句话，不超过 80 字>

## 3. 关键证据与解决建议
- 关键证据：
  1. <证据 1：只摘关键 input/output/tool result>
  2. <证据 2>
  3. <证据 3，可选>
- 解决建议：
  1. <建议 1，必须可执行>
  2. <建议 2>
  3. <建议 3，可选>
```

### 详细版报告

仅当用户明确要求“详细展开 / 完整证据链 / 归档报告 / 输出完整链路时间线”时，才按以下结构输出：

```markdown
# Trace 错误定位报告（详细版）

## 问题理解
- 用户期望/正确表现：...
- 实际错误表现：...
- 本次定位目标：...

## Trace / Session 信息
- Trace：[`<trace_id>`](<trace_url>)
- Project ID：...
- Session：[`<session_id>`](<session_url>)；如链接不可打开，可在 XRay/Langfuse 以 session_id 检索
- 时间范围：...

## 结论先行
- 错误类型：...
- 错误位置：...
- 责任归属：...
- 根因一句话：...
- 影响：...

## 错误位置明细
| 维度 | 结论 |
|---|---|
| 所属模块/Agent | ... |
| 具体 observation | ... |
| 发生时间 | ... |
| 上游输入是否正确 | ... |
| 当前节点输出是否正确 | ... |
| 下游是否继续放大问题 | ... |

## 链路时间线
| 顺序 | 时间 | observation | 归属 | 类型 | 动作 | 结果 |
|---|---|---|---|---|---|---|
| 1 | ... | ... | ... | ... | ... | ... |

## 关键证据
### 证据 1：...
- observation: ...
- input 关键片段：...
- output/tool result 关键片段：...
- 说明：...

## 错误原因
### 直接原因
- ...

### 深层原因
- ...

### 责任边界
- ...

## 解决方案
### P0
- ...

### P1
- ...

### 工程改动建议
- ...

## 回归验证
- 用例 1：...
- 用例 2：...
```

## 针对 AdsBrain 执行 Agent 的常用判断规则

### 二次确认后的预算/出价修改

如果用户/前端输入中已经包含：

- `confirmation_signal=客户已二次确认`
- `execution_payload.tool`
- 对象 ID，例如 `campaignId`
- 目标值，例如 `campaignDayBudget` / `eventBid`

则模型不应再次生成澄清或二次确认卡片，而应进入：

```text
必要校验 → searchKnowledge 风控检索 → 对应修改 Tool → 结构化执行结果
```

若此时多了一次“确认一下/澄清一下”，重点判断是否：

1. 前端没有透传 `confirmation_signal` 或 `execution_payload`
2. 模型没有正确识别已确认状态
3. Prompt 中“模糊意图要澄清”的规则覆盖了“已确认执行”的规则
4. Tool 返回了 `clarificationQuestion`，模型误把只读解析结果当成必须询问

### 正确链路应包含

- 首轮未确认时：查询对象详情/资格校验 → 输出 `campaign_edit_plans` 二次确认卡片
- 用户确认后：识别确认信号 → 风控检索 → 修改 Tool → 成功/失败 JSON

### 错误链路常见信号

- 用户确认后仍出现自然语言确认文案
- 已有 `execution_payload` 但重新解析出不同目标值
- 已确认后又输出 `campaign_edit_plans` 卡片
- 标准投/简单投路由与 `creationType` 不一致
- `updateCampaign` / `modifyCascade` / `simpleUpdateAd` 等 Tool 未被调用
- 最终输出不是规定 JSON

## 交互策略

- 如果 trace_id 明确：不要追问，直接查询并分析。
- 如果只有截图但没有 trace_id：先让用户补充 trace 链接、trace_id，或提供时间范围 + project_id + 关键对象 ID。
- 如果查询到多个候选 trace：列出最多 5 个候选，让用户选；每个候选只展示 trace_id、时间、session_id、关键 input/output 摘要。
- 如果数据为空：说明可能是 project_id、环境、时间范围不对，并给出下一步需要的信息。
- 默认报告必须控制篇幅，避免超过 80 行；详细版不受此限制。

## Agent 名称识别提示

在 trace 中可通过以下线索识别 agent：

- `agentId`、`sessionId`、`ark.ai.agent.name`、`ark.ai.session.id`
- system prompt 中的角色描述，例如“执行 Agent”“规划 Agent”“诊断 Agent”“盯盘 Agent”
- tool 列表和 tool 名称：
  - 执行 agent：`updateCampaign`、`modifyCascade`、`simpleUpdateAd`、`queryAdIndex`、`checkAdvertiserCreateAccess`、`searchKnowledge`
  - 规划 agent：生成方案、推荐预算/出价、构造 `executionPayload`
  - 诊断 agent：分析投放问题、生成诊断原因和建议
  - 盯盘 agent：`watchdog_report`、一键采纳、风险/机会建议
  - master agent：路由、任务拆解、agent 分发
- 如果无法确定 agent 名称，要写“无法从当前 trace 明确识别”，并说明还需要 session 上游 trace 或更完整链路。

## 注意事项

- 不要泄露不必要的完整用户输入、广告主敏感数据和超长 Prompt，只摘录定位所需片段。
- `trace_id` 必须完整展示，不要截断。
- 用户给的是北京时间，脚本参数使用 UTC。
- 结论必须区分“确定事实”和“推测原因”。
- 如果发现是埋点缺失，也要单独指出会影响定位准确性。
- 默认简版报告优先回答“在哪、为什么、怎么修”，不要堆完整链路细节。
