# 🛒 Best Product Recommender

Find the best products in any category with expert picks, value recommendations, and budget options across US, UK, and EU retailers.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-1.0.2-blue)](https://github.com/openclaw/skills)
[![Platform](https://img.shields.io/badge/Platform-OpenClaw-green)](https://openclaw.ai)

## Features

- 🎯 **Expert Picks** — Top-rated products from trusted sources
- 💎 **Best Value** — Best performance per euro/dollar/pound
- 💶 **Budget Options** — Solid picks under $50/£40/€50
- 🌍 **Multi-Region** — US, UK, Germany, France, Italy, Spain, NL, BE, PL, EU
- 📦 **Price Comparison** — Lowest price including shipping
- ⏱️ **6-Hour Cache** — Fast responses, fresh data

## Installation

```bash
clawhub install best-product
```

Or manually: Copy `SKILL.md` to your skills folder.

## Usage

```bash
# Netherlands (default — Ralph is based in NL)
/best earbuds
/best airfryer
/best laptop

# Override per query — UK
/best earbuds uk

# Germany
/best earbuds de
/best toaster de

# France
/best headphones fr

# Italy
/best headphones it

# Spain
/best headphones es

# Belgium
/best headphones be

# Poland
/best laptop pl

# EU (generic)
/best laptop eu
```

## Supported Regions

| Region | Retailers |
|--------|-----------|
| **NL (default)** | Amazon NL, Coolblue, MediaMarkt |
| UK | Amazon UK, Currys, John Lewis |
| DE | Amazon DE, MediaMarkt, Saturn, Otto, Coolblue |
| FR | Amazon FR, Fnac, Darty, Boulanger |
| IT | Amazon IT, MediaMarkt, Unieuro |
| ES | Amazon ES, MediaMarkt, El Corte Inglés |
| BE | Amazon BE, MediaMarkt, Coolblue |
| PL | Amazon PL, Media Expert, RTV Euro AGD |
| US | Amazon, Best Buy, Walmart |
| AT | Amazon AT, MediaMarkt AT |
| SE | Amazon SE, MediaMarkt SE |
| DK | Amazon DK |
| FI | Amazon FI |
| CH | Amazon CH |

## Review Sources

- **US:** Wirecutter, RTINGS, Consumer Reports
- **UK:** TechRadar UK, Which?
- **NL:** Tweakers, Kieskeurig, Consumentenbond
- **DE:** Testberichte.de, Stiftung Warentest
- **FR:** 01net, Les Numériques
- **IT:** Altroconsumo
- **ES:** Xataka
- **PL:** Benchmark.pl, Komputer Świat
- **BE:** Test-Aankoop

## Output Example

```
🎧 /best earbuds

📍 NL — 8 mrt 2026

🏆 TOP PICK
Sony WF-1000XM5
€182 • Amazon
Kleinste behuizing, beste ANC ooit, 8u accu
https://www.google.nl/search?q=Sony+WF-1000XM5

💎 BEST VALUE
OnePlus Buds Pro 3
€109 • Proshop
Uitstekend geluid, prima ANC, 43u met case
https://www.google.nl/search?q=OnePlus+Buds+Pro+3

💶 BUDGET
Sony WF-C710N
€76 • Amazon
Goede ANC voor de prijs, 8.5u batterij
https://www.google.nl/search?q=Sony+WF-C710N

Sources: AndroidPlanet, Consumentenbond
```

## Link Verification

All output URLs are Google search links — user clicks to see current prices at local retailers. No direct retailer links (these often block or change).

## Security & Privacy

- **Data leaving the machine:** Product search terms → Brave Search API; product names → Google Search links (for price comparison)
- **Data at rest:** Results cached locally for 6 hours in `~/.openclaw/cache/best-products/` (optional — can be cleared)
- **Region default:** NL (Netherlands) — override with `/best earbuds de` etc.
- **No credentials required:** Uses OpenClaw's built-in web_search and web_fetch
- **No PII:** No user identifiers, emails, or personal information processed

## Technical Details

- **Cache:** 6 hours in `~/.openclaw/cache/best-products/` (optional)
- **Default region:** NL (can be overridden: `/best earbuds de`, `/best laptop uk`, etc.)
- **No credentials required:** Uses OpenClaw's web_search and web_fetch

## License

MIT License — See [LICENSE](LICENSE) for details.

## Author

OpenClaw Community

---

*Part of the OpenClaw skill ecosystem — discover more at [clawhub.ai](https://clawhub.ai)*
