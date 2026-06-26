# 🔥 AMPHP v3 Skill for AI Coding Assistants

> Teach AI agents to write **correct non-blocking async PHP using AMPHP v3**

[![Claude Code](https://img.shields.io/badge/Claude-Code-blue)]()
[![Cursor](https://img.shields.io/badge/Cursor-Compatible-purple)]()

Skill that teaches AI coding assistants (**Claude, Codex, OpenClaw, Cursor agents**) to generate **production-ready async PHP using AMPHP v3**.

Prevents common mistakes like:

* blocking I/O inside event loops
* outdated AMPHP v2 patterns
* incorrect async patterns
* unsafe JSON handling
* broken connection reuse

---

# 📚 Table of Contents

* [✨ Features](#-features)
* [📸 Demo](#-demo)
* [🚀 Quick Start](#-quick-start)
* [📖 How to Use](#-how-to-use)
* [⚙️ Requirements](#️-requirements)
* [🛠 Best Practices](#-best-practices)
* [⚠️ Limitations](#️-limitations)

---

# ✨ Features

✅ Generates **correct async PHP code**
✅ Enforces **AMPHP v3 architecture**
✅ Prevents **blocking operations in event loop**
✅ Rewrites **AMPHP v2 → v3 patterns**
✅ Safe **JSON handling with exceptions**
✅ Proper **HTTP body consumption**
✅ Correct **async concurrency patterns**

Supports ecosystem:

* `amphp/amp`
* `amphp/http-server`
* `amphp/http-client`
* `amphp/websocket`
* `amphp/mysql`
* `amphp/redis`
* `amphp/socket`
* `amphp/file`
* `amphp/cache`
* `amphp/sync`
* `amphp/process`
* `amphp/parallel`
* `revolt/event-loop`

---

# 📸 Demo

### ❌ Without the skill

AI often generates blocking code:

```php
$response = file_get_contents($url);
sleep(1);
```

### ✅ With the skill

AI generates correct async code:

```php
use Amp\Http\Client\HttpClientBuilder;
use function Amp\delay;

$client = HttpClientBuilder::buildDefault();
$response = $client->request($request);

await delay(1);
```

---

# 🚀 Quick Start

## 1️⃣ Claude Code (global install)

```bash
git clone https://github.com/opencck/skill-amphp ~/.claude/skills/amphp
```

Restart Claude Code.

---

## 2️⃣ Claude Code (per project)

```bash
mkdir -p .claude/skills
git clone https://github.com/opencck/skill-amphp .claude/skills/amphp
```

---

## 3️⃣ Cursor

Cursor loads skills from the project folder.

```bash
mkdir -p .cursor/skills
git clone https://github.com/opencck/skill-amphp .cursor/skills/amphp
```

Restart Cursor.

---

## 4️⃣ Generic AI Agents (Codex / OpenClaw / MCP)

Place the skill file manually:

```
skills/amphp/SKILL.md
```

Example:

```
skills/
 └ amphp/
   └ SKILL.md
   └ ...
```

---

# 📖 How to Use

The skill **activates automatically** when Claude detects:

```
Amp\Future
Amp\async
Amp\delay
Revolt\EventLoop
amphp/*
```

or async server patterns.

---

## Example prompts

### Convert blocking PHP to async

```
Convert this PHP code to AMPHP v3 async style
```

---

### Create async HTTP server

```
Create an async HTTP server using amphp/http-server
```

---

### Async MySQL

```
Write async MySQL queries using amphp/mysql
```

---

<details>
<summary>More prompt examples</summary>

```
Build a WebSocket server using amphp/websocket

Create an async queue worker

Convert this blocking script to non-blocking AMPHP
```

</details>

---

# ⚙️ Requirements

| Requirement       | Version |
| ----------------- | ------- |
| PHP               | 8.1+    |
| AMPHP             | v3      |
| Revolt Event Loop | 1+      |

Composer example:

```bash
composer require amphp/amp revolt/event-loop
```

---

# 🧪 Tested With

| Model             | Result      |
| ----------------- | ----------- |
| Claude Sonnet 3.5 | ✅ Excellent |
| Claude Sonnet 4   | ✅ Excellent |
| Claude Opus       | ✅ Excellent |
| Cursor Agents     | ✅ Works     |
| MCP Agents        | ✅ Works     |

---

# 🛠 Best Practices

### Ask for async explicitly

Good prompt:

```
Write async AMPHP v3 code for this API client
```

Bad prompt:

```
Write PHP HTTP client
```

---

### Provide context

```
Use amphp/http-server
Use Revolt event loop
Use async concurrency
```

---

### Combine with other skills

Works great with:

* **PHP refactor skills**
* **async architecture skills**
* **performance optimization skills**

---

# ⚠️ Limitations

* Not designed for **AMPHP v2**
* Assumes **PHP 8.1+**
* Works best when prompts mention **async or AMPHP**

---

# 📜 License

MIT License

---

# ⭐ Support the Project

If this skill helped you:

⭐ **Star the repository**

[https://github.com/opencck/skill-amphp](https://github.com/opencck/skill-amphp)

It helps other developers discover it.

---

# 🇷🇺 Русская версия

<details>
<summary>Открыть описание на русском</summary>

### Что делает этот skill

Помогает AI-ассистентам писать **асинхронный PHP код с AMPHP v3** без типичных ошибок.

Исправляет:

* блокирующий I/O
* устаревший AMPHP v2 код
* неправильные async-паттерны

### Установка

```
git clone https://github.com/opencck/skill-amphp ~/.claude/skills/amphp
```

### Использование

Просто пишите:

```
Convert this code to AMPHP async
```

или

```
Create async HTTP server using amphp
```

Skill активируется автоматически.

</details>

---

⭐ If you like this project — **give it a star!**
