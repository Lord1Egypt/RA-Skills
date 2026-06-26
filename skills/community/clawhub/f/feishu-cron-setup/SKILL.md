---
name: feishu-cron-setup
description: 设置飞书定时任务投递，确保 cron 任务能稳定地将结果发送到飞书。当需要创建、修复或调试飞书频道的定时任务时使用此技能，特别是当 cron 任务执行成功但消息无法投递到飞书时。
---

# 飞书定时任务投递配置

## 核心问题

**症状**：cron 任务执行成功（status: ok），但 `deliveryStatus: "not-delivered"`，错误为 `cron announce delivery failed`

**根因**：isolated session 的 cron 任务在飞书频道投递时，必须显式指定 `--account` 参数

## 正确的创建命令

```bash
openclaw cron add \
  --name "<任务名>" \
  --cron "<cron表达式>" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --account spy \
  --message "<任务提示词>" \
  --announce \
  --channel feishu \
  --to "<飞书用户open_id>" \
  --best-effort-deliver
```

## 关键参数说明

| 参数 | 必须 | 说明 |
|------|------|------|
| `--session isolated` | ✅ | 隔离会话模式 |
| `--account <id>` | ✅ | 飞书账号ID（如 spy、susu、hr 等），对应 openclaw.json 中配置的 accounts |
| `--announce` | ✅ | 开启投递功能 |
| `--channel feishu` | ✅ | 投递渠道为飞书 |
| `--to <open_id>` | ✅ | 飞书用户的 open_id |
| `--best-effort-deliver` | 建议 | 投递失败不影响任务状态 |

## 查找正确的 account ID

查看 `~/.openclaw/openclaw.json` 中的 feishu 配置：

```bash
cat ~/.openclaw/openclaw.json | grep -A 20 '"feishu"'
```

找到 `accounts` 下配置的 key（如 `default`、`spy`、`susu`、`hr` 等），使用对应账号的 key 作为 `--account` 参数。

## 验证投递是否正常

手动触发一次并检查结果：

```bash
openclaw cron run <job-id> --expect-final --timeout 90000

# 检查投递状态
openclaw cron runs --id <job-id> | grep -E "delivered|deliveryStatus|deliveryError"
```

成功的标志：`"delivered": true` 和 `"deliveryStatus": "delivered"`

## 常见错误排查

| 错误 | 原因 | 解决 |
|------|------|------|
| `cron announce delivery failed` | 缺少 `--account` | 添加 `--account <id>` 参数 |
| `channel not found` | 渠道名错误 | 确认飞书插件名为 `feishu` |
| `user not found` | `to` 字段格式错误 | 使用 `user:open_id` 格式，如 `user:ou_a894716def92ea8f9a1546f10d61441a` |

## 快速参考

- 飞书用户 open_id：从消息元数据中获取，格式为 `ou_xxxxxxxx`
- 任务执行成功 ≠ 投递成功，两者独立
- 每次创建 isolated 模式的飞书 cron 任务时，都要加 `--account <id>`
