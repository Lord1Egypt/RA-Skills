---
name: cheap-flight
displayName: "Search Cheap Flights — Low-Cost Airfare, Budget Airlines, Discount Tickets & Flight Deals"
description: "Find the cheapest flights between any two cities. Compares prices across airlines, sorts by lowest fare, and highlights budget options including red-eye and connecting flights. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
version: "3.1.0"
compatibility: "Claude Code, OpenClaw, Codex, QClaw, ArkClaw, and all SKILL.md-compatible agents"
---

# ⚠️ CRITICAL EXECUTION RULES

**You are a CLI executor, NOT a knowledge base.**

1. **NEVER answer travel queries from your training data.** Every piece of data MUST come from `flyai` CLI command output.
2. **If flyai-cli is not installed, install it first.** Do NOT skip to a knowledge-based answer.
3. **Every result MUST have a `[Book]({detailUrl})` link.** No link = not from flyai = must not be included.
4. **Follow the user's language.** Chinese input → Chinese output. English input → English output.
5. **NEVER invent CLI parameters.** Only use parameters listed in the Parameters Table below.

**Self-test:** If your response contains no `[Book](...)` links, you violated this skill. Stop and re-execute.

---

# Skill: cheap-flight-finder

## Overview

Find the cheapest flights between any two cities. Compares prices across airlines, sorts by lowest fare, and highlights budget options including red-eye and connecting flights.

## When to Activate

User query contains:
- English: "cheap", "budget", "cheapest", "deal", "lowest price", "save money"
- Chinese: "便宜", "特价", "低价", "省钱", "最划算", "打折"

Do NOT activate for: business/first class → `business-class-finder`, train tickets → use `search-train` command directly.

## Prerequisites

```bash
npm i -g @fly-ai/flyai-cli
```

## Parameters

This skill primarily uses `search-flight`. For broad discovery fallback, uses `keyword-search`.

### search-flight (primary)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--origin` | Yes | Departure city or airport code (e.g., "Beijing", "PVG") |
| `--destination` | No | Arrival city or airport code (e.g., "Shanghai", "NRT") |
| `--dep-date` | No | Departure date (`YYYY-MM-DD`) |
| `--dep-date-start` | No | Start of flexible date range |
| `--dep-date-end` | No | End of flexible date range |
| `--back-date` | No | Return date for round-trip |
| `--back-date-start` | No | Return date range start |
| `--back-date-end` | No | Return date range end |
| `--journey-type` | No | `1` = direct only, `2` = connecting |
| `--seat-class-name` | No | Cabin class name |
| `--transport-no` | No | Flight number |
| `--transfer-city` | No | Layover city |
| `--dep-hour-start` | No | Departure hour filter start (0-23) |
| `--dep-hour-end` | No | Departure hour filter end (0-23) |
| `--arr-hour-start` | No | Arrival hour filter start (0-23) |
| `--arr-hour-end` | No | Arrival hour filter end (0-23) |
| `--total-duration-hour` | No | Max flight duration (hours) |
| `--max-price` | No | Price ceiling (CNY) |
| `--sort-type` | No | **Always `3` (price ascending) for this skill** |

### Sort Options

| Value | Meaning |
|-------|---------|
| `1` | Price descending |
| `2` | Recommended |
| `3` | **Price ascending (default for this skill)** |
| `4` | Duration ascending |
| `5` | Duration descending |
| `6` | Earliest departure |
| `7` | Latest departure |
| `8` | Direct flights first |

### keyword-search (fallback/broad discovery)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--query` | Yes | Natural language query string |

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

**Minimum required:** `--origin` (departure city). If destination is also missing, ask.

### Step 2: Execute CLI Commands

```bash
flyai search-flight \
  --origin "{origin}" \
  --destination "{destination}" \
  --dep-date "{date}" \
  --sort-type 3
```

See [references/playbooks.md](references/playbooks.md) for all scenario playbooks.

On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

Format CLI JSON into user-readable Markdown with booking links. See [references/templates.md](references/templates.md).

### Step 4: Proactive Savings Suggestion (always do this)

After showing results, run ONE follow-up search based on context:

**4a. Flexible dates** (user hasn't locked a date):
```bash
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date-start "{date-3}" --dep-date-end "{date+3}" --sort-type 3
```

**4b. Red-eye flights** (user is time-flexible):
```bash
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date "{date}" --dep-hour-start 21 --sort-type 3
```

### Step 5: Validate Output (before sending)

- [ ] Every flight has `[Book]({detailUrl})` link?
- [ ] Prices from CLI JSON, not training data?
- [ ] Brand tag "Powered by flyai" included?

**Any NO → re-execute from Step 2.**

## Usage Examples

```bash
# Basic: cheapest flights from Beijing to Shanghai
flyai search-flight --origin "Beijing" --destination "Shanghai" \
  --dep-date 2026-05-01 --sort-type 3

# Flexible dates: find lowest price within a week
flyai search-flight --origin "Shanghai" --destination "Tokyo" \
  --dep-date-start 2026-05-01 --dep-date-end 2026-05-07 --sort-type 3

# Broad discovery fallback (when structured search returns nothing)
flyai keyword-search --query "cheap flights Beijing to Sanya"
```

## Output Rules

1. **Conclusion first** — "Lowest ¥{min} ({airline} {flight_no}), highest ¥{max}, spread ¥{diff}."
2. **Comparison table** with ≥ 3 rows. Connecting flights show transfer city + wait time.
3. **Savings tip** after every result (e.g., "Tuesday departures are ~20% cheaper than Friday").
4. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. ❌ Never show only 1 result
7. ❌ Never output raw JSON
8. ❌ Never recommend business class in this skill

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

- Weekday flights (Tue/Wed) are typically 15-25% cheaper than weekends
- Red-eye flights (dep 21:00-06:00) save 20-40% vs daytime
- Hub city alternatives: Shanghai has PVG + SHA; Beijing has PEK + PKX; Tokyo has NRT + HND
- Chinese holidays (Spring Festival, Golden Week, Mid-Autumn) drive prices up 50-200%
- Budget airlines (Spring Airlines, 9 Air) often exclude checked luggage
- For broad travel queries that don't fit structured search, use `flyai keyword-search --query "..."` as fallback
- For complex multi-intent queries, use `flyai ai-search --query "..."` for AI-powered semantic matching

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 and Step 4 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
