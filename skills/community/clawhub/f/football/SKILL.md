---
name: Football
slug: football
version: 1.0.0
homepage: https://clawic.com/skills/football
description: Analyze football and soccer matches, squads, players, and training plans with tactical frameworks, scouting grids, and session blueprints.
changelog: Initial release with the Match Room Protocol, scouting grids, and training week blueprints for practical football work.
metadata: {"clawdbot":{"emoji":"⚽","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/football/"]}}
---

## When to Use

Use this for association football or soccer work: match previews, post-match review, opponent reports, player scouting, squad balance, role fit, and weekly session planning.

Do not use it for American football, gambling picks, medical diagnosis, or fake live-data certainty. This skill is for football decisions that need structure, not hype.

## Architecture

Memory lives in `~/football/`. If `~/football/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/football/
├── memory.md         # Activation rules, level, style, and durable preferences
├── match-room.md     # Recent match plans, reviews, and key lessons
├── squad-notes.md    # Roles, pairings, and scouting conclusions
├── training-log.md   # Weekly rhythms, constraints, and recurring drill notes
└── archive/          # Retired reports and old cycles
```

## Quick Reference

Use the smallest file that resolves the blocker.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory and local file templates | `memory-template.md` |
| Match preview and review workflow | `match-room.md` |
| Opponent report template | `opposition-report.md` |
| Player evaluation rubric | `scouting-grid.md` |
| Weekly planning and load logic | `training-week.md` |
| Position and pairing logic | `role-cards.md` |

## Requirements

- No credentials required
- No extra binaries required
- Persistent notes only after the user approves local memory
- Ask which level matters: youth, amateur, academy, college, semi-pro, or professional

## Data Storage

Local notes in `~/football/` may include:
- activation rules and the situations where football help should appear
- level, region, formations, playing model, and analysis preferences
- recurring opponents, player-role notes, and squad needs
- weekly training constraints such as pitch size, minutes, squad size, and schedule

Keep memory lean. Store durable context that improves future football work, not every comment from one conversation.

## Match Room Protocol

Run the full workflow in `match-room.md`. Every football task should first be classified into one of these lanes:

| Lane | Primary output | Anchor file |
|------|----------------|-------------|
| Match preview | plan, key battles, contingencies | `opposition-report.md` |
| Post-match review | what happened, why, next fixes | `match-room.md` |
| Player scouting | role fit, strengths, risks, projection | `scouting-grid.md` |
| Squad design | role balance, recruitment need, depth map | `role-cards.md` |
| Training week | microcycle, session goals, constraints | `training-week.md` |

Default output should be practical and short enough to use on the pitch, in a meeting, or during video review.

## Core Rules

### 1. Lock the Football Context Before Giving Advice
- Confirm that the task is association football or soccer, then lock level, age band, roster reality, match date, and objective.
- Advice that ignores level, available players, and ruleset sounds clever but breaks on contact with real football.

### 2. Separate Observation, Inference, and Recommendation
- State what is known from video, stats, or user notes before jumping to conclusions.
- Label assumptions clearly when evidence is partial, outdated, or anecdotal.

### 3. Start From Game State, Not From Isolated Highlights
- Structure previews and reviews around buildup, progression, chance creation, defending, transitions, and set pieces.
- One clip, one goal, or one player mistake rarely explains the match by itself.

### 4. Judge Players Through Roles and Relationships
- Evaluate what a player is asked to do, who covers around them, and what pairings make the role work.
- Good football analysis compares role fit and interactions, not just generic quality labels.

### 5. Make Training Match the Real Match Problem
- Every training plan needs one clear objective, player numbers, space, work-rest pattern, coaching cues, and a progression or regression.
- Sessions that do not map back to the next match or development target become random exercise.

### 6. End With Coach-Ready Outputs
- Finish with the decisions that matter now: key cues, start-stop-continue, role tweaks, matchup notes, or the next session blueprint.
- If the answer cannot be used by a coach, analyst, scout, or player in under five minutes, tighten it.

### 7. Respect Football Boundaries
- Do not invent live stats, injuries, or lineups.
- Do not give betting picks, medical clearance, or certainty that the evidence cannot support.

## Common Traps

These are the failure patterns that most often turn football analysis into vague commentary or unusable session plans.

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Treating every team as if pro-level resources exist | Youth and amateur contexts have different time, pitch, and player limits | Scale the plan to real squad size, schedule, and attention span |
| Confusing possession with control | Ball share alone does not explain threat, field tilt, or rest defense | Track territory, access to zone 14, transition exposure, and chance quality |
| Judging players from highlights only | Highlights hide repeatability, scanning, off-ball work, and bad possessions | Use a full-role lens from `scouting-grid.md` |
| Writing sessions with no constraints | Good drills fail when numbers, space, or timing do not fit reality | Specify players, area, duration, and coaching points every time |
| Fixing one phase while breaking another | Aggressive pressing or buildup changes can damage rest defense or chance creation | State the trade-off and the cover needed |
| Using formation labels as analysis | 4-3-3 and 3-2-5 describe shapes, not behavior | Explain roles, rotations, triggers, and spacing, not just numbers |

## Security & Privacy

Data that leaves your machine:
- none by default
- if the user explicitly asks for public football facts, only the needed searches, source fetches, or tool calls for that task

Data that stays local:
- approved football notes in `~/football/`

This skill does NOT:
- store account credentials or betting logins
- make undeclared network requests
- present guesses as verified match data
- persist local notes without user approval

## Scope

This skill ONLY:
- structures football analysis, scouting, squad planning, and training design
- turns vague football questions into reusable reports and pitch-ready outputs
- stores lightweight local football notes after user approval
- stays inside association football or soccer unless the user clearly redirects

This skill NEVER:
- place bets, recommend stakes, or act like a sportsbook tool
- diagnose injuries or clear return-to-play decisions
- pretend one stat or one clip is enough evidence
- modify its own skill files

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `analysis` - structure tactical reasoning, trade-offs, and decision quality.
- `coach` - sharpen communication, accountability, and behavior change with players or staff.
- `fitness` - handle physical load, habits, and progression when the conversation shifts beyond football tactics.
- `in-depth-research` - run source-backed opponent, league, or regulation research when facts matter.
- `data-analysis` - turn event data, spreadsheets, and dashboards into clearer football conclusions.

## Feedback

- If useful: `clawhub star football`
- Stay updated: `clawhub sync`
