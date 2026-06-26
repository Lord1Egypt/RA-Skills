---
name: daily-news-push
description: 自包含的每日热点订阅推送技能。用于创建、查询、修改、取消固定时间自动发送的新闻简报订阅，适合“每天中午12点推送国际科技和国际军事”“工作日早上8点推送今日热点”这类场景。不用于一次性临时查新闻。内置时区管理、中文时间解析、订阅状态存储与 OpenClaw cron 调度，QQ 用户首次创建前需先设置时区。
---

# Daily News Push

用于“每天定时推送新闻/热点简报”的场景。

这个技能现在是自包含版本。

它内部已经包含：
- 新闻订阅管理逻辑
- 时区存储逻辑
- 中文时间解析逻辑
- OpenClaw cron 创建、查询、修改、删除逻辑
- 定时触发后的新闻简报投递逻辑

## 适用场景

当用户表达以下意图时使用：
- 每天给我推送热点
- 每天中午 12 点发科技和军事新闻
- 订阅国际科技新闻
- 定时推送今日热点
- 每天固定时间给我一份新闻简报
- 帮我做新闻订阅
- 把我的新闻订阅改到晚上 8 点
- 取消我的每日新闻推送

## 不适用场景

以下情况不要优先走这个 skill：
- 用户只是想“现在看一下今天新闻”
- 用户只要一次性新闻汇总，不需要订阅
- 用户要中文互联网热搜/舆情，而不是固定订阅式简报

这些情况更适合直接走普通新闻聚合流程，而不是创建订阅。

## 强制规则

1. 不要口头答应“以后每天给你发”，必须创建真实 cron 任务。
2. 第一次创建订阅时，必须要求用户明确指定推送时间。
3. 如果是 QQ 用户，首次创建前还必须确保已设置时区。若未设置，先要求时区。
4. 默认输出为简洁新闻简报，不要生成过长长文。
5. 优先覆盖用户指定主题；如果用户没限定主题，可默认给出“国际科技 + 国际军事”。

## 默认订阅模型

若用户没有额外说明，默认订阅内容：
- 国际科技
- 国际军事

可选主题示例：
- 国际科技
- 国际军事
- 国内科技
- 国内军事
- 综合热点
- 社会热点

## 自包含说明

当前 `daily-news-push` 不再依赖其他 skill 的脚本文件。

即使下面这些 skill 不存在，它也应当能正常工作：
- `news-aggregator`
- `qqbot-remind-absolute`

它只依赖运行时本身提供的 OpenClaw 能力，例如：
- `openclaw cron`
- 触发后的代理执行能力
- 抓新闻时可用的网页访问工具

## 首次创建流程

### 第一步，确认推送时间

如果用户只说“每天推送”但没有具体时间，先追问。

示例追问：
- `你想让我每天几点推送？例如每天中午12点。`
- `先说清楚推送时间，比如 08:00、12:00、20:30。`

### 第二步，若当前是 QQ 通道，确认时区

如果是 QQ 用户，先检查时区：
- `python scripts/manage_daily_news.py get-timezone --to "<qq-target>"`

若结果为空，不要创建订阅，先让用户明确提供时区，例如：
- `Asia/Shanghai`
- `Asia/Tokyo`
- `America/Los_Angeles`

设置时区：
- `python scripts/manage_daily_news.py set-timezone --to "<qq-target>" --timezone "Asia/Shanghai"`

### 第三步，创建订阅

使用脚本创建每日推送任务：
- `python scripts/manage_daily_news.py add --to "<qq-target>" --time "每天中午12点" --topics "国际科技,国际军事"`

也可以指定其他时间：
- `python scripts/manage_daily_news.py add --to "<qq-target>" --time "每天早上8点" --topics "国际科技"`
- `python scripts/manage_daily_news.py add --to "<qq-target>" --time "工作日晚上7点" --topics "国际军事,综合热点"`
- `python scripts/manage_daily_news.py add --to "<qq-target>" --time "5分钟后" --topics "今日新闻"`
- `python scripts/manage_daily_news.py add --to "<qq-target>" --time "一小时后" --topics "国际科技"`

这个脚本现在会直接创建真正的 OpenClaw cron 任务，而不是只保存本地记录。
定时任务触发后，会要求代理当场抓取当天新闻并把最终简报投递到 QQ。

## 查询与取消

### 查询当前新闻订阅

- `python scripts/manage_daily_news.py list --to "<qq-target>"`

### 修改新闻订阅

- 只改时间：`python scripts/manage_daily_news.py update --id "<job-id>" --time "每天晚上8点"`
- 只改主题：`python scripts/manage_daily_news.py update --id "<job-id>" --topics "国际科技,综合热点"`
- 同时改时间和主题：`python scripts/manage_daily_news.py update --id "<job-id>" --time "工作日早上8点" --topics "国际军事,国际科技"`

### 测试推送链路

- 默认 5 分钟后发一条测试新闻：`python scripts/manage_daily_news.py test --to "<qq-target>" --topics "今日新闻"`
- 指定测试时间：`python scripts/manage_daily_news.py test --to "<qq-target>" --time "10分钟后" --topics "国际科技"`

### 取消新闻订阅

- `python scripts/manage_daily_news.py remove --id "<job-id>"`

## 推送内容生成规则

定时任务触发后，生成一份当天简报。内容要求：

1. 先抓取当天热点，再筛选与用户订阅主题匹配的内容。
2. 优先使用较可靠来源。
3. 去重，避免同一条新闻重复表述。
4. 每个主题给 2 到 4 条即可。
5. 每条包含：
   - 标题
   - 来源
   - 一句话要点
6. 总长度保持简洁，适合消息推送阅读。

建议输出结构：

```markdown
今日热点简报

## 国际科技
1. 标题
   来源：xxx
   要点：xxx

## 国际军事
1. 标题
   来源：xxx
   要点：xxx
```

## cron 任务内容要求

创建 cron 时，任务消息要直接告诉运行中的代理：
- 今天要生成“每日新闻简报”
- 订阅主题是什么
- 输出要简洁
- 直接投递到 QQ
- 在触发当刻重新抓取当天新闻，不要复用创建订阅当天的旧内容

## 回复风格

保持简短直接。

示例：
- `先告诉我你想每天几点收到，例如每天中午12点。`
- `还需要你的时区，例如 Asia/Shanghai，我再给你建每日推送。`
- `好，我会每天中午12点给你推送国际科技和国际军事热点。`
- `📋 这是你当前的新闻订阅列表。`
- `✅ 已帮你更新这个新闻订阅。`
- `✅ 已帮你取消这个新闻订阅。`

## 备注

- 这个技能现在已经负责“订阅、查询、修改、取消、调度”，并创建真实 cron 任务。
- 真正的新闻内容在任务触发时再现抓，不要在创建订阅时把当天新闻固化进任务。
- 订阅元数据会保存到 `data/subscriptions.json`，时区数据会保存到 `data/user_timezones.json`。
- 若以后要扩展到非 QQ 通道，可复用同样脚本思路，但当前优先面向 QQ 推送。