# Proposal: `coc-helper` Skill (v0.1 — original draft)

> Status note (v1.0): This document is the **original design proposal** kept for historical reference. The current implementation may differ; see [SKILL.md](./SKILL.md) for the authoritative v1.0 description. Notable divergences are flagged inline as **[v1.0 divergence]**.

A Call of Cthulhu 7th Edition dice & Keeper assistant skill, designed for running COC tabletop sessions.

---

## 1. Motivation & Design Goals

A lightweight, offline-first dice and Keeper assistant for Call of Cthulhu 7th Edition tabletop sessions. The skill is built around the following goals:

| Goal          | How `coc-helper` achieves it                                                            |
| ------------- | --------------------------------------------------------------------------------------- |
| System        | COC 7e (d100 roll-under, success levels, bonus/penalty dice, SAN chains)                |
| Randomness    | `node cli.mjs ...` helper, **deterministic & seedable** via `--seed`                    |
| External deps | **Zero network deps** — all data ships inline                                           |
| State         | **Session state** (investigators, SAN, HP, MP, luck, rules) persisted to JSON           |
| Output format | Text **and** `--json` for programmatic chaining                                         |
| Tables        | Rollable tables (phobias, manias, occupation skills, names, hooks)                      |
| Modularity    | Modular: `dice.mjs`, `investigator.mjs`, `tables.mjs`, `sanity.mjs`, `rules-config.mjs` |

### Key design principles

1. **Offline-first.** All data is shipped inline so the skill works air-gapped — no API to rate-limit, go offline, or change schema.
2. **Reproducible rolls.** `--seed <n>` flag for verifiable / shareable rolls (useful for Play-by-Post and dispute resolution).
3. **Stateful sessions.** Track multiple investigators across rolls — SAN, HP, MP, luck, current skill ratings — instead of treating each roll as isolated.
4. **System-specific mechanics baked in.** Bonus/penalty dice, regular/hard/extreme success levels, opposed rolls, pushed rolls, sanity loss chains — not just "roll XdY".
5. **Smaller, testable surface.** Each command is a pure function over JSON; easy to unit-test and to extend (e.g., Pulp Cthulhu toggle).
6. **Configurable rules.** Critical/Fumble ranges and SAN thresholds can be customized per session, with preset `strict` / `lenient` variants.

---

## 2. Feature Set

> [v1.0 divergence] Sub-command syntax differs from this draft. The shipped CLI uses `roll opposed`, `roll push`, `roll luck <name>` as separate sub-commands rather than `--opposed` / `--push` / `--luck` flags. `--secret` Keeper-only rolls and `--luck <amount>` spend-to-lower are **not implemented** (only `luck-gain` between-session recovery). `inv update <field>=<value>` is **not implemented**. `loom` scene generator was renamed to `table hook`.

### 2.1 Dice rolling (core)

- `roll 1d100` — percentile check vs a target number
- `roll 3d6*5` — characteristic rolls (COC 7e convention)
- `roll 2d6+3` — generic polyhedral
- Success level auto-detected when a target is supplied: **Critical (01) / Extreme (½) / Hard (½ of target / 2) / Regular / Failure / Fumble**
- `--bonus N` / `--penalty N` — roll extra tens-digit dice, keep favorable / unfavorable (1 or 2)
- `roll opposed <a> <b>` — compare two checks (higher success level wins; tie → higher target wins)
- `roll push <spec> --target N` — re-roll a failed check (cannot be used on luck / SAN / combat / damage)
- `roll luck <name>` — luck check vs investigator's luck pool
- [v1.0 divergence] `--secret` — **not implemented**

### 2.2 Sanity

- `san check <name> <loss>` — roll d100 vs current SAN, compute SAN loss, deduct, flag possible bouts of madness
  - [v1.0] `<loss>` accepts `X/Y` expression (loss on success / loss on failure), e.g. `1/1d4`, `0/1d6`, `1d10/1d100`
