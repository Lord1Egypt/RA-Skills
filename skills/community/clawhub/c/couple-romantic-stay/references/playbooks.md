# Playbooks — couple-romantic-stay

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Romantic Stay

**Trigger:** "romantic hotel", "情侣酒店"

```bash
flyai search-hotel --dest-name "{city}" --hotel-bed-types "大床房" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** King beds, highest rated.

---

## Playbook B: Scenic View Room

**Trigger:** "有景观的房间"

```bash
flyai search-hotel --dest-name "{city}" --hotel-bed-types "大床房" --key-words "景观" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Rooms with views.

---

## Playbook C: Anniversary Special

**Trigger:** "anniversary hotel", "纪念日"

```bash
flyai search-hotel --dest-name "{city}" --hotel-stars 5 --hotel-bed-types "大床房" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** 5-star luxury for special occasions.

---

