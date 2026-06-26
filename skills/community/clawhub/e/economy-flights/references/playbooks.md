# Playbooks — economy-flights

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| seat-class-name | `--seat-class-name` | Always **economy** |
| sort-type | `--sort-type` | Default: **3** (price ascending) |
| max-price | `--max-price` | Optional: budget cap |
| dep-date-start | `--dep-date-start` | Optional: flexible dates start |
| dep-date-end | `--dep-date-end` | Optional: flexible dates end |

---

## Playbook A: Cheapest Economy

**Trigger:** User says "economy flights", "经济舱机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name economy --sort-type 3
```

**Output:** Economy flights sorted by lowest price.

---

## Playbook B: Flexible Date Cheapest

**Trigger:** User says "cheapest economy any day", "哪天最便宜".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start "{date-3}" --dep-date-end "{date+3}" --seat-class-name economy --sort-type 3
```

**Output:** Economy prices across a 7-day window, cheapest first.

---

## Playbook C: Budget-Capped Economy

**Trigger:** User says "economy under ¥{price}", "{price}以内的经济舱".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name economy --max-price {budget} --sort-type 3
```

**Output:** Economy flights within budget, sorted by price.

---

## Playbook D: Broad Search (no economy found)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
flyai keyword-search --query "{origin} to {destination} cheapest flights"
```

**Output:** Broader search without seat-class filter + keyword fallback.
