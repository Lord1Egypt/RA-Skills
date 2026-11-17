---
name: coc-helper
description: COC 7th Edition tabletop assistant. Dice rolling (success levels, bonus/penalty dice, critical/fumble), SAN system (X/Y loss expressions, temporary/indefinite insanity, INT check memory suppression), investigator management, madness tables / occupations / weapons / NPCs, combat initiative, configurable rules system (critical/fumble ranges, SAN thresholds, preset strict/lenient variants). Supports --seed for reproducible rolls, --json for programmatic chaining, and investigator state persistence.
---

# coc-helper v1.0 — COC 7e Tabletop Assistant

A command-line skill for running Call of Cthulhu 7th Edition tabletop sessions. All rule values are drawn from the COC 7e Keeper Rulebook and Investigator Handbook; some data tables reference the Congyu coc7 blank character sheet CY23.2 Plus (2023/04).

> Version note: This document describes the **v1.0 implemented state**. The original design proposal is at [PROPOSAL.md](./PROPOSAL.md) (v0.1 draft; some content has since been iterated). Chinese version: [SKILL.zh.md](./SKILL.zh.md).

## When to use

- A player or KP needs to **roll dice** (characteristics, damage, d100 checks)
- Need to **determine success level** (Critical / Extreme / Hard / Regular / Failure / Fumble)
- Handle **SAN checks**, loss resolution (X/Y expressions), temporary insanity, indefinite insanity, INT-check memory suppression, recovery
- **Create / manage investigators** (HP / SAN / MP / major wound / dying / skill growth / luck enhancement)
- Draw from **madness tables, phobias, manias**
- Generate **NPCs, names, plot hooks**
- Look up **occupations, weapons**
- Compute **combat / chase initiative**
- **Configure variable rules** (critical/fumble ranges, SAN thresholds)

## How to use

Entry script: `cli.mjs` (Node.js ESM, zero dependencies, requires Node ≥ 18).

Invocation: `node <skill-dir>/cli.mjs <command> [options]`

### Global options

- `--seed N`: use a seeded PRNG (mulberry32) for reproducible rolls; if omitted, `node:crypto` cryptographic randomness is used
- `--json`: JSON output for programmatic chaining
- `--quiet`: terse output (totals only)
- `-h, --help`: help

### Command reference

#### `roll <spec>` — Dice rolling

Supported expressions: `3d6*5` / `2d6+3` / `1d100` / `8d6` / `d20-2` (no division, no mixed multi-dice arithmetic).

- `--target N`: d100 check target value, triggers COC 7e success-level resolution
- `--bonus N` / `--penalty N`: number of bonus / penalty dice (1 or 2, mutually exclusive)

COC 7e success levels (default `strict` rules; switch with `config variant lenient`):

- ≤ target × 1/5 → Extreme success
- ≤ target × 1/2 → Hard success
- ≤ target → Regular success
- > target → Failure
- Critical: default die value = 01; under `lenient`, 1-5
- Fumble: default 96-100 when target < 50, or 100 when target ≥ 50; under `lenient`, always 96-100
- Range precedence: when a die falls in the Critical/Fumble range it takes precedence, even if it crosses the target

Sub-commands:

- `roll opposed <a> <b> [--a-label X --b-label Y]` — opposed check (higher success level wins; on a tie, higher target wins)
- `roll push <spec> --target N` — pushed roll (re-roll once on failure; cannot be used on luck, sanity, combat, or damage dice)
- `roll luck <name>` or `roll luck --target N` — luck check

**Examples:**

```
node cli.mjs roll 1d100 --target 60 --bonus 1
node cli.mjs roll 3d6*5 --seed 42
node cli.mjs roll opposed 55 45 --a-label "Dr. Chen" --b-label "Cultist"
node cli.mjs roll push 1d100 --target 50
node cli.mjs roll luck "Dr. Chen"
```

#### `san <action>` — Sanity system

Operates on an investigator's SAN. All SAN changes persist to `session.json`. Rule parameters can be tuned via the `config` command.

