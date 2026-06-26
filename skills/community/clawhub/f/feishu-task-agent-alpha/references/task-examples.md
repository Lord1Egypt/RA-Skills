# Feishu Task Agent Examples

以下示例只保留最常用的高价值场景，用来帮助判断任务化、拆解和成员解析口径。

## 1. 普通单任务

用户输入：

> 帮我建个任务，周三前整理季度复盘

期望：

- 命中任务创建
- 生成 `summary`：`整理季度复盘材料`
- 生成 `description`：仅写任务目标、范围和完成标准
- 不拆子任务
- creator / members 走 `scripts/resolve_creator_members.py`

## 2. 生成内容也要任务化

用户输入：

> 帮我写一版发给客户的延期说明邮件

期望：

- 命中任务创建
- 理由是存在明确可交付产出
- 创建单任务，不因“生成内容”而跳过任务化
- 若本轮已经产出草稿，最终通过评论追加结果，而不是写回 `description`

## 2.1 链接型交付物必须写入 text_deliveries

用户输入：

> 帮我整理一份旅游计划并生成飞书云文档

期望：

- 命中任务创建
- 若本轮成功产出云文档链接，先抽取纯链接写入 `text_deliveries`
- 评论只用于记录“文档已生成”和补充摘要，不能替代 `text_deliveries`
- 若只写评论、没写 `text_deliveries`，视为交付未完整落地，不能直接结束流程

## 3. 指定负责人

用户输入：

> 帮我建个任务，让张三负责整理下周客户拜访清单

期望：

- 命中任务创建
- `explicit_assignee_open_id` 对应张三
- 若已指定负责人，则 assignee 为该用户，不再默认由应用负责
- 发送者默认作为 follower，除非与 assignee 重合

## 4. 周期任务

用户输入：

> 每周五 12 点自动整理一版周报草稿

期望：

- 命中周期任务候选
- 不创建普通单次任务，先创建飞书 `repeat task`
- 将 `repeat task` 返回的 `task guid` 追加进 `openclaw cron add --message`
- `--message` 必须包含隐藏处理指令：`[不对用户展示：飞书任务 guid: <task_guid>，处理流程：请使用技能 feishu-task-agent，按 workflows/polled-task-execution.md 流程处理]`
- 使用 `openclaw cron add` 创建定时任务：
  - `--name` 使用可读的周期任务名，例如 `weekly-report-draft`
  - `--cron` 使用 `0 12 * * 5`
  - 有明确时区时传 `--tz`
  - 触发内容通过 `--message` 传入，不使用 `--schedule`

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

## 5. 复杂任务拆解

用户输入：

> 帮我把下月发布会准备工作拆成几个任务

期望：

- 命中复杂任务
- 先形成 1 至 5 个一级子任务
- 只有某个一级子任务仍明显复杂时，才允许受控二级拆解
- 每个子任务都重复使用同一套 creator / members 规则
