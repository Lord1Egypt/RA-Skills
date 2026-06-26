# Playbooks — flexible-flights

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Week Scan

**Trigger:** "cheapest day this week"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {mon} --dep-date-end {sun} --sort-type 3
```

**Output emphasis:** Show lowest per day in table format.

---

## Playbook B: Month Scan

**Trigger:** "cheapest in May"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {month-1} --dep-date-end {month-end} --sort-type 3
```

**Output emphasis:** Scan entire month, highlight cheapest week.

---

## Playbook C: Flexible ±3 Days

**Trigger:** "around May 1st"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {date-3} --dep-date-end {date+3} --sort-type 3
```

**Output emphasis:** Show ±3 days around preferred date.

---