- `check <name> <loss>`: SAN check
  - `loss` accepts an `X/Y` expression (loss on success / loss on failure), e.g. `1/1d4` / `0/1d6` / `1/1d4+1` / `1d10/1d100`
  - Legacy form `san check <name> 1d4` is equivalent to `1/1d4`
  - Success (≤ SAN): lose X
  - Failure (> SAN): lose full Y
  - Fumble: lose the maximum possible value of Y (e.g. `1d4` → 4)
  - Critical: lose X (same as success)
  - Single loss ≥ tempInsanityThreshold (default 5) → triggers an INT check:
    - INT check succeeds → memory suppressed, no insanity
    - INT check fails → temporary insanity (duration 1D10 hours)
  - Single loss ≥ indefiniteInsanitySingleLoss (default 20) → indefinite insanity
  - SAN reaches 0 → permanent insanity
- `gain <name>`: end-of-session recovery d10 (capped at max)
- `private <name> [--psy N]`: private / home care (monthly; 01-95 or under Psychoanalysis skill → recover 1d3; 96-00 → lose 1d6)
- `institution <name>`: institutional care (monthly; 01-50 → recover 3; 51-95 → no effect; 96-00 → lose 1d6)
- `threshold <name>`: show current SAN thresholds

**Examples:**

```
node cli.mjs san check "Dr. Chen" 1/1d4 --seed 42
node cli.mjs san check "Dr. Chen" 0/1d6
node cli.mjs san gain "Dr. Chen"
node cli.mjs san private "Dr. Chen" --psy 60
```

#### `inv <action>` — Investigator management

Investigator state persists to `session.json`.

- `create --name X --age N [--occupation Y] [--pulp]`: create a character
  - Auto-rolls characteristics (STR/CON/DEX/APP/POW = 3d6×5, SIZ/INT/EDU = (2d6+6)×5, Luck = 3d6×5)
  - Auto-applies age adjustments (15-19 EDU -5 + Luck keeps higher; 20+ EDU enhancement checks; 40+ attribute penalties)
  - Auto-computes derived stats (HP/MP/SAN/DB/Build/MOV/Dodge)
- `list`: list all investigators
- `show <name>`: full sheet
- `damage <name> <N>`: apply damage (auto-marks major wound / dying / unconscious)
- `heal <name> <N>`: heal HP
- `delete <name>`: remove
- `derive --str N --con N --siz N --dex N --app N --int N --pow N --edu N [--age N] [--pulp]`: compute derived stats only (no character created)
- `growth <name> <skill1> [skill2 ...]`: between-session skill growth (1d100 vs current per skill; on success +1d10)
- `luck-gain <name>`: between-session luck enhancement (1d100 > current luck → +1d10, cap 99)

**Damage rules:**

- HP ≤ 0: dying (needs a CON check to stabilize, otherwise dies in 1d10 rounds)
- Single damage ≥ maxHp/2: major wound (needs a CON×5 check to avoid unconsciousness)
- HP = 0: unconscious

**Examples:**

```
node cli.mjs inv create --name "Dr. Chen" --age 35 --occupation "Doctor" --seed 42
node cli.mjs inv damage "Dr. Chen" 8
node cli.mjs inv growth "Dr. Chen" "Library Use" "Spot Hidden" "Listen"
node cli.mjs inv luck-gain "Dr. Chen"
node cli.mjs inv show "Dr. Chen"
```

#### `table <action>` — Table helpers

- `madness [--summary]`: draw from the madness table (default: instant symptoms 1d10; `--summary`: summary symptoms 1d10)
- `phobia`: random phobia (1d20)
- `mania`: random mania (1d20)
- `npc [--zh|--en]`: random NPC (name / gender / occupation / credit rating / skills / contacts; random language by default)
- `name [--male|--female] [--zh|--en]`: random name (random gender and language by default)
- `occupations`: list built-in occupations (30)
- `weapons [name]`: list weapons (22) / fuzzy-search by name
- `hook`: generate a plot hook (subject + threat + location)

**Examples:**

```
node cli.mjs table madness --summary
node cli.mjs table npc --zh --seed 7
node cli.mjs table weapons ".38"
```

#### `combat <action>` — Combat helpers

- `init name1:DEX name2:DEX ...`: combat initiative (DEX descending)
- `chase name1:MOV name2:MOV ...`: chase initiative (MOV descending)

