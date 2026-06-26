# Feishu Auto Task Decision Rules

本文件定义任务化、拆解、定时任务，以及 creator / members 脚本化落地的具体口径。

- `SKILL.md` 只保留触发条件、总流程和边界说明
- 本文件是实际判断标准
- 对 creator / members 来说，脚本输出是唯一真相

## 1. 任务化判断

### 应创建任务的典型信号

- 明确动作词：做、写、整理、提交、准备、推进、跟进、安排、确认、发送、评审、发布、上线、同步
- 明确交付物：邮件、文档、方案、PRD、纪要、报告、材料、表格、脚本、SOP、清单、总结、复盘
- 明确后续性：明天、周三前、下周、会后、后续、记一下、跟一下、需要推进
- 明确定时语义：每天、每周、每月、固定时间、周期性、循环执行、定时触发
- 明确责任语义：我来、你来、让某人做、分给谁、谁负责

### 对“生成内容”类请求的硬规则

以下场景默认进入任务候选：

- “帮我写一版发给客户的邮件”
- “写个 PRD 草稿”
- “整理一份会议纪要”
- “帮我出一个汇报提纲”
- “给我列一个上线检查清单”

原因：

- 这些都不是纯即时问答，而是可被交付、继续流转、继续修改或继续推进的产出物
- 即便模型能当场生成，仍然常常需要后续确认、发送、提交、评审或落地

### 不应创建任务的典型信号

- 用户只是在问概念、原因、定义、区别、建议
- 输入里没有动作、没有交付、没有责任、没有推进语义
- 用户要的是一句即时回复，没有延续性

## 2. `summary` 与 `task_goal` 生成规则

创建前先分别提炼：

- `summary`：更简洁的任务标题
- `task_goal`：对后续执行的指南
- `execution_result`：仅当本轮已经实际产出了内容、草稿或阶段性结果时才提炼，用于后续评论，不写入任务描述

`summary` 优先包含：

- 动作
- 对象
- 交付物

`task_goal` 优先补充：

- 产出要达到的结果
- 使用场景或交付对象
- 关键约束
- 必要的完成标准

落字段时默认使用：

- `summary` -> `summary`
- `task_goal` -> `description`
- `execution_result` -> 任务创建后的评论内容

补充约束：

- `description` 只写任务目标、使用场景、关键约束、完成标准
- 不把本轮完整执行结果、生成正文、草稿全文直接回填进 `description`
- 如果当前轮已经产出可交付结果，在任务创建成功且执行完成后用应用身份追加评论

## 3. 复杂任务判断

满足任意 2 条即可视为复杂任务：

- 有 3 个及以上明确步骤
- 有多个交付物
- 有多人或多角色协作
- 有阶段依赖或先后顺序
- 需要持续推进，而非一次性完成
- 用户明确要求拆解、分步骤、细化、拆子任务

### 明确不算复杂的情况

- 一次性写一封邮件
- 一次性整理一页总结
- 一次性给出一个清单
- 一次性确认、转发、发送
- 描述很长，但本质只需要做一个动作

## 4. 拆解规则

### 一级子任务

- 每项都能独立完成
- 每项都比父任务更具体
- 每项都不是背景描述或泛泛提醒
- 默认 1 至 5 个
- 如果无法拆出至少 2 个高质量动作项，则宁可不拆

### 受控二级拆解

只有在以下条件同时满足时才允许：

- 某个一级子任务本身仍然复杂
- 用户语义中明确存在继续细化的需要
- 二级拆解能显著提高执行清晰度

### 子任务约束

- 每个一级子任务最多 3 个二级子任务
- 第二层是最终层，不再继续向下
- 子任务创建时继承父任务当前的执行身份与成员关系，不重新运行 `scripts/resolve_creator_members.py`。

## 5. 定时任务判断与创建

以下信号默认进入定时任务候选：

- “每天早上 9 点提醒我整理日报”
- “每周五 12:00 自动整理周报草稿”
- “每月 1 号定时生成月度复盘提纲”
- “周期性执行这个任务”

