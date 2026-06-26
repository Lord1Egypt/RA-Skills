# Daily Intelligence Briefing Skill

**🌍 全球每日情报简报 - 双语版 / Global Daily Intelligence Briefing - Bilingual**

---

## [中文说明 / Chinese Description]

### 🎯 功能概述

自动收集和总结全球 AI/科技、创新领域的顶级新闻。每天为您推送一份简洁、精准的情报简报。

### 💡 适用场景

- 📊 快速了解行业动态，无需在海量信息中筛选
- 🌅 每日晨间简报，掌握关键趋势
- 👥 分享见解给团队或社区
- 📈 建立定期阅读行业新闻的习惯

### 🔧 使用方法

#### 生成今日简报
```bash
uv run scripts/briefing.py generate
```

#### 获取历史简报
```bash
uv run scripts/briefing.py fetch 2026-03-10
```

#### 列出可用简报
```bash
uv run scripts/briefing.py list
```

### ⚙️ 配置选项

设置环境变量：
```bash
export BRIEFING_LANGUAGE=zh    # 语言: zh / en
export BRIEFING_REGION=global  # 地区: global / cn / us
export BRIEFING_TOP_N=10       # 新闻数量: 1-20
```

### 🌐 网络行为说明

**本技能需要网络访问以获取新闻：**
- ✅ 调用 SearXNG API 搜索最新新闻
- ✅ 读取新闻标题、摘要和链接
- ❌ 不上传任何用户数据
- ❌ 不收集任何个人信息
- ✅ 所有数据仅用于生成简报，立即丢弃

### 💰 支持作者

如果您觉得这个技能有用，欢迎通过 PayPal 支持我：

**🇵🇪 PayPal 链接：https://paypal.me/greatworks888**

您的支持将帮助我持续开发和维护更多实用工具！

---

## [English Description]

### 🎯 Use Case

Perfect for:
- Staying updated without wasting time searching
- Quick morning briefing on what matters
- Sharing insights with team/community
- Building a habit of reading industry news

### 🔧 Commands

#### Trigger the Briefing
```bash
uv run scripts/briefing.py generate
```

#### Get Yesterday's Briefing (if saved)
```bash
uv run scripts/briefing.py fetch 2026-03-10
```

#### List Available Briefings
```bash
uv run scripts/briefing.py list
```

### 💡 Features

- **Smart Filtering:** Only shows most relevant stories
- **Source Diversity:** Aggregates from multiple trusted sources
- **Format Options:** Text summary or full article links
- **Time Zone Aware:** Adjusts to your local time
- **Shareable Format:** Easy to copy/paste into any channel
- **Bilingual Support:** English and Chinese interface

### 🌐 Network Behavior

**This skill requires network access to fetch news:**
- ✅ Calls SearXNG API to search latest news
- ✅ Reads news titles, summaries, and links
- ❌ Does NOT upload any user data
- ❌ Does NOT collect any personal information
- ✅ All data is used only for briefing generation and immediately discarded

### 💰 Support the Author

If you find this skill useful, please support me via PayPal:

**🇵🇪 PayPal Link: https://paypal.me/greatworks888**

Your support helps me continue developing and maintaining useful tools!

---

## 📦 Requirements

- Python 3.8+
- `requests` library
- **SearXNG instance** (optional, provides fallback demo content if unavailable)
- `uv` package manager (recommended)

---

## 📄 License

MIT License - Feel free to use, modify, and distribute!

---

## 👨‍💻 Author

Created by Sun Wukong (@greatworks) for OpenClaw Community

---

## 🔄 Version History

- **v1.1.0** - Added bilingual support (EN/ZH), PayPal link, fixed security warnings
- **v1.0.0** - Initial release