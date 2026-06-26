# GitHub Trending 每日推送

🔥 自动获取 GitHub Trending 热门项目，推送到你的通知渠道。

## 特点

- ✅ 零成本运行
- ✅ 支持多语言过滤
- ✅ 支持多种推送渠道（Telegram、钉钉、企业微信）
- ✅ 可设置 Cron 定时任务
- ✅ 纯 Python 实现，无需额外依赖

## 安装

```bash
# 克隆或下载项目
git clone https://github.com/your-username/github-trending-daily.git
cd github-trending-daily

# 运行
python3 trending.py
```

## 使用方法

### 基本使用

```bash
# 获取今日热门项目
python3 trending.py

# 只看 Python 项目
python3 trending.py --language python

# 获取本周热门
python3 trending.py --since weekly
```

### 推送到 Telegram

```bash
python3 trending.py --telegram --token YOUR_BOT_TOKEN --chat_id YOUR_CHAT_ID
```

### 推送到钉钉

```bash
python3 trending.py --dingtalk --webhook YOUR_WEBHOOK_URL
```

### 推送到企业微信

```bash
python3 trending.py --wecom --webhook YOUR_WEBHOOK_URL
```

## 定时任务

设置每天早上 9 点自动推送：

```bash
# 编辑 crontab
crontab -e

# 添加一行
0 9 * * * python3 /path/to/github-trending-daily/trending.py --telegram --token xxx --chat_id xxx
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--language` | 编程语言过滤（python, javascript, go 等） |
| `--since` | 时间范围（daily, weekly, monthly） |
| `--telegram` | 推送到 Telegram |
| `--dingtalk` | 推送到钉钉 |
| `--wecom` | 推送到企业微信 |
| `--token` | Telegram Bot Token |
| `--chat_id` | Telegram Chat ID |
| `--webhook` | 钉钉/企业微信 Webhook URL |
| `--output` | 输出格式（text, json） |

## 收入模式

这个工具可以作为：

1. **ClawHub 技能** - 上架免费分享，建立影响力
2. **定制服务** - 为企业定制内部推送工具
3. **GitHub Sponsors** - 接受赞助

## 许可证

MIT License - 自由使用、修改、分发

---

Made with ❤️ by 9527