- `san gain <name>` — recover d10 at session end
- `san private <name> [--psy N]` — private/home care
- `san institution <name>` — institutional care
- `san threshold <name>` — show SAN, insanity threshold
- [v1.0] Temporary insanity triggers when single-loss ≥ `tempInsanityThreshold` (default 5) **and** INT check fails; duration is **1D10 hours** (not rounds). INT check success suppresses the memory.
- [v1.0] Indefinite insanity triggers on single-loss ≥ `indefiniteInsanitySingleLoss` (default 20) **or** daily cumulative loss ≥ 1/5 of current SAN.
- [v1.0] Permanent insanity when SAN reaches 0.

### 2.3 Investigators (stateful)

- `inv create --name X --age N [--occupation Y] [--pulp]` — guided 7e character creation
- `inv list` — show all tracked investigators
- `inv show <name>` — full sheet
- `inv damage <name> <N>` — apply damage, track HP / major wound / dying
- `inv heal <name> <N>` — heal HP
- `inv delete <name>` — remove
- `inv derive --str N ...` — compute derived stats only
- [v1.0] `inv growth <name> <skill>...` — between-session skill growth
- [v1.0] `inv luck-gain <name>` — between-session luck enhancement
- [v1.0 divergence] `inv update <field>=<value>` — **not implemented**
- State file: `.trae/skills/coc-helper/session.json`

### 2.4 Keeper helpers

- `table name [--male|--female] [--zh|--en]` — random names
- `table npc [--zh|--en]` — quick NPC with occupation & demeanor
- `table phobia` / `table mania` / `table occupations` / `table weapons [name]` — rollable 7e tables
- `table madness [--summary]` — madness bout tables
- `table hook` — scene / hook prompt generator (seeded phrase tables, no AI calls)
- `combat init name1:DEX ...` — DEX-based initiative list
- `combat chase name1:MOV ...` — MOV-based chase initiative

### 2.5 Rules configuration (added in v1.0)

- `config show` / `config defaults` / `config reset`
- `config variant [strict|lenient]` — preset rule variants
- `config set <key> <value>` — customize:
  - `criticalRange` (e.g. `1` or `1-5`)
  - `fumbleRange` (e.g. `100`, `96-100`, or `auto`)
  - `tempInsanityThreshold` (default 5)
  - `indefiniteInsanitySingleLoss` (default 20)
  - `indefiniteInsanityDailyFraction` (default 0.2)

### 2.6 Output

- Human-readable by default
- `--json` on every command for chaining / programmatic use
- `--quiet` for terse inline output (just the total)

---

## 3. Architecture

```
.trae/skills/coc-helper/
├── SKILL.md              # English entry (v1.0, Trae skill loader)
├── SKILL.zh.md           # Chinese version (v1.0)
├── PROPOSAL.md           # English proposal (v0.1 original draft)
├── PROPOSAL.zh.md        # Chinese proposal (v0.1 original draft)
├── lib/
│   ├── dice.mjs          # Pure dice + COC success-level logic
│   ├── investigator.mjs  # Stateful CRUD over session.json
│   ├── sanity.mjs        # SAN check chain & madness flags
│   ├── tables.mjs        # Inline data: names, occupations, phobias, manias, hooks
│   └── rules-config.mjs  # Rules configuration system (added in v1.0)
├── cli.mjs               # argv parsing, dispatches to lib/*
└── session.json          # Auto-created on first stateful command (gitignored)
```

- **Language:** Node.js (ESM, zero npm deps — only `node:crypto` for RNG). Aligns with the JS-flavored workspace and avoids the Python toolchain assumption.
- **RNG:** `crypto.randomInt` for cryptographic-quality randomness; `--seed` mixes into a deterministic PRNG (mulberry32) for reproducible runs.
- **State:** single JSON file, atomic writes via `fs.rename` to a temp file.
- **Skill interface:** `SKILL.md` tells the agent to invoke `node <skill-dir>/cli.mjs <args>`. The agent formats results for the user.

---

