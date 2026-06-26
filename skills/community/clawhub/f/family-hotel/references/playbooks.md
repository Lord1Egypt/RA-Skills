# Playbooks — family-hotel

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Family Room

**Trigger:** "family hotel", "亲子酒店"

```bash
flyai search-hotel --dest-name "{city}" --hotel-bed-types "多床房" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Multi-bed rooms, highest rated.

---

## Playbook B: Family + Kids Area

**Trigger:** "有儿童乐园的酒店"

```bash
flyai search-hotel --dest-name "{city}" --key-words "亲子" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Hotels with kids facilities.

---

## Playbook C: Family + Theme Park

**Trigger:** "Disney area family hotel"

```bash
flyai search-hotel --dest-name "{city}" --key-words "亲子" --hotel-bed-types "多床房" --sort distance_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Family hotels near attractions.

---

