---
name: acpx-supervised-execution
description: Use when a coding, debugging, or research task should run inside one long-lived ACPX session while a separate supervisor keeps checking real engineering progress until the work is accepted complete or explicitly failed. 用于需要单一 ACPX 长会话执行、并由独立监工持续检查真实工程进度直到任务明确完成或失败的场景。
---

# ACPX Supervised Execution

## Overview

用 **1 个 ACPX 主执行 session** 真正干活，用 **1 个低频监工** 持续验收并自动回推修正，直到任务被验收通过或被明确判定失败。

核心原则：**监工看真实工程进度，不看“进程还活着”假象；验收不过就继续推同一个 ACPX session，不重新开实现 session。**

默认开场白：`我正在使用 acpx-supervised-execution 技能：1 个 ACPX 主执行 session + 1 个默认每 5 分钟检查一次的监工。`

## When to Use

- 任务需要在 ACPX 里持续推进，不能做成“一次派发后静默等待”。
- 任务有明确产物、测试、日志、diff、报告或其他可检查工程证据。
- 你希望监工周期性验收，并在不通过时继续推动同一实现 session 修正。
- 你需要最终自动收口：完成/失败都汇报，监工停止，自身 session 关闭。

不要用于：

- 单次 read、单次 edit、一次性问答。
- 需要多个并行实现 worker 的任务。
- 只想看存活状态、不关心实际工程进度的场景。

## Hard Invariants

1. **只允许 1 个 ACPX 主执行 session。**
2. **监工默认每 5 分钟检查一次。** 只有明确理由才改 cadence，禁止高频轮询。
3. **监工每次都检查真实工程证据。** 至少看其中两类：代码 diff、测试结果、日志、报告、生成物、提交记录、阻塞说明。
4. **每次监工输出都必须显式包含这两个段落：**
   - `已完成`
   - `未完成`
5. **验收不过时，监工必须把 continue/correction prompt 发回同一个 ACPX 主执行 session。**
6. **自动推进直到两种终态之一：**
   - 验收通过完成
   - 明确失败（不可恢复阻塞、达到失败条件、或人工取消）
7. **完成和失败都必须有最终汇报/通知。**
8. **任务进入终态后，监工必须自删/自停。**
9. **任务进入终态后，ACPX 主执行 session 也必须关闭。**

## Minimum Artifact Contract

启动前先约定可检查产物；没有产物路径就不要启动监工。

推荐最小集合：

- `reports/<slug>/task-brief.md`：目标、约束、验收标准、失败条件
- `reports/<slug>/progress.md`：执行 session 持续写入进展与证据
- `reports/<slug>/review.md`：监工逐轮追加验收记录

如果任务还有额外关键产物，也在 brief 里提前列出，例如：

- 测试命令与预期结果
- 目标文件路径
- 生成物路径
- 阻塞日志路径

## Step 1: Brief the Task

在派发前写清这 5 件事：

1. 目标是什么
2. 什么算完成
3. 什么算失败
4. 监工要检查哪些证据路径
5. 如果验收失败，允许监工回推什么类型的 correction

推荐 brief 结构：

```md
# <task title>

## Goal
<目标>

## Acceptance
- <验收条件 1>
- <验收条件 2>

## Failure
- <失败条件 1>
- <失败条件 2>

## Evidence Paths
- reports/<slug>/progress.md
- <test/log/output path>

## Non-Goals
- <本轮不做什么>
```

## Step 2: Start the Single ACPX Execution Session

派发 **一个** ACPX session 执行主任务。prompt 必须明确：

- 先读 brief
- 按 brief 的验收目标推进
- 持续把真实进展写进 `progress.md`
- 不得自行再开第二个实现 session
- 被监工纠偏时，继续在当前 session 内修正，不要重建执行链路

推荐执行 prompt 模板：

```text
先读取 reports/<slug>/task-brief.md 并严格按其目标、约束、验收标准执行。

你是唯一的 ACPX 主执行 session。

执行要求：
1. 直接推进工程工作，不要只汇报计划。
2. 每拿到新证据、完成一个子阶段、或遇到阻塞，都要把可检查事实写入 reports/<slug>/progress.md。
3. 写入内容必须包含：时间、改动/动作、证据路径、当前阻塞（若有）。
4. 不要新开第二个实现 session；后续 correction 只在本 session 内继续处理。
5. 当你认为任务完成时，必须给出对应证据；如果确认失败，也要写明失败原因和已尝试项。
```

## Step 3: Start the Supervisor

再启动一个独立监工，**默认每 5 分钟检查一次**。

监工职责只有三件事：

1. 看真实工程进度
2. 给出显式 `已完成` / `未完成` 验收报告
3. 不通过时，把 correction 发回同一个 ACPX 主执行 session

### 监工每轮必须检查什么

至少检查以下项目中的两类，最好三类：

- `progress.md` 是否出现新的事实性进展，而不是空话
- 工作区 diff / 改动文件是否与目标一致
- 测试、构建、脚本、日志结果是否推进了验收
- 关键产物是否生成且内容可信
- 阻塞是否被真实缩小，而不是重复描述