## 4. SKILL.md Trigger Examples

The agent should invoke `coc-helper` when the user says things like:

- "Roll a sanity check for Anna, she's at 65 SAN, lose 1/1d4"
- "Roll 1d100 vs 60 with a penalty die"
- "Create a new COC investigator"
- "Opposed roll: Anna Spot Hidden 55 vs the cultist's 40"
- "Push the roll"
- "Give me a random 1920s NPC"
- "Switch to lenient rules: critical 1-5, fumble 96-100"

Non-triggers: generic dice (`roll 2d6` with no COC context) — handled inline by the agent unless the user explicitly asks for `coc-helper`.

---

## 5. Implementation Phases

1. **Phase 1 — Dice core.** `dice.mjs` + `cli.mjs` supporting `roll`, success levels, bonus/penalty dice, `--json`, `--seed`. No state.
2. **Phase 2 — Sanity.** `sanity.mjs` with SAN check chain logic and madness flagging.
3. **Phase 3 — Investigators.** `investigator.mjs` with create/list/show/damage/heal and `session.json` persistence.
4. **Phase 4 — Tables & Keeper helpers.** `tables.mjs` with names, occupations, phobias, manias, hooks; `chase init` / `combat init`.
5. **Phase 5 — SKILL.md + polish.** Frontmatter, invocation guide, examples, error messages.
6. **Phase 6 — Rules configuration (v1.0).** `rules-config.mjs` with default values, preset variants, persistent customization.

Each phase ships a runnable CLI; nothing is hidden behind a future phase.

---

## 6. Decisions (locked)

1. **Edition:** COC 7e + Pulp Cthulhu toggle (`--pulp` flag and `pulp: true` in session.json). No 6e.
2. **Setting:** 1920s classic — default tables use 1920s names/occupations/hooks. Modern/Pulp tables added behind the pulp flag where relevant.
3. **RNG:** `node:crypto.randomInt` by default; `--seed <n>` switches to a seeded mulberry32 PRNG for reproducible rolls.
4. **Runtime:** Node.js ESM, zero npm deps.
5. **State location:** `.trae/skills/coc-helper/session.json` (skill-local, gitignored).
6. **Skill name:** `coc-helper` (renamed from `coc-keeper` in v1.0 to better reflect "assistant" rather than "warden" role).
7. **[v1.0] Critical/Fumble ranges:** user-configurable; default `strict` = critical 1, fumble auto (96-100 if target<50 else 100); `lenient` = critical 1-5, fumble 96-100.

### Pulp Cthulhu additions (Phase 4) — [v1.0: partially implemented]

- [v1.0: implemented] `--pulp` doubles HP (HP = (SIZ + CON) / 5 instead of /10)
- [v1.0: not implemented] Hero points, two-fisted combat, pulp-archetype table

---

## 7. Data Source & Reference Tables

All numerical tables below are sourced from `coc7空白人物卡CY23.2Plus.xlsx` (by 丛雨, 2023/04) and cross-checked against the COC 7e Keeper Rulebook. They are embedded inline in `lib/tables.mjs` so the skill works offline.

### 7.1 Characteristics (rolled at creation)

| Characteristic | Roll        | Range                                                         |
| -------------- | ----------- | ------------------------------------------------------------- |
| STR            | 3d6 × 5     | 15–90                                                         |
| CON            | 3d6 × 5     | 15–90                                                         |
| DEX            | 3d6 × 5     | 15–90                                                         |
| APP            | 3d6 × 5     | 15–90                                                         |
| POW            | 3d6 × 5     | 15–90                                                         |
| SIZ            | (2d6+6) × 5 | 40–90                                                         |
| INT            | (2d6+6) × 5 | 40–90                                                         |
| EDU            | (2d6+6) × 5 | 40–90                                                         |
| Luck           | 3d6 × 5     | 15–90 (rolled separately; 15–19 age rolls twice, keep higher) |

### 7.2 Derived stats

