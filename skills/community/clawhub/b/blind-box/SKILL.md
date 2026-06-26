---
name: blind-box
version: 1.0.0
author: jiajiaoy
homepage: https://clawhub.ai/skills/blind-box
description: "Virtual blind box gacha skill — pull random collectible figures with rarity tiers (Common to Limited), 5 themed series, 10-pull mode, daily free pull, and shareable reveal cards."
keywords:
  - blind box
  - 盲盒
  - gacha
  - gacha game
  - collectible
  - random
  - lucky draw
  - surprise box
  - mystery box
  - rarity
  - hidden figure
  - limited edition
  - pop mart
  - 泡泡玛特
  - 抽卡
  - 十连抽
  - 隐藏款
  - 限定款
  - daily pull
  - 每日盲盒
  - fun
  - shareable
  - 分享
  - virtual collectible
  - anime figure
  - 手办
---

# Blind Box

Pull virtual blind boxes with a full rarity system — from Common to ultra-rare Limited editions. Five themed series, 10-pull mode, daily free pull, and beautiful shareable reveal cards.

## Series

| Series | Theme | Figures |
|--------|-------|---------|
| 🐱 猫咪日常 | Daily Cat | 12 figures |
| 🚀 宇宙探险 | Space Explorer | 10 figures |
| 🍜 美食精灵 | Food Spirit | 10 figures |
| 🌸 四季精灵 | Season Spirit | 8 figures |
| ⚔️ 古风仙侠 | Wuxia | 12 figures |

## Rarity

| Rarity | Rate |
|--------|------|
| ⚪ 普通款 Common | 55% |
| 🔵 稀有款 Rare ★ | 25% |
| 🟡 超稀有 Super Rare ★★ | 12% |
| 🟠 史诗款 Epic ★★★ | 6% |
| 🟣 隐藏款 Hidden ✦ | 1.5% |
| 🔴 限定款 Limited ✦✦ | 0.5% |

## Commands

```bash
# Single pull (random series)
node scripts/pull.js

# Choose a series
node scripts/pull.js --series cat
node scripts/pull.js --series space
node scripts/pull.js --series food
node scripts/pull.js --series spirit
node scripts/pull.js --series wuxia

# 10-pull
node scripts/pull.js --series cat --count 10

# Daily free pull (slightly better rates)
node scripts/daily.js

# Browse all series
node scripts/series.js

# English output
node scripts/pull.js --lang en
node scripts/daily.js --lang en
```
