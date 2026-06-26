# Playbooks — breakfast-included-hotel

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: With Breakfast

**Trigger:** "breakfast included", "含早"

```bash
flyai search-hotels --dest-name "{city}" --key-words "含早" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Hotels with breakfast included.

---

## Playbook B: Budget + Breakfast

**Trigger:** "cheap with breakfast"

```bash
flyai search-hotels --dest-name "{city}" --key-words "含早" --sort price_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Cheapest options with breakfast.

---

