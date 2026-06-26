# Playbooks — capsule-pod-hotel

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Capsule Hotel

**Trigger:** "capsule hotel", "胶囊酒店"

```bash
flyai search-hotel --dest-name "{city}" --key-words "太空舱" --sort price_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Pod hotels, cheapest first.

---

## Playbook B: Near Station/Airport

**Trigger:** "capsule near train station"

```bash
flyai search-hotel --dest-name "{city}" --key-words "太空舱 火车站" --sort distance_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Capsule hotels near transit hubs.

---

