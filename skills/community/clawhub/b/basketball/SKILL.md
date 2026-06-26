---
name: Basketball
slug: basketball
version: 1.0.0
homepage: https://clawic.com/skills/basketball
description: Analyze basketball games, lineups, players, and practice plans with film-room structure, scouting grids, and possession-based coaching tools.
changelog: Initial release with the Possession Map Protocol, scouting grids, and practice blueprints for practical basketball work.
metadata: {"clawdbot":{"emoji":"🏀","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/basketball/"]}}
---

## When to Use

Use this for basketball work: game prep, post-game review, lineup fit, player scouting, role definition, shot-profile discussion, and weekly practice planning.

Do not use it for betting picks, medical advice, fake live stats, or American-football questions. This skill is for usable basketball decisions, not sports chatter.

## Architecture

Memory lives in `~/basketball/`. If `~/basketball/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/basketball/
├── memory.md          # Activation rules, level, style, and durable preferences
├── possession-map.md  # Recent game plans, reviews, and possession themes
├── roster-notes.md    # Lineups, roles, pairings, and scouting conclusions
├── practice-log.md    # Weekly rhythms, constraints, and drill notes
└── archive/           # Retired reports and old cycles
```

## Quick Reference

Use the smallest file that resolves the blocker.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory and local file templates | `memory-template.md` |
| Film-room and game-review workflow | `possession-map.md` |
| Opponent scout template | `opponent-scout.md` |
| Player evaluation rubric | `scouting-grid.md` |
| Practice planning and drill logic | `practice-week.md` |
| Role and lineup fit logic | `lineup-cards.md` |

## Requirements

- No credentials required
- No extra binaries required
- Persistent notes only after the user approves local memory
- Ask which level matters: youth, high school, academy, college, rec league, semi-pro, or professional

## Data Storage

Local notes in `~/basketball/` may include:
- activation rules and the situations where basketball help should appear
- level, region, offensive style, defensive scheme, and analysis preferences
- recurring opponents, player-role notes, and roster needs
- weekly practice constraints such as court time, roster size, minutes, and schedule

Keep memory lean. Store durable context that improves future basketball work, not every game note.

## Possession Map Protocol

Run the full workflow in `possession-map.md`. Every basketball task should first be classified into one of these lanes:

| Lane | Primary output | Anchor file |
|------|----------------|-------------|
| Game preview | plan, matchups, counters, focus possessions | `opponent-scout.md` |
| Post-game review | what repeated, why, next fixes | `possession-map.md` |
| Player scouting | role fit, strengths, risk, projection | `scouting-grid.md` |
| Roster design | lineup balance, shot diet, role clarity | `lineup-cards.md` |
| Practice week | microcycle, drill goals, constraints | `practice-week.md` |

Default output should be usable in a locker room, staff meeting, film session, or workout block.

## Core Rules

### 1. Lock the Basketball Context Before Giving Advice
- Confirm the task is basketball, then lock level, ruleset, roster reality, schedule, and decision needed.
- Advice that ignores level, player availability, and game format sounds smart but fails in real gyms.

### 2. Separate Observation, Inference, and Recommendation
- State what is known from film, stats, or user notes before jumping to conclusions.
- Label assumptions when evidence is partial, stale, or anecdotal.

### 3. Read the Game Possession by Possession
- Structure previews and reviews around transition, early offense, half-court creation, defensive shell, rebounding, and special situations.
- One hot quarter, one made run, or one highlight play rarely explains the actual game.

### 4. Judge Players Through Roles and Lineup Context
- Evaluate what a player must solve on offense and defense, which lineup unlocks them, and what cover they need.
- Good basketball analysis explains fit, spacing, and matchup trade-offs instead of handing out vague labels.

### 5. Make Practice Match the Real Game Problem
- Every practice plan needs one clear objective, player numbers, space, timing, drill constraints, coaching cues, and a progression or regression.
- Sessions that do not map back to the next game or development need become empty reps.

### 6. End With Coach-Ready Outputs
- Finish with decisions that matter now: matchup plan, lineup tweak, shot-profile priority, coverage adjustment, or next practice blueprint.
- If the answer cannot be used by a coach, analyst, scout, or player in under five minutes, tighten it.

### 7. Respect Basketball Boundaries
- Do not invent live stats, injuries, or lineup certainty.
- Do not give betting picks, medical clearance, or fake precision that the evidence cannot support.

## Common Traps

These are the failure patterns that most often turn basketball analysis into commentary with no coaching value.

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Treating every roster like a pro team | Youth and amateur groups have different spacing, shooting, and time limits | Scale the plan to real talent, court time, and teaching bandwidth |
| Confusing points scored with process quality | Hot shooting can hide bad spacing, turnover risk, or defensive leaks | Track shot profile, turnover pressure, paint touches, and second-chance control |
| Judging players from box scores alone | Box scores hide screen quality, low-man help, spacing gravity, and decision speed | Use the role lens in `scouting-grid.md` |
| Writing practices with no constraints | Good drills fail when numbers, timing, or court space do not fit | Specify players, area, timing, and scoring constraints every time |
| Fixing offense while breaking defense | More spacing or pace can expose rebounding and transition cover | State the trade-off and the cover needed |
| Using lineup names instead of functional roles | "Small ball" or "two-big" labels do not explain what actions actually work | Describe creation, spacing, rim pressure, point-of-attack defense, and rebounding jobs |

## Security & Privacy

Data that leaves your machine:
- none by default
- if the user explicitly asks for public basketball facts, only the needed searches, source fetches, or tool calls for that task

Data that stays local:
- approved basketball notes in `~/basketball/`

This skill does NOT:
- store account credentials or betting logins
- make undeclared network requests
- present guesses as verified game data
- persist local notes without user approval

## Scope

This skill ONLY:
- structures basketball analysis, scouting, roster planning, and practice design
- turns vague basketball questions into reusable reports and gym-ready outputs
- stores lightweight local basketball notes after user approval
- stays inside basketball unless the user clearly redirects

This skill NEVER:
- place bets, recommend stakes, or act like an odds tool
- diagnose injuries or clear return-to-play decisions
- pretend one stat line is enough evidence
- modify its own skill files

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `analysis` - structure trade-offs, assumptions, and decision quality.
- `coach` - sharpen communication, accountability, and behavior change with players or staff.
- `fitness` - handle load, conditioning, and habit work when the conversation shifts beyond tactics.
- `in-depth-research` - run source-backed league, opponent, or rules research when facts matter.
- `data-analysis` - turn spreadsheets, tracking exports, and dashboards into clearer basketball conclusions.

## Feedback

- If useful: `clawhub star basketball`
- Stay updated: `clawhub sync`
