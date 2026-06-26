---
name: cron-model-manager
description: |
  管理 OpenClaw 定时任务：查看、切模型、启用/禁用、手动触发、删除。
  触发词："定时任务"、"cron"、"切换模型"、"查看定时任务"、"定时任务管理"
---

# Cron 定时任务管理器

## 前置检查

用 `exec` 运行 `openclaw cron list`。如果报错：
- `Unrecognized key: "toolCall"` → `exec` 运行 `sed -i '/"toolCall": true/d' ~/.openclaw/openclaw.json` 后重试
- 其他错误 → 告知用户手动修复

## 查看任务

用 `exec` 运行 `openclaw cron list`，直接展示输出表格。如果需要更详细信息，加 `--json` 解析。

## 切换模型

1. 展示当前状态
2. 输出方案：`任务名: 旧模型 → 新模型`
3. 确认后执行：`exec: openclaw cron edit <id> --model <model>`
4. 验证：`exec: openclaw cron list` 确认生效

## 启用/禁用

- 启用：`exec: openclaw cron edit <id> --enable`
- 禁用：`exec: openclaw cron edit <id> --disable`

## 手动触发（测试）

`exec: openclaw cron run <id>`

切模型后建议立刻触发一次验证效果。

## 删除任务

先展示任务详情，用户确认后：
`exec: openclaw cron rm <id>`

## 获取可用模型

`exec: openclaw cron list --json` 中提取已有 model 字段，或直接问用户。

## 注意事项

- model 格式：`provider/model`（如 `custom/mimo-v2.5-pro`）
- 修改立即生效，下次执行使用新模型
- 必须通过 CLI 命令操作，不要直接改 jobs.json
