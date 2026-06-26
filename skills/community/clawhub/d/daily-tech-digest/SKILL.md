---
name: daily-tech-digest
description: 每日科技热点简报生成器。自动收集AI、数码、科技领域时事热点，整理到Obsidian，推送到手机负一屏。支持定时任务和手动触发。
trigger: 
  - "生成科技简报"
  - "今日科技新闻"
  - "每日简报"
  - "科技热点"
  - "新闻简报"
config:
  optional:
    - obsidian_vault: "Obsidian Vault 路径，默认使用全局配置"
    - max_items_per_category: "每类最多显示条数，默认10"
    - summary_length: "摘要长度，默认400字"
    - push_to_negative_screen: "是否推送到负一屏，默认true"
  note: "需要 daily-tech-broadcast skill 作为数据源"
---

# Daily Tech Digest - 每日科技简报

## 技能概述

自动收集 AI、数码、科技领域时事热点，生成结构化简报，整理到 Obsidian，并推送到手机负一屏。

## 🚀 快速开始

### 手动生成简报

```bash
# 生成今日科技简报
python ~/.openclaw/workspace/skills/daily-tech-digest/scripts/daily_tech_digest.py

# 整理并归档新闻
python ~/.openclaw/workspace/skills/daily-tech-digest/scripts/daily_news_organizer.py
```

### 设置定时任务

```bash
# 早上 8:00 生成简报
openclaw cron add "0 8 * * *" \
  --command "python3 ~/.openclaw/workspace/skills/daily-tech-digest/scripts/daily_tech_digest.py" \
  --channel xiaoyi-channel \
  --model deepseek/deepseek-chat

# 晚上 8:00 整理归档
openclaw cron add "0 20 * * *" \
  --command "python3 ~/.openclaw/workspace/skills/daily-tech-digest/scripts/daily_news_organizer.py" \
  --channel xiaoyi-channel \
  --model deepseek/deepseek-chat
```

## 📋 功能特性

### 1. 自动收集热点

- **数据源**：新浪科技、IT之家等主流科技媒体
- **领域覆盖**：AI人工智能、数码产品、科技互联网、行业动态
- **智能过滤**：只保留今天或昨天的新闻，排除过时内容

### 2. 正文摘要抓取

- 自动抓取每篇文章正文
- 生成 300-500 字摘要
- 保留原文链接

### 3. Obsidian 整理

**简报结构：**
```
每日科技简报/
├── 2026-04-22_索引.md    ← 索引文件（归档后保留）
└── (归档后删除长文)

归档/
├── AI人工智能/
│   └── 2026-04-22_xxx.md
├── 数码产品/
│   └── 2026-04-22_xxx.md
├── 科技互联网/
│   └── 2026-04-22_xxx.md
└── 行业动态/
    └── 2026-04-22_xxx.md
```

### 4. 负一屏推送

- 使用 `today-task` skill 推送到华为手机负一屏
- 显示今日重点新闻（5条摘要）
- 卡片格式优化，适合移动端阅读

## 🔄 工作流程

```
早上 8:00                    晚上 8:00
    │                           │
    ▼                           ▼
┌─────────────┐          ┌─────────────┐
│ 收集新闻    │          │ 读取简报    │
│ 抓取正文    │          │ 解析内容    │
│ 分类整理    │          │ 拆分笔记    │
│ 生成简报    │          │ 归档分类    │
│ 保存Obsidian│          │ 生成索引    │
│ 推送负一屏  │          │ 删除长文    │
└─────────────┘          │ 推送负一屏  │
                         └─────────────┘
```

## 📁 文件结构

```
daily-tech-digest/
├── SKILL.md                    # 技能定义
├── scripts/
│   ├── daily_tech_digest.py   # 简报生成脚本
│   └── daily_news_organizer.py # 新闻整理脚本
└── templates/
    └── note_template.md       # 笔记模板（可选）
```

## ⚙️ 配置说明

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OBSIDIAN_VAULT` | Obsidian Vault 路径 | `/home/sandbox/.openclaw/workspace/repo/obsidian-vault` |
| `DIGEST_FOLDER` | 简报存放文件夹 | `每日科技简报` |
| `ARCHIVE_FOLDER` | 归档文件夹 | `归档` |

### 分类配置

脚本内置以下分类关键词：

| 分类 | 关键词示例 |
|------|-----------|
| AI人工智能 | AI, GPT, 大模型, OpenAI, 人工智能 |
| 数码产品 | 手机, iPhone, 华为, 芯片, 显卡 |
| 科技互联网 | 互联网, 云计算, 自动驾驶, 电商 |
| 行业动态 | 其他科技相关新闻 |

## 🔗 依赖技能

- **daily-tech-broadcast**：提供新闻数据源
- **today-task**：推送到负一屏卡片
- **obsidian-git-vault**：Git 同步（可选）

## 📝 输出示例

### 负一屏卡片

```
📰 每日科技简报

2026-04-22 · 共 11 条热点

─────────────

🔥 今日重点

1. AI接得住情绪，能否接得住真实？
   越来越多人在代码中寻找共鸣...

2. OpenAI CEO 奥尔特曼炮轰 Anthropic...
   IT之家 4 月 22 日消息...

...

─────────────

📱 详情请查看 Obsidian 笔记
```

### Obsidian 笔记

```markdown
---
title: 每日科技简报 - 2026-04-22
date: 2026-04-22
tags:
  - 科技简报
  - AI
  - 数码
---

# 📰 每日科技简报
**日期**: 2026-04-22

---

## 🤖 AI人工智能

### 1. OpenAI 发布新模型

> 📌 **来源**: IT之家

OpenAI 今日宣布推出新一代模型...

🔗 [阅读原文](https://...)

---
```

## ⚠️ 注意事项

1. **数据源依赖**：需要 `daily-tech-broadcast` skill 正常工作
2. **网络要求**：抓取正文需要稳定的网络连接
3. **负一屏推送**：需要手机联网并登录华为账号
4. **Git 同步**：自动提交到 Obsidian Git 仓库

## 🛠️ 故障排查

### 问题：无法获取新闻

**解决方案**：
1. 检查 `daily-tech-broadcast` skill 是否正常
2. 检查网络连接
3. 查看脚本输出的错误信息

### 问题：负一屏推送失败

**解决方案**：
1. 确认手机已联网
2. 确认已登录华为账号
3. 检查负一屏设置中的"AI任务完成通知"开关

### 问题：Git 同步失败

**解决方案**：
1. 检查 Git 仓库配置
2. 手动执行 `git pull` 和 `git push` 测试
3. 检查网络连接

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 平均执行时间 | 30-60 秒 |
| 新闻条数 | 10-20 条/天 |
| 摘要长度 | 300-500 字 |
| 推送成功率 | >95% |

## 🔄 更新日志

### v1.0.0 (2026-04-22)

- ✅ 初始版本
- ✅ 支持自动收集新闻
- ✅ 支持正文摘要抓取
- ✅ 支持 Obsidian 整理
- ✅ 支持负一屏推送
- ✅ 支持定时任务

---

*由小艺 Claw 自动维护*
