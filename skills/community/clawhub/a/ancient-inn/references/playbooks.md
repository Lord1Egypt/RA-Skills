# Playbooks — ancient-town-inn

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Inn Inside Town

**Trigger:** "stay in ancient town"

```bash
flyai search-poi --city-name "{city}" --category "古镇古村" --keyword "{town}"
flyai search-hotels --dest-name "{town}" --hotel-types "客栈" --sort rate_desc
```

**Output emphasis:** Verify town → search inns inside.

---

## Playbook B: Courtyard Inn

**Trigger:** "四合院客栈"

```bash
flyai search-hotels --dest-name "{town}" --hotel-types "客栈" --key-words "四合院" --sort rate_desc
```

**Output emphasis:** Traditional courtyard inns.

---

## Playbook C: Budget Inn

**Trigger:** "cheap inn", "便宜客栈"

```bash
flyai search-hotels --dest-name "{town}" --hotel-types "客栈" --sort price_asc
```

**Output emphasis:** Affordable ancient town accommodation.

---

