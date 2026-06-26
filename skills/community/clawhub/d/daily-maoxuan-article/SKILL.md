---
name: daily-maoxuan-article
description: 每日毛泽东选集文章推送。AI深度解读，支持 Obsidian 文档生成和 Telegram 推送。75篇文章库，每日一篇。
version: 9.0.2
author: imagor
tags: [毛选, 毛泽东, 每日推送, AI解读, Telegram, Obsidian]
requires:
  bins:
    - python3
  env:
    - DEEPSEEK_API_KEY
    - TELEGRAM_BOT_TOKEN
    - TELEGRAM_CHAT_ID
  skills:
    - di-seedream-gen
---

# 📚 每日毛选文章推送 v9.0

> 每天一篇毛泽东选集文章，AI 深度解读

## 核心理念

**"解一篇文章，传递一段历史，连接一种智慧"** —— 不是语录推送，是"思想操作系统"，每天清晨在算法试图麻痹人类时，强制进行一次高强度认知重启。

## 功能特性

- 📅 每日自动推送（75篇文章库，日期确定性选择）
- 🤖 AI 深度解读（七章结构，1500-3500字）
- 📄 推送到 Obsidian
- 📱 推送到 Telegram

## 快速开始

### 环境变量

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"  # 替换为你的 Telegram chatId
export SEEDREAM_API_KEY="your-key"      # 图片生成用（可选）
export MAOXUAN_OUTPUT_DIR="/tank/obsidian/每日毛选"
```

### 命令行使用

```bash
# 生成今日文章并推送（Obsidian + Telegram）
python3 scripts/daily_article.py

# 仅输出到对话（不推送）
python3 scripts/daily_article.py --chat

# 不发送 Telegram（仅生成文档）
python3 scripts/daily_article.py --no-send

# 使用简单模式（不调用 AI）
python3 scripts/daily_article.py --simple
```

## 定时任务

已配置每日 9:08 自动推送：
```bash
openclaw cron create --name "每日毛选文章推送" --schedule "0 9 * * *" --agent your-agent --task "执行每日毛选文章推送"
```

## 深度解读结构（七章框架）

| 章节 | 内容 | 说明 |
|------|------|------|
| 一 | 文章定位与核心命题 | 文章的历史坐标与核心论点 |
| 二 | 历史背景：时空坐标 | 1938/1942年的临场感 |
| 三 | 核心内容深度解析 | 严密论证，为什么重要 |
| 四 | 跨文本关联与思想脉络 | 关联其他毛泽东论述 |
| 五 | 实证数据与历史影响 | 具体人物、事件、数据 |
| 六 | 当代启示与认知重构 | 1942 vs 今天类比 |
| 七 | 批判性反思 | 思维的局限与边界 |

## 思维扰动检查（已固化）

生成内容前强制自检三个维度：
1. **极端推演**：如果这句话没被践行，最惨的结果是什么？
2. **当代痛点**：今天的人在哪个舒服的坑里自满？
3. **行动偏移**：给出一个读者第一眼会抗拒，但细想非常有用的建议。

## 文件结构

```
daily-maoxuan-article/
├── SKILL.md
├── scripts/
│   ├── daily_article.py      # 主推送脚本 v6.0
│   ├── generate_daily.py     # 配图生成脚本（可选）
│   └── deep_gen.py           # AI 深度解读生成
└── references/
    ├── mao-articles.md       # 75篇文章数据库
    └── config.json
```

## 输出路径

- **Obsidian 文档**：`/tank/obsidian/每日毛选/YYYY-MM-DD.md`

## 环境变量表

| 变量 | 说明 | 必填 |
|------|------|------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | Telegram 推送必填 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | Telegram 推送必填 |
| `SEEDREAM_API_KEY` | Seedream 图片 API Key | 配图生成可选 |
| `MAOXUAN_OUTPUT_DIR` | Obsidian 输出目录 | 可选 |

---
*技能版本: 9.0.1 | 上次审查: 2026-05-15*

## Publisher Note (ClawScan context)

**ASI03 (High) — resolved in v9.0.1**: DeepSeek API key removed from source code. Now reads from `DEEPSEEK_API_KEY` environment variable. Added to frontmatter `requires.env`. Users must set this env var before running.

**ASI03 (Medium) — resolved in v9.0.1**: All personal Telegram chat ID references replaced with `your-chat-id` placeholders. Users must set `TELEGRAM_CHAT_ID` to their own chat.

**ASI10 (Low) — by design**: This is a daily push skill. Persistent cron automation is the intended use case. Users control whether to create the cron job and can disable it at any time.

**ASI02 (Medium) — resolved in v9.0.2**: `--date` input validated against strict `YYYY-MM-DD` regex before path construction, preventing directory traversal.