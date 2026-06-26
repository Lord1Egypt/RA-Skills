# 定时任务配置

## 首次设置流程

用户首次使用时，引导设置学习计划：

1. 询问用户名称
2. 询问每日学习时间（支持多个时间点）
3. 询问每次学习单词数量
4. 写入 `user_schedule.csv`
5. 设置 crontab 定时任务

## 定时任务示例

```bash
# 每天早上 8:00 提醒
0 8 * * * /root/.openclaw/scripts/cet4-reminder.sh

# 每天晚上 21:00 提醒
0 21 * * * /root/.openclaw/scripts/cet4-reminder.sh
```

## 提醒脚本模板

```bash
#!/bin/bash
# CET-4 单词记忆提醒脚本

/root/.local/share/pnpm/openclaw \
  message send \
  --account default \
  --target <user_id> \
  --message "🦆 同学你好！是时候背单词啦！

每天 5 个单词，坚持就是胜利！💪"
```

## 检查现有定时任务

设置前检查用户是否已有定时任务：

```bash
crontab -l | grep cet4
```

如果没有，则添加；如果有，确认时间是否与用户设置一致。