---
name: ai-writing-assistant
description: AI 智能写作助手 - 支持多平台内容创作，包括公众号、小红书、知乎、LinkedIn 等风格。提供 AI 查重、SEO 优化、改写润色等功能，一键生成高质量内容。
homepage: https://github.com/openclaw/ai-writing-assistant
metadata:
  openclaw:
    emoji: ✍️
    requires:
      bins: ["node"]
      env: ["TAVILY_API_KEY"]
    primaryEnv: "TAVILY_API_KEY"
---

# AI 智能写作助手

一站式 AI 内容创作工具，支持多平台风格，助你轻松产出爆款内容。

## ✨ 功能特点

- 📝 **多平台风格** - 支持公众号、小红书、知乎、LinkedIn、Twitter 等
- 🎨 **10+ 写作风格** - 专业、轻松、幽默、故事化等
- 🔍 **AI 查重检测** - 检测内容原创度，避免重复
- 📈 **SEO 优化** - 自动插入关键词，提升搜索排名
- 🔄 **智能改写** - 一键改写、润色、扩写、缩写
- ⚡ **一键生成** - 输入主题，快速生成完整文章

## 🚀 使用方法

### 生成文章

```bash
# 公众号风格
node {baseDir}/scripts/write.mjs --topic "AI 投资趋势" --style wechat --tone professional

# 小红书风格
node {baseDir}/scripts/write.mjs --topic "理财小白入门" --style xiaohongshu --tone casual

# 知乎风格
node {baseDir}/scripts/write.mjs --topic "如何选股" --style zhihu --tone story
```

### 改写润色

```bash
node {baseDir}/scripts/rewrite.mjs --file ./article.md --style professional
```

### SEO 优化

```bash
node {baseDir}/scripts/seo.mjs --file ./article.md --keywords "AI,投资,股票"
```

## 🎨 支持的平台风格

| 平台 | 风格特点 |
|------|---------|
| **wechat** | 公众号 - 深度长文，逻辑清晰 |
| **xiaohongshu** | 小红书 - 短平快，emoji 多 |
| **zhihu** | 知乎 - 专业严谨，数据支撑 |
| **linkedin** | LinkedIn - 职场专业，简洁有力 |
| **twitter** | Twitter/X - 简短精悍，观点鲜明 |
| **weibo** | 微博 - 热点结合，互动性强 |
| **douyin** | 抖音 - 口语化，节奏快 |

## 📝 语气风格

- **professional** - 专业严谨
- **casual** - 轻松随意
- **humorous** - 幽默风趣
- **story** - 故事化叙述
- **persuasive** - 说服力强
- **emotional** - 情感共鸣

## 🔧 配置

需要设置 Tavily API Key（用于热点话题搜索）：

```bash
export TAVILY_API_KEY=your_api_key_here
```

## 📄 输出示例

```markdown
# AI 投资新趋势：普通人如何抓住机会 🤖💰

> 本文 1500 字，阅读约 5 分钟

最近，AI 投资成为了热门话题...

## 为什么现在是入场时机？

...

---

*本文由 AI 智能写作助手生成*
```

## License

MIT
