---
name: cron-limited
description: 创建支持有限次数重复的定时任务，自动在第N次执行后清理自身。支持农历生日提醒，农历日期自动转阳历后每年自动重复。当用户需要「每X分钟执行一次，执行N次后自动停止」或「农历生日每年提醒，提前N天提醒」时使用。
---

# cron-limited: 有限次数重复任务 + 农历生日提醒

## 重要：处理每日自动检查

当收到消息「CRON-LIMITED-DAILY-CHECK」时（由每日cron任务触发），必须执行以下步骤：

1. 读取 `~/.openclaw/cron-limited/birthdays.json` 配置
2. 获取今天日期（上海时区）
3. 对比配置中每个生日的提醒日期（生日日期 - 提前天数）
4. 如果今天匹配任何提醒日期，使用以下命令发送提醒：

```bash
openclaw agent --message "<提醒消息>" --deliver --channel <channel> --to <to>
```

**JSON配置格式：**
```json
[
  {
    "lunar_month": 8,
    "lunar_day": 15,
    "message": "生日快乐！",
    "time": "10:00",
    "days_before": 3,
    "channel": "openclaw-weixin",
    "to": "o9cq807t3Jl4ow-J7evcB-2LeEzc@im.wechat"
  }
]
```

**提醒消息格式：**
- 提前N天：`📅 提醒：农历{月}月{日}日是 {生日阳历日期}，还有 {N} 天！\n{自定义消息}`
- 当天：`🎂 今天是农历{月}月{日}日！\n{自定义消息}`

---

## 模式1: 有限次数重复任务

```bash
openclaw cron-limited add \
  --every <duration> \
  --repeat <count> \
  --message "<text>" \
  [--channel <channel>] \
  [--to <destination>]
```

**参数说明：**

| 参数 | 必须 | 说明 |
|------|------|------|
| `--every` | 是 | 重复间隔，如 `5m`、`1h`、`30s` |
| `--repeat` | 是 | 重复次数，执行N次后自动删除 |
| `--message` | 是 | 发送的消息内容 |
| `--channel` | 否 | 渠道，默认 `openclaw-weixin` |
| `--to` | 否 | 投递目标，默认使用当前会话的目标 |

**示例：**

```bash
# 每5分钟提醒喝水，共3次
openclaw cron-limited add --every 5m --repeat 3 --message "记得喝水! 💧" \
  --channel openclaw-weixin --to "o9cq807t3Jl4ow-J7evcB-2LeEzc@im.wechat"
```

---

## 模式2: 农历生日提醒

```bash
openclaw cron-limited add-lunar \
  --lunar <月份-日期> \
  --message "<text>" \
  [--time <HH:MM>] \
  [--days-before <N>] \
  [--yearly] \
  [--channel <channel>] \
  [--to <destination>]
```

**参数说明：**

| 参数 | 必须 | 说明 |
|------|------|------|
| `--lunar` | 是 | 农历月-日，如 `8-15` 表示农历8月15 |
| `--message` | 是 | 发送的消息内容 |
| `--time` | 否 | 提醒时间，默认 `08:00` |
| `--days-before` | 否 | 提前N天提醒，默认 0（当天） |
| `--yearly` | 否 | 是否每年重复，默认 false |
| `--channel` | 否 | 渠道，默认 `openclaw-weixin` |
| `--to` | 否 | 投递目标，默认使用当前会话的目标 |

**示例：**

```bash
# 农历8月15生日提醒（当天早上10点）
openclaw cron-limited add-lunar --lunar 8-15 \
  --message "🎂 生日快乐！" \
  --time 10:00 \
  --channel openclaw-weixin --to "o9cq807t3Jl4ow-J7evcB-2LeEzc@im.wechat"

# 农历8月15，提前3天提醒
openclaw cron-limited add-lunar --lunar 8-15 \
  --message "🎂 记得准备好庆祝！" \
  --time 09:00 \
  --days-before 3 \
  --yearly \
  --channel openclaw-weixin --to "o9cq807t3Jl4ow-J7evcB-2LeEzc@im.wechat"

# 春节提醒（农历正月初一）
openclaw cron-limited add-lunar --lunar 1-1 \
  --message "🧧 春节快乐！新的一年开始了！" \
  --time 08:00 \
  --yearly \
  --channel openclaw-weixin --to "o9cq807t3Jl4ow-J7evcB-2LeEzc@im.wechat"
```

---

## 工作原理

### 有限次数重复
1. 创建主任务（循环任务）
2. 根据 `--every` 和 `--repeat` 计算第N次的执行时间
3. 在第N次执行时间 + 1分钟 创建「删除主任务」的一次性任务
4. 主任务执行第N次后，下一分钟自动被删除

### 农历生日提醒（每年模式）
1. 将农历日期转换为当年对应的阳历日期
2. 保存配置到 `~/.openclaw/cron-limited/birthdays.json`
3. 创建每日检查cron任务（早上7点）
4. 每日检查任务触发时，agent读取配置并发送当日所有提醒

---

## 依赖

- Python 3 + lunarcalendar 库
- openclaw CLI
- jq
