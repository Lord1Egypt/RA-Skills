# Competitive-Ops -- Competitive Analysis Pipeline

## Origin

This system automates competitive intelligence: tracks competitors, monitors pricing changes, detects feature shifts, and generates reports.

**It will work out of the box, but it's designed to be made yours.** Customize archetypes, scoring, alerts, and reports to match your market context.

## Data Contract (CRITICAL)

There are two layers. Customization goes in the User Layer.

**User Layer (NEVER auto-updated, personalization goes HERE):**
- `cv.md`, `config/profile.yml`, `modes/_profile.md`
- `data/*`, `reports/*`, `snapshots/*`

**System Layer (auto-updatable, DON'T put user data here):**
- `modes/_shared.md`, `modes/*.md`
- `CLAUDE.md`, `*.mjs` scripts, `templates/*`, `config/*.yml`

**THE RULE: When the user asks to customize anything (archetypes, scoring, alerts, reports), ALWAYS write to `modes/_profile.md` or `config/profile.yml`. NEVER edit system files for user-specific content.**

## Update Check

On the first message of each session, run the update checker silently:

```bash
node update-system.mjs check
```

Parse the JSON output:
- `{"status": "update-available", ...}` → tell the user an update is available
- `{"status": "up-to-date"}` → say nothing

## What is competitive-ops

AI-powered competitive intelligence built on Claude Code: competitor tracking, pricing monitoring, feature detection, and report generation.

### Main Files

| File | Function |
|------|----------|
| `data/competitors.md` | Competitor tracker |
| `data/reports/` | Generated analysis reports |
| `data/snapshots/` | Historical snapshots |
| `config/profile.yml` | Company/product configuration |
| `config/sources.yml` | Trusted data sources |
| `scripts/` | Python utilities (cross_validate, change_detector) |

### First Run -- Onboarding (IMPORTANT)

**Before doing ANYTHING else, check if the system is set up:**

1. Does `cv.md` exist?
2. Does `config/profile.yml` exist?
3. Does `data/competitors.md` exist?

If any are missing, enter onboarding mode and guide the user through setup.

### Skill Modes

| If the user... | Mode |
|----------------|------|
| Adds a competitor | `add-competitor` |
| Runs competitive analysis | `analyze` |
| Generates a report | `report` |
| Checks for changes | `diff` |
| Monitors pricing | `pricing` |

---

## Ethical Guidelines

**This system is for competitive intelligence, not industrial espionage.**
- Only use public data sources
- Respect website terms of service
- Do not attempt to bypass paywalls or access restrictions
- Focus on market analysis, not stealing trade secrets

---

## Stack and Conventions

- Skill-based pipeline (Claude Code skills)
- Python utilities for validation/detection (`scripts/*.py`)
- YAML (config), Markdown (data)
- Report naming: `{competitor}-{date}.md`
