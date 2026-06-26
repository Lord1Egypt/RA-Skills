# Skill Creator

**The factory that builds the factory.**

> Meta-skill that generates production-grade agent skills from natural language. Every skill in the Acrid ecosystem starts here.

**Version:** 2.0.0 | **Author:** Acrid Automation | **Status:** PROD | **License:** MIT

---

## What It Does

You describe what you want in plain English. Skill Creator analyzes your request, architects the solution, generates all files, runs quality gates, and delivers a ready-to-use skill — complete with documentation, error handling, and helper scripts if needed.

It's not a template copier. It **thinks** about what you need, picks the right complexity tier, designs the contract, and builds it clean.

## Quick Start

```
Create a skill called "weather-alert" that checks weather conditions
for a given city and returns a summary with any active alerts.
```

That's it. Skill Creator handles the rest.

## What Gets Generated

Depending on complexity, you get:

```
skills/<your-skill>/
  SKILL.md        # The skill logic — deterministic, error-aware steps
  README.md       # Full docs with examples and setup
  src/            # Helper scripts (only when needed)
    main.py|js    # Core computation logic
  config/         # Defaults and configuration (advanced skills only)
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Kebab-case skill name (e.g., `deploy-monitor`) |
| `description` | Yes | What the skill does — be specific |
| `requirements` | No | Tools, APIs, constraints, auth needs |
| `outputs` | No | What format the skill returns (defaults to structured text) |
| `complexity` | No | `simple`, `standard`, or `advanced` (auto-detected if omitted) |

## Examples

### Simple Skill
```
Create a skill called "json-formatter" that takes raw JSON input and
returns it pretty-printed with syntax validation.
```

### Standard Skill
```
Create a skill called "stock-checker" that fetches the current price
of a stock by ticker symbol. Use a free API. Return price in USD with
daily change percentage.
```

### Advanced Skill
```
Create a skill called "deploy-monitor" that watches a GitHub Actions
workflow run, reports status updates, alerts on failure with error logs,
and posts a summary to a Notion page when complete.
```

## Quality Standards

Every generated skill passes these gates before delivery:

| Gate | What It Checks |
|------|---------------|
| **Atomic** | Does exactly one thing |
| **Named** | Name tells you what it does |
| **Typed** | All inputs have types and validation |
| **Specified** | Output format is explicitly defined |
| **Error-Proof** | Every external call has a failure path |
| **Documented** | README has Quick Start + real examples |
| **Deterministic** | Same input = same execution flow |
| **Lean** | No dead code, no over-engineering |
| **First-Run Ready** | Works immediately with documented setup |

## How It Works

1. **Intelligence Gathering** — Parses your request, extracts purpose, tools, APIs, inputs, outputs, and failure modes
2. **Architecture** — Designs the skill contract and picks the right complexity tier
3. **Generation** — Writes SKILL.md with deterministic steps, README.md with full docs, and helper scripts if needed
4. **Quality Gates** — Runs every file through the Acrid Quality Checklist
5. **Delivery** — Writes files and gives you a ready-to-use invocation

## Anti-Patterns It Avoids

- Vague steps ("process the data" — instead specifies exactly HOW)
- Placeholder code ("TODO: implement")
- Undocumented secrets or env vars
- Over-engineered abstractions for single-use logic
- Dependencies on unavailable tools
- Missing error handling on external calls

## File Reference

| File | Purpose |
|------|---------|
| `SKILL.md` | Core skill logic — the full generation pipeline |
| `README.md` | This file |
| `templates/SKILL_TEMPLATE.md` | Template used for generated SKILL.md files |
| `templates/README_TEMPLATE.md` | Template used for generated README.md files |
| `examples/stock-checker/` | Complete example of a generated skill |

---

*Built by Acrid Automation. No fluff, just execution.*
