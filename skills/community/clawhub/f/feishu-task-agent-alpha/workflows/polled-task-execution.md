# Workflow: 处理后台轮询的未完成任务 (Polled Task Execution)

## Overview

本工作流用于处理来自后台 Cronjob 轮询的任务。它和聊天触发的“新建任务”流程是两条独立链路。
本流程不仅处理来自 `get-agent-unfinished-tasks`（定期拉取普通待办）的任务，还兼容**来自其他自定义定时任务（Cronjob）拉取的周期性飞书任务（Repeat Tasks）**。

轮询准入规则统一以 `scripts/should_execute_polled_task.py` 的输出为准。
针对周期性任务，新流程增加了特有的**执行后查询下一次任务 ID (`next_task_guid`)** 以及**回写更新 Cronjob** **`--message`** 的核心闭环逻辑。

除“轮询准入判断”“基于已有任务重新提炼`task_goal`”“复杂任务判断与子任务创建”这三类差异外，状态流转、`agent_task_progress`、`append_steps`、评论、交付物落地、最终用户输出，全部严格按 [../references/task-decision-rules.md](../references/task-decision-rules.md) 第 12 至 16 节执行。若本文件与该 reference 有任何不一致，以 reference 为准。

## When to Use

当输入来自后台的 Cronjob 轮询（包含 `get-agent-unfinished-tasks` 或其他用户自定义的定时任务）时触发。

## Workflow Steps

### 步骤 1：来源判定与准入校验 (Source & Qualification)

1. 获取待执行的任务列表。
   1. `get-agent-unfinished-tasks`以应用身份调用 `feishu_task_task.list`，参数`agent_task_status=1`。
   2. 其他定时任务来源以应用身份调用 `feishu_task_task.get`，参数 `task_guid` 为定时任务 message中的guid。
2. 对每个任务运行判断脚本（注意通过 `--source` 传递任务来源）。**注意：只需要找到 2 个 `should_execute=true` 的实际需要运行的任务进行处理即可，找到并处理完 2 个后即可结束当前轮询，不需要处理完拉到的所有任务**：

```bash
python3 ./scripts/should_execute_polled_task.py \
  --source "<定时任务名称，如 get-agent-unfinished-tasks 或其他 cronjob 名称>" \
  --input-json '<task_json>'
```

1. 脚本的 JSON 输出中包含 `should_execute` 和 `is_repeat_task` 字段。分支判断逻辑已完全收敛到该脚本内：
   - 如果是 `get-agent-unfinished-tasks`，\*\*不处理（抛弃）\*\*循环任务。
   - 如果是其他定时任务来源，脚本内部会检查 `is_repeat_task`，若非循环任务会直接返回 `should_execute=false`。
2. **执行决策**：大模型仅需查看 `should_execute` 字段。
   - 若脚本返回 `should_execute=false`，本轮直接跳过该任务，不改状态、不写评论、不写日志。
   - 若脚本返回 `should_execute=true`，继续执行后续步骤（注意：一旦累计找到并处理了 2 个 `should_execute=true` 的任务，即刻终止整个轮询流程，不再处理其余拉取到的任务）。

### 步骤 2：状态流转与业务执行 (Execution & State Machine)

1. 基于任务现有 `summary`、`description` 以及最新相关用户评论（若有）重新提炼 `task_goal`。
2. 保留复杂任务判断。满足任意 2 条即可视为复杂任务：
   - 有 3 个及以上明确步骤
   - 有多个交付物
   - 有多人或多角色协作
   - 有阶段依赖或先后顺序
   - 需要持续推进，而非一次性完成
   - 从现有任务内容或评论里能明确看出需要拆解、分步骤、细化
