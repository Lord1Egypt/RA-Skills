---
name: AB-Agents-Vision-MiniMax
description: "👁️ Image analysis via MiniMax VL API. Describe images, extract text from screenshots, analyze photos. Requires MiniMax Token Plan API key (free tier available)."
version: 1.0.1
author: AB-Agents
homepage: https://github.com/alexburrstudio/ab-agents-vision
license: MIT
tags: ["vision", "image", "minimax", "minimax-vl", "ocr", "screenshot", "text-extraction", "ab-agents"]
acceptLicenseTerms: true
---

# AB Agents Vision (MiniMax) 👁️

Image analysis via MiniMax VL API — simple, fast, reliable.

> ⚠️ **Requires MiniMax Token Plan API key** — [get free key](https://platform.minimax.io)

## What It Does

- 📸 **Describe images** — Get detailed scene descriptions
- 📝 **Extract text** — Read from screenshots, photos, documents
- 🔍 **Analyze photos** — Identify objects, people, settings
- 🌐 **URL support** — Analyze images from the web

## Requirements

- **MiniMax Token Plan API key** — [Subscribe free](https://platform.minimax.io)
- Linux/macOS
- `uvx` (auto-installed)

## Quick Start

```bash
# 1. Install uvx
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Get free MiniMax API key
# https://platform.minimax.io → Subscribe → Token Plan (free tier)

# 3. Use
export MINIMAX_API_KEY="sk-cp-your-key"
./vision.sh image.jpg "Describe this image"
```

## Usage

```bash
# Basic description
./vision.sh photo.jpg

# With custom prompt
./vision.sh screenshot.png "What text do you see?"

# URL support
./vision.sh "https://example.com/image.jpg" "Describe this"
```

## Examples

**Screenshot analysis:**
```
Input: screenshot.png + "What text is in the image?"
Output: "The screenshot shows a code editor with Python code..."
```

**Photo description:**
```
Input: photo.jpg + "Describe in detail"
Output: "A person's bare foot and lower leg resting on a brown
textured waffle-weave blanket. The skin is light-toned..."
```

## Installation

```bash
git clone https://github.com/alexburrstudio/ab-agents-vision.git
cd ab-agents-vision/skills/vision
chmod +x vision.sh
```

Or via ClaWHub:
```bash
clawhub install AB-Agents-Vision-MiniMax
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| API Error: 1033 | Retry — MiniMax system error |
| No response | Check MINIMAX_API_KEY is set correctly |
| Slow | Use smaller images (<10MB) |

---

**AB-Agents** 🦀

## Related Skills

📊 **[AB Agents Meter Reader](https://github.com/alexburrstudio/ab-agents-meter-reader)** — Read meter readings from photos (uses this skill for vision)

---

**AB-Agents** 🦀

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

*by [Alex Burr](https://t.me/AlexBurrOne) | [Канал AB Agents](https://t.me/alexburr_agents)*
