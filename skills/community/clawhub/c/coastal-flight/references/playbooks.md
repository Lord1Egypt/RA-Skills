# Playbooks — coastal-flight

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| sort-type | `--sort-type` | Default: **2** (recommended) |
| dep-date-start/end | `--dep-date-start/end` | Seasonal window |

---

## Playbook A: Recommended Coastal Route

**Trigger:** User says "coastal flight", "沿海航班", "沿海机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
```

**Output:** Recommended flights to coastal cities.

---

## Playbook B: Budget Coastal Getaway

**Trigger:** User says "cheap coastal flight", "便宜沿海机票", "特价海边".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 3
```

**Output:** Cheapest flights to coastal destinations.

---

## Playbook C: Direct Coastal Flight

**Trigger:** User says "direct to coast", "沿海直飞", "不中转沿海".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

**Output:** Direct flights to coastal cities.

---

## Playbook D: Broad Search

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} coastal flights"
```

**Output:** Broader search + keyword fallback.