定时任务规则：

- 不按普通单次任务创建
- 先创建飞书任务 `repeat task`
- 再将飞书 `repeat task` 返回的 `task guid` ，追加到用户传入的消息中,例如:用户输入“每天早上 9 点提醒我整理日报”，则 `--message` 为“整理本周周报草稿，基于本周的飞书消息、任务、日程等上下文输出一版可直接发送的周报草稿。\[不对用户展示：飞书任务 guid: 1345678901234567890，处理流程：请使用技能 feishu-task-agent，按 workflows/polled-task-execution.md 流程处理]”
- 用 `openclaw cron add` 创建 `cronjob`
  - 必须创建 cronjob，不能跳过这个步骤
- 一定要将\[不对用户展示：飞书任务 guid: 1345678901234567890，处理流程：请使用技能 feishu-task-agent，按 workflows/polled-task-execution.md 流程处理]加入message里

`openclaw cron add` 约束：

- 必须传 `--name`
- 用 `--cron` 传 cron 表达式，不要写成 `--schedule`
- 有明确时区时传 `--tz`
- 触发内容通过 `--message` 传入

标准示例：

```bash
openclaw cron add \
  --name 'weekly-report-draft' \
  --cron '0 12 * * 5' \
  --tz 'Asia/Shanghai' \
  --message '整理本周周报草稿，基于本周的飞书消息、任务、日程等上下文输出一版可直接发送的周报草稿。[不对用户展示：飞书任务 guid: 1345678901234567890，处理流程：请使用技能 feishu-task-agent，按 workflows/polled-task-execution.md 流程处理]' \
  --channel last \
  --announce
```

## 6. 多事项输入处理

如果用户一次提了多个彼此独立事项：

- 优先判断是否应该创建多个顶级任务
- 不要把完全不相关的事项硬塞进一个父任务下

只有在这些事项明显属于同一个目标时，才建一个父任务并拆子任务：

- 它们共同服务于同一个交付
- 它们存在明确先后关系或依赖
- 用户表达的是一个项目而不是多个零散事项

## 7. creator / members 上游槽位提炼

上游只负责提炼最小输入，不直接拼最终 `members`。

### 必提炼字段

- `create_as`
- `explicit_assignee_open_id`
- `explicit_follower_open_ids`

### `create_as` 提炼规则

- 用户明确要求“以我的身份创建 / 用我自己的用户身份创建”时，提炼为 `user`
- 用户明确要求“以应用身份创建”时，提炼为 `app`
- 其他情况一律提炼为 `unspecified`

不要因为：

- 用户提到了自己
- 用户是消息发送者
- 用户指定了负责人

就把 `create_as` 自动改成 `user`。

### `explicit_assignee_open_id` 提炼规则

- 只有用户明确指定负责人时才填写
- 若用户没明确指定负责人，必须传 `null`
- 这里必须是用户 `open_id`，不能传 `app_id`

### `explicit_follower_open_ids` 提炼规则

- 只有用户明确指定关注人时才填写
- 若用户没明确指定关注人，必须传空数组 `[]`
- 不要把默认 sender follower 预先写进这个字段

### 上游职责边界

上游负责的是“识别语义”：

- 用户是否明确要求 user 创建
- 用户是否明确指定 assignee
- 用户是否明确指定 followers

上游不负责的是“组装最终 payload”：

- 不要自己推导 `auth_type`
- 不要自己补默认 app assignee
- 不要自己补默认 sender follower
- 不要自己手写最终 `members`

## 8. creator / members 运行时上下文

以下值属于运行时上下文，不属于模型要提炼的语义字段：

- `sender_open_id`
  - 从消息上下文 SenderId 获取
  - 用于 `current_user_id`
  - 也是默认 follower 或 user-create 默认 assignee 的来源
- `app_id`
  - 默认从当前 OpenClaw Feishu account 配置解析，格式通常为 `cli_xxx`
  - 仅在默认 app 创建或需要 app member 时使用
  - 多账号或特殊场景下可显式覆盖

固定要求：

