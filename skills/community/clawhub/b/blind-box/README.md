# Blind Box — Virtual Gacha & Collectible Skill

> Pull random collectible figures with rarity tiers, 5 themed series, 10-pull mode, and shareable reveal cards.

[![clawhub](https://img.shields.io/badge/clawhub-blind--box-blue)](https://clawhub.ai/skills/blind-box)
[![openclaw](https://img.shields.io/badge/openclaw-skill-orange)](https://openclaw.ai)

## What it does

Blind Box brings the excitement of unboxing to your terminal. Pull from 5 themed series, chase ultra-rare Hidden and Limited editions, do a 10-pull for better odds, and get a daily free pull every day — all with beautiful reveal cards you can share.

**5 series** — Cats 🐱 · Space 🚀 · Food 🍜 · Seasons 🌸 · Wuxia ⚔️  
**6 rarity tiers** — Common / Rare ★ / Super Rare ★★ / Epic ★★★ / Hidden ✦ / Limited ✦✦  
**10-pull mode** — pull 10 at once, see your haul at a glance  
**Daily free pull** — slightly boosted rates, resets every day  
**Shareable cards** — beautifully formatted reveal cards to post  
**Bilingual** — Chinese and English output

## Rarity Rates

| | Rarity | Rate |
|-|--------|------|
| ⚪ | Common | 55% |
| 🔵 | Rare ★ | 25% |
| 🟡 | Super Rare ★★ | 12% |
| 🟠 | Epic ★★★ | 6% |
| 🟣 | Hidden ✦ | 1.5% |
| 🔴 | Limited ✦✦ | 0.5% |

## Installation

```bash
openclaw install blind-box
```

## Usage

```bash
# Single pull
node scripts/pull.js

# Pick a series: cat / space / food / spirit / wuxia
node scripts/pull.js --series cat

# 10-pull
node scripts/pull.js --series wuxia --count 10

# Daily free pull (boosted rates)
node scripts/daily.js

# Browse series
node scripts/series.js

# English mode
node scripts/pull.js --lang en
```

## Keywords

blind box · 盲盒 · gacha · gacha game · collectible · random · lucky draw · surprise box · mystery box · rarity · hidden figure · limited edition · pop mart · 泡泡玛特 · 抽卡 · 十连抽 · 隐藏款 · 限定款 · daily pull · 每日盲盒 · virtual collectible · 手办 · fun · shareable · anime figure · 开盒 · 抽盲盒

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai](https://clawhub.ai/skills/blind-box)
