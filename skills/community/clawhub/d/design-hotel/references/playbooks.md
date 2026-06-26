# Playbooks — boutique-design-hotel

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Best Design Hotel

**Trigger:** "boutique hotel", "精品酒店"

```bash
flyai search-hotels --dest-name "{city}" --key-words "精品" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Top-rated boutique properties.

---

## Playbook B: Art Hotel

**Trigger:** "art hotel", "艺术酒店"

```bash
flyai search-hotels --dest-name "{city}" --key-words "艺术" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Hotels with artistic themes.

---

## Playbook C: Design + Views

**Trigger:** "有设计感的景观酒店"

```bash
flyai search-hotels --dest-name "{city}" --key-words "精品 景观" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Design hotels with scenic views.

---

