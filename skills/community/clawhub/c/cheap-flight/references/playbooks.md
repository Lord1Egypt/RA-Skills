# Playbooks — cheap-flight-finder

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.
> Commands used: `search-flight` (primary), `keyword-search` (fallback), `ai-search` (complex intent fallback)

---

## Playbook A: Maximum Savings

**Trigger:** "cheapest possible", "穷游", "最便宜"

```bash
# 1. Base search — price ascending
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date 2026-05-01 --sort-type 3

# 2. Flexible dates ±3 days
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date-start 2026-04-28 --dep-date-end 2026-05-04 --sort-type 3

# 3. Red-eye flights
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date 2026-05-01 --dep-hour-start 21 --sort-type 3
```

**Output:** Compare lowest from all 3 searches. Show savings: "Flexible dates + red-eye saves ¥XXX vs fixed date."

---

## Playbook B: Budget Cap

**Trigger:** "under 500", "不超过XXX", "budget 800"

```bash
# 1. Strict budget
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date 2026-05-01 --max-price 500 --sort-type 3

# 2. If results < 3 → relax 20%
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date 2026-05-01 --max-price 600 --sort-type 3
```

**Output:** Split display — "Within budget: X options" + "Slightly over: X options (marked)."

---

## Playbook C: Urgent Departure

**Trigger:** "tomorrow", "tonight", "ASAP", "明天就飞", "今晚"

```bash
# Today
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date {today} --sort-type 3

# Tomorrow
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date {tomorrow} --sort-type 3
```

**Output:** Flag "Last-minute pricing may be higher than average. Book quickly to secure the fare."

---

## Playbook D: Round Trip Savings

**Trigger:** "return ticket", "round trip", "往返", "来回"

```bash
# Bundled round-trip
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date 2026-05-01 --back-date 2026-05-05 --sort-type 3

# Separate legs for comparison
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date 2026-05-01 --sort-type 3
flyai search-flight --origin "{d}" --destination "{o}" \
  --dep-date 2026-05-05 --sort-type 3
```

**Output:** Show "Bundled ¥XXX" vs "Separate total ¥XXX". Flag which is cheaper.
