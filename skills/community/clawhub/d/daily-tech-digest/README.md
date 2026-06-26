# Daily Tech Digest

每日科技热点简报生成器 - 自动收集、整理、推送

## 安装

```bash
# 已内置，无需额外安装
```

## 使用

### 手动触发

```bash
# 生成简报
python scripts/daily_tech_digest.py

# 整理归档
python scripts/daily_news_organizer.py
```

### 定时任务

```bash
# 早上 8:00
openclaw cron add "0 8 * * *" \
  --command "python3 ~/.openclaw/workspace/skills/daily-tech-digest/scripts/daily_tech_digest.py" \
  --channel xiaoyi-channel

# 晚上 8:00
openclaw cron add "0 20 * * *" \
  --command "python3 ~/.openclaw/workspace/skills/daily-tech-digest/scripts/daily_news_organizer.py" \
  --channel xiaoyi-channel
```

## 依赖

- `daily-tech-broadcast` - 新闻数据源
- `today-task` - 负一屏推送
- `obsidian-git-vault` - Git 同步（可选）

## 许可

MIT
