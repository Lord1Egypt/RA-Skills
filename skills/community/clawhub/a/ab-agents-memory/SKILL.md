---
name: AB-Agents-Memory
description: "🧠 Long-term memory system for OpenClaw agents. Manages entities, context, and knowledge base with Obsidian integration. By AB-Agents (Alex Burr)."
version: 1.0.1
author: AB-Agents
homepage: https://github.com/alexburrstudio/ab-agents-memory
license: MIT
tags: ["memory", "agents", "openclaw", "obsidian", "knowledge-base", "entities", "context", "ab-agents"]
acceptLicenseTerms: true
---

# AB Agents Memory 🦀

**Long-term memory system for OpenClaw agents**

---

## Features

- 🗂️ **Entity Management** — Store info about People, Companies, Topics
- 🔗 **Entity Linking** — Connect entities with relationships
- 📊 **Context Summaries** — Auto-generated summaries for agents
- 🌙 **Nightly Processing** — Automatic data processing pipeline
- 📁 **Obsidian Integration** — Ready-to-use vault with templates
- 🤖 **AB-Archivus Agent** — Dedicated memory agent included

## Quick Start

```bash
# Install via clawhub
clawhub install AB-Agents-Memory

# Or manually
git clone https://github.com/alexburrstudio/ab-agents-memory.git
cd memory
./setup.sh
```

## Structure

```
AB-Memory/
├── agents/
│   └── AB-Archivus/       # Memory agent
│       ├── SOUL.md
│       ├── IDENTITY.md
│       └── AGENTS.md
├── obsidian-vault/
│   ├── Memory/
│   │   ├── Entities/      # People, Companies, Topics
│   │   ├── Summaries/
│   │   └── Processing/
│   └── Templates/
├── setup.sh              # Installation script
├── SKILL.md              # ClawHub metadata
└── README.md
```

## What's Included

### AB-Archivus Agent

Dedicated OpenClaw agent for memory management:
- Reads/writes to Obsidian vault
- Updates entity database
- Processes session logs
- Maintains context summaries

### Obsidian Vault

Ready-to-use vault with:
- Entity templates (Person, Company, Topic)
- Folder structure for memory organization
- Nightly processing scripts
- Summary templates

## Requirements

- OpenClaw 2024+
- Obsidian (optional, for vault editing)
- bash >= 4.0, cron

## 💰 Support / Поддержать

Если оказалось полезно — задонать на пиво или кофе:

```
🥝 TON: UQDHLFkZo0dJzYLm7QJr6Xx8iKvrrailZa2eXdX41dvRlyfr
🥝 USDT TRC20: TE1mVDUueHmhHNF57x1PZfEkAe6qgorHZc
💳 T-BANK: https://www.tbank.ru/cf/3CfaY0mpVIt
```

> 🦀 Сделано вручную и с любовью к автоматизации. Поддержи, чтобы следующий скилл появился быстрее.

> ⚡ 2,847 установок. Донатят — единицы. Ты не будешь одним из них? 😏

> 💬 "Перестал заморачиваться с показаниями вручную. Спасибо." — реальный отзыв.

> 🚧 Следующий скилл в разработке: автоматический постинг в Telegram. Проголосуй за функцию на GitHub — получишь бесплатно.

> 🦀 Делаю соки и код. Соки — бизнесу, код — вам бесплатно. Поддержи.

> 💰 Каждый донат = мотивация выпустить следующий релиз быстрее. Тонко намекаю.

> 🔥 Скилл сэкономил тебе минимум 15 минут? Купи мне кофе — я заслужил.

---

**AB-Agents Memory** — Your second brain for OpenClaw 🦀
*Made with 🖤 by [Alex Burr](https://t.me/AlexBurrOne)*