**禁止只根据“session 仍在运行”就判定正常推进。**

### 监工输出格式

每一轮都按下面格式写到 `reports/<slug>/review.md`，并在对外状态消息里保持同样结构：

```md
## Review <timestamp>

### 已完成
- <本轮确认完成的事实 1>
- <本轮确认完成的事实 2>

### 未完成
- <仍缺失的验收项 1>
- <仍缺失的验收项 2>

### Decision
- accepted | continue | failed

### Next Action
- <若 continue，写明要发回主执行 session 的修正方向>
- <若 accepted/failed，写明收口动作>
```

## Step 4: Correction Loop

只要还有 `未完成` 项，监工就不能结束。

当决策是 `continue` 时，监工必须：

1. 提炼这轮验收失败的具体缺口
2. 形成一段简短、可执行的 continue/correction prompt
3. **发送到同一个 ACPX 主执行 session**
4. 等下一轮 5 分钟检查，再重新验收

推荐 correction prompt 模板：

```text
继续当前任务，不要新开 session。

上轮验收结果：
已完成：
- <保留有效进展>

未完成：
- <缺口 1>
- <缺口 2>

请优先补齐以上未完成项，并把新的工程证据写入 reports/<slug>/progress.md。
如果遇到阻塞，写明阻塞原因、已尝试动作、下一步建议。
```

## Step 5: Decide the Terminal State

监工每轮只能落在 3 种决策之一：

- `accepted`：验收条件全部满足
- `continue`：还可继续推进
- `failed`：命中失败条件，或已无合理继续路径

### `accepted` 时必须做完的动作

1. 输出最终报告，且明确写出：
   - `已完成`
   - `未完成`（如果为空，也要写 `- 无`）
2. 发送最终完成通知
3. 关闭 ACPX 主执行 session
4. 监工自删/自停
5. 如果监工自身也运行在 ACPX session 中，完成上述动作后再关闭这个监工自己的 ACPX session

### `failed` 时必须做完的动作

1. 输出最终失败报告，且明确写出：
   - `已完成`
   - `未完成`
2. 写清失败原因、已尝试动作、缺失条件
3. 发送最终失败通知
4. 关闭 ACPX 主执行 session
5. 监工自删/自停
6. 如果监工自身也运行在 ACPX session 中，完成上述动作后再关闭这个监工自己的 ACPX session

## Supervisor Decision Rules

按下面顺序判断：

1. **先看 acceptance 是否全部满足** → 是则 `accepted`
2. **再看是否命中 failure 条件** → 是则 `failed`
3. 其他情况一律 `continue`

不要把“当前还在跑”当成 `continue` 的充分理由；必须能指出新的工程证据和下一步纠偏方向。

## Example Supervisor Prompt

```text
你是任务 <slug> 的低频监工。默认每 5 分钟执行一次检查。

必读：
- reports/<slug>/task-brief.md
- reports/<slug>/progress.md
- reports/<slug>/review.md（若已存在）

本轮要求：
1. 检查真实工程进度，不要只看 session 是否存活。
2. 至少核对两类证据：diff / test / log / artifact / report。
3. 追加一条 review 到 reports/<slug>/review.md，格式必须包含：已完成、未完成、Decision、Next Action。
4. 若验收未过，向同一个 ACPX 主执行 session 发送 continue/correction prompt。
5. 若验收通过，发送最终完成通知，然后关闭主执行 session，并让监工自己停止。
6. 若明确失败，发送最终失败通知，然后关闭主执行 session，并让监工自己停止。

输出约束：
- 每次都必须显式输出“已完成”和“未完成”两段。
- 没有未完成项时也要写“未完成：- 无”。
- 不得新开第二个实现 session。
```

## Failure-Proofing Checklist

开始前确认：

- 已有明确 brief
- 已有证据路径
- 已知哪个 session 是唯一 ACPX 主执行 session
- 已知监工默认 cadence = 5 分钟
- 已知终态收口动作：最终通知、关闭主执行 session、监工自停

如果其中任一项缺失，先补齐再启动。

## Common Mistakes

| 错误 | 正确做法 |
| --- | --- |
| 验收不过就新开实现 session | 继续推动同一个 ACPX 主执行 session |
| 监工只看“还活着” | 监工必须看 diff / test / artifact / log / report |
| 监工高频轮询 | 默认 5 分钟一次，只有明确理由才更改 |
| 监工只发一句“还在进行中” | 每轮都必须写 `已完成` / `未完成` |
| 完成后只通知、不关资源 | 最终通知后必须关闭主执行 session，并让监工自停 |
| 失败时静默退出 | 必须发最终失败报告与通知，写清未完成项 |

## Done Means Done

只有同时满足下面 5 条，任务才算真正结束：

1. 监工判定 `accepted` 或 `failed`
2. 最终报告已落盘
3. 最终通知已发出
4. ACPX 主执行 session 已关闭
5. 监工已自删/自停
