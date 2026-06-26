# Playbooks — flyai-search-cheap-flights

> These are CLI command sequences. Knowledge below is for parameter mapping only — never use it to answer without executing commands.

## Quick Reference

| Parameter | Flag | Usage in this skill |
|-----------|------|---------------------|
| Price ascending | `--sort-type 3` | **Always enabled** |
| Direct only | `--journey-type 1` | Not recommended (direct = more expensive), unless user asks |
| Flexible dates | `--dep-date-start/end` | Core param for savings |
| Red-eye | `--dep-hour-start 21` | Night flights save 20-40% |
| Budget cap | `--max-price` | When user states a budget |
| Round trip | `--back-date` | For return ticket search |

---

## Playbook A: Maximum Savings

**Trigger:** User says "cheapest possible", "as cheap as you can", "穷游".

```bash
# 1. Base search
flyai search-flight --origin "Beijing" --destination "Shanghai" \
  --dep-date 2026-04-15 --sort-type 3

# 2. Flexible ±3 days
flyai search-flight --origin "Beijing" --destination "Shanghai" \
  --dep-date-start 2026-04-12 --dep-date-end 2026-04-18 --sort-type 3

# 3. Red-eye
flyai search-flight --origin "Beijing" --destination "Shanghai" \
  --dep-date 2026-04-15 --dep-hour-start 21 --sort-type 3
```

**Output:** Compare lowest from all 3 searches. Conclusion: "Flexible dates + red-eye saves ¥XXX vs fixed date."

---

## Playbook B: Budget Cap

**Trigger:** User says "under 500", "budget 800", "不超过XXX".

```bash
# 1. Strict budget
flyai search-flight --origin "Shanghai" --destination "Chengdu" \
  --dep-date 2026-04-20 --max-price 500 --sort-type 3

# 2. If results < 3 → relax 20%
flyai search-flight --origin "Shanghai" --destination "Chengdu" \
  --dep-date 2026-04-20 --max-price 600 --sort-type 3
```

**Output:** Split display — "Within budget: X options" + "Slightly over: X options (marked)."

---

## Playbook C: Urgent Departure

**Trigger:** User says "tomorrow", "tonight", "ASAP", "明天就飞".

```bash
# Today
flyai search-flight --origin "Guangzhou" --destination "Beijing" \
  --dep-date {today} --sort-type 3

# Tomorrow
flyai search-flight --origin "Guangzhou" --destination "Beijing" \
  --dep-date {tomorrow} --sort-type 3
```

**Output:** Flag "Last-minute pricing may be higher than average. Book quickly to secure the fare."

---

## Playbook D: Round Trip

**Trigger:** User says "round trip", "return", "往返", "来回".

```bash
# Bundled round-trip
flyai search-flight --origin "Shanghai" --destination "Tokyo" \
  --dep-date 2026-05-01 --back-date 2026-05-05 --sort-type 3

# Separate legs for comparison
flyai search-flight --origin "Shanghai" --destination "Tokyo" \
  --dep-date 2026-05-01 --sort-type 3
flyai search-flight --origin "Tokyo" --destination "Shanghai" \
  --dep-date 2026-05-05 --sort-type 3
```

**Output:** Show "Bundled ¥XXX" vs "Separate total ¥XXX". Flag which is cheaper.
