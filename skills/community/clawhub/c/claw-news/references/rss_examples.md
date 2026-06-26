# Newsman Skill - 使用示例

## 快速开始

### 1. 手动运行

```bash
# 获取最新科技新闻
python scripts/fetch_news.py --category tech --max-items 5 --output tech_news.json

# 生成摘要
python scripts/summarize.py --input tech_news.json --output tech_summaries.json

# 创建 Markdown 简报
python scripts/digest.py --input tech_summaries.json --format markdown --output tech_digest.md
```

### 2. 在 OpenClaw 中使用

```
获取今天的科技新闻
生成一个科技新闻简报
搜索关于 AI 的新闻
```

### 3. 设置定时简报 (Cron)

```bash
# 每天早上 8 点发送科技简报
openclaw cron add \
  --name "morning-tech-digest" \
  --schedule "0 8 * * *" \
  --command "python skills/newsman/scripts/fetch_news.py --category tech --max-items 10 | python skills/newsman/scripts/summarize.py | python skills/newsman/scripts/digest.py --format slack"

# 每 4 小时获取财经新闻
openclaw cron add \
  --name "finance-updates" \
  --schedule "0 */4 * * *" \
  --command "python skills/newsman/scripts/fetch_news.py --category finance --hours 4"
```

## 输出格式

### Markdown (默认)
适合阅读、邮件、文档

### JSON
适合程序处理、API 响应

### Slack
适合发送到 Slack 频道

### Plain Text
适合短信、命令行显示

## 添加自定义新闻源

编辑 `references/sources.md`，添加新的 RSS 源：

```yaml
- name: my-custom-source
  url: https://example.com/feed.xml
  category: tech
  language: en
```

## 集成到消息推送

```python
# 示例：获取新闻并通过 Slack 发送
import subprocess
import json

# Fetch news
result = subprocess.run(
    ['python', 'scripts/fetch_news.py', '--category', 'tech', '--max-items', '5'],
    capture_output=True, text=True
)
news = json.loads(result.stdout)

# Generate digest digest_result = subprocess.run(     ['python', 'scripts/digest.py', '--format', 'slack'],
    input=result.stdout, capture_output=True, text=True
)

# Send via OpenClaw message tool
# (use message tool to send to Slack/Telegram/Discord)
```

---

**文件位置**: `skills/newsman/`
**打包文件**: `skills/newsman.skill`
