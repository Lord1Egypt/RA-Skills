# Playbooks — beachfront-resort-finder

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Beach Resort

**Trigger:** "beach hotel", "海边酒店"

```bash
flyai search-poi --city-name "{city}" --category "沙滩海岛"
flyai search-hotels --dest-name "{city}" --key-words "海景" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Beach POIs → oceanfront hotels.

---

## Playbook B: Private Beach

**Trigger:** "private beach resort"

```bash
flyai search-hotels --dest-name "{city}" --key-words "私人海滩" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Resorts with private beach access.

---

## Playbook C: Budget Beach

**Trigger:** "cheap beach hotel"

```bash
flyai search-hotels --dest-name "{city}" --key-words "海景" --sort price_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Affordable oceanfront options.

---

