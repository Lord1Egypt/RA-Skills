---
name: AB-Agents-Meter-Reader
description: "📊 Read meter readings from photos. Electricity (day/night tariffs) and water meters. Saves history and generates messages for landlord."
version: 1.0.0
author: AB-Agents
homepage: https://github.com/alexburrstudio/ab-agents-meter-reader
license: MIT
tags: ["meters", "utilities", "readings", "electricity", "water", "ab-agents"]
acceptLicenseTerms: true
---

# AB Agents Meter Reader 📊

Read meter readings from photos — electricity and water meters.

## Features

- ⚡ Read electricity meters (single or dual tariff)
- 💧 Read water meters (hot and cold)
- 📝 Save readings history with dates
- 📨 Generate message for landlord
- 🔄 Track multiple apartments

## Setup

### Requirements

- MiniMax Token Plan API key (for vision)
- Linux/macOS

### Quick Start

```bash
# First run - it will ask questions
./meter-reader.sh

# Later runs - just send photos
./meter-reader.sh photo.jpg
```

## First Run Setup

The script will ask:

1. **Tenant name** — your name
2. **Apartment address** — full address
3. **Meter layout** — how to tell meters apart:
   - "left=hot,right=cold" (default)
   - Or custom description

## Supported Meter Types

### Electricity
- Single tariff
- Dual tariff (day/night) — T1=day, T2=night
- Multi-tariff (cycle through screens)

### Water
- Cold water (usually on left)
- Hot water (usually on right)
- Cubic meters (m³)

## Usage

```bash
# Interactive mode (asks for photo)
./meter-reader.sh

# With photo
./meter-reader.sh /path/to/meter.jpg

# Generate message for landlord
./meter-reader.sh --message
```

## How It Works

1. Analyzes photo using MiniMax VL API
2. Identifies meter type automatically
3. Reads the numbers
4. Saves to readings history
5. Generates formatted message

## History

Readings saved to: `~/.meter-readings/history.json`

Format:
```json
{
  "apartments": {
    "address": {
      "tenant": "Name",
      "layout": "left=hot,right=cold",
      "readings": [
        {"date": "2026-04-26", "electricity_day": 8495, "electricity_night": 3008, "water_cold": 423, "water_hot": 240}
      ]
    }
  }
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Wrong numbers | Check meter photo quality, ensure numbers are clear |
| Can't identify meter type | Name photo file: `electricity.jpg`, `water.jpg` |
| Vision error | Check MINIMAX_API_KEY is set |

---

**AB-Agents** 🦀

## Requirements

👁️ **[AB Agents Vision (MiniMax)](https://github.com/alexburrstudio/ab-agents-vision)** — Required for image analysis. Install first:
```bash
clawhub install AB-Agents-Vision-MiniMax
```

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
