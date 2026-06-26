# AB Agents Memory 🦀

**Long-term memory system for OpenClaw agents**

*by AB-Agents (Alex Burr)*

---

## 🇷🇺 Русский

### Описание

AB Agents Memory — система управления долгосрочной памятью агентов OpenClaw. Включает агента AB-Archivus и готовый Obsidian vault.

### Установка

```bash
git clone https://github.com/alexburrstudio/ab-agents-memory.git
cd memory
./setup.sh
```

### Структура памяти

```
Memory/
├── Entities/              # Сущности
│   ├── People/           # Люди
│   ├── Companies/        # Компании
│   └── Topics/           # Темы
├── Summaries/           # Сводки
└── Processing/          # Обработка
    └── Nightly/         # Ночные скрипты
```

### Что внутри

- 🤖 **AB-Archivus** — агент-хранитель памяти
- 📁 **Obsidian Vault** — готовое хранилище с шаблонами
- 🔗 **Связи между сущностями** — кто с кем работает
- 🌙 **Ночная обработка** — автоматическое обновление


## 🇬🇧 English

### Description

AB Agents Memory is a long-term memory management system for OpenClaw agents. Includes AB-Archivus agent and ready-to-use Obsidian vault.

### Installation

```bash
git clone https://github.com/alexburrstudio/ab-agents-memory.git
cd memory
./setup.sh
```

### Memory Structure

```
Memory/
├── Entities/              # Entities
│   ├── People/           # People
│   ├── Companies/        # Companies
│   └── Topics/           # Topics
├── Summaries/           # Summaries
└── Processing/          # Processing
    └── Nightly/         # Nightly scripts
```

### What's Inside

- 🤖 **AB-Archivus** — memory keeper agent
- 📁 **Obsidian Vault** — ready-to-use vault with templates
- 🔗 **Entity Links** — connections between entities
- 🌙 **Nightly Processing** — automatic updates


## 📸 Screenshots

### Obsidian Vault Structure

```
📁 AB-Memory-Vault/
├── 📁 Memory/
│   ├── 📁 Entities/
│   │   ├── 📁 People/
│   │   ├── 📁 Companies/
│   │   └── 📁 Topics/
│   ├── 📁 Summaries/
│   └── 📁 Processing/
│       └── 📁 Nightly/
└── 📁 Templates/
    └── 📄 person-template.md
```

### Entity Example (Person)

```markdown
# Person Entity Template

## Identity
- **Name:** John Doe
- **Role:** Software Engineer
- **Contact:** john@company.com
- **Channel:** @johndoe
- **Location:** Moscow, Russia

## Relations
- Works at: [[Tech Company]]
- Colleagues: [[Alice]], [[Bob]]

## Notes
- Prefers concise communication
- Expert in Python, Go

## Timeline
- 2026-01-15: First contact
- 2026-03-20: Project started
```

---

## 🚀 Quick Install

```bash
# One-liner
git clone https://github.com/alexburrstudio/ab-agents-memory.git && cd memory && ./setup.sh
```

Or via ClawHub:

```bash
clawhub install AB-Agents-Memory
```

---

## 📦 What's Included

| Component | Description |
|-----------|-------------|
| `agents/AB-Archivus/` | OpenClaw agent for memory management |
| `obsidian-vault/` | Ready-to-use Obsidian vault |
| `setup.sh` | Automated installation script |
| `SKILL.md` | ClawHub package metadata |
| `package.json` | npm package manifest |

---

## 🔧 Configuration

### Vault Location

Default: `/data/obsidian/AB-Memory-Vault/`

Override:
```bash
VAULT_DEST=/custom/path ./setup.sh
```

### Agent Location

Default: `~/.openclaw/agents/AB-Archivus/`

---

## 🌐 Links

- 🌐 **AB Agents Channel:** https://t.me/alexburr_agents
- 📖 **Documentation:** [README.md](README.md)
- 🐛 **Issues:** https://github.com/alexburrstudio/ab-agents-memory/issues
- 📦 **ClawHub:** https://clawhub.com/ab-agents-memory

---

## 📄 License

MIT License

---

**AB Agents Memory** — Your second brain for OpenClaw 🦀

---

## 💰 Support / Поддержать

Если AB Agents Memory оказался полезен — пиши в канал:

- 🌐 **Канал:** https://t.me/alexburr_agents
- 👤 **Автор:** [@AlexBurrOne](https://t.me/AlexBurrOne)

---

**AB Agents Memory** 🦀 © 2026 [Alex Burr](https://t.me/AlexBurrOne)
