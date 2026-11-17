# Capstone Proposal Coach (Embedded)

Turn a blank proposal document into a plan your supervisor approves on the first pass.

Part of the **Capstone Mentor suite** for engineering students (embedded / electronics / mechatronics / IoT).

## What it does

Section-by-section proposal framework guidance, system block diagram with hardware/software task split, backward-planned milestones where every step has an acceptance artifact, reference handling with a zero-fabrication rule, proposal-defense Q&A prep, and an AI Use Declaration draft.

## Requirements

- An AI agent that supports Agent Skills (OpenClaw, Claude, WorkBuddy, etc.)
- No API keys, no binaries, no network access required — pure instruction skill

## Install

The zip is **flat** (`SKILL.md` sits at the archive root), so unzip it *into a folder named after the skill* — not into the skills directory itself:

```bash
unzip capstone-proposal-coach-1.0.0.zip -d ~/.qoder/skills/capstone-proposal-coach/
```

Any agent root works (`~/.qoder/skills/`, `~/.claude/skills/`, or a project-level `skills/`). The loader looks for `<skills-root>/<name>/SKILL.md`; extracting the loose files straight into the skills root puts `SKILL.md` one level too high and **the skill will not load**. Restart the session afterwards.

## Usage

- **outline** — proposal framework per your institution template (or a generic six-section skeleton)
- **route** — technical route breakdown: block diagram, task table, 2-3 key technical points, risk fallbacks
- **schedule** — backward-planned milestone table from proposal date to defense date
- **refs** — search strategy + organization of references you actually found (never generated)
- **ai-statement** — AI Use Declaration draft matching university disclosure norms

## What it will NOT do

- It will not write your report/proposal for you (academic integrity by design)
- It will not fabricate data, references, or test results
- It will not promise a passing grade — the final call is always your supervisor's

## Academic Integrity

This skill is designed to keep you compliant with university AI policies (three-tier: Prohibited / Allowed-with-disclosure / Encouraged). It marks everything you must do yourself with [FILL IN] / [VERIFY] / [SUPERVISOR] tags and supports AI Use Declaration drafting.

## Companion Skills

- **capstone-topic-advisor** — topic selection before the proposal
- **capstone-report-reviewer** — report writing after approval
- **capstone-presentation-coach** / **capstone-viva-prep** — defense stage

## Author

fangcun — embedded engineer.

## License

MIT
