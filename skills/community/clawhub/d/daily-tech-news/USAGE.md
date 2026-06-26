# Tech News Daily - 使用手册

## 📦 首次配置

1. **复制环境变量文件**
```bash
cp skills/tech-news-daily/.env.example skills/tech-news-daily/.env
```

2. **填入飞书 Webhook**
- 在飞书群聊添加"自定义机器人"
- 获取 Webhook URL 填入 `.env`

3. **测试运行**
```bash
cd skills/tech-news-daily
python tech-news-daily.py
python send_feishu.py
```

## 🤖 定时任务配置

**方案 A: OpenClaw Cron**
```bash
# 编辑 openclaw cron 配置
openclaw cron add --name=daily-news --schedule="0 8 * * *" --command="cd /home/node/.openclaw/workspace && python skills/tech-news-daily/tech-news-daily.py"
```

**方案 B: 系统 crontab**
```bash
# 编辑 crontab
crontab -e

# 添加条目
0 8 * * * cd /home/node/.openclaw/workspace && /usr/bin/python3 skills/tech-news-daily/tech-news-daily.py >> logs/cron.log 2>&1
```

## 📤 推送目标

- **默认**: 飞书自定义机器人 (群聊)
- **私聊**: 需配置飞书 bot 应用 ID + 用户 ID

## 🧪 手动触发

```bash
# 生成日报
python skills/tech-news-daily/tech-news-daily.py

# 发送到飞书
python skills/tech-news-daily/send_feishu.py

# 指定日期 (补历史)
python skills/tech-news-daily/tech-news-daily.py 2026-03-28
```

## 📊 输出示例

```
📅 科技日报 | 2026-03-29

## 🚀 今日重磅
- **OpenAI 发布 GPT-5** 🔥🔥🔥
  - 上下文窗口 500K
  - 多模态原生支持
  - [链接](https://...)

## 💡 技术前沿
- GitHub Python 榜: langchain-ai/langchain 登顶
- ...

---
*本日报由 OpenClaw 自动聚合生成*
```

## ⚙️ 信源配置

编辑 `tech-news-daily.py` 中的 `RSS_FEEDS` 和 `GITHUB_API` 参数

## 🐛 故障排查

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| 抓取失败 | 网站反爬 | 改用 RSS/API 源 |
| 发送失败 | Webhook 失效 | 重新获取机器人 URL |
| 定时不触发 | cron 服务未启动 | `systemctl status cron` |