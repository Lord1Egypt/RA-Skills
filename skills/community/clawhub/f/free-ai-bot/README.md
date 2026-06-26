# 🤖 Free AI Bot

[English](README_en.md) | [中文](README_zh.md)

免费 AI 聚合器 - 让 AI 零成本运行

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## ✨ 特性

- 🏠 **本地模型** - Ollama 免费开源模型
- ☁️ **云端免费** - Cloudflare Workers AI + Groq
- 🧠 **智能路由** - 自动选择最优方案
- 🔄 **故障转移** - 一个不行换另一个
- 💰 **完全免费** - 零成本运行 AI

## 🚀 快速开始

### 1. 安装

```bash
git clone https://github.com/yourusername/free-ai-bot.git
cd free-ai-bot
```

### 2. 配置（可选）

```bash
# 本地模型（推荐）
export OLLAMA_HOST=http://localhost:11434

# Cloudflare（可选）
export CF_ACCOUNT_ID=your_account_id
export CF_API_TOKEN=your_token

# Groq（可选）
export GROQ_API_KEY=your_key
```

### 3. 使用

```bash
# 自动选择最佳方案
python3 scripts/ask_free_ai.py "你好，请介绍一下自己"

# 指定本地模型
python3 scripts/ask_free_ai.py "你好" --provider ollama --model llama3.2
```

## 📊 支持的 Provider

| Provider | 类型 | 免费额度 | 特点 |
|----------|------|----------|------|
| Ollama | 本地 | 无限 | 最快/最隐私 |
| Cloudflare | 云端 | 100K/天 | 稳定快速 |
| Groq | 云端 | 60/分钟 | 推理极快 |

## 🏗️ 架构

```
User Query
    ↓
[智能路由]
    ↓
┌─────────────────────────────────────┐
│ 1. Ollama (本地)    → 最快/免费     │
│ 2. Cloudflare       → 稳定         │
│ 3. Groq             → 推理快        │
└─────────────────────────────────────┘
    ↓
Response
```

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License - 免费开源
