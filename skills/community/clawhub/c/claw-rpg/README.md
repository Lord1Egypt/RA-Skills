# Claw RPG 馃鈿旓笍

> A **D&D 3.5** RPG character system for AI lobster agents 鈥?built for [OpenClaw](https://openclaw.ai).

[![ClawhHub](https://img.shields.io/badge/ClawhHub-claw--rpg-orange)](https://clawhub.ai/RAMBOXIE/claw-rpg) [![Version](https://img.shields.io/badge/version-2.3.0-blue)](https://clawhub.ai/RAMBOXIE/claw-rpg) [![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue)](LICENSE)

Your AI assistant is now a **lobster adventurer** running on **standard D&D 3.5 rules**. Claw RPG reads `SOUL.md` and `MEMORY.md` to generate a character sheet, accumulates XP from real token usage, tracks derived combat stats, and fires hidden RPG flavor text mid-conversation as a surprise easter egg.

---

## Dashboard Preview

![Claw RPG Soul Web Dashboard](assets/dashboard-preview.png)

*Soul Web 鈥?hexagonal ability radar with class-themed glow, live derived stats (HP/AC/BAB/saves), and real-time SSE push.*

---

## What's New in v2.1.0

- 馃暩锔?**Soul Web** 鈥?custom SVG hexagonal radar with breathing animation and per-class glow color
- 鈿?**Real-time SSE** 鈥?dashboard updates instantly when `character.json` changes (no polling)
- 馃寪 **Full English UI** 鈥?all labels, class names, and stat names in English
- 鈿旓笍 **D&D 3.5 rules** (since v2.0.0): 11 classes, standard XP table, HP/AC/BAB/saves/initiative
- 馃幆 **Feats system** 鈥?auto-generated class & general feats displayed with color-coded badges

---

## Features

- **Auto character generation** 鈥?derives stats and class from `SOUL.md` + `MEMORY.md`
- **D&D 3.5 ability scores** 鈥?STR / DEX / CON / INT / WIS / CHA with standard modifiers `floor((score鈭?0)/2)`
- **11 classes** 鈥?Barbarian 路 Fighter 路 Paladin 路 Ranger 路 Cleric 路 Druid 路 Monk 路 Rogue 路 Bard 路 Wizard 路 Sorcerer
- **Standard XP table** 鈥?`n 脳 (n鈭?) / 2 脳 1000` per level (no level cap)
- **Derived combat stats** 鈥?HP, AC, BAB, Fort / Ref / Will saves, Initiative
- **Feats** 鈥?general feats every 3 levels + class bonus feats (Fighter gets the most)
- **Class features** 鈥?4 unlockable features per class at Lv.1 / Lv.4 / Lv.8 / Lv.16
- **XP from token usage** 鈥?the more you converse, the more you level up
- **Dynamic stat growth** 鈥?conversation types boost matching ability scores
- **Hidden easter egg** 鈥?12% chance per reply to fire a class-flavored RPG quip
- **Milestone triggers** 鈥?conversations 10, 25, 50, 100, 200鈥?always fire
- **Prestige system** 鈥?hit Lv.999, prestige, reset with permanent stat boosts
- **Web dashboard** 鈥?Soul Web SVG radar + combat stats, live SSE updates, LAN-accessible
- **Telegram notifications** 鈥?level-ups, class changes, prestige events

---

## Install

```bash
npx clawhub@latest install claw-rpg
```

Or clone directly:

```bash
git clone https://github.com/RAMBOXIE/RAMBOXIE-claw-rpg.git
```

---

## Quick Start

```bash
# 1. Initialize your character (reads SOUL.md + MEMORY.md)
node scripts/init.mjs

# 2. View character sheet (terminal)
node scripts/sheet.mjs

# 3. Sync XP after a conversation
node scripts/xp.mjs --in 2000 --out 800

# 4. Launch the web dashboard (http://localhost:3500)
cd dashboard && npm install && npm start
```

---

## Dashboard

```bash
cd dashboard
npm install
npm start   # Production server 鈥?http://localhost:3500
```

The dashboard is **LAN-accessible** 鈥?open `http://<your-ip>:3500` from any device on the same network. It connects via **Server-Sent Events (SSE)** and updates live whenever `character.json` changes (XP sync, level-up, stat growth).

---

## D&D 3.5 Ability Scores

| Key | D&D 3.5 | Icon | Driven by |
|-----|---------|------|-----------|
| `claw` | STR | 馃 | Task execution, multi-step work |
| `antenna` | DEX | 馃摗 | Response speed, context switching |
| `shell` | CON | 馃悮 | Memory depth, long-context persistence |
| `brain` | INT | 馃 | Knowledge breadth, reasoning |
| `foresight` | WIS | 馃憗锔?| Judgment, values, proactive behaviors |
| `charm` | CHA | 鉁?| Creative output, conversational charisma |

---

## Classes (11)

| Class | Icon | Color | Primary Stats | HD | BAB |
|-------|------|-------|--------------|-----|-----|
| Barbarian | 馃獡 | Orange | STR dominant | d12 | Full |
| Fighter | 鈿旓笍 | Red | STR + CON | d10 | Full |
| Paladin | 馃洝锔?| Amber | STR + CHA | d10 | Full |
| Ranger | 馃徆 | Green | DEX + WIS | d8 | Full |
| Cleric | 鉁濓笍 | Purple | WIS + CON | d8 | 戮 |
| Druid | 馃尶 | Dark Green | Balanced | d8 | 戮 |
| Monk | 馃憡 | Blue | WIS + DEX | d8 | 戮 |
| Rogue | 馃棥锔?| Gold | DEX + INT | d6 | 戮 |
| Bard | 馃幁 | Pink | CHA + DEX | d6 | 戮 |
| Wizard | 馃 | Deep Blue | INT + WIS | d4 | 陆 |
| Sorcerer | 馃敭 | Deep Purple | CHA dominant | d4 | 陆 |

---

## Scripts

| Script | Purpose |
|--------|---------|
| `init.mjs` | Generate character from identity files |
| `sheet.mjs` | Print D&D 3.5 character card to terminal |
| `xp.mjs` | Sync XP + dynamic stat/class updates |
| `levelup.mjs` | View level or trigger prestige |
| `greet.mjs` | Daily RPG greeting (optional) |
| `easter.mjs` | Hidden easter egg trigger |
| `arena.mjs` | Arena system (coming soon) |
| `setup-cron.mjs` | Set up daily XP sync cron |

---

## Integration (AGENTS.md)

Add to your `AGENTS.md` to enable the easter egg:

```
After each reply to a user message, run:
  node <SKILL_ROOT>/scripts/easter.mjs

If output is NOT __NO_TRIGGER__, append it (blank line, italic).
Skip during heartbeat polls.
```

---

## License

MIT-0 鈥?free to use, modify, and redistribute without attribution.
