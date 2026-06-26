---
name: daily-brief
description: Daily Brief - 每日简报 - 整合天气和热门新闻，一键获取每日资讯！
homepage: https://github.com/yourusername/daily-brief
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":["curl"]}}
---

# Daily Brief 每日简报

一键获取每日天气和热门新闻，省时又实用！

## Features
- 🌤️ 实时天气查询（免API key）
- 📰 热门新闻聚合
- 📋 一键生成精美简报
- 🌍 支持多个城市

## Quick Start

```bash
# 获取默认城市（上海）的天气和新闻
daily-brief

# 指定城市
daily-brief Beijing

# 仅天气
daily-brief --weather-only

# 仅新闻
daily-brief --news-only
```

## Weather

使用wttr.in，免费免key！

```bash
curl -s "wttr.in/Shanghai?format=3"
```

## News

使用免费新闻源，无需API key！

```bash
# 可以扩展更多新闻源
```

## Output Format

```
📅 2026-03-16 每日简报

🌤️ 天气: 上海: ⛅️ +18°C

📰 热门新闻:
1. 新闻标题1
2. 新闻标题2
3. 新闻标题3

💡 今日提示: 记得带伞！
```

## Customization

编辑 `~/.daily-brief/config.json` 来配置默认城市和新闻源。

---

Made with ❤️ for OpenClaw
