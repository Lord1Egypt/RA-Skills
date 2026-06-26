# Playbooks — border-flight

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| sort-type | `--sort-type` | Default: **2** (recommended) |
| journey-type | `--journey-type` | 1=direct, 2=connecting |

---

## Playbook A: Recommended International Route

**Trigger:** User says "international flight", "国际航班", "出境航班".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
```

**Output:** Recommended international flights.

---

## Playbook B: Budget International Travel

**Trigger:** User says "cheap international flight", "便宜国际机票", "特价出国".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 3
```

**Output:** Cheapest international flights.

---

## Playbook C: Direct International Flight

**Trigger:** User says "direct international", "国际直飞", "不中转国际".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 8
```

**Output:** Direct international flights first.

---

## Playbook D: Broad Search

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} international flights"
```

**Output:** Broader search + keyword fallback.
