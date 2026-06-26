# Playbooks — anniversary

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| journey-type | `--journey-type` | Default: **1** (direct) |
| sort-type | `--sort-type` | Default: **2** (recommended) |
| seat-class-name | `--seat-class-name` | Optional: business / first |

---

## Playbook A: Romantic Getaway

**Trigger:** User says "anniversary flight", "纪念日航班", "纪念日旅行".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

---

## Playbook B: Premium Anniversary

**Trigger:** User says "luxury anniversary", "高端纪念旅行", "商务舱纪念".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name business --journey-type 1 --sort-type 2
```

---

## Playbook C: Budget Anniversary Trip

**Trigger:** User says "budget anniversary", "经济纪念旅行", "性价比纪念".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 3
```

---

## Playbook D: Broad Search

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} anniversary romantic flights"
```