3. 若判断结果为复杂任务，先形成 1 至 5 个一级子任务，并实际创建子任务；只有某个一级子任务仍明显复杂时，才允许受控二级拆解，且每个一级子任务最多 3 个二级子任务。
4. 子任务创建时继承父任务当前的执行身份与成员关系，不重新运行 `scripts/resolve_creator_members.py`。
5. 父任务进入执行流程，按以下顺序执行：
   - 调用 `feishu_task_task.patch(auth_type=tenant, agent_task_status=2, agent_task_progress="正在执行")`
   - 立刻调用 1 次 `feishu_task_task.append_steps(auth_type=tenant, ...)` 写入起始日志
   - 根据阶段调用 `feishu_task_task.patch(auth_type=tenant, agent_task_progress="<阶段名>")`
   - 若需要用户确认，先调用 `feishu_task_comment.create(auth_type=tenant, ...)`，再调用 `feishu_task_task.patch(auth_type=tenant, agent_task_status=3, agent_task_progress="等待回复")`
   - 若用户回复后恢复执行，调用 `feishu_task_task.patch(auth_type=tenant, agent_task_status=2, agent_task_progress="<恢复后的阶段名或正在执行>")`
   - 仅在状态为 `2` 时追加 `feishu_task_task.append_steps(auth_type=tenant, ...)`
   - 若准备从状态 `2` 切到 `3` 或 `4`，且仍有未 flush 的新增输出，先补 1 条收尾日志，再切状态
   - 若有交付物，按类型落地：
     - 如果交付物是图片/文件，通过 `feishu_task_attachment.upload` 以应用身份上传附件, 参数如下:`resource_type`为'task\_delivery', `resource_id`为当前这个任务的guid, `file`为图片/文件内容的base64 string `name`为图片/文件名称加对应后缀。
     - 如果交付物是链接，通过 `feishu_task_task.patch` 以应用身份更新`text_deliveries`。若 agent 输出为“说明文本 + 链接”的混合内容，必须先只抽取其中的链接，去掉所有说明、标题、前后缀文本和标点，仅将纯链接写入 `text_deliveries`；说明文本可放在评论摘要中，不得混入 `text_deliveries`。
     - 链接型交付物的 `text_deliveries` 写入是必做落地动作，不得只写评论不写 `text_deliveries`。
     - 若本轮有链接型交付物，必须先确认 `text_deliveries` 已成功写入，再允许进入完成态、发送最终回执，或结束当前交付流程。
     - 如果交付物是文本/富文本，先将文本转成标准的markdown格式后，将markdown格式内容作为文本内容，并根据内容提炼一个标题作为文件名，然后通过 `feishu_task_attachment.upload` 以应用身份上传附件，参数如下 `resource_type`为'task\_delivery', `resource_id`为当前这个任务的guid, `file`为文本内容的base64 string， `name`为提取的名称.md
   - 完成时调用 `feishu_task_task.patch(auth_type=tenant, agent_task_status=4, agent_task_progress="执行完成")`
   - 最后调用 `feishu_task_comment.create(auth_type=tenant, content="<结果摘要/附件说明/最终结果>")`

### 步骤 3：周期任务的闭环（Next Task ID 轮询与 Cronjob 更新）

1. **适用条件**：仅对来自其他定时任务（非 `get-agent-unfinished-tasks`）的**循环任务**，在状态更新为 `4` (已完成) 之后执行。
2. **轮询获取 Next Task ID 并更新 Cronjob**：

- 因为只能通过 `feishu_task_task.get` 获取详细信息，且飞书在循环任务完成后会异步生成下一次任务。大模型需要调用 `feishu_task_task.get` 获取刚完成任务的详情，并从中提取 `next_task_guid` 字段。
- 由于异步生成可能有延迟，大模型需要进行最多 3 次退避轮询，每次失败后分别休眠 1秒、5秒、10秒。
- 成功获取到 `next_task_guid` 后，大模型必须调用 `openclaw cron list --all --json` 获取所有定时任务列表。
- 在返回的 JSON 数据中，找到当前任务对应的 `cronjob id` 和 `message`。
- 将找到的 `message` 中的旧飞书任务 ID 替换为新获取到的 `next_task_guid`，组合成新的 `message`。
- 最后调用 `openclaw cron update` 命令将新的 `message` 更新回定时任务，命令格式为：
  ```bash
  openclaw cron update <cronjob_id> --patch '{
    "payload": {
      "message": "<这里换成替换了新 task_guid 后的完整 message 文案>"
    }
  }'
  ```

## Explicit Exclusions

本流程不做以下动作：

- 不重新做任务化判断
- 不重新提炼 creator/member 语义槽位
- 不运行 `scripts/resolve_creator_members.py`
- 不为父任务调用 `feishu_task_task.create`
- 不为父任务补 `agent_task_status=1`

## References

- creator / members 契约：读 [../references/task-output-contract.md](../references/task-output-contract.md)
- 详细判定与状态规则：读 [../references/task-decision-rules.md](../references/task-decision-rules.md)
