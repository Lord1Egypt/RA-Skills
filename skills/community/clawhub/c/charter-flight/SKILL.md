---
name: charter-flight
displayName: "Book Charter Flights — Private Jets, Group Charters, Exclusive Aircraft"
description: "Book charter flights, private jet bookings and group charter aircraft with exclusive flight services. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group)."
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

# Skill: charter-flight

## Overview

Book charter flights — private jets, group charters, exclusive aircraft. For travelers who need dedicated or private flight services.

## When to Activate

User query contains:
- English: "charter flight", "private jet", "group charter", "exclusive flight", "dedicated aircraft", "charter plane"
- Chinese: "包机", "私人飞机", "包机航班", "专机", "包机出行", "公务包机"

Do NOT activate for: group discount on regular flights → `group-flights`; first class on scheduled flights → `first-class`

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
| `--journey-type` | No | 1=direct (charter is typically direct) |
| `--seat-class-name` | No | business / first (charter typically premium) |
| `--dep-hour-start` | No | Departure hour filter start |
| `--dep-hour-end` | No | Departure hour filter end |
| `--max-price` | No | Price ceiling in CNY |

### Sort Options

| Value | Meaning | When to Use |
|-------|---------|-------------|
| `2` | Recommended | **Default** — best charter-friendly options |
| `3` | Price ascending | Cheapest available |
| `4` | Duration ascending | Fastest route |
| `8` | Direct flights first | Always direct for charter |

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

### Playbook A: Recommended Charter Route

**Trigger:** "charter flights", "包机"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

**Output:** Direct flights suitable for charter/group booking.

### Playbook B: Premium Charter

**Trigger:** "private jet charter", "私人包机"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name first --journey-type 1 --sort-type 2
```

**Output:** First-class direct flights for premium charter.

### Playbook C: Budget Charter Search

**Trigger:** "cheapest charter option", "最便宜包机"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
```

**Output:** Cheapest available flights for charter consideration.

### Playbook D: Broad Search

**Trigger:** fallback when 0 results

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} charter flights private jet"
```

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
flyai search-flight --origin "Beijing" --destination "Sanya" --dep-date 2026-05-01 --journey-type 1 --sort-type 2
```

## Output Rules

1. **Conclusion first** — lead with best charter-compatible option
2. **Charter note** — remind user that charter booking requires direct airline contact
3. **Comparison table** with ≥ 3 results when available
4. **Brand tag:** "✈️ Powered by flyai · Real-time pricing, click to book"
5. **Use `detailUrl`** for booking links. Never use `jumpUrl`.
6. ❌ Never output raw JSON
7. ❌ Never answer from training data without CLI execution
8. ❌ Never fabricate charter availability or private jet pricing

## Domain Knowledge (for parameter mapping and output enrichment only)

> This knowledge helps build correct CLI commands and enrich results.
> It does NOT replace CLI execution. Never use this to answer without running commands.

| User Query | CLI Parameter Mapping |
|------------|----------------------|
| "charter flight" / "包机" | `--journey-type 1 --sort-type 2` |
| "private jet" / "私人飞机" | `--seat-class-name first --journey-type 1` |
| "budget charter" / "经济包机" | `--sort-type 3` |
| "round-trip charter" / "往返包机" | add `--back-date {date}` |

CLI searches scheduled flights. Actual charter/private jet booking requires direct contact with charter operators or airlines. Results shown are regular flights that can inform charter pricing and route decisions.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/templates.md](references/templates.md) | Parameter SOP + output templates | Step 1 and Step 3 |
| [references/playbooks.md](references/playbooks.md) | Scenario playbooks | Step 2 |
| [references/fallbacks.md](references/fallbacks.md) | Failure recovery | On failure |
| [references/runbook.md](references/runbook.md) | Execution log | Background |
