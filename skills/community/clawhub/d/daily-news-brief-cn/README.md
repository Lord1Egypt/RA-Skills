# 每日新闻简报 📰

> 自动抓取当日热点新闻，AI 提炼重点，定时推送到你的聊天软件

## ✨ 功能特点

- 📰 **多源抓取**: 知乎/微博/财经网站/科技媒体
- 🤖 **AI 提炼**: 智能总结重点，不是简单聚合
- ⏰ **定时推送**: 早 8 点/晚 8 点，可自定义
- 🎯 **行业定制**: 交易员→财经优先，开发者→科技优先

## 🚀 快速开始

### 1. 安装技能

```bash
# 方式 1: 从 ClawHub 安装（推荐）
clawdhub install daily-news-brief

# 方式 2: 手动克隆
git clone https://github.com/zt6558609-cpu/daily-news-brief.git
cp -r daily-news-brief ~/.openclaw/workspace/skills/
```

### 2. 测试运行

```bash
cd ~/.openclaw/workspace/skills/daily-news-brief
python3 scripts/fetch_news.py
```

### 3. 配置新闻源

编辑 `config/sources.json`:

```json
{
  "categories": ["财经", "科技", "国际"],
  "keywords": {
    "财经": ["油价", "黄金", "股市"],
    "科技": ["AI", "大模型", "芯片"],
    "国际": ["大选", "贸易", "外交"]
  }
}
```

### 4. 启用定时推送

```bash
# 添加到 OpenClaw 定时任务
openclaw cron add daily-news-brief --time "08:00,20:00"
```

## 📋 输出示例

```
📰 每日新闻简报 - 2026 年 03 月 24 日

【财经】
1. 今日油价：2026 年 3 月 24 日，国内加油站调整后 92 号、95 号...
2. 3 月 23 日油价大涨，95、92 号汽油价格预计涨到 9 元时代

【科技】
1. OpenAI 发布 GPT-5，推理能力提升 300%
2. 苹果发布新款 iPhone，AI 功能成亮点

【国际】
1. 美联储维持利率不变，暗示 5 月可能降息
2. 欧盟通过新的人工智能法案

---
💡 简报由 AI 生成，全文阅读请访问来源链接
```

## ⚙️ 配置说明

### 新闻源配置 (config/sources.json)

```json
{
  "categories": ["财经", "科技", "国际"],  // 新闻分类
  "keywords": {                            // 每类的搜索关键词
    "财经": ["油价", "黄金", "股市"],
    "科技": ["AI", "大模型", "芯片"],
    "国际": ["大选", "贸易", "外交"]
  },
  "exclude_keywords": ["广告", "推广"]    // 排除关键词
}
```

### 定时配置 (config/schedule.json)

```json
{
  "morning": "08:00",      // 早间推送时间
  "evening": "20:00",      // 晚间推送时间
  "timezone": "Asia/Shanghai",
  "enabled": true          // 是否启用
}
```

## 🔧 高级用法

### 自定义新闻源

```json
{
  "custom_sources": [
    {
      "name": "我的博客",
      "url": "https://example.com/feed",
      "category": "科技"
    }
  ]
}
```

### 修改输出模板

编辑 `templates/brief.md` 自定义格式。

### 添加推送渠道

通过 OpenClaw 配置，支持 QQ/微信/Telegram/Discord 等。

## 📦 文件结构

```
daily-news-brief/
├── SKILL.md              # 技能说明
├── README.md             # 使用教程
├── scripts/
│   ├── fetch_news.py     # 新闻抓取脚本
│   └── output/           # 输出目录
├── templates/
│   └── brief.md          # 输出模板
└── config/
    ├── sources.json      # 新闻源配置
    └── schedule.json     # 定时配置
```

## ❓ 常见问题

**Q: 可以只推送财经新闻吗？**  
A: 可以！在 `config/sources.json` 中只保留"财经"分类。

**Q: 能推送多次吗？**  
A: 可以！修改 `config/schedule.json`，添加更多时间点。

**Q: 新闻源可以自定义吗？**  
A: 可以！支持 RSS/网站/API 多种方式。

**Q: 如何查看历史简报？**  
A: 查看 `scripts/output/` 目录，按日期保存。

## 📝 更新日志

### v1.0.0 (2026-03-24)
- ✅ 首次发布
- ✅ 支持多源新闻抓取
- ✅ AI 智能总结
- ✅ 定时推送

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📬 联系方式

- GitHub: https://github.com/zt6558609-cpu/daily-news-brief
- 作者：小爪 AI

---

**觉得有用？给个 Star 吧！⭐**
