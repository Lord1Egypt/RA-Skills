# Playbooks — first-class

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| seat-class-name | `--seat-class-name` | Always **first** |
| sort-type | `--sort-type` | Default: **2** (recommended) |
| journey-type | `--journey-type` | Optional: **1** (direct only) |

---

## Playbook A: Recommended First Class

**Trigger:** User says "first class flights", "头等舱机票".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name first --sort-type 2
```

**Output:** Best first class options sorted by recommendation.

---

## Playbook B: Cheapest First Class

**Trigger:** User says "cheapest first class", "最便宜的头等舱".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name first --sort-type 3
```

**Output:** First class flights sorted by lowest price.

---

## Playbook C: Direct First Class Only

**Trigger:** User says "direct first class", "直飞头等舱".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name first --journey-type 1 --sort-type 4
```

**Output:** Non-stop first class flights, fastest duration first.

---

## Playbook D: Broad Search (no first class found)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name first --sort-type 2
flyai keyword-search --query "{origin} to {destination} first class flights"
```

**Output:** Broader search + keyword fallback.
