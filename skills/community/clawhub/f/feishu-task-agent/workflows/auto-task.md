# Workflow: 飞书任务编排

## Overview

本工作流负责把任务化候选落成飞书任务，包括一次性任务、复杂任务拆解、周期性任务，以及负责人为应用时的执行状态编排。

creator / members 不允许由 agent 手工拼装。`scripts/resolve_creator_members.py` 的输出是唯一真相。

## When to Use

当请求命中以下任一情况时进入本工作流：

- 明确要求建任务、待办、to-do、跟进项
- 输入里已经形成明确行动项、交付物或推进事项
- 用户要求生成可交付内容，且该内容明显需要后续发送、提交、评审、使用或推进
- 用户要求把一个事项拆成步骤、阶段或子任务
- 用户要求按每天、每周、固定时间或周期性方式执行

以下情况默认不进入：

- 纯问答、纯解释、纯闲聊
- 没有后续动作、交付物或推进价值的即时回复
- 无法稳定提炼出任务标题的模糊背景描述

## Workflow

1. 先依据 [../references/task-decision-rules.md](../references/task-decision-rules.md) 判断是否任务化、是否复杂、是否属于周期任务。
2. 提炼 `summary`、`task_goal`，必要时提炼 `execution_result`。
3. 若属于周期任务，直接走 `cronjob + repeat task` 路径，不先创建普通单次任务。
4. 若不是周期任务但属于复杂任务，先形成 1 至 5 个一级子任务草案；只有确实必要时才做受控二级拆解。
5. 仅提炼 creator/member 语义槽位：`create_as`、`explicit_assignee_open_id`、`explicit_follower_open_ids`。
6. 注入运行时上下文：
   - `sender_open_id` 从消息上下文读取
   - `app_id` 优先让脚本从当前 OpenClaw Feishu account 配置自动解析
7. 必须运行下列命令，使用脚本产出的 `auth_type`、`current_user_id` 和 `members` 创建任务：
   ```bash
   python3 scripts/resolve_creator_members.py \
   --sender-open-id "<SenderId>" \
   --input-json '<semantic_json>'
   ```
8. 调用 `feishu_task_task.create` 创建任务，`description` 只写任务目标、范围、关键约束和完成标准，不回填本轮完整执行结果。
9. 若当前 assignee 为应用，进入执行阶段后所有状态更新、执行日志、评论与交付物写入都必须显式使用应用身份：
   - 创建成功后立刻 `patch auth_type=tenant, agent_task_status=1`
   - 真正开始执行时先 `patch auth_type=tenant, agent_task_status=2` 且更新 `agent_task_progress`
   - 进入 `agent_task_status=2` 后，无论任务长短，至少写入 1 条 `append_steps` 作为执行起始日志
   - 等待用户确认时先评论 `auth_type=tenant`，再 `patch auth_type=tenant, agent_task_status=3`
   - 执行完成后 `patch auth_type=tenant, agent_task_status=4`
10. 仅当 `agent_task_status=2` 时追加执行日志，统一使用 `feishu_task_task.append_steps`，并显式传 `auth_type=tenant`，不要沿用创建任务时的用户身份。即使是短任务，只要真正进入执行态，也必须至少写入 1 条起始日志；若存在中间输出，按聚合批次补充后续日志；若离开执行态前仍有未 flush 的新增输出，必须先补 1 条收尾日志。
11. 若当前轮已产出交付物或阶段结果，通过 `feishu_task_comment.create` 追加评论，不写回 `description`。评论默认承载摘要、阶段说明或交付说明，不作为文本交付物的唯一落点。
12. 若当前轮已产出交付物，按需对不同类型的交付物进行处理：
    - 如果交付物是图片/文件，通过 `feishu_task_attachment.upload` 以应用身份上传附件, 参数如下:`resource_type`为'task_delivery', `resource_id`为当前这个任务的guid, `file`为图片/文件内容的base64 string `name`为图片/文件名称加对应后缀。
    - 如果交付物是链接，通过 `feishu_task_task.patch` 以应用身份更新`text_deliveries`。若 agent 输出为“说明文本 + 链接”的混合内容，必须先只抽取其中的链接，去掉所有说明、标题、前后缀文本和标点，仅将纯链接写入 `text_deliveries`；说明文本可放在评论摘要中，不得混入 `text_deliveries`。
    - 链接型交付物的 `text_deliveries` 写入是必做落地动作，不得只写评论不写 `text_deliveries`。
    - 若本轮有链接型交付物，必须先确认 `text_deliveries` 已成功写入，再允许进入完成态、发送最终回执，或结束当前交付流程。
    - 如果交付物是文本/富文本，先将文本转成标准的markdown格式后，将markdown格式内容作为文本内容，并根据内容提炼一个标题作为文件名，然后通过 `feishu_task_attachment.upload` 以应用身份上传附件，参数如下 `resource_type`为'task_delivery', `resource_id`为当前这个任务的guid, `file`为文本内容的base64 string， `name`为提取的名称.md

13. 若需要拆解，按同样规则创建子任务；只有 assignee 为应用的子任务才应用执行约束。
   - 子任务创建时继承父任务当前的执行身份与成员关系，不重新运行 `scripts/resolve_creator_members.py`。


## Rules

- 不要把“模型能当场生成内容”误判为“不需要任务”。
- 默认应用负责、发送者关注；若用户明确指定负责人，则由指定用户替代应用负责。
- 若脚本失败、运行时上下文缺失、或 `app` 创建场景拿不到 `app_id`，立即停止并明确报错。
- 是否应用执行约束，不看创建身份，只看当前 assignee 是否为 `type=app`。
- 不新增直连 Feishu API 的脚本，也不修改官插底层代码。

## References

- 详细判定与状态规则：读 [../references/task-decision-rules.md](../references/task-decision-rules.md)
- 精简场景样例：读 [../references/task-examples.md](../references/task-examples.md)
- 脚本输入输出契约：读 [../references/task-output-contract.md](../references/task-output-contract.md)