**Examples:**

```
node cli.mjs combat init "Dr. Chen:60" "Cultist:50" "Monster:80"
node cli.mjs combat chase "Dr. Chen:8" "Cultist:7"
```

#### `config <action>` — Rules configuration

Variable rules / optional thresholds, persisted to `session.json`. Defaults to the `strict` variant (1/100).

- `show`: show current rules configuration
- `defaults`: show default rules configuration
- `set <key> <value>`: set a single option (see configurable keys below)
- `variant [name]`: list / apply a preset variant
  - `strict`: strict (rulebook baseline: critical 1, fumble 100 / 96-100 auto)
  - `lenient`: lenient (dramatic: critical 1-5, fumble 96-100)
- `reset`: reset to default rules

Configurable keys:

- `criticalRange`: critical-success die range (`"1"` or `"1-5"`)
- `fumbleRange`: fumble die range (`"100"` / `"96-100"` / `"auto"` for target-based auto)
- `tempInsanityThreshold`: single-loss threshold for temporary insanity (default 5)
- `indefiniteInsanitySingleLoss`: single-loss threshold for indefinite insanity (default 20)
- `indefiniteInsanityDailyFraction`: daily cumulative-loss fraction for indefinite insanity (default 0.2 = 1/5)

**Examples:**

```
node cli.mjs config show
node cli.mjs config variant lenient
node cli.mjs config set criticalRange 1-5
node cli.mjs config set fumbleRange auto
node cli.mjs config set tempInsanityThreshold 3
node cli.mjs config reset
```

## Data sources

- COC 7e Keeper Rulebook / Investigator Handbook
- Congyu coc7 blank character sheet CY23.2 Plus (2023/04): characteristic roll ranges, derived-stat formulas, age adjustments, SAN rules, weapon table, madness tables, phobias/manias, occupation list

## Architecture

```
coc-helper/
├── SKILL.md              # This file — English entry (v1.0 implementation reference, Trae skill loader)
├── SKILL.zh.md           # Chinese version (v1.0 implementation reference)
├── PROPOSAL.md           # English proposal (v0.1 original draft)
├── PROPOSAL.zh.md        # Chinese proposal (v0.1 original draft)
├── cli.mjs               # CLI entry (command dispatch + output formatting)
├── lib/
│   ├── dice.mjs          # Dice + COC 7e success levels (bonus/penalty dice, custom ranges)
│   ├── sanity.mjs        # SAN system (X/Y loss / temp insanity / indefinite insanity / INT suppression / recovery)
│   ├── investigator.mjs  # Investigator management (creation / age adjustments / derived stats / damage / growth / persistence)
│   ├── tables.mjs        # Inline data tables (madness / phobias / manias / occupations / weapons / NPCs / names / hooks / initiative)
│   └── rules-config.mjs  # Rules configuration system (defaults / preset variants / persistence)
└── session.json          # Investigator state + rules config persistence (auto-created at runtime)
```

## Design principles

1. **Zero dependencies**: only Node.js built-in modules (`node:crypto` / `node:fs` / `node:path`)
2. **Reproducible**: `--seed N` switches to a mulberry32 PRNG — same seed, same sequence
3. **Chainable**: `--json` emits structured data for other tools / AI consumption
4. **Persistent**: investigator state and rules config written to `session.json`, preserved across commands
5. **Offline-friendly**: all data tables are inline, no network required
6. **Configurable rules**: critical/fumble ranges, SAN thresholds, etc. are user-decidable, with sensible defaults and preset variants

## Limitations

- Dice expressions do not support mixed arithmetic (e.g. `2d6+1d4`); not needed for COC 7e character creation
- Weapon table is a curated subset (22 items); the full 180+ table can be expanded on demand
- Occupation table is a curated subset (30 items); the full 100+ occupations can be expanded on demand
- Does not include all Pulp Cthulhu rules (only `--pulp` HP doubling is supported)
- Does not include dynamic adjustment of the SAN cap by Cthulhu Mythos skill (default maxSan=99)
- No `--secret` hidden rolls, no `--luck <amount>` spend-to-lower (only between-session `luck-gain` is supported)
