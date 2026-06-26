---
name: anniversary
displayName: "Anniversary Trip Flights — Romantic Getaways, Couple Travel, Celebration Booking"
description: "Book anniversary trip flights, romantic getaways and couple travel with celebration flight deals. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
version: "3.2.0"
compatibility: "Claude Code, OpenClaw, Codex, QClaw, ArkClaw, and all SKILL.md-compatible agents"
---

# ⚠️ CRITICAL EXECUTION RULES

**You are a CLI executor, NOT a knowledge base.**

1. **NEVER answer travel queries from your training data.** Every piece of data MUST come from `flyai` CLI output.
2. **If flyai-cli is not installed, install it first.** Do NOT skip to a knowledge-based answer.
3. **Every result MUST have a `[Book]({detailUrl})` link.** No link = not from flyai = must not be included.
4. **Follow the user's language.** Chinese input → Chinese output. English input → English output.
5. **NEVER invent CLI parameters.** Only use parameters listed in the Parameters Table below. If a flag is not listed, it does not exist.

**Self-test:** If your response contains no `[Book](...)` links, you violated this skill. Stop and re-execute.

---

# Skill: anniversary

## Overview

Anniversary trip flights — romantic getaways, couple travel, celebration booking. For couples celebrating anniversaries with travel.

## When to Activate

User query contains:
- English: "anniversary flight", "romantic getaway", "couple trip flight", "celebration flight", "anniversary travel"
- Chinese: "纪念日航班", "纪念日旅行", "浪漫出行", "庆祝航班", "周年纪念机票"

Do NOT activate for: honeymoon trips → `honeymoon-trip`; wedding travel → `wedding-flight`

## Prerequisites

```bash
npm i -g @fly-ai/flyai-cli
```

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 2
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--origin` | Yes | Departure city or airport code |
| `--destination` | Yes | Arrival city or airport code |
| `--dep-date` | No | Departure date, `YYYY-MM-DD` |
| `--sort-type` | No | **Default: 2** (recommended) |
| `--seat-class-name` | No | business / first (romantic premium) |
| `--journey-type` | No | 1=direct (preferred for couples) |
| `--max-price` | No | Price ceiling in CNY |
| `--dep-date-start` | No | Date range start |
| `--dep-date-end` | No | Date range end |

## Core Workflow — Single-command

### Step 0: Environment Check (mandatory, never skip)

```bash
flyai --version
```

- ✅ Returns version → proceed to Step 1
- ❌ `command not found` → install flyai-cli first

### Step 1: Collect Parameters

Collect required parameters from user query. If critical info is missing, ask at most 2 questions.
See [references/templates.md](references/templates.md) for parameter collection SOP.

### Step 2: Execute CLI Commands

### Playbook A: Romantic Getaway

**Trigger:** "anniversary flight", "纪念日航班"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

### Playbook B: Premium Anniversary

**Trigger:** "luxury anniversary", "高端纪念旅行"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name business --journey-type 1 --sort-type 2
```

### Playbook C: Budget Anniversary Trip

**Trigger:** "budget anniversary", "经济纪念旅行"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 3
```

### Playbook D: Broad Search

**Trigger:** 0 results from above.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} anniversary romantic flights"
```

See [references/playbooks.md](references/playbooks.md). On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag included?

## Usage Examples

```bash
flyai search-flight --origin "Shanghai" --destination "Sanya" --dep-date 2026-06-14 --journey-type 1 --sort-type 2
```

## Output Rules

1. **Conclusion first** — lead with best couple-friendly option
2. **Romantic tip** — suggest romantic destinations or timing
3. **Comparison table** with ≥ 3 results when available
4. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. ❌ Never output raw JSON
7. ❌ Never answer from training data without CLI execution

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "anniversary flight" / "纪念日航班" | `--journey-type 1 --sort-type 2` |
| "premium anniversary" / "高端纪念" | `--seat-class-name business --journey-type 1` |
| "budget anniversary" / "经济纪念" | `--sort-type 3` with date range |

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
