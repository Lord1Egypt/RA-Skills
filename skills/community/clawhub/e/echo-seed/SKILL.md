---
name: echo-seed
description: 简洁优雅的想法记录工具 / Simple and elegant idea capture tool
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "echo-seed-deps",
              "kind": "pip",
              "package": "flask requests",
              "label": "安装 Echo Seed 依赖 / Install Echo Seed dependencies",
            },
          ],
      }
  }
---

# Echo Seed / 回声种子

> 让每一个想法都有回声 🌱  
> Every idea deserves an echo.

简洁优雅的想法记录工具，支持快速记录、智能分类、时间线视图和多端同步。

A simple and elegant idea capture tool with quick notes, smart categorization, timeline view, and multi-platform sync.

---

## 🚀 快速开始 / Quick Start

### 启动服务 / Start Service

```bash
# 启动 Web 服务 / Start Web service
python3 scripts/echo-web.py

# 访问 / Visit
http://localhost:5000
```

---

## 📋 前置依赖 / Prerequisites

### 必需依赖 / Required

| 依赖 / Dependency | 用途 / Purpose | 配置说明 / Setup |
|-------------------|----------------|------------------|
| **Python 3.10+** | 运行环境 / Runtime | `python3 --version` |
| **Flask** | Web 框架 / Web framework | `pip install flask` |
| **Requests** | HTTP 请求 / HTTP client | `pip install requests` |
| **SQLite** | 数据库 / Database | 内置 / Built-in |

### 可选依赖 / Optional

| 依赖 / Dependency | 用途 / Purpose | 配置说明 / Setup |
|-------------------|----------------|------------------|
| **Notion API** | 云端同步 / Cloud sync | 需配置 API Key（见下文）|
| **Google Calendar API** | 待办同步 / Todo sync | 需配置 OAuth（见下文）|
| **Telegram Bot** | 快速输入 / Quick input | 需创建 Bot（见下文）|
| **MiniMax API** | AI 分析 / AI analysis | 需配置 API Key（见下文）|

---

## 🔧 配置步骤 / Setup Guide

### 1️⃣ 创建 Telegram Bot（可选）/ Create Telegram Bot (Optional)

用于快速创建种子 / For quick seed creation:

1. 在 Telegram 中联系 **@BotFather**
2. 发送 `/newbot` 创建新 Bot
3. 设置 Bot 名称（如：Echo Seed Bot）
4. 获取 **Bot Token**（格式：`123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`）
5. 将 Token 配置到 Bot 脚本中

**Bot 命令列表 / Bot Commands:**
- `/note` - 创建笔记 / Create note
- `/idea` - 创建灵感 / Create idea
- `/link` - 创建链接 / Create link
- `/todo` - 创建待办 / Create todo
- `/diary` - 创建日记 / Create diary
- `/thought` - 创建思考 / Create thought
- `/collect` - 创建收藏 / Create collection
- `/voice` - 创建语音 / Create voice
- `/list` - 查看最近种子 / List recent seeds
- `/search` - 搜索种子 / Search seeds
- `/stats` - 统计信息 / Statistics

### 2️⃣ 配置 Notion API（可选）/ Configure Notion API (Optional)

用于云端同步 / For cloud sync:

1. 访问 https://www.notion.so/my-integrations
2. 创建新 Integration / Create new integration
3. 复制 **Internal Integration Token**
4. 在 `config.yaml` 中配置：

```yaml
notion:
  enabled: true
  api_key: "your_notion_api_key"
  parent_page_id: "your_parent_page_id"
```

### 3️⃣ 配置 Google Calendar（可选）/ Configure Google Calendar (Optional)

用于待办事项同步 / For todo sync:

1. 访问 Google Cloud Console
2. 启用 Google Calendar API
3. 创建 OAuth 2.0 凭证
4. 下载 `credentials.json` 到项目目录

### 4️⃣ 配置 AI 服务（可选）/ Configure AI Service (Optional)

用于 AI 分析功能 / For AI analysis:

```yaml
ai:
  enabled: true
  provider: "minimax"  # 或 "deepseek" / or "deepseek"
  api_key: "your_api_key"
  model: "MiniMax-M2.5"
```

---

## 📁 项目结构 / Project Structure

```
echo-seed/
├── scripts/
│   ├── echo-web.py          # Web 后端 / Web backend
│   ├── echo-telegram-bot.py # Telegram Bot
│   ├── db_helper.py         # 数据库助手 / Database helper
│   └── ai_service.py        # AI 服务 / AI service
├── templates/
│   └── index.html           # Web 界面 / Web UI
├── data/
│   └── echo.db              # SQLite 数据库 / Database
├── config.example.yaml      # 配置示例 / Config example
├── requirements.txt         # Python 依赖 / Dependencies
└── SKILL.md                 # 本文件 / This file
```

---

## 🤖 功能特性 / Features

- 📝 **快速记录** - 8 种类型（笔记/灵感/链接/日记/思考/收藏/待办/语音）
- 🎨 **智能分类** - 自动标签、颜色编码
- 📅 **时间线视图** - 按时间浏览想法
- 🔍 **搜索筛选** - 全文搜索、类型过滤
- 📊 **统计面板** - 数据可视化
- 🤖 **AI 增强** - 点子扩张、链接分析、智能关联
- 🔄 **多端同步** - Notion、Google Calendar、Telegram Bot

- 📝 **Quick Capture** - 8 types (note/idea/link/diary/thought/collection/todo/voice)
- 🎨 **Smart Categorization** - Auto tags, color coding
- 📅 **Timeline View** - Browse by time
- 🔍 **Search & Filter** - Full-text search, type filter
- 📊 **Statistics** - Data visualization
- 🤖 **AI Enhanced** - Idea expansion, link analysis, smart relations
- 🔄 **Multi-Platform Sync** - Notion, Google Calendar, Telegram Bot

---

## 📖 详细文档 / Documentation

- **AI 功能说明 / AI Features:** [README-AI.md](README-AI.md)
- **GitHub 仓库 / GitHub Repo:** https://github.com/zheznanohana/echo-seed

---

## ⚠️ 注意事项 / Notes

1. **首次启动** 会自动创建数据库 / Database auto-created on first run
2. **配置文件** 可选，无配置也可使用基础功能 / Config is optional
3. **Telegram Bot** 需要单独运行 / Bot runs separately
4. **AI 功能** 需要 API Key / AI requires API key

---

**版本 / Version:** 1.0.0  
**作者 / Author:** @zheznanohana  
**许可证 / License:** MIT
