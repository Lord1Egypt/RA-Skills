# 📚 每日毛选文章推送

> **解一篇文章，传递一段历史，连接一种智慧** — 每天清晨，在算法试图麻痹你时，强制进行一次高强度认知重启。

**daily-maoxuan-article** 是一款基于 OpenClaw 的 AI 自动化技能。每天从《毛泽东选集》75篇文章中选出一篇，生成 1500-3500 字的深度认知解读，推送到你的 Obsidian 笔记库和 Telegram。

---

## ✨ 核心特色

### 📅 75篇完整文章库

覆盖《毛泽东选集》全五卷核心篇章，**按日期确定性选择**，每个日期对应唯一文章，确保内容丰富且不重复。

### 🤖 AI 深度解读（七章框架）

每篇文章从 **文章定位 → 历史背景 → 核心解析 → 思想脉络 → 实证数据 → 当代启示 → 批判反思** 七个维度深度解构。

### 🖼️ 智能配图（可选）

调用 Seedream API 生成 2K 高清配图，风格与文章主题契合。

### 📱 多渠道推送

- **Obsidian**：标准 Markdown 文档，兼容双向链接
- **Telegram**：直接推送到聊天，随时可读

### ⏰ 定时自动化

配置一次，每天 9:00 自动执行，无需人工干预。

---

## 🚀 快速开始

### 1. 安装技能

```bash
clawhub install daily-maoxuan-article
```

### 2. 配置环境变量

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
export SEEDREAM_API_KEY="your-key"  # 可选，配图用
export MAOXUAN_OUTPUT_DIR="/tank/obsidian/每日毛选"
```

### 3. 手动测试

```bash
# 生成今日文章并推送（Obsidian + Telegram）
python3 scripts/daily_article.py

# 仅输出到对话
python3 scripts/daily_article.py --chat

# 不发送 Telegram（仅生成文档）
python3 scripts/daily_article.py --no-send

# 使用简单模式（不调用 AI）
python3 scripts/daily_article.py --simple
```

### 4. 配置定时任务

```bash
openclaw cron create \
  --name "每日毛选文章推送" \
  --schedule "0 9 * * *" \
  --agent <your-agent> \
  --task "执行每日毛选文章推送" \
  --timezone "Asia/Shanghai"
```

---

## 📖 深度解读框架（七章结构）

| 章节 | 内容 | 说明 |
|------|------|------|
| **一** | 文章定位与核心命题 | 文章的历史坐标与核心论点 |
| **二** | 历史背景：时空坐标 | 1938/1942年的临场感，知识储备不足的焦虑 |
| **三** | 核心内容深度解析 | 严密论证，为什么不仅是个人修养，更是政治风险 |
| **四** | 跨文本关联与思想脉络 | 关联《实践论》《改造我们的学习》等 |
| **五** | 实证数据与历史影响 | 具体人物、事件、数据 |
| **六** | 当代启示与认知重构 | 1942 vs 今天类比，知识匮乏 vs 信息过剩 |
| **七** | 批判性反思 | 思维的局限与边界 |

---

## 🧠 思维扰动检查

生成内容前强制自检三个维度：

1. **极端推演**：如果这篇文章没被践行，最惨的结果是什么？
2. **当代痛点**：今天的人在哪个舒服的坑里自满？
3. **行动偏移**：给出一个读者第一眼会抗拒，但细想非常有用的建议。

---

## 📁 输出示例

```
/tank/obsidian/每日毛选/2026-05-14.md
```

文档结构：
```markdown
# 📚 每日毛选文章 | 2026-05-14

## 《改造我们的学习》

> **原文摘录**：...（核心段落）

## 一、文章定位与核心命题

...

## 二、历史背景：时空坐标

...
```

---

## 🔧 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | Telegram 推送必填 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | Telegram 推送必填 |
| `SEEDREAM_API_KEY` | Seedream API Key | 配图生成可选 |
| `MAOXUAN_OUTPUT_DIR` | Obsidian 输出目录 | 可选 |

---

## 📦 文件结构

```
daily-maoxuan-article/
├── SKILL.md
├── README.md
├── scripts/
│   ├── daily_article.py      # 主推送脚本
│   ├── generate_daily.py     # 配图生成（可选）
│   └── deep_gen.py           # AI 深度解读生成
└── references/
    ├── mao-articles.md       # 75篇文章数据库
    └── config.json
```

---

## 💡 核心理念

> 这个技能不是为了"学历史"。
> **是为了每天强迫你进行一次认知重启——在信息茧房、短视频、算法推荐的围剿中，杀出一条思想的血路。**

如果你发现每天读完后有一种"脑子被重启"的感觉——这就对了。

---

**作者**：imagor  
**版本**：9.0.0  
**许可证**：MIT