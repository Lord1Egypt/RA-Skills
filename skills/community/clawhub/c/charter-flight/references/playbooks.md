# Playbooks — charter-flight

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| journey-type | `--journey-type` | Default: **1** (direct) |
| sort-type | `--sort-type` | Default: **2** (recommended) |
| seat-class-name | `--seat-class-name` | Optional: first / business |

---

## Playbook A: Recommended Charter Route

**Trigger:** User says "charter flights", "包机航班".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

**Output:** Direct flights suitable for charter/group booking.

---

## Playbook B: Premium Charter (Private Jet Style)

**Trigger:** User says "private jet charter", "私人包机", "专机".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name first --journey-type 1 --sort-type 2
```

**Output:** First-class direct flights for premium charter.

---

## Playbook C: Budget Charter Search

**Trigger:** User says "cheapest charter option", "最便宜包机".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
```

**Output:** Cheapest available flights for charter consideration.

---

## Playbook D: Broad Search (no direct flights found)

**Trigger:** Playbook A/B/C returns 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} charter flights private jet"
```

**Output:** Broader search without direct filter + keyword fallback.
