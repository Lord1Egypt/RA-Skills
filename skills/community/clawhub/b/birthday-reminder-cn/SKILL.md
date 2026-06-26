---
name: birthday-reminder
description: 管理并计算生日提醒（阳历与农历），支持每条记录单独配置和全局默认值，支持当天提醒/提前 N 天/多次提醒和提醒时间配置，默认使用北京时间。用于需要生成或维护生日提醒方案、编写配置文件、验证提醒是否到期，并结合官方定时任务技能自动触发通知发送。
---

# Birthday Reminder

## 5分钟上手

### 1) 先决条件

- 已安装本技能。
- 环境可执行 `python3`（建议 3.9+）。
- 已准备官方定时任务 skill（Automation）。
- 已准备通知通道凭据（如 Telegram 的 `bot_token` 和 `chat_id`）。

### 2) 准备 `birthdays.json`

复制下面模板并按需修改：

```json
{
  "defaults": {
    "calendar": "solar",
    "timezone": "Asia/Shanghai",
    "remind_at": "09:00",
    "offset_days": [7, 1, 0],
    "leap_strategy": "skip"
  },
  "people": [
    {
      "name": "妻子",
      "calendar": "solar",
      "month": 3,
      "day": 25
    },
    {
      "name": "父母",
      "calendar": "lunar",
      "month": 8,
      "day": 8,
      "offset_days": [15, 3, 0]
    }
  ]
}
```

关键字段：

- `defaults`：全局默认值。
- `people`：生日记录列表；每一条可覆盖任意默认字段。
- `calendar`：`solar` 或 `lunar`。
- `month/day`：生日月日。
- `offset_days`：提醒提前天数数组，`0` 表示当天提醒。
- `remind_at`：提醒时间，格式 `HH:MM`。
- `timezone`：IANA 时区名，默认 `Asia/Shanghai`。
- `leap_month`：仅农历使用，是否闰月生日。
- `leap_strategy`：闰月缺失年份处理策略。
- `skip`：该年跳过。
- `use-non-leap`：该年改用同月非闰月。

### 3) 准备 `notify.json`

建议从 `assets/notify.example.json` 复制后修改。常见 Telegram 配置：

```json
{
  "message_style": "warm",
  "channels": [
    {
      "type": "telegram",
      "enabled": true,
      "bot_token": "你的_bot_token",
      "chat_id": "你的_chat_id"
    }
  ]
}
```

支持的通知类型：

- `console`
- `file`
- `webhook`
- `feishu`
- `dingtalk`
- `slack`
- `telegram`

### 4) 三步检查（推荐顺序）

先看会生成哪些提醒：

```bash
python3 scripts/birthday_reminder.py list --config /绝对路径/birthdays.json
```

再查当前是否有到期提醒：

```bash
python3 scripts/birthday_reminder.py check --config /绝对路径/birthdays.json --output json
```

最后预览发送内容（不真实发送）：

```bash
python3 scripts/notify_bridge.py \
  --birthday-config /绝对路径/birthdays.json \
  --notify-config /绝对路径/notify.json \
  --dry-run
```

时间模拟（推荐格式 `yyyy-MM-DD HH:mm:ss`）：

```bash
python3 scripts/notify_bridge.py \
  --birthday-config /绝对路径/birthdays.json \
  --notify-config /绝对路径/notify.json \
  --now "2026-03-18 19:00:00"
```

### 5) 自动运行（官方定时任务 skill）

在官方定时任务 skill（Automation）里定时执行：

```bash
python3 scripts/notify_bridge.py \
  --birthday-config /绝对路径/birthdays.json \
  --notify-config /绝对路径/notify.json
```

- 推荐频率：每 10 分钟。
- 推荐时区：`Asia/Shanghai`。

## 用户示例请求

- “添加一条农历八月初八的生日，并提前 15 天和当天上午 9 点提醒。”
- “把妻子生日设为阳历 3 月 25 日，默认时区北京，提前 7 天和 1 天提醒。”

### 示例：桐桐（阳历 3/18 晚上 19:00，Telegram 提醒）

`birthdays.json`：

```json
{
  "defaults": {
    "calendar": "solar",
    "timezone": "Asia/Shanghai",
    "remind_at": "09:00",
    "offset_days": [0],
    "leap_strategy": "skip"
  },
  "people": [
    {
      "name": "桐桐",
      "calendar": "solar",
      "month": 3,
      "day": 18,
      "remind_at": "19:00",
      "offset_days": [0]
    }
  ]
}
```

`notify.json`：

```json
{
  "channels": [
    {
      "type": "telegram",
      "enabled": true,
      "bot_token": "你的_bot_token",
      "chat_id": "你的_chat_id"
    }
  ]
}
```

测试发送：

```bash
python3 scripts/notify_bridge.py \
  --birthday-config /绝对路径/birthdays.json \
  --notify-config /绝对路径/notify.json \
  --now "2026-03-18 19:00:00"
```

## 常见问题

- 配置了但没收到提醒：
  - 通常是官方定时任务 skill 没触发到 `notify_bridge.py`。
- `--now` 怎么写：
  - 推荐 `yyyy-MM-DD HH:mm:ss`，例如 `2026-03-25 09:00:00`。
- 只执行了 `check` 为什么没发消息：
  - `check` 只检查；真正发送需要执行 `notify_bridge.py`。

## 问题反馈

- 代码仓库：`https://github.com/905583906/jeff-skills`
- 提交问题（Issues）：`https://github.com/905583906/jeff-skills/issues`

遇到问题时，建议在 Issue 里附上：

- 你的配置片段（隐藏敏感信息）
- 执行命令
- 报错信息或截图
