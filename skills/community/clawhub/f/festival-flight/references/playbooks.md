# Playbooks — festival-flight

> Scenario-specific CLI command templates.

---

## Playbook A: Festival Season Search

**Trigger:** "festival flight", "节日航班", "节日出行"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 2
```

**Fallback if 0 results:** Try `--sort-type 3` for cheapest options.

---

## Playbook B: Specific Festival Date

**Trigger:** "spring festival flight", "春节机票", "中秋节航班"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
```

**Fallback if 0 results:** Try ±3 days around the date.

---

## Playbook C: Budget Festival Travel

**Trigger:** "cheapest festival flight", "节日特价机票"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 3
```

**Fallback if 0 results:** Try `--sort-type 2` for recommended options.

---

## Playbook D: Broad Search (last resort)

**Trigger:** All above playbooks return 0 results.

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} festival holiday flights"
```
