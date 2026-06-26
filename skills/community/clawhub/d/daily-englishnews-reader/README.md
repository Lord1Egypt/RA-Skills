<div align="center">

# 📚 Daily-EnglishNews-Reader

**基于 OpenClaw 的英语新闻检索 Skill**  
*用 i+1 学习法轻松学英语 + 了解全球资讯*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-brightgreen)
![Python 3](https://img.shields.io/badge/Python-3-yellow)

[功能特性](#-核心特性) • [安装指南](#%EF%B8%8F-安装与准备) • [使用方法](#-使用指南) • [配置说明](#-目录结构与配置说明)

</div>

---

## 📖 项目简介

**Daily-EnglishNews-Reader** 基于 OpenClaw 的英语新闻检索 Skill，旨在帮助用户用 i+1 学习法轻松学英语 + 了解全球资讯

> **Skill 运行效果**：OpenClaw 会自动返回一个 **飞书云文档链接**，包含：
> * 📄 **4 篇精选文章**：基于高质量新闻源，重写为符合你阅读难度的文章。
> * 📝 **生词讲解**：每篇文章末尾用简单的英文解析 自定义 个数量的 i+1 难度的生词，并附带例子
> * 🔗 **来源追溯**：附带文章的原始出处链接。

![](./static/1.png)

### 进阶玩法
可以让openclaw每日定时调用这个skills，生成每日阅读资料，快速了解近期国际新闻，顺便学习英语

### 💡"i+1 学习法"介绍

- **i+1 理论**：公认最高效的英语学习方法。"i" 代表你当前的水平，"+1" 代表稍高一点的挑战。
- **自然习得**：不靠死记硬背，而是通过大量阅读，在上下文中自然吸收那 10% 的新内容。
- **完美学习体验**：比背单词有意思，容易坚持

### 🎯 解决两大痛点

1. **😫 语料收集麻烦**：自动搜索最新全球高质量文章，内容覆盖全球新闻、经济、科技、科学文化，学英语的同时了解行业资讯
2. **😵 难度难以匹配**：自动重写文章以匹配你的 **CEFR 英语水平等级（A1-C1）**，每天都能通读大量英文语料。

## 🛠️ 安装与准备

本 Skill 基于openclaw开发，首先需要下载安装openclaw
依赖 Python 环境及飞书官方 OpenClaw 插件。

### 📦 快速部署

1. 将本项目文件夹拖拽到 `.openclaw/workspace/skills` 目录下。
2. 重启 OpenClaw。
3. 再次与 OpenClaw 交互时，系统会引导你完成依赖安装。

### ⚙️ 依赖说明

系统会自动通过 metadata 安装以下依赖：
* **Python 3 库**：`requests`, `feedparser`
* **OpenClaw 飞书插件**：`@larksuite/openclaw-lark-tools`

### 🔑 飞书授权（必读）

> **说明**：本 Skill 使用功能更强大的飞书官方插件 `@larksuite/openclaw-lark-tools`。安装后会自动禁用 OpenClaw 自带的飞书插件。
飞书官方插件安装文档在这：https://bytedance.larkoffice.com/docx/MFK7dDFLFoVlOGxWCv5cTXKmnMh

若openclaw引导安装飞书插件失败，请手动按以下步骤操作：

1. **安装插件**：执行命令：
   ```bash
   npx -y @larksuite/openclaw-lark-tools install
   # 如遇权限问题请加 sudo
   ```
2. **创建/关联机器人**：按终端提示选择「新建机器人」并扫码，或「关联已有机器人」。
3. **激活机器人**：在飞书客户端给该机器人发送任意消息。
4. **验证安装**：发送 `/feishu start`，返回版本号即成功。
5. **给机器人授权**：在使用skills的时候，机器人会询问你修改云文档的授权，同意即可。

> ⚠️ **注意**：必须完成飞书授权，否则无法生成云文档。

---

## 🚀 使用指南

### 1️⃣ 首次初始化

首次调用时，系统会引导你配置个性化参数（自动更新 `config/config.json`）：

- **📊 阅读难度 (CEFR)**：`A1` / `A2` / `B1` / `B2` / `C1`（默认：`A2`）
- **📝 文章字数**：每篇改写后的目标字数（默认：`350`）
- **🧠 讲解生词数**：每篇提取的生词数量（默认：`3`）

### 2️⃣ 唤醒与运行

发送自然语言指令即可调用：

> 🗣️ *"生成今天的英语阅读材料"*
>
> 🗣️ *"调用 Daily-EnglishNews-Reader"*

---
## ✨ 核心特性

| 特性 | 说明 |
| :--- | :--- |
| **🌍 多源聚合** | 自动从 4 个分类 RSS 源中各抽取 1 篇最新高质量文章。 |
| **🎚️ 智能适配** | 利用大模型将文章改写为指定的 **CEFR 难度** 和目标字数，行文地道。 |
| **📖 自动生词** | 智能提取 `+1` 难度生词，加粗显示并提供英文释义及例句。 |
| **☁️ 飞书直达** | 自动生成排版精美的 **飞书云文档**，直接返回阅读链接。 |
| **🛡️ 智能去重** | 内置本地记录机制，确保每天推荐的文章不重复。 |

---



## 📁 目录结构与配置说明

所有自定义配置均存放在 `config` 目录下：

| 文件名 | 说明 |
| :--- | :--- |
| **`config.json`** | **基础阅读偏好配置**<br>包含难度、字数、生词数等设置。 |
| **`rss_sources.json`** | **RSS 订阅源**<br>支持用户自行添加或修改订阅链接。 |
| **`sent_articles.json`** | **已读记录**<br>系统自动维护，用于去重。 |

**`config.json` 示例：**
```json
{
  "reading": {
    "difficulty": "A2",
    "words_per_article": 350,
    "words_per_article_to_explain": 3
  }
}
```

### 🔄 工作流解析

1. 📥 **读取配置**：加载 `config/rss_sources.json` 订阅源。
2. 🎲 **随机筛选**：从 4 个领域中随机挑选 RSS 源。
3. 🕵️ **抓取过滤**：抓取文章并根据 `config/sent_articles.json` 历史记录去重。
4. 🤖 **AI 重写**：大模型按指定难度和字数重写文章。
5. 📚 **生词提取**：加粗生词，附上释义和例句。
6. ☁️ **生成文档**：调用飞书 API 生成排版精美的云文档。
7. 🔗 **返回链接**：发送文档链接给用户。
8. 📝 **记录去重**：更新 `sent_articles.json`，防止重复推荐。

---

## 📄 License

This project is licensed under the **MIT License**.

## ⚖️ Disclaimer & Fair Use

**This project (English Daily Reader) is an educational tool designed exclusively for language learning purposes.**

- **Transformative Use**: The articles processed by this tool are heavily modified, summarized, and rewritten to match specific CEFR language levels (e.g., A1-C1). Under copyright law, this constitutes "transformative use" and falls under Fair Use principles.
- **Attribution**: All generated content retains clear attribution to the original publishers and provides direct links to the original source articles.
- **No Affiliation**: This project is strictly independent. It is not affiliated with, sponsored by, or endorsed by any of the news outlets or RSS feed providers used in the default configuration.
- **Non-Commercial**: This codebase and its outputs are intended for personal, non-commercial use. Users who deploy this tool to generate and distribute content for commercial gain do so entirely at their own legal risk.

> *Notice to Copyright Holders: If you believe that this project's use of your public RSS feeds exceeds fair use, please open an issue, and your domain will be promptly removed from the default source list.*