# dws 产品命令摘要

所有命令都必须追加 `--format json`，并从返回结果中提取真实 ID。

## calendar

- 查询日程：`dws calendar event list --start <ISO-8601> --end <ISO-8601> --format json`
- 查询个人日程：`dws calendar event list-mine --start <ISO-8601> --end <ISO-8601> --format json`

注意：当前命令摘要未确认 `--keyword` 参数。按客户名筛选时，先按时间范围查询，再在 JSON 结果中筛选标题/摘要。

## todo

- 查询待办：`dws todo task list --page 1 --size 50 --format json`
- 查询未完成待办：`dws todo task list --status false --format json`
- 创建待办：`dws todo task create --title "<标题>" --executors "<userId列表>" --due <ISO-8601> --priority 20 --format json`
- 查询详情：`dws todo task get --task-id <taskId> --format json`

注意：当前命令摘要未确认 `--keyword` 参数。按客户名筛选时，先查询待办列表，再在 JSON 结果中筛选标题/摘要。

待办注意事项：

- 默认创建给当前用户。
- 如需指派给他人，必须让用户选择联系人或授权查询联系人，禁止要求用户手填 userId。
- 优先级取值：`10` 低、`20` 普通、`30` 较高、`40` 紧急。文本写“高优先级”时不要使用 `10`。
- `--executors` 是必填参数。默认当前用户时，命令示例写 `--executors "<系统从授权上下文解析的当前用户userId>"`。

## doc

- 搜索文档：`dws doc search --keyword "<关键词>" --format json`
- 读取文档：`dws doc read --node <nodeId或URL> --format json`
- 创建文档：`dws doc create --name "<标题>" --markdown "<Markdown正文>" --format json`
- 更新文档：`dws doc update --node <nodeId或URL> --markdown "<Markdown正文>" --mode append --format json`

文档注意事项：

- `dws doc create --name` 已经设置一级标题，正文不要再以 `#` 开头。
- Markdown 参数中的换行必须是真实换行符。
- 默认使用 `append`，除非用户明确要求覆盖。
- 搜索无结果时，换用更宽泛关键词重试。

## aitable

- 查询记录：`dws aitable record query --base-id <baseId> --table-id <tableId> --format json`
- 关键词查询：`dws aitable record query --base-id <baseId> --table-id <tableId> --keyword "<关键词>" --format json`
- 新增记录：`dws aitable record create --base-id <baseId> --table-id <tableId> --records '<JSON数组>' --format json`
- 更新记录：`dws aitable record update --base-id <baseId> --table-id <tableId> --records '<JSON数组>' --format json`

AI 表格注意事项：

- `baseId`、`tableId`、`recordId` 必须来自用户提供或上游查询结果。
- 单次新增或更新最多 100 条记录。
- 不要写“从授权上下文解析 baseId/tableId”。如果用户没有指定目标 AI 表格，应先询问或跳过写表动作。

## oa

- 查询待我处理审批：`dws oa approval list-pending --start <ISO-8601> --end <ISO-8601> --format json`
- 查询我发起的审批：`dws oa approval list-initiated --start <ISO-8601> --end <ISO-8601> --format json`
- 查询审批详情：`dws oa approval detail --instance-id <instanceId> --format json`
- 查询审批操作记录：`dws oa approval records --instance-id <instanceId> --format json`

## chat

- 拉取群消息：`dws chat message list --group <openconversation_id> --time "<yyyy-MM-dd HH:mm:ss>" --limit 100 --format json`
- 拉取单聊消息：`dws chat message list --user <userId> --time "<yyyy-MM-dd HH:mm:ss>" --limit 100 --format json`

群消息注意事项：

- dws 只负责拉取消息，摘要、待办提取、口径归纳由 AI 二次处理完成。
- 群 ID 或用户 ID 必须来自真实上下文或用户提供。
- 催办消息只能先生成草稿；发送前必须展示收件人、消息内容和发送原因，并等待用户二次确认。
