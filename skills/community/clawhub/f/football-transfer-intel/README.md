# Football Transfer Intel — Real-Time Rumour Intelligence

> Track football transfer rumours in real time. AI Truth Meter scores credibility 0–100 across 137,000+ transfer events.

[![ClawHub](https://img.shields.io/badge/ClawHub-football--transfer--intel-orange)](https://clawhub.ai/leeleon/football-transfer-intel)
[![API](https://img.shields.io/badge/API-api.risingtransfers.com-blue)](https://api.risingtransfers.com)

---

## What It Does

Stop guessing which football transfer stories are real. This skill aggregates data from **3 independent sources** and runs each rumour through an AI Truth Meter that scores it 0–100:

- **0–30**: Speculation / clickbait
- **31–60**: Emerging rumour, early signals
- **61–80**: Credible, multiple source confirmation
- **81–100**: Likely confirmed, official signals detected

**Hot Topics** (trending transfers right now) are always **free — no API key needed**.

---

## Example Queries

```
"What are the hottest football transfer rumours right now?"
"How credible is Gyökeres to Arsenal?"
"Is the Osimhen to Chelsea deal actually happening?"
"Rate the truth of the Salah to Saudi Arabia transfer story"
"What are the latest rumours around Mbappé?"
```

---

## Example Output

```
📡 Truth Meter: Gyökeres → Arsenal

Score: 78/100 — LIKELY ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━

Source Authority:   34/40  (Romano, Sky Sports, Record)
Official Signals:   17/20  (Agent contacted, Club negotiating)
Progress Signals:   15/20  (Medical rumoured, fee agreed)
Market Heat:        12/20  (€80M reported)

Top Sources: Fabrizio Romano (★★★★★), Sky Sports (★★★★)
Last updated: 2 hours ago
```

---

## Three Modes

| Mode | What It Does | Credits |
|------|-------------|---------|
| **Hot Topics** | Live trending football transfers | 0 (free) |
| **Transfer Detail** | Full rumour profile for a player | 3 credits |
| **Truth Meter** | AI credibility score for a specific link | 1–5 credits |

---

## Installation

1. Install from [ClawHub](https://clawhub.ai/leeleon/football-transfer-intel)
2. Get your free API key at [api.risingtransfers.com](https://api.risingtransfers.com)
3. Set your key:

```bash
claw env set RT_API_KEY=rt_sk_your_key_here
```

> Hot Topics work immediately with no key required.

---

## Pricing

| Plan | Price | Queries/Day |
|------|-------|-------------|
| Free | $0 | 10 hot topics + 3 detailed queries |
| Pro | $29/mo | 1,000 req/day |
| Business | $99/mo | 5,000 req/day |

Get your key: [api.risingtransfers.com](https://api.risingtransfers.com)

---

## Data Sources

- **Transfermarkt** — Europe's most comprehensive transfer database
- **Sportmonks** — Professional football data API
- **Social intelligence** — Twitter/X signals, journalist credibility weighting

**137,000+** transfer events tracked across all major leagues.

---

## Support

- Docs & API: [api.risingtransfers.com](https://api.risingtransfers.com)
- Email: api@risingtransfers.com
- GitHub: [LeoandLeon/rising-transfers-clawhub-skills](https://github.com/LeoandLeon/rising-transfers-clawhub-skills)
