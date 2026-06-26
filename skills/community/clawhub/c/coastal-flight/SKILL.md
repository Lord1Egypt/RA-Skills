---
name: coastal-flight
displayName: "Search Coastal Flights — Seaside Cities, Beach Towns, Harbor Destinations"
description: "Search coastal flights, seaside city flights and beach town flights with harbor destination booking. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
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

# Skill: coastal-flight

## Overview

Search coastal flights — seaside cities, beach towns, harbor destinations. For travelers heading to coastal and seaside destinations.

## When to Activate

User query contains:
- English: "coastal flight", "seaside flight", "beach town flight", "harbor flight", "coastal city flight", "shoreline flight"
- Chinese: "沿海航班", "海滨航班", "海边机票", "沿海城市机票", "港口城市航班", "海边出行"

Do NOT activate for: island destinations → `island-flight`; mountain trips → `mountain-flight`

## Prerequisites

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
| `--journey-type` | No | 1=direct, 2=connecting |
| `--max-price` | No | Price ceiling in CNY |
| `--dep-date-start` | No | Date range start |
| `--dep-date-end` | No | Date range end |

### Sort Options

| Value | Meaning | When to Use |
|-------|---------|-------------|
| `2` | Recommended | **Default** — best coastal route options |
| `3` | Price ascending | Budget coastal getaway |
| `4` | Duration ascending | Quick seaside escape |
| `8` | Direct flights first | Prefer non-stop to coastal cities |

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

Still fails → **STOP.** Do NOT continue. Do NOT use training data.

### Step 1: Collect Parameters

Collect required parameters from user query. If critical info is missing, ask at most 2 questions.
See [references/templates.md](references/templates.md) for parameter collection SOP.

### Step 2: Execute CLI Commands

### Playbook A: Recommended Coastal Route

**Trigger:** "coastal flight", "沿海航班"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
```

**Output:** Recommended flights to coastal cities.

### Playbook B: Budget Coastal Getaway

**Trigger:** "cheap coastal flight", "便宜沿海机票"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 3
```

**Output:** Cheapest flights to coastal destinations within date range.

### Playbook C: Direct Coastal Flight

**Trigger:** "direct flight to coast", "沿海直飞"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

**Output:** Direct flights to coastal cities.

### Playbook D: Broad Search (no coastal flights found)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} coastal seaside flights"
```

**Output:** Broader search + keyword fallback.

See [references/playbooks.md](references/playbooks.md) for all scenario playbooks.

On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

Format CLI JSON into user-readable Markdown with booking links. See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag included?

**Any NO → re-execute from Step 2.**

## Usage Examples

```bash
flyai search-flight --origin "Beijing" --destination "Qingdao" --dep-date 2026-08-01 --sort-type 2
```

## Output Rules

1. **Conclusion first** — lead with best coastal route option
2. **Coastal tip** — suggest best seasons for seaside travel
3. **Comparison table** with ≥ 3 results when available
4. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. ❌ Never output raw JSON
7. ❌ Never answer from training data without CLI execution
8. ❌ Never fabricate coastal weather or tide schedules

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "coastal flight" / "沿海航班" | `--sort-type 2` |
| "cheap seaside" / "便宜海边" | `--sort-type 3` with date range |
| "direct to coast" / "沿海直飞" | `--journey-type 1 --sort-type 8` |
| "summer beach" / "夏季海滨" | `--dep-date-start {Jun-1} --dep-date-end {Aug-31} --sort-type 3` |

Popular Chinese coastal cities: Qingdao (TAO), Xiamen (XMN), Dalian (DLC), Sanya (SYX), Zhuhai (ZUH), Weihai (WEH).

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