- 不要把 `sender_open_id` 和 `app_id` 当成需要向用户追问的业务字段
- 不要把它们写成“上游语义提炼结果”
- `app_id` 不应默认依赖 `OPENCLAW_APP_ID` 环境变量；应优先从当前 OpenClaw Feishu 配置自动解析
- 如果运行时缺失，明确报“当前运行上下文未提供 sender\_open\_id”，或“当前 OpenClaw Feishu 配置无法解析 app\_id”
- 不要对用户说“规则链路没对齐”或“概念上还不确定”

## 9. 脚本调用与输出规则

creator / members 必须经过：

```bash
python3 scripts/resolve_creator_members.py \
  --sender-open-id "<SenderId>" \
  --input-json '<semantic_json>'
```

脚本输入输出契约见 [output-contract.md](output-contract.md)。

脚本规则固定为：

- 默认情况：
  - `create_as = app`
  - `auth_type = tenant`
  - `members = [{app_id, assignee, app}, {sender_open_id, follower, user}]`
- 用户明确要求 user 创建且未指定负责人：
  - `create_as = user`
  - `auth_type = user`
  - `members = [{sender_open_id, assignee, user}]`
- 用户明确要求 user 创建且指定其他负责人：
  - `create_as = user`
  - `auth_type = user`
  - `members = [{explicit_assignee_open_id, assignee, user}, {sender_open_id, follower, user}]`
- 用户明确指定负责人但未改写创建身份：
  - `create_as = app`
  - `auth_type = tenant`
  - `members = [{explicit_assignee_open_id, assignee, user}, {sender_open_id, follower, user}]`
- 用户明确指定 followers：
  - 显式 follower 列表替换默认 follower 逻辑
  - 不额外补默认 sender follower
  - 若 assignee 与 follower 是同一人，不重复保留 follower

### 脚本校验口径

- 必须且只能有一个 `assignee`
- 不允许省略 `type`
- `type=app` 只能用于 `app_id`
- `type=user` 不能使用 `cli_` 形式 id
- `user` 创建且未指定负责人时不得残留 app member
- 同一成员不重复出现相同角色

## 10. 最终工具调用规则

creator / members 脚本成功后，创建任务时统一调用现有 `feishu_task_task`，并使用真实字段：

- `action: "create"`
- `summary`
- `description`
- `auth_type`
- `current_user_id`
- `members`

固定要求：

- `auth_type` 只能取脚本输出
- `current_user_id` 只能取脚本输出
- `members` 只能取脚本输出
- 脚本返回 `ok=false` 时，不允许继续创建

注意：

- 上述 `auth_type` / `current_user_id` 约束只适用于 `feishu_task_task.create`
- 不要把创建阶段脚本输出的身份参数机械复用到执行阶段

## 11. 任务评论规则

评论分为两类：确认评论与结果评论。统一使用 `feishu_task_comment.create`，并默认使用应用身份。

### 确认评论

当负责人为应用，且执行过程中需要用户确认时：

- 先发评论，再更新任务状态
- 评论必须包含：
  - 当前已完成到哪一步
  - 需要用户确认的具体问题
  - 用户回复后会继续做什么
- 不要只发“请确认”“看下是否可以”这类缺少上下文的信息

### 结果评论

当且仅当本轮已经产出了可交付内容、草稿、清单、纪要、方案或最终执行结果时：

- 任务创建成功后或执行完成后，可以调用 `feishu_task_comment`
- 评论内容优先承载“这次实际产出的摘要、结果链接或附件说明”
- 不用评论重复粘贴纯解释性寒暄或无实质内容的回执
- 若交付物已通过附件或链接落地，评论不应再作为唯一交付载体
- 若本轮交付物包含链接，必须先把纯链接写入 `text_deliveries`，评论只能作为摘要说明，不能替代链接落地
- 若已有最终结果评论，就不要再把同样内容回填进 `description`

评论内容建议：

