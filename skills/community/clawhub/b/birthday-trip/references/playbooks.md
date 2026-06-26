# Playbooks — birthday-trip

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| sort-type | `--sort-type` | Default: **2** (recommended) |

---

## Playbook A: Birthday Getaway

**Trigger:** User says "birthday flight", "生日航班", "生日旅行".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
```

---

## Playbook B: Budget Birthday Trip

**Trigger:** User says "cheap birthday trip", "经济生日旅行", "省钱生日出行".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 3
```

---

## Playbook C: Surprise Trip

**Trigger:** User says "surprise trip", "生日惊喜出行", "直接飞".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

---

## Playbook D: Broad Search

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} flights"
```
