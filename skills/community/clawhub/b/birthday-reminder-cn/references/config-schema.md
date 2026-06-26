# Birthday Config Schema

## 顶层

- `defaults` (object)：全局默认配置。
- `people` (array)：生日条目列表。

## defaults

- `calendar`：`solar` 或 `lunar`。
- `timezone`：IANA 时区，默认 `Asia/Shanghai`。
- `remind_at`：`HH:MM`。
- `offset_days`：非负整数数组，支持多个提醒点。
- `leap_strategy`：`skip` 或 `use-non-leap`。

## people[]

- `name` (required)
- `month` (required)
- `day` (required)
- `calendar` (optional)
- `timezone` (optional)
- `remind_at` (optional)
- `offset_days` (optional)
- `leap_month` (optional, lunar only)
- `leap_strategy` (optional, lunar only)

## 约束

- 农历转换范围：1900-2099。
- `offset_days` 不能为负数。
- `remind_at` 必须符合 `HH:MM`。
- 阳历 `2/29` 在平年默认顺延到 `3/1`。

## 相关命令

- 检查当前窗口到期提醒：
  - `python3 scripts/birthday_reminder.py check --config <path-to-json>`
- 列出所有已配置提醒（按下一次生日计算）：
  - `python3 scripts/birthday_reminder.py list --config <path-to-json>`
- 通知分发（多通道）：
  - `python3 scripts/notify_bridge.py --birthday-config <birthday-json> --notify-config <notify-json>`

## 定时触发建议

- 推荐：用官方定时任务 skill（Automation）每 10 分钟执行一次 `notify_bridge.py`

## 用户示例请求

- “添加一条农历八月初八的生日，并提前 15 天和当天上午 9 点提醒。”
- “把妻子生日设为阳历 3 月 25 日，默认时区北京，提前 7 天和 1 天提醒。”

## notify.json（通知配置）

建议从 `assets/notify.example.json` 复制。

- 顶层：
  - `message_style`：`warm|simple`，默认 `warm`
  - `channels` (array)
- 每个通道公共字段：
  - `type`：`console|file|webhook|feishu|dingtalk|slack|telegram`
  - `enabled`：`true/false`

按类型的额外字段：

- `file`：`path`
- `webhook`：`url`、可选 `payload_template`
- `feishu`：`webhook`
- `dingtalk`：`webhook`
- `slack`：`webhook`
- `telegram`：`bot_token`、`chat_id`

## 示例：桐桐 + Telegram

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

## 校验建议

- 先跑：`python3 scripts/birthday_reminder.py list --config <path-to-json>`
- 再跑：`python3 scripts/birthday_reminder.py check --config <path-to-json> --output json`

## 问题反馈

- 代码仓库：`https://github.com/905583906/jeff-skills`
- 提交问题（Issues）：`https://github.com/905583906/jeff-skills/issues`