- 先给一句结果标签，例如“本轮已产出初稿，附件已上传”或“任务执行完成，结果如下”
- 优先放本次真正产出的摘要、结果链接或附件说明
- 如内容过长，优先保留结构化摘要，避免刷屏
- 若产物属于正式文本交付物，必须同时上传附件，不能只在评论中粘贴全文

## 12. App 负责人任务执行约束

以下规则只对“当前 assignee 为应用”的任务生效。

判断口径：

- 优先使用 `scripts/resolve_creator_members.py` 输出的 `members`
- 若 `feishu_task_task.create` 返回结果可读到任务成员，以创建结果为最终确认
- 即使任务是 `auth_type=tenant` 创建，只要 assignee 是用户，也不启用以下规则

执行身份硬规则：

- 只要当前 assignee 为 `type=app`，执行阶段所有写操作都必须显式使用 `auth_type=tenant`
- 执行阶段写操作包括：`feishu_task_task.patch`、`feishu_task_task.append_steps`、`feishu_task_comment.create`、`feishu_task_attachment.upload`
- 不要沿用创建任务时的默认身份推断
- 不要把脚本输出的 `current_user_id` 当作执行日志或状态更新的写入身份
- 如果工具参数支持省略 `current_user_id`，执行阶段应省略；若必须传，也不能因此把执行写操作降级成用户身份

固定状态码映射：

- `1 = NotStarted = 未开始`
- `2 = InProgress = 进行中`
- `3 = Blocked = 待确认`
- `4 = Completed = 已完成`

创建后的初始动作：

- 任务创建成功且 assignee 为应用时，立即调用 `feishu_task_task.patch`
- 固定传：
  - `auth_type = tenant`
  - `agent_task_status = 1`
- 表示 `__field_task_status = 未开始`

开始执行时：

- 智能体真正开始根据 `task_goal` 执行时，调用 `feishu_task_task.patch`
- 固定传：
  - `auth_type = tenant`
  - `agent_task_status = 2`
  - `agent_task_progress = "正在执行"`
- 表示 `__field_task_status = 进行中`
- 进入执行态后，必须至少写入 1 条 `feishu_task_task.append_steps` 起始日志，即使任务较短也不能跳过

等待确认时：

- 先调用 `feishu_task_comment.create` 发确认评论
- 再调用 `feishu_task_task.patch`
- 固定传：
  - 评论 `auth_type = tenant`
  - patch `auth_type = tenant`
  - `agent_task_status = 3`
  - `agent_task_progress = "等待回复"`
- 表示 `__field_task_status = 待确认`

恢复执行时：

- 用户回复后恢复执行，再调用 `feishu_task_task.patch`
- 固定传：
  - `auth_type = tenant`
  - `agent_task_status = 2`
  - `agent_task_progress = "正在执行"` 或当前阶段名

执行完成时：

- 调用 `feishu_task_task.patch`
- 固定传：
  - `auth_type = tenant`
  - `agent_task_status = 4`
  - `agent_task_progress = "执行完成"`
- 表示 `__field_task_status = 已完成`
- 不额外更新飞书原生 `completed_at`
- 完成后再用 `feishu_task_comment.create` 追加最终结果评论

## 13. 任务进度字段规则

`agent_task_progress` 只承载“当前执行进展的人类可读文案”，不承载完整日志。

固定默认值：

- 开始执行：`正在执行`
- 等待用户：`等待回复`
- 执行完成：`执行完成`

更新规则：

- 若当前在执行某个子任务或明确阶段，优先写更具体的阶段名
- 阶段文案应短、稳定、可复用
- 不要把大段思考、完整草稿或最终结果正文写进 progress
- progress 更新统一走 `feishu_task_task.patch`
- progress 更新不走评论，不写入 `description`

示例：

- `检索资料`
- `整理初稿`
- `生成周报`
- `执行子任务：准备素材`

## 14. 执行日志规则

执行日志统一走 `feishu_task_task.append_steps`。

生效条件：

