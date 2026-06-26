# Playbooks — budget-hotel-finder

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Under ¥300

**Trigger:** "cheap hotel", "便宜酒店"

```bash
flyai search-hotel --dest-name "{city}" --max-price 300 --sort price_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Budget options, cheapest first.

---

## Playbook B: Under ¥500 with Rating

**Trigger:** "good but cheap"

```bash
flyai search-hotel --dest-name "{city}" --max-price 500 --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Best rated within budget.

---

## Playbook C: Cheapest in City

**Trigger:** "最便宜的住一晚"

```bash
flyai search-hotel --dest-name "{city}" --sort price_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** No budget filter, pure cheapest.

---

