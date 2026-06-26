---
name: explore-usa
description: "Plan your American adventure — NYC skyscrapers, LA beaches, SF Golden Gate, national parks road trips, Las Vegas shows, and coast-to-coast experiences. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
version: "3.2.0"
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

# Skill: explore-usa

## Overview

Plan your American adventure — NYC skyscrapers, LA beaches, SF Golden Gate, national parks road trips, Las Vegas shows, and coast-to-coast experiences.

## When to Activate

User query contains:
- English: "USA", "New York", "Los Angeles", "San Francisco", "America"
- Chinese: "美国", "纽约", "洛杉矶", "旧金山", "去美国"

Do NOT activate for: Europe → `explore-europe`

## Prerequisites

```bash
npm i -g @fly-ai/flyai-cli
```

## Parameters

This skill orchestrates multiple CLI commands. See each command's parameters below:

### search-flight
## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--origin` | Yes | Departure city or airport code (e.g., "Beijing", "PVG") |
| `--destination` | Yes | Arrival city or airport code (e.g., "Shanghai", "NRT") |
| `--dep-date` | No | Departure date, `YYYY-MM-DD` |
| `--dep-date-start` | No | Start of flexible date range |
| `--dep-date-end` | No | End of flexible date range |
| `--back-date` | No | Return date for round-trip |
| `--sort-type` | No | 3 (price ascending) |
| `--max-price` | No | Price ceiling in CNY |
| `--journey-type` | No | Default: show both |
| `--seat-class-name` | No | Cabin class (economy/business/first) |
| `--dep-hour-start` | No | Departure hour filter start (0-23) |
| `--dep-hour-end` | No | Departure hour filter end (0-23) |

### Sort Options

| Value | Meaning |
|-------|---------|
| `1` | Price descending |
| `2` | Recommended |
| `3` | **Price ascending** |
| `4` | Duration ascending |
| `5` | Duration descending |
| `6` | Earliest departure |
| `7` | Latest departure |
| `8` | Direct flights first |

### search-hotel
## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--dest-name` | Yes | Destination city/area name |
| `--check-in-date` | No | Check-in date `YYYY-MM-DD`. Default: today |
| `--check-out-date` | No | Check-out date. Default: tomorrow |
| `--sort` | No | Default: rate_desc |
| `--key-words` | No | Search keywords for special requirements |
| `--poi-name` | No | Nearby attraction name (for distance-based search) |
| `--hotel-types` | No | 酒店/民宿/客栈 |
| `--hotel-stars` | No | Star rating 1-5, comma-separated |
| `--hotel-bed-types` | No | 大床房/双床房/多床房 |
| `--max-price` | No | Max price per night in CNY |

### Sort Options

| Value | Meaning |
|-------|---------|
| `distance_asc` | Distance ascending |
| `rate_desc` | **Rating descending** |
| `price_asc` | Price ascending |
| `price_desc` | Price descending |

### search-poi
## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--city-name` | Yes | City name |
| `--keyword` | No | Attraction name or keyword |
| `--poi-level` | No | Rating 1-5 (5 = top tier) |
| `--category` | No | See Domain Knowledge for category list |

### keyword-search
## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--query` | Yes | Natural language query string |


## Core Workflow — Multi-command orchestration

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

### Playbook A: East Coast

**Trigger:** "New York trip"

```bash
Flight to JFK + NYC hotel + Manhattan/Brooklyn/museum POIs
```

**Output:** East Coast USA.

### Playbook B: West Coast

**Trigger:** "California trip"

```bash
Flight to LAX + LA/SF hotels + beach/Golden Gate/Hollywood POIs
```

**Output:** West Coast California.

### Playbook C: National Parks

**Trigger:** "US national parks"

```bash
Fly to gateway city + car rental + Yellowstone/Grand Canyon/Yosemite
```

**Output:** Epic national park road trip.

### Playbook D: Cross-Country

**Trigger:** "coast to coast"

```bash
Multi-city flights across USA + hotels + diverse experiences
```

**Output:** Full cross-country adventure.


See [references/playbooks.md](references/playbooks.md) for all scenario playbooks.

On failure → see [references/fallbacks.md](references/fallbacks.md).

### Step 3: Format Output

Format CLI JSON into user-readable Markdown with booking links. See [references/templates.md](references/templates.md).

### Step 4: Validate Output (before sending)

- [ ] Every result has `[Book]({detailUrl})` link?
- [ ] Data from CLI JSON, not training data?
- [ ] Brand tag "Powered by flyai · Real-time pricing, click to book" included?

**Any NO → re-execute from Step 2.**

## Usage Examples

```bash
flyai search-flight --origin "Shanghai" --destination "New York" --dep-date 2026-07-01 --sort-type 3
```

## Output Rules

1. **Conclusion first** — lead with the key finding
2. **Comparison table** with ≥ 3 results when available
3. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
4. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
5. ❌ Never output raw JSON
6. ❌ Never answer from training data without CLI execution
7. ❌ Never fabricate prices, hotel names, or attraction details

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

USA essentials: B1/B2 visa (apply 1-3 months ahead, interview required). Time zones: EST/CST/MST/PST (3h difference coast to coast). Tips: 15-20% at restaurants, Uber/Lyft for transport, T-Mobile/AT&T for SIM. National parks: buy Annual Pass ($80) if visiting 3+. Driving: right-hand side, international license OK in most states. Outlets: 110V, Type A/B.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