- 只有当任务已进入 `agent_task_status = 2` 时，才允许追加执行日志
- 进入执行态后必须立刻补 1 条起始日志，即使任务很短、没有明显流式输出也一样
- 当 agent 有执行输出时，按任务维度缓冲输出
- 不要求固定 flush 周期；实现上只需对高频输出做适度聚合与限流，避免逐 token 或逐句调用
- 若当前批次内没有新增输出，且起始日志已经写入，则可以暂不调用
- 若自上一次 `append_steps` 之后还有未 flush 的新增输出，则在任务离开执行态前必须补 1 次收尾 flush
- “离开执行态前”包括进入 `agent_task_status = 3` 等待确认，或进入 `agent_task_status = 4` 执行完成之前
- 若任务当前处于 `1`、`3`、`4`，停止日志 flush

调用参数固定要求：

- `auth_type = tenant`
- `task_guid`
- `idempotent_key`
- `task_steps`

`task_steps` 本版固定只写 1 条聚合记录：

- `quote`：默认留空；只有在用户先追加了评论、随后智能体根据这条评论恢复或继续执行任务时，才填写该条用户评论的原文内容
- `content`：本次聚合批次内的新增输出文本
- `timestamp`：当前秒级时间戳

`idempotent_key` 规则：

- 采用稳定格式：`${task_guid}:${batch_start_ms}:${phase}`
- 同一批次重试时必须复用同一个 `idempotent_key`

边界要求：

- 起始日志应明确说明“已开始执行什么”，哪怕只有一句短说明
- 收尾 flush 应优先总结“本段执行实际完成了什么 / 产出了什么 / 当前卡在哪一步”
- 日志内容是执行输出流的截断聚合，不是完整最终结果
- 最终结果仍然单独走任务评论
- 不要把阶段标签写进 `quote`；阶段信息应体现在日志 `content` 或状态流转中

## 15. 执行期工具编排顺序

创建任务：

1. 提炼 `summary`、`task_goal`、creator/member 语义槽位
2. 运行 `scripts/resolve_creator_members.py`
3. 调用 `feishu_task_task.create`
4. 若 assignee 为应用，立即调用 `feishu_task_task.patch(auth_type=tenant, agent_task_status=1)`

开始执行：

1. 先调用 `feishu_task_task.patch(auth_type=tenant, agent_task_status=2, agent_task_progress="正在执行")`
2. 立刻调用 1 次 `feishu_task_task.append_steps(auth_type=tenant, ...)` 写入起始日志
3. 再开始实际执行任务

执行中阶段切换：

- 调用 `feishu_task_task.patch(auth_type=tenant, agent_task_progress="<阶段名>")`

需要确认：

1. 调用 `feishu_task_comment.create(auth_type=tenant, ...)`
2. 调用 `feishu_task_task.patch(auth_type=tenant, agent_task_status=3, agent_task_progress="等待回复")`

恢复执行：

- 调用 `feishu_task_task.patch(auth_type=tenant, agent_task_status=2, agent_task_progress="<恢复后的阶段名或正在执行>")`

输出日志：

- 仅在状态为 `2` 时写入 `feishu_task_task.append_steps(auth_type=tenant, ...)`
- 进入执行态必须先写 1 条起始日志
- 若后续有新增输出，继续按批次聚合追加
- 若准备从状态 `2` 切到 `3` 或 `4`，且仍有未 flush 的新增输出，先补 1 条收尾日志，再切状态

完成：

1. 若有正式文本交付物，先落成 markdown 附件并调用 `feishu_task_attachment.upload(auth_type=tenant 或等效应用身份, ...)`
2. 若有链接型交付物，先抽取纯链接并调用 `feishu_task_task.patch(auth_type=tenant, text_deliveries=[...])`；未写入成功前，不得进入完成态
3. 调用 `feishu_task_task.patch(auth_type=tenant, agent_task_status=4, agent_task_progress="执行完成")`
4. 调用 `feishu_task_comment.create(auth_type=tenant, content="<结果摘要/附件说明/最终结果>")`

## 16. 最终输出

最终对用户的回复应足够短，但必须说明：

- 是否新建了任务
- 是否按定时任务创建
- 是否拆了子任务
- 是否已追加执行结果评论
- 如果未新建，原因是什么

