# Capstone Topic Advisor (Embedded)

Choose the right capstone / final-year project topic before you sink months into the wrong one.

Part of the **Capstone Mentor suite** for engineering students (embedded / electronics / mechatronics / IoT).

## What it does

Generates 7-10 ranked topic candidates in three tiers (safe / solid / standout), each with a full evaluation card: difficulty, net timeline, BOM budget, biggest risk, defense talking points. Includes an 8-category prior table, a cliche-topic blacklist with an increment-fix formula, and four working modes.

## Requirements

- An AI agent that supports Agent Skills (OpenClaw, Claude, WorkBuddy, etc.)
- No API keys, no binaries, no network access required — pure instruction skill

## Install

The zip is **flat** (`SKILL.md` sits at the archive root), so unzip it *into a folder named after the skill* — not into the skills directory itself:

```bash
unzip capstone-topic-advisor-1.0.0.zip -d ~/.qoder/skills/capstone-topic-advisor/
```

Any agent root works (`~/.qoder/skills/`, `~/.claude/skills/`, or a project-level `skills/`). The loader looks for `<skills-root>/<name>/SKILL.md`; extracting the loose files straight into the skills root puts `SKILL.md` one level too high and **the skill will not load**. Restart the session afterwards.

## Usage

- **recommend** — answer a few constraint questions (major, existing hardware, budget, window), get ranked candidates
- **check** — already have a topic? It passes your topic through seven gates (blacklist, scope, ethics, timeline, budget, novelty, grilling) with PASS/WARN/FAIL
- **compare** — torn between 2-3 candidates? Get a 7-dimension comparison table with a clear recommendation
- **budget** — BOM estimation with money-saving tactics and procurement-trap warnings

## What it will NOT do

- It will not write your report/proposal for you (academic integrity by design)
- It will not fabricate data, references, or test results
- It will not promise a passing grade — the final call is always your supervisor's

## Academic Integrity

This skill is designed to keep you compliant with university AI policies (three-tier: Prohibited / Allowed-with-disclosure / Encouraged). It marks everything you must do yourself with [FILL IN] / [VERIFY] / [SUPERVISOR] tags and supports AI Use Declaration drafting.

## Companion Skills

- **capstone-proposal-coach** — proposal stage
- **capstone-report-reviewer** — report writing stage
- **capstone-presentation-coach** — defense slides
- **capstone-viva-prep** — oral defense drill

## Author

fangcun — embedded engineer.

## License

MIT
