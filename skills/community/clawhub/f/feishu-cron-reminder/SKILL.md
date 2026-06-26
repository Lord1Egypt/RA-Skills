---
name: feishu-cron-reminder
description: 在飞书机器人上创建和管理定时提醒任务。支持一次性提醒和循环提醒，自动发送消息到飞书用户或群组。当用户提到"飞书定时提醒"、"飞书定时任务"、"飞书 cron"、"飞书提醒"时激活。
---

# feishu-cron-reminder：飞书定时提醒

在 OpenClaw 中创建定时任务，自动将提醒消息推送到飞书。

## 前置要求

1. OpenClaw 已配置飞书机器人
2. 飞书机器人已添加到目标用户/群组

## 使用方法

用户只需说「提醒我明天9点开会」，AI 自动解析并创建 cron 任务。

### 支持的提醒类型

| 类型 | 示例 | 说明 |
|------|------|------|
| 一次性 | "提醒我明天9点开会" | 到指定时间发一次 |
| 每日循环 | "每天早上8点提醒我" | 每天固定时间 |
| 工作日循环 | "每个工作日18点提醒下班" | 周一到周五 |
| 每周循环 | "每周一9点提醒周会" | 每周固定星期 |

## 命令模板

### 一次性提醒（at 定时）

```bash
openclaw cron add \
  --name "我的提醒" \
  --at "2026-04-08T09:00:00.000Z" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "直接发送以下文字到飞书，不需要调用任何工具：开会时间到了！" \
  --timeout-seconds 180 \
  --delete-after-run \
  --announce \
  --channel feishu \
  --to user:ou_XXXXXXXXXXXXXXXX \
  --description "一次性提醒示例"
```

### 每日循环提醒

```bash
openclaw cron add \
  --name "每日早提醒" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "直接发送以下文字到飞书，不需要调用任何工具：早安，今天也要加油！" \
  --timeout-seconds 180 \
  --announce \
  --channel feishu \
  --to user:ou_XXXXXXXXXXXXXXXX \
  --description "每日提醒"
```

### 工作日提醒

```bash
openclaw cron add \
  --name "工作日下班提醒" \
  --cron "0 18 * * 1-5" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "直接发送以下文字到飞书，不需要调用任何工具：下班时间到，记得整理桌面！" \
  --timeout-seconds 180 \
  --announce \
  --channel feishu \
  --to user:ou_XXXXXXXXXXXXXXXX \
  --description "工作日下班提醒"
```

### 发送到群组

将 `--to` 参数改为群组 ID：
```bash
--to channel:oc_XXXXXXXXXXXXXXXX
```

## cron 表达式参考

| 表达式 | 含义 |
|--------|------|
| `0 8 * * *` | 每天 08:00 |
| `0 9 * * 1-5` | 工作日 09:00 |
| `30 18 * * 1-5` | 工作日 18:30 |
| `0 9 * * 1` | 每周一 09:00 |
| `0 20 * * *` | 每天 20:00 |

## 关键参数说明

| 参数 | 必须 | 说明 |
|------|------|------|
| `--name` | 是 | 任务名称 |
| `--cron` | 与`--at`二选一 | cron 表达式 |
| `--at` | 与`--cron`二选一 | ISO 绝对时间（UTC） |
| `--tz` | 是 | 写 `Asia/Shanghai` |
| `--session` | 是 | 写 `isolated` |
| `--message` | 是 | 要发送的文字内容 |
| `--timeout-seconds` | 是 | 最小 180，建议 180 |
| `--delete-after-run` | 一次性任务必填 | 完成后自动删除 |
| `--announce` | 是 | 启用结果投递 |
| `--channel feishu` | 是 | 投递到飞书 |
| `--to` | 是 | 目标 ID（见下方） |

## 飞书目标 ID

- **用户 ID**：`user:ou_XXXXXXXXXXXXXXXX`（以 `ou_` 开头）
- **群组 ID**：`channel:oc_XXXXXXXXXXXXXXXX`（以 `oc_` 开头）

获取方法：在飞书开发者后台查看机器人的 openId 或群 ID。

## 时区注意事项

`--at "2026-04-08T09:00:00.000Z"` 是 **UTC 时间**，不是北京时间。

换算：北京时间 = UTC + 8 小时
- 北京时间 09:00 = UTC 01:00 → `--at "2026-04-08T01:00:00.000Z"`

建议：用 `--cron` + `--tz Asia/Shanghai` 代替 `--at`，自动处理时区。

## 常见错误排查

| 症状 | 原因 | 解决方法 |
|------|------|---------|
| 消息没发出去 | `--to` ID 格式错误 | 必须是 `user:ou_` 或 `channel:oc_` 开头 |
| 任务不触发 | `--at` 时间在过去 | 确认时间是未来，用 ISO 绝对时间 |
| 超时无响应 | `--timeout-seconds` 太小 | 设为 180，不要低于 120 |
| 飞书收不到 | 没有飞书机器人 | 确认 OpenClaw 飞书配置正确 |

## 架构说明

本 Skill 调用 OpenClaw 内置的 `openclaw cron` 命令创建定时任务，消息通过 OpenClaw 的 announce 机制投递到飞书频道，不需要额外的 feishu_chat 工具。
