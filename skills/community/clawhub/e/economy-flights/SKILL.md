---
name: economy-flights
displayName: "Find Economy Flights — Lowest Fares, Budget Airlines, Basic Economy Tickets"
description: "Find economy flights, cheapest airfare and budget airline tickets with basic economy fares and low-cost options. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
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

# Skill: economy-flights

## Overview

Find economy flights — lowest fares, budget airlines, and basic economy tickets. For price-conscious travelers who want the cheapest way to fly.

## When to Activate

User query contains:
- English: "economy flight", "cheapest flight", "budget airline", "basic economy", "low cost flight", "cheapest airfare"
- Chinese: "经济舱", "最便宜机票", "廉价航空", "特价机票", "低成本航班", "省钱机票"

Do NOT activate for: business/first class → `business-flights` or `first-class`

## Prerequisites

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 2
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--origin` | Yes | Departure city or airport code (e.g., "Beijing", "PVG") |
| `--destination` | Yes | Arrival city or airport code (e.g., "Shanghai", "NRT") |
| `--dep-date` | No | Departure date, `YYYY-MM-DD` |
| `--dep-date-start` | No | Start of flexible date range |
| `--dep-date-end` | No | End of flexible date range |
| `--sort-type` | No | **Default: 3** (price ascending — cheapest first) |
| `--max-price` | No | Price ceiling in CNY |
| `--journey-type` | No | 1=direct, 2=connecting |
| `--seat-class-name` | No | **Always `economy` for this skill** |
| `--dep-hour-start` | No | Departure hour filter start (0-23) |
| `--dep-hour-end` | No | Departure hour filter end (0-23) |

### Sort Options

| Value | Meaning | When to Use |
|-------|---------|-------------|
| `3` | Price ascending | **Default** — cheapest first |
| `4` | Duration ascending | Fastest economy |
| `6` | Earliest departure | Morning economy |
| `8` | Direct flights first | Non-stop economy |

## Core Workflow — Single-command

### Step 0: Environment Check (mandatory, never skip)

```bash
flyai --version
```

- ✅ Returns version → proceed to Step 1
- ❌ `command not found` →

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
```

Still fails → **STOP.** Tell user to run `npm i -g @fly-ai/flyai-cli` manually. Do NOT continue. Do NOT use training data.

### Step 1: Collect Parameters

Collect required parameters from user query. If critical info is missing, ask at most 2 questions.
See [references/templates.md](references/templates.md) for parameter collection SOP.

### Step 2: Execute CLI Commands

### Playbook A: Cheapest Economy

**Trigger:** "economy flights", "经济舱机票"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name economy --sort-type 3
```

**Output:** Economy flights sorted by lowest price.

### Playbook B: Flexible Date Cheapest

**Trigger:** "cheapest economy any day", "哪天最便宜"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start "{date-3}" --dep-date-end "{date+3}" --seat-class-name economy --sort-type 3
```

**Output:** Economy prices across a 7-day window, cheapest first.

### Playbook C: Budget-Capped Economy

**Trigger:** "economy under ¥{price}", "{price}以内的经济舱"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name economy --max-price {budget} --sort-type 3
```

**Output:** Economy flights within budget, sorted by price.

### Playbook D: Broad Search (no economy found)

**Trigger:** fallback when 0 results

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
flyai keyword-search --query "{origin} to {destination} cheapest flights"
```

**Output:** Broader search without seat-class filter + keyword fallback.

See [references/playbooks.md](references/playbooks.md) for all scenario playbooks.

On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

Format CLI JSON into user-readable Markdown with booking links. See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag "Powered by flyai · Real-time pricing, click to book" included?
- [ ] All results are economy cabin?

**Any NO → re-execute from Step 2.**

## Usage Examples

```bash
flyai search-flight --origin "Beijing" --destination "Shanghai" --dep-date 2026-05-01 --seat-class-name economy --sort-type 3
```
```bash
flyai search-flight --origin "Shanghai" --destination "Guangzhou" --dep-date 2026-06-01 --seat-class-name economy --max-price 500 --sort-type 3
```

## Output Rules

1. **Conclusion first** — lead with cheapest economy fare
2. **Comparison table** with ≥ 3 results when available
3. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
4. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
5. ❌ Never output raw JSON
6. ❌ Never answer from training data without CLI execution
7. ❌ Never fabricate prices, flight numbers, or schedules

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "economy" / "经济舱" | `--seat-class-name economy` |
| "cheapest economy" / "最便宜经济舱" | add `--sort-type 3` |
| "flexible date" / "日期灵活" | add `--dep-date-start "{date-3}" --dep-date-end "{date+3}"` |
| "under budget" / "预算内" | add `--max-price {budget}` |
| "round-trip economy" / "往返经济舱" | add `--back-date {date}` |

Economy is available on virtually all flights. If specific route returns 0 results, try flexible dates or nearby airports. Mid-week flights (Tue/Wed) are often 20-40% cheaper than weekends.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
