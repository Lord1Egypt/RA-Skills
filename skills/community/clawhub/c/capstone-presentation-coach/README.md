# Capstone Presentation Coach (Embedded)

Build a defense deck for the examiner's eyes — they spend under 30 seconds per slide.

Part of the **Capstone Mentor suite** for engineering students (embedded / electronics / mechatronics / IoT).

## What it does

Reviewer-perspective 8-12 slide structure scaled to your time slot, low-text high-figure rules (max 5 bullets, 50%+ figures, font minimums), testing plus live demo taking at least 35% of time, per-topic-type emphasis, a probability-ordered live-demo anti-failure checklist, and backup-slide tactics for predictable examiner questions.

## Requirements

- An AI agent that supports Agent Skills (OpenClaw, Claude, WorkBuddy, etc.)
- No API keys, no binaries, no network access required — pure instruction skill

## Install

The zip is **flat** (`SKILL.md` sits at the archive root), so unzip it *into a folder named after the skill* — not into the skills directory itself:

```bash
unzip capstone-presentation-coach-1.0.0.zip -d ~/.qoder/skills/capstone-presentation-coach/
```

Any agent root works (`~/.qoder/skills/`, `~/.claude/skills/`, or a project-level `skills/`). The loader looks for `<skills-root>/<name>/SKILL.md`; extracting the loose files straight into the skills root puts `SKILL.md` one level too high and **the skill will not load**. Restart the session afterwards.

## Usage

- **collect → outline** — answer a few questions (topic, time limit, demo feasibility, topic type), get a per-slide outline with time allocation
- **script** — demo narration script with contingency plans
- **backup** — backup-slide list answering the questions examiners WILL ask
- **rehearse** — rehearsal checklist with stopwatch points

## What it will NOT do

- It will not write your report/proposal for you (academic integrity by design)
- It will not fabricate data, references, or test results
- It will not promise a passing grade — the final call is always your supervisor's

## Academic Integrity

This skill is designed to keep you compliant with university AI policies (three-tier: Prohibited / Allowed-with-disclosure / Encouraged). It marks everything you must do yourself with [FILL IN] / [VERIFY] / [SUPERVISOR] tags and supports AI Use Declaration drafting.

## Companion Skills

- **capstone-viva-prep** — the Q&A drill pair (slides here, follow-up questions there)
- **capstone-report-reviewer** — slide data must match the report

## Author

fangcun — embedded engineer.

## License

MIT
