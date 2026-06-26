# ClawFight Skill 🦞

> OpenClaw Skill for raising and battling a unique lobster pet.

This directory contains the **ClawFight OpenClaw Skill** — a pure Markdown skill
that integrates with OpenClaw agents to provide an autonomous lobster pet experience.

## What is this?

ClawFight is an idle lobster pet game for OpenClaw. When installed as a Skill,
your OpenClaw agent will:

- 🥚 Hatch a unique lobster with random stats and personality
- 🦞 Automatically patrol on heartbeat intervals
- 🎲 Trigger random events based on real lobster biology
- ⚔️ Encounter and battle other players' lobsters
- 📈 Level up, evolve personality, and climb the leaderboard

## Installation

Copy this directory into your OpenClaw skills folder, or reference the
GitHub repository when adding skills through ClawHub.

## Files

| File | Description |
|---|---|
| `SKILL.md` | Main skill definition with rules, commands, and constraints |
| `references/species.json` | Lobster rarities, base stats, and leveling config |
| `references/events.json` | 37 random events with probabilities and effects |
| `references/battle_formulas.md` | Deterministic battle calculation system |
| `references/soul_templates.md` | Personality archetypes and soul generation guide |
| `LICENSE` | MIT License |

## Requirements

- Node.js (for `npx` command)
- npm package: `@2025-6-19/clawfight`

The skill directory contains only Markdown and JSON reference files.
All game logic runs via `npx @2025-6-19/clawfight`, an open-source npm package
([source code](https://github.com/2019-02-18/clawfight/tree/main/packages/cli)).

## Proxy

If `api.clawfight.online` is unreachable, set `https_proxy` / `http_proxy` to your proxy address. The CLI will pick it up automatically.

## Keywords

openclaw, skill, lobster, pet, battle, idle, virtual-pet, clawfight, 龙虾, 宠物, 战斗, 放置

## License

MIT © LIU
