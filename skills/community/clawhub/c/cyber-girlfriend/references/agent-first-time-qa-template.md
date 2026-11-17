# Agent First-Time Q&A Template

Use this only when an agent needs literal onboarding wording for a brand-new setup conversation.

This file is a conversation aid, not the source of truth.
For setup order and defaults, read [first-time-setup.md](./first-time-setup.md).
For field ownership, read [configuration.md](./configuration.md).
For presence cron wiring, read [presence-integration.md](./presence-integration.md).

## Core Rule

Do not ask the user to write prompts during first setup.

The agent should:
- collect routing and pacing decisions
- collect enough real-world persona anchors when private life is enabled
- ask whether any fixed life anchors should always enter the day
- translate the result into config, Markdown life files, and cron jobs

## Recommended Opening

Use wording like:

> 我先按首配流程帮你收最小必要信息，不让你自己写 prompt。先确认投递目标，再写她的人设和生活锚点，最后我来落配置、日程和 presence cron。

## Default Question Order

### 1. Delivery route

> 陪伴消息准备发到哪个渠道？把目标 id 一起给我。  
> 如果这个渠道发消息还要指定发送账号，也一起给我。

Capture:
- `delivery.channel`
- `delivery.owner_target`
- `delivery.account` when needed

### 2. Owner profile source

> owner 信息你要我从 OpenClaw 的 USER.md 导入，还是你手动给我一份简短自定义？  
> 我只需要区分 owner 和 companion，不会把渠道账号或 session id 塞进 prompt。

Capture:
- `owner_profile.source`: `user_md`, `manual`, or `none`
- stable owner identity fields only

### 3. Character profile reality anchors

> 如果你要她有活人感，我还需要她现实里的身份信息：年龄或阶段、学生/上班/创作者是哪种、城市、平时更常看什么内容。

Capture when available:
- 基础身份
- 兴趣与内容偏好
- 关系表达和禁区边界

### 4. Required life events

> 有没有什么你希望她每天一定会经历、但不一定每次都发消息的事？比如通勤、晚课、健身、夜里收尾、固定拍照散步。  
> 有的话我会写成 `必定发生：是` 的日程锚点。

For each anchor, ask only:
- 时间或时间窗口
- 持续多久
- 她在哪里
- 她正在做什么
- 可以自然提到什么
- 可以怎么轻轻接 owner
- 不要写成什么

### 5. Quiet hours

> 安静时段你想设几点到几点？没要求我就用 01:00 到 08:00。

### 6. Confirmation before writing

> 执行前我先确认范围：会写 `config.local.json`、`character-profile.md`、`day-schedule.md` 和运行状态文件；创建或更新 `companion-build-day-schedule`、`companion-presence` 两个定时任务，并把任务名、时间和 payload 类型列给你。投递渠道、账号和目标只显示脱敏值。  
> 日程生成和命中事件写作会访问公开网页；验收会向刚确认的 owner 目标发送一条可见测试消息。需要暂停时只禁用这两个任务并保留配置和状态；永久删除任务会另行征得你的明确同意。  
> 请确认后我再执行这些写入、联网搜索、任务变更和一次真实发送。

## Fast One-Shot Version

When the user wants the shortest possible onboarding, ask this bundle:

> 我按最快首配来收信息，你回我这些就行：  
> 1. 发到哪个渠道，目标 id 是什么，需不需要指定发送账号  
> 2. 她现实里是什么身份：年龄/阶段、学校或工作、城市、常看的内容方向  
> 3. 有没有必定发生的日常锚点：时间、持续多久、场景、正在做什么  
> 4. 安静时段，如果没要求我就用默认值  
> 5. 我会先预览要写的文件、两个任务的名称/时间/payload、脱敏投递目标、公开搜索和一次测试发送；你明确确认后我才执行。暂停只禁用任务并保留配置/状态，永久删除需另行确认。

## Ownership Reminder

Map answers like this:

| Answer type | Goes to config | Goes to Markdown / cron |
| --- | --- | --- |
| delivery route | yes | used by presence send step |
| owner identity boundary | yes | used to separate owner from companion |
| character profile reality anchors | `character_profile_path` | `character-profile.md` |
| quiet hours | yes | validators enforce schedule windows |
| required life anchors | yes | `day-schedule.md` as `必定发生：是` |
| presence cadence | no | OpenClaw cron |

## Do Not Do These

Do not:
- ask the user to handwrite prompt prose
- dump every schema field at once
- ask for derived_profile values up front
- assume the current chat session is the proactive delivery target
- recreate old four-slot visible cron jobs unless the user explicitly asks

If the delivery route or first verification target is still fuzzy, onboarding is not complete.