- **HP** = floor((CON + SIZ) / 10), minimum 1 (Pulp: /5)
- **MP** = floor(POW / 5)
- **SAN** (initial) = POW; SAN (max) = 99 − Cthulhu Mythos skill
- **Dodge** (initial) = floor(DEX / 2)
- **Native language** (initial) = EDU
- **Interest skill points** = INT × 2
- **Damage Bonus (DB) & Build** (STR+SIZ table):

  | STR+SIZ     | DB   | Build |
  | ----------- | ---- | ----- |
  | 2–64        | −2   | −2    |
  | 65–84       | −1   | −1    |
  | 85–124      | 0    | 0     |
  | 125–164     | +1d4 | 1     |
  | 165–204     | +1d6 | 2     |
  | 205–244     | +2d6 | 3     |
  | 245–284     | +3d6 | 4     |
  | 285–324     | +4d6 | 5     |
  | 325–364     | +5d6 | 6     |
  | … (+40/step | +1d6 | +1    |

- **MOV** (base 9 for 1920s/modern humans):
  - +1 if both STR and DEX > SIZ
  - −1 if both STR and DEX ≤ SIZ
  - Age penalty: 40+ → −1, 50+ → −2, 60+ → −3, 70+ → −4, 80+ → −5 (auto-calculated)

### 7.3 Age adjustments

| Age   | EDU checks        | STR+SIZ / STR+CON+DEX | APP | Luck                    |
| ----- | ----------------- | --------------------- | --- | ----------------------- |
| 15–19 | −5 EDU            | STR+SIZ total −5      | —   | Roll twice, keep higher |
| 20–39 | 1 EDU enhancement | —                     | —   | —                       |
| 40–49 | 2 EDU enhancement | STR+CON+DEX total −5  | −5  | —                       |
| 50–59 | 3 EDU enhancement | STR+CON+DEX total −10 | −10 | —                       |
| 60–69 | 4 EDU enhancement | STR+CON+DEX total −20 | −15 | —                       |
| 70–79 | 4 EDU enhancement | STR+CON+DEX total −40 | −20 | —                       |
| 80–89 | 4 EDU enhancement | STR+CON+DEX total −80 | −25 | —                       |

EDU enhancement check: roll d100 ≥ current EDU on a success raises EDU by 1d10 (cap 99).

### 7.4 Success levels (COC 7e d100 roll-under)

| Result (d100)                               | Level            |
| ------------------------------------------- | ---------------- |
| ≤ target × 1/5                              | Extreme success  |
| ≤ target × 1/2                              | Hard success     |
| ≤ target                                    | Regular success  |
| > target                                    | Failure          |
| Critical range (default 1; lenient 1-5)     | Critical success |
| Fumble range (default auto; lenient 96-100) | Fumble           |

> [v1.0] Critical/Fumble ranges take precedence over regular success/failure when the die falls in their range, even if it crosses the target.

### 7.5 Sanity rules

- SAN check: d100 vs current SAN. Loss values come from the source of trauma (monster / spell / scene), expressed as `X/Y` (success-loss / failure-loss).
- If SAN loss ≥ `tempInsanityThreshold` (default 5) in a single check → INT check:
  - Success → memory suppressed, no insanity bout
  - Failure → temporary insanity bout, duration **1D10 hours**
- Single SAN loss ≥ `indefiniteInsanitySingleLoss` (default 20) → indefinite insanity.
- Daily cumulative SAN loss ≥ 1/5 of current SAN → indefinite insanity.
- SAN reaches 0 → permanent insanity.
- **SAN recovery:**
  - Private/home care: monthly d100, 01–95 (or under Psychoanalysis skill) → recover 1d3 SAN + sanity check to exit insanity; 96–00 → lose 1d6 SAN.
  - Institutional care: monthly d100, 01–50 → recover 3 SAN + sanity check to exit; 51–95 → no effect; 96–00 → lose 1d6 SAN.
- **Interlude SAN gain:** when an investigator has any skill at 90+ at session end, gain 2d6 SAN (cannot exceed SAN max).

### 7.6 Bonus & penalty dice

- Roll two tens-digit dice (00, 10, …, 90) and one ones-digit die.
- **Bonus:** keep the lower tens value.
- **Penalty:** keep the higher tens value.
- Ones digit is shared.
- [v1.0] Supports 1 or 2 bonus/penalty dice (`--bonus 2` / `--penalty 2`).

### 7.7 Opposed checks

- Both sides roll d100 vs their target.
- Higher success level wins (Critical > Extreme > Hard > Regular).
- Tie on success level → higher roll value wins (i.e., rolled higher but still succeeded).
- Opposed checks cannot be pushed.

### 7.8 Pushed rolls

- On a failed check, investigator may push once: re-roll d100 vs the same target.
- Cannot push combat rolls, SAN checks, or opposed checks (per 7e RAW).
- Consequence on failure is escalated (Keeper's call).

### 7.9 Luck

- [v1.0] `roll luck <name>` — roll d100 vs investigator's luck score as a target.
- [v1.0] `inv luck-gain <name>` — between-session luck enhancement (1d100 > current luck → +1d10, cap 99).
- [v1.0 divergence] `--luck <amount>` spend-to-lower — **not implemented**.
- Luck pool refreshes per Keeper ruling.

### 7.10 Embedded data tables (from the xlsx)

These sheets are extracted to JSON and shipped in `lib/tables.mjs`:

| Source sheet                 | Data                                                                                                                            |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 职业列表 (Occupations)       | Selected 30 occupations: credit rating range, occupational attribute formula, skill list, contacts, description                 |
| 本职技能 (Occupation skills) | Skill-group definitions used by occupations                                                                                     |
| 武器列表 战斗 (Weapons)      | Selected 22 weapons: type, skill, damage, range, penetration, attacks/round, magazine, malfunction, era, price (1920s / modern) |
| 疯狂表 (Madness)             | 10 instant-sanity symptoms, 10 summary-sanity symptoms, phobia table, mania table                                               |
| 资产及物价参考 (Assets)      | (future) Credit-rating → cash/assets levels, item prices                                                                        |
| 技能注释 (Skill notes)       | Skill list with base success rates, success-tier meanings                                                                       |
| 属性注释 (Attribute notes)   | Characteristic roll formulas, DB/Build/MOV tables, age adjustment tables                                                        |

### 7.11 Weapon data sample (first 5 rows from the sheet)

| Weapon                    | Skill | Damage   | Range   | Penetrate | Atk/Rnd | Magazine | Malfunction | Era           | Price (1920s/modern $) |
| ------------------------- | ----- | -------- | ------- | --------- | ------- | -------- | ----------- | ------------- | ---------------------- |
| 弓箭 (Bow)                | 弓术  | 1d6+½DB  | 30 yd   | ×         | 1       | 1        | 97          | 1920s, modern | 7 / 75                 |
| 黄铜指节 (Brass Knuckles) | 斗殴  | 1d3+1+DB | contact | ×         | 1       | —        | —           | 1920s, modern | 1 / 10                 |
| 长鞭 (Whip)               | 鞭子  | 1d3+½DB  | 10 ft   | ×         | 1       | —        | —           | 1920s         | 5 / 50                 |
| 燃烧的火把 (Torch)        | 斗殴  | 1d6+burn | contact | ×         | 1       | —        | —           | 1920s, modern | 0.05 / 0.5             |
| 电锯 (Chainsaw)           | 电锯  | 2d8      | contact | √         | 1       | —        | 95          | modern        | — / 300                |

> [v1.0] Note: an earlier draft mistranslated "Brass Knuckles" as "黄铜指铜" (zh) / "黄铜指北" — corrected to "黄铜指节".

---

## 8. Next Step

[v1.0 status] All six phases are implemented. Future work may include: full 180+ weapon table, 100+ occupation table, `--secret` rolls, `--luck <amount>` spend, Pulp Cthulhu hero points.
