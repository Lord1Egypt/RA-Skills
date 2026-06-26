# decision-algorithm-skill

English translation and adaptation of the EKB Decision Algorithm — a Claude Code skill that helps users analyze life decisions using Expected Value, Kelly Criterion, and Bayesian updating.

## Structure

- `SKILL.md` — Core skill definition (the entry point Claude Code reads)
- `tools/decision_calculator.py` — CLI calculator for EV and Kelly computations
- `docs/methodology.md` — Framework methodology deep-dive
- `meta.json` — Skill metadata for registry platforms

## Publishing

Distributed via:
- **skills.sh**: `npx skills add truenorth-lj/decision-algorithm-skill`
- **ClawHub**: `clawhub install truenorth-lj/decision-algorithm-skill`
- **Manual**: Copy into `~/.claude/skills/decision-algorithm/`

## Attribution

Based on [caomz/decision-algorithm](https://github.com/caomz/decision-algorithm), originally derived from Lao Yu's EKB decision research.
