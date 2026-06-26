---
name: ai-content-tailor
version: 1.0.0
description: 一篇文章快速拆分成多个平台版本（公众号/小红书/知乎/抖音）
author: 小叮当
tags:
  - content
  - social-media
  - repurpose
  -写作
---

# Content Repurposer - 内容多平台适配器

一键将同一篇文章改写成适合不同平台的版本，节省内容创作者的时间。

## 功能

- 📱 **多平台适配**：公众号、小红书、知乎、抖音四种格式
- 🤖 **AI 智能改写**：使用 LLM 调整语气、长度、结构
- ⚡ **快速处理**：几秒钟生成4个版本
- 📝 **保持核心**：保留原文核心观点，只调整呈现方式
- 🎯 **平台优化**：符合各平台特性（标题、段落、标签等）
- 👀 **预览功能**：预览所有平台版本后再输出

## 快速开始

### 1. 安装

```bash
clawhub install ai-content-tailor
cd ~/.openclaw/workspace/skills/ai-content-tailor
./install.sh
```

### 2. 配置 OpenAI API

```bash
export OPENAI_API_KEY="your-api-key"
```

### 3. 使用

```bash
# 快速改写
ai-content-tailor repurpose article.md --output ./versions/

# 指定平台
ai-content-tailor repurpose article.md --platforms wechat,xiaohongshu,zhihu,dy

# 预览模式
ai-content-tailor repurpose article.md --preview

# 批量处理
ai-content-tailor batch ./articles/ --output ./repurposed/
```

## 参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `input` | 路径 | 是 | 输入文章（Markdown/Text） |
| `command` | 选项 | 是 | `repurpose` 或 `batch` |
| `--output` | 路径 | 否 | 输出目录（默认：当前目录） |
| `--platforms` | 列表 | 否 | 平台列表：wechat,xhs,zhihu,dy（默认：全部） |
| `--model` | 字符串 | 否 | LLM 模型：gpt-4o/gpt-4o-mini（默认：gpt-4o-mini） |
| `--preview` | 布尔 | 否 | 只预览，不保存文件 |
| `--tone` | 选项 | 否 | 语气：professional,casual,storytelling（默认：自动） |

## 平台特性

### 公众号 (wechat)
- 标题：简洁有力，~20字以内
- 结构：段落清晰，每段2-3行
- 风格：正式+亲和力
- 配图提示：[图片] 标注

### 小红书 (xhs)
- 标题：爆款风格，表情符号，~10-15字
- 开头：引起兴趣/痛点/悬念
- 标签：添加3-5个相关话题标签
- 风格：口语化，真实分享

### 知乎 (zhihu)
- 标题：具体/疑问/干货
- 结构：观点+论证+案例
- 风格：理性，专业，有深度
- 结尾：开放式问题或总结

### 抖音 (dy)
- 标题：简短有力，引发好奇
- 结构：快速切入，分点简短
- 风格：口语，节奏快
- 适合口播文案

## 输入文章要求

- 格式：Markdown 或纯文本
- 长度：建议 500-3000 字
- 内容：完整观点 + 支撑材料
- 标题：清晰的主题

## 输出文件

```
article.md
├── wechat_article.md
├── xhs_post.md
├── zhihu_answer.md
└── dy_script.md
```

## 使用示例

```bash
# 改写一篇公众号文章为四个平台版本
ai-content-tailor repurpose my_article.md --output ./all_platforms/

# 只生成小红书和抖音版本
ai-content-tailor repurpose my_article.md --platforms xhs,dy

# 用正式语气改写
ai-content-tailor repurpose my_article.md --tone professional

# 批量处理 articles 文件夹
ai-content-tailor batch ./articles/ --output ./repurposed/ --preview
```

## 技术栈

- **LLM**：OpenAI GPT-4o-mini（默认）
- **依赖**：openai, python-dotenv
- **配置**：~/.openclaw/workspace/skills/ai-content-tailor/.env

## License

MIT