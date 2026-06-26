# Playbooks — connecting

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| journey-type | `--journey-type` | Always **2** (connecting) |
| sort-type | `--sort-type` | Default: **3** (cheapest) |
| transfer-city  total-duration-hour | `--total-duration-hour` | Optional: max trip hours |

---

## Playbook A: Cheapest Connecting Flight

**Trigger:** User says "connecting flights", "中转航班".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 2 --sort-type 3
```

---

## Playbook B: Fastest Connecting Flight

**Trigger:** User says "fastest connecting flight", "最快中转".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 2 --sort-type 4
```

---

## Playbook C: Via Specific Transit City

**Trigger:** User says "connecting via {city}", "经{city}中转".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
```

---

## Playbook D: Broad Search

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
flyai keyword-search --query "{origin} to {destination} connecting flights layover"
```
