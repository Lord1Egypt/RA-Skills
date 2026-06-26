---
name: claw-rpg
description: D&D 3.5 standard rules RPG character system for AI lobster assistants. Automatically generates a character sheet from SOUL.md and MEMORY.md, assigns one of 11 classes (barbarian/fighter/paladin/ranger/cleric/druid/monk/rogue/bard/wizard/sorcerer) and 6 stats mapped to D&D 3.5 ability scores (STR/DEX/CON/INT/WIS/CHA), tracks XP using D&D 3.5 standard formula (n*(n-1)/2*1000), computes derived stats (HP/AC/BAB/Fort/Ref/Will/Initiative), generates class feats, levels up with a prestige system, fires hidden easter egg flavor text during conversations, sends daily RPG reports, and includes an arena battle system. Use when: initializing a lobster's RPG character, syncing XP after conversations, checking level/stats/derived combat stats, running prestige, launching the character dashboard, or scheduling daily RPG status reports.
---

# Claw RPG 🦞⚔️

A D&D-style character growth system for AI lobster agents. Reads your `SOUL.md` + `MEMORY.md` to generate a character sheet, accumulates XP from token usage, levels up from 1 to 999, and occasionally fires hidden RPG flavor text mid-conversation.

## Quick Start

```bash
# 1. Initialize your character (reads SOUL.md + MEMORY.md)
node scripts/init.mjs

# 2. View your character sheet (terminal)
node scripts/sheet.mjs

# 3. Launch the web dashboard
cd dashboard && npm install && npm start     # http://localhost:3500
```

## Hidden Easter Egg Trigger (Recommended)

After each reply, `easter.mjs` fires with a **12% base probability** — appending a single line of italic RPG flavor text. Milestone conversations (10th, 25th, 50th, 100th, every 100 after...) always trigger.

```bash
node scripts/easter.mjs            # Normal call (updates conversation counter)
node scripts/easter.mjs --force    # Force trigger (debug)
node scripts/easter.mjs --preview  # Preview without writing to character data
```

**Integration** — add to your `AGENTS.md`:

```
After each reply to a user message, run: node <SKILL_ROOT>/scripts/easter.mjs
If the output is NOT __NO_TRIGGER__, append it to the reply (blank line + italic).
Do not run during heartbeat polls.
```

## Daily Greeting (Optional)

For a daily RPG-style self-intro on the first conversation of the day:

```bash
node scripts/greet.mjs             # Fires once per day (checks lastGreetDate)
node scripts/greet.mjs --force     # Force send
node scripts/greet.mjs --preview   # Preview without saving
```

## XP Sync

```bash
# Pass token delta from the current conversation
node scripts/xp.mjs --in 2000 --out 800

# With bonus XP (after completing a significant task)
node scripts/xp.mjs --in 2000 --out 800 --bonus 30

# Conversation count only
node scripts/xp.mjs --conversations 1
```

## Prestige (Lv.999 cap reached)

```bash
node scripts/levelup.mjs --prestige
```

Prestige resets level to 1, permanently boosts all stats by +10%, and unlocks a new title tier.

## Automated XP Sync (Recommended)

Set up a daily cron at 03:00 with the built-in setup script:

```bash
node scripts/setup-cron.mjs
```

Or call manually from a heartbeat/cron job:

```javascript
const { execSync } = require('child_process');
execSync(`node ${SKILL_ROOT}/scripts/xp.mjs --in ${deltaIn} --out ${deltaOut}`);
```

## Classes & Abilities

See `references/classes.md` and `references/abilities.md`

## Prestige System

See `references/prestige.md`

## Daily Report (v1.1.0)

Send a daily RPG status report to Telegram (level, stats, XP progress, class quip):

```bash
node scripts/report.mjs            # Send report now
node scripts/report.mjs --preview  # Preview without sending
```

Set up as an automated daily cron (default 18:00):

```bash
node scripts/setup-cron.mjs
```

## Arena (v1.1.0)

Battle other agents or NPCs. Results affect XP and morale:

```bash
node scripts/arena.mjs --opponent "Shadow Wizard"
node scripts/arena.mjs --list   # View battle history
```

## XP Recovery

If XP data gets out of sync, recover from session logs:

```bash
node scripts/sync-xp-recovery.mjs
```

## Files

| File | Description |
|------|-------------|
| `character.json` | Character data (auto-generated, do not edit manually) |
| `arena-history.json` | Arena battle history |
| `config.json` | Optional: Telegram notification config (`{ "telegram_chat_id": "..." }`) |

## What's New in v1.1.2

- **Save file protection** — `character.json` now stored in `~/.openclaw/workspace/claw-rpg/` instead of the skill directory. Reinstalling the skill no longer resets your level and XP.
- **Auto migration** — `init.mjs` automatically moves existing save data to the new location on first run.

## What's New in v1.1.0

- **Per-conversation XP** — `easter.mjs` now awards ~80 XP per conversation automatically
- **Daily Report** — `report.mjs` + `setup-cron.mjs` for automated daily status push to Telegram
- **Arena system** — `arena.mjs` for agent vs agent/NPC battles
- **XP Recovery** — `sync-xp-recovery.mjs` to repair XP sync issues
- **Milestone triggers** — Easter egg always fires at 10th, 25th, 50th, 100th, every 100 after
