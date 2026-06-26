---
name: feishu-cron-announce
description: 创建定时任务并通过 OpenClaw cron announce 直接推送结果到飞书。当需要设置定时监控任务（如版本发布、天气、股票等）并让结果自动推送到飞书时使用。关键词：飞书定时推送、cron 定时任务、飞书 announce、定时监控、飞书监控通知。
version: 1.0.0
tags: [feishu, cron, announce, monitoring, feishu-cron, notification]
license: MIT
---

# 飞书 Cron Announce 定时推送

## 核心要点

**成功关键**：`--session isolated` + `--announce` + `--channel feishu` + `--to` + `--tz Asia/Shanghai`

## 标准命令模板

```bash
openclaw cron add \
  --name "<任务名>" \
  --cron "<cron表达式>" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "<提示词：让 AI 检查什么并生成简短结论>" \
  --announce \
  --channel feishu \
  --to "<飞书用户 open_id>" \
  --best-effort-deliver
```

## 参数说明

| 参数 | 必须 | 说明 |
|------|------|------|
| `--session isolated` | ✅ | 隔离会话，announce 必须用 isolated |
| `--tz "Asia/Shanghai"` | ✅ | 指定时区，避免 UTC 偏移 |
| `--announce` | ✅ | 开启结果投递 |
| `--channel feishu` | ✅ | 投递渠道为飞书 |
| `--to "<open_id>"` | ✅ | 飞书用户 open_id（格式：`ou_xxx`） |
| `--best-effort-deliver` | 建议 | 投递失败不影响任务状态 |
| `--account default` | ⚠️ | 多账号时必须指定；单账号可不写 |
| `--cron` | ✅ | 标准 cron 表达式（`0 * * * *` = 每小时整点） |

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `deliveryStatus: "not-delivered"` | 多账号未指定 `--account` | 添加 `--account default` |
| `channel not found` | 渠道名错误 | 确认用 `feishu` |
| `user not found` | open_id 格式错误 | 用 `ou_` 开头的用户 ID |

## 验证命令

```bash
# 手动触发
openclaw cron run <job-id>

# 检查结果
openclaw cron runs --id <job-id>

# 成功标志
"delivered": true
"deliveryStatus": "delivered"
```

## 快速参考

- 飞书 open_id：从消息元数据获取，格式 `ou_xxx`
- cron 表达式：`0 * * * *` 每小时整点，`0 9 * * *` 每天 9 点
- 任务执行成功 ≠ 投递成功，两者独立
