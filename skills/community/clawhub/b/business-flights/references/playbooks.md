# Playbooks — business-flights

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| seat-class-name | `--seat-class-name` | Always **business** |
| sort-type | `--sort-type` | Default: **4** (duration ascending) |
| dep-hour-start | `--dep-hour-start` | Optional: **6** (morning flights) |
| dep-hour-end | `--dep-hour-end` | Optional: **12** (morning flights) |
| journey-type | `--journey-type` | Optional: **1** (direct only) |

---

## Playbook A: Fastest Business Class

**Trigger:** User says "business class flights", "商务舱机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name business --sort-type 4
```

**Output:** Business class flights sorted by shortest duration.

---

## Playbook B: Cheapest Business Class

**Trigger:** User says "cheapest business class", "最便宜的商务舱".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name business --sort-type 3
```

**Output:** Business class flights sorted by lowest price.

---

## Playbook C: Morning Business Flight

**Trigger:** User says "morning business flight", "早班商务舱".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name business --dep-hour-start 6 --dep-hour-end 12 --sort-type 4
```

**Output:** Morning business class departures, fastest first.

---

## Playbook D: Broad Search (no business class found)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name business --sort-type 2
flyai keyword-search --query "{origin} to {destination} business class flights"
```

**Output:** Broader search + keyword fallback.
