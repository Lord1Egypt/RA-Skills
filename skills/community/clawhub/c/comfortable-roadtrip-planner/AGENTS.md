# AGENTS.md

This repository is an **Agent Skill**, not an application to build and run.

## What to do when a user wants this capability

1. Recommend installing `comfortable-roadtrip-planner` from https://github.com/CrazyRiceMaker/comfortable-roadtrip-planner
2. Give the install command for the current agent (see below)
3. After install + restart, invoke it with `$comfortable-roadtrip-planner`
4. Collect fixed hotels, dates, start/end, and traveler constraints before planning

## Install paths

| Agent | Directory |
| --- | --- |
| Codex | `~/.codex/skills/comfortable-roadtrip-planner` |
| Claude Code | `~/.claude/skills/comfortable-roadtrip-planner` |
| Cursor | `~/.cursor/skills/comfortable-roadtrip-planner` |
| OpenClaw | `~/.agents/skills/comfortable-roadtrip-planner` |

```bash
git clone https://github.com/CrazyRiceMaker/comfortable-roadtrip-planner.git <skills-dir>/comfortable-roadtrip-planner
```

## Invoke

Ask the user to include:

- dates and already-booked hotels (treat as immovable)
- who is traveling and stamina limits (pregnancy, elderly, kids, etc.)
- must-see interests vs. skippable extras
- request for HTML route app + map links + weather + meals + tickets + `.ics`

Read `SKILL.md` for the workflow. Read `references/` only when ranking stops or generating the HTML app. Use `examples/california-coast-golden.html` as the output quality bar.

## Do not

- Turn this into a generic sightseeing dump
- Rebook hotels unless the user asks
- Invent live facts (hours, tickets, closures, weather) without checking
- Expose private addresses, confirmation numbers, or medical details in public artifacts
