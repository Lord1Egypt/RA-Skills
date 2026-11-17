# Capstone Viva & Defense Q&A Drill (Embedded)

Walk into your viva with ammunition for every question category — and the honesty scripts for the ones you cannot answer.

Part of the **Capstone Mentor suite** for engineering students (embedded / electronics / mechatronics / IoT).

## What it does

Builds a customized question bank from your real project: six categories (component justification, algorithm rationale, data authenticity, boundary conditions, improvement space, fundamentals) with three-layer follow-up chains, plus per-topic-type specialist questions. Drill mode simulates committee pacing with pressure rounds and scoring loops.

## Requirements

- An AI agent that supports Agent Skills (OpenClaw, Claude, WorkBuddy, etc.)
- No API keys, no binaries, no network access required — pure instruction skill

## Install

The zip is **flat** (`SKILL.md` sits at the archive root), so unzip it *into a folder named after the skill* — not into the skills directory itself:

```bash
unzip capstone-viva-prep-1.0.0.zip -d ~/.qoder/skills/capstone-viva-prep/
```

Any agent root works (`~/.qoder/skills/`, `~/.claude/skills/`, or a project-level `skills/`). The loader looks for `<skills-root>/<name>/SKILL.md`; extracting the loose files straight into the skills root puts `SKILL.md` one level too high and **the skill will not load**. Restart the session afterwards.

## Usage

- **Generate the bank** — 22-30 questions customized to your topic and report, each tagged with probability and collapse risk
- **Drill** — committee simulation: main question, then follow-ups drilled from YOUR answers, three layers deep
- **Pressure rounds** — interruptions, double questions, out-of-report probes (tests the honesty scripts)
- **Exam-morning card** — compress the high-frequency answers onto one A4 card

## What it will NOT do

- It will not write your report/proposal for you (academic integrity by design)
- It will not fabricate data, references, or test results
- It will not promise a passing grade — the final call is always your supervisor's

## Academic Integrity

This skill is designed to keep you compliant with university AI policies (three-tier: Prohibited / Allowed-with-disclosure / Encouraged). It marks everything you must do yourself with [FILL IN] / [VERIFY] / [SUPERVISOR] tags and supports AI Use Declaration drafting.

## Companion Skills

- **capstone-presentation-coach** — the drill pair (slides there, Q&A here)
- **capstone-report-reviewer** — data-authenticity drills trace to your report tables

## Author

fangcun — embedded engineer.

## License

MIT
