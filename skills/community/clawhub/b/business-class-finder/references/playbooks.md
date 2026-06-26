# Playbooks — business-class-finder

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Business Class

**Trigger:** "business class", "商务舱"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name business --sort-type 3
```

**Output emphasis:** Business class options, cheapest first.

---

## Playbook B: First Class

**Trigger:** "first class", "头等舱"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --seat-class-name first --sort-type 3
```

**Output emphasis:** First class, luxury comparison.

---

## Playbook C: Premium Economy Alternative

**Trigger:** "premium but not too expensive"

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
# Filter for premium options from results
```

**Output emphasis:** When business is too expensive, show premium economy.

---

