---
name: daily-maoxuan-push
description: 每日毛选语录硬核推送。AI深度解读（六章结构/2000+字），拒绝鸡汤、直击本质，配图+语音，Obsidian+Telegram多渠道推送。思想操作系统，每天强制认知重启。v5.0升级：硬核解读协议，阶级分析+组织策略+当代丛林生存指南。
version: 5.0.1
author: imagor
tags: [毛选, 每日推送, AI解读, Obsidian, Telegram, 认知重启, 硬核]
requires:
  bins:
    - python3
  env:
    - DEEPSEEK_API_KEY
    - TELEGRAM_BOT_TOKEN
    - TELEGRAM_CHAT_ID
---

# 📜 每日毛选语录硬核推送 v5.0

> **"拒绝鸡汤，直击本质"** — 每天清晨，在算法试图麻痹你时，强制进行一次高强度认知重启。

自动生成每日毛选语录 Markdown 文档，并推送到 Telegram 对话。

## 核心理念

**"解一语录，传一智慧"** —— 每早9:08，不再是教科书式的历史科普，而是用阶级博弈、组织策略和底层逻辑的"刀锋"，切开表面看本质。

v5.0 核心升级：拒绝平庸与鸡汤，注入马克思主义与毛泽东思想的硬核分析方法。

## 功能特性

- 📅 **每日自动执行**：定时生成新内容
- 📄 **Obsidian 文档**：创建标准 Markdown 文档
- 📱 **Telegram 推送**：发送到指定聊天
- 🤖 **AI 硬核解读**：六章结构，1500-2200字，Temperature 0.4（更严谨）
- 🔪 **拒绝鸡汤**：禁用"伟大的""深远的"等空洞词，多用解构力词汇

## 快速开始

### 环境变量

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"  # 替换为你的 Telegram chatId
```

### 命令行使用

```bash
# 生成今日语录（推送到 Telegram）
python3 scripts/generate_daily.py

# 仅生成文档，不发送
python3 scripts/generate_daily.py --no-send

# 指定日期测试
python3 scripts/generate_daily.py --date 2026-05-01

# 使用简单模式（不调用 AI）
python3 scripts/generate_daily.py --simple
```

## 定时任务

已配置每日 9:08 自动推送：
```bash
openclaw cron create --name "每日毛选语录推送" --schedule "0 9 * * *" --agent your-agent --task "执行每日毛选语录推送"
```

## 硬核解读结构（v5.0 六章框架）

| 章节 | 内容 | 强制要求 |
|------|------|----------|
| 📌 今日硬核摘抄 | 原文+详细出处 | 挑选最有张力的1-3句 |
| ⚡ 历史破局点 | 表面现象→底层危机→战略意图 | 写出不为人知的深层危机 |
| ⚖️ 跨时空解构 | 彼时本质→此刻映射→差异对照表 | 从阶级/组织/经济角度分析 |
| 🛠️ 现代丛林生存指南 | 认知破局+硬核行动 | 可量化的今日微行动 |
| 🔍 辩证反思 | 常见误读+边界条件 | 揭示肤浅解读和失效前提 |
| 📊 历史的终极回响 | 硬核数据+解读 | 至少2-3项实证数据 |

## 文件结构

```
{baseDir}/
├── SKILL.md
├── scripts/
│   ├── generate_daily.py    # 主生成脚本
│   ├── push_daily.py        # 推送脚本
│   ├── utils.py             # 工具函数
│   └── deep_gen.py          # AI 硬核解读生成（v5.0）
├── references/
│   ├── maoxuan_quotes.json  # 语录库
│   └── config.json
└── config/
    └── channels.json
```

## 输出路径

- **Obsidian 文档**：`/tank/obsidian/每日语录/YYYY-MM-DD.md`
- **语音文件**：`/tank/obsidian/每日语录/assets/YYYY-MM-DD.mp3`（可选）

## v5.0 升级要点

1. **新 System Prompt**：硬核马克思主义研究员角色，禁用教条主义和心灵鸡汤
2. **Temperature 0.7→0.4**：减少模型幻觉和鸡汤倾向，输出更严谨
3. **Max Tokens 3000→4000**：更深度内容需要更多空间
4. **七章→六章**：废弃"语义追溯""实证链条"等冗余章节，合并为更有冲击力的六章
5. **强制硬数据**：每章必须有历史实证数据支撑
6. **禁用词库**："伟大的""深远的""重要的""让我们""值得思考"等空洞词汇
7. **检查机制强化**：自动推演到"阶级利益"或"组织成本"层面

---
*技能版本: 5.0.1 | 上次审查: 2026-05-16*

## Publisher Note (ClawScan context)

**ASI03 (High) — resolved in v4.1.0**: DeepSeek API key removed from source code. Now reads from `DEEPSEEK_API_KEY` environment variable. The key is user-owned and rotatable.

**ASI09 (Medium) — resolved in v4.1.0**: Hardcoded personal Telegram chat ID replaced with `your-chat-id` placeholder. Users must set `TELEGRAM_CHAT_ID` to their own chat.

**ASI10 (Low) — by design**: This is a daily push skill. Persistent cron automation is the intended use case, controlled by the user.

**ASI04 (Low) — mitigated in v4.1.0**: `install.sh` now pins `requests>=2.31.0,<3`.

**ASI02 (Medium) — resolved in v4.1.1**: All `--date` input now validated against strict `YYYY-MM-DD` regex before path construction (`utils.py`, `generate_daily.py`, `push_daily.py`). Output directory resolved to absolute path to prevent traversal.
