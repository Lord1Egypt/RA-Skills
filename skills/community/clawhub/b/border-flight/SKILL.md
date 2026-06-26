---
name: border-flight
displayName: "Cross-Border Flights — International Departures, Visa-Required Routes, Overseas Travel"
description: "Search cross-border flights, international departures and visa-required routes with overseas travel booking. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
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

# Skill: border-flight

## Overview

Cross-border flights — international departures, visa-required routes, overseas travel. For travelers flying internationally across borders.

## When to Activate

User query contains:
- English: "border flight", "cross-border flight", "international departure", "overseas flight", "visa-required flight", "outbound flight"
- Chinese: "跨境航班", "国际航班", "出境航班", "出国机票", "海外航班", "出港航班"

Do NOT activate for: domestic flights → `economy-flights`; connecting flights → `connecting`

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
| `2` | Recommended | **Default** — best international options |
| `3` | Price ascending | Budget international travel |
| `4` | Duration ascending | Fastest international route |
| `8` | Direct flights first | Prefer non-stop international |

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

### Playbook A: Recommended International Route

**Trigger:** "international flight", "国际航班"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
```

**Output:** Recommended international flights.

### Playbook B: Budget International Travel

**Trigger:** "cheap international flight", "便宜国际机票"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 3
```

**Output:** Cheapest international flights within date range.

### Playbook C: Direct International Flight

**Trigger:** "direct international flight", "国际直飞"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

**Output:** Direct international flights.

### Playbook D: Broad Search (no international flights found)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} international flights"
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
flyai search-flight --origin "Shanghai" --destination "Tokyo" --dep-date 2026-06-01 --sort-type 2
```

## Output Rules

1. **Conclusion first** — lead with best international option
2. **Visa reminder** — note visa requirements for the destination country
3. **Comparison table** with ≥ 3 results when available
4. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. ❌ Never output raw JSON
7. ❌ Never answer from training data without CLI execution
8. ❌ Never fabricate visa policies or entry requirements

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "international flight" / "国际航班" | `--sort-type 2` |
| "cheap overseas" / "便宜出国" | `--sort-type 3` with date range |
| "direct international" / "国际直飞" | `--journey-type 1 --sort-type 8` |
| "outbound flight" / "出境航班" | `--sort-type 2` |

Major Chinese international hubs: PEK, PVG, CAN, SZX, CTU. CLI does not have a border/customs filter — all results are regular flights.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
