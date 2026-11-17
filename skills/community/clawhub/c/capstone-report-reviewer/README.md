# Capstone Report Structure Reviewer (Embedded)

Turn your capstone report from a product manual into an engineering verification report — without crossing academic-integrity lines.

Part of the **Capstone Mentor suite** for engineering students (embedded / electronics / mechatronics / IoT).

## What it does

Reviews your report chapter by chapter against an engineering-evidence chain with explicit failure points; teaches the three-layer component-justification method, test-case tables, and error analysis; provides write-as-you-build scheduling, an originality self-check for high-similarity sections, and AI-disclosure compliance rules.

## Requirements

- An AI agent that supports Agent Skills (OpenClaw, Claude, WorkBuddy, etc.)
- No API keys, no binaries, no network access required — pure instruction skill

## Install

The zip is **flat** (`SKILL.md` sits at the archive root), so unzip it *into a folder named after the skill* — not into the skills directory itself:

```bash
unzip capstone-report-reviewer-1.0.0.zip -d ~/.qoder/skills/capstone-report-reviewer/
```

Any agent root works (`~/.qoder/skills/`, `~/.claude/skills/`, or a project-level `skills/`). The loader looks for `<skills-root>/<name>/SKILL.md`; extracting the loose files straight into the skills root puts `SKILL.md` one level too high and **the skill will not load**. Restart the session afterwards.

## Usage

- **Not started** — get the six-chapter framework + write-as-you-build schedule
- **Halfway** — paste existing content for an evidence-chain completeness review, then fill gaps against the framework
- **Nearly done** — run the pre-submission checklist (three-place spec consistency, cross-references, format) + originality self-check
- **Defense season** — hands off to the presentation coach and viva prep skills

## What it will NOT do

- It will not write your report/proposal for you (academic integrity by design)
- It will not fabricate data, references, or test results
- It will not promise a passing grade — the final call is always your supervisor's

## Academic Integrity

This skill is designed to keep you compliant with university AI policies (three-tier: Prohibited / Allowed-with-disclosure / Encouraged). It marks everything you must do yourself with [FILL IN] / [VERIFY] / [SUPERVISOR] tags and supports AI Use Declaration drafting.

## Companion Skills

- **capstone-topic-advisor** — topic stage
- **capstone-proposal-coach** — proposal stage
- **capstone-presentation-coach** / **capstone-viva-prep** — defense stage

## Author

fangcun — embedded engineer.

## License

MIT
