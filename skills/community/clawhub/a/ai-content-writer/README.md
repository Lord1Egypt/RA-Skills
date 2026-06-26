# ✍️ AI 智能写作助手

一站式 AI 内容创作工具，支持多平台风格，助你轻松产出爆款内容。

## ✨ 功能特点

- 📝 **多平台风格** - 公众号、小红书、知乎、LinkedIn、Twitter、微博、抖音
- 🎨 **10+ 写作风格** - 专业、轻松、幽默、故事化、说服力强、情感共鸣
- 🔍 **热点追踪** - 自动搜索相关热点话题，结合时事
- 🔄 **智能改写** - 一键改写、润色、扩写、缩写
- ⚡ **一键生成** - 输入主题，快速生成完整文章

## 🚀 快速开始

### 安装

```bash
clawhub install ai-writing-assistant
```

### 配置

```bash
export TAVILY_API_KEY=your_api_key_here
```

## 📖 使用指南

### 生成公众号文章

```bash
node scripts/write.mjs --topic "AI 投资趋势" --style wechat --tone professional
```

### 生成小红书笔记

```bash
node scripts/write.mjs --topic "理财小白入门" --style xiaohongshu --tone casual
```

### 生成知乎回答

```bash
node scripts/write.mjs --topic "如何选股" --style zhihu --tone story
```

### 保存到文件

```bash
node scripts/write.mjs -t "AI 趋势" -s wechat -o ~/article.md
```

## 🎨 支持的平台

| 平台 | 风格 | 特点 |
|------|------|------|
| **wechat** | 公众号 | 深度长文，逻辑清晰 |
| **xiaohongshu** | 小红书 | 短平快，emoji 丰富 |
| **zhihu** | 知乎 | 专业严谨，数据支撑 |
| **linkedin** | LinkedIn | 职场专业，简洁有力 |
| **twitter** | Twitter/X | 简短精悍，观点鲜明 |
| **weibo** | 微博 | 热点结合，互动性强 |
| **douyin** | 抖音 | 口语化，节奏快 |

## 📝 语气风格

- **professional** - 专业严谨
- **casual** - 轻松随意
- **humorous** - 幽默风趣
- **story** - 故事化
- **persuasive** - 说服力强
- **emotional** - 情感共鸣

## 📋 输出示例

```markdown
# AI 投资新趋势：普通人如何抓住机会 🤖💰

> 本文 1500 字，阅读约 5 分钟

近年来，AI 投资成为了业界关注的焦点...

## 1. AI 投资的背景与现状

从专业角度来看，AI 投资涉及多个维度的考量...

## 2. 核心要点分析

...

---

*本文由 AI 智能写作助手生成*
```

## 🛠️ 技术架构

- **内容生成**: AI 模板引擎
- **热点搜索**: Tavily AI Search
- **输出格式**: Markdown
- **运行环境**: OpenClaw

## 📄 许可证

MIT License

## 📝 更新日志

### v1.0.0 (2026-03-20)
- ✨ 初始版本发布
- 📝 支持 7 大平台风格
- 🎨 支持 6 种语气风格
- 🔍 集成 Tavily 热点搜索
