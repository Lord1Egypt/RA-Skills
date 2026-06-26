# Playbooks — airport-transit-hotel

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Near Airport

**Trigger:** "airport hotel", "机场酒店"

```bash
flyai search-hotel --dest-name "{city}" --key-words "机场" --sort distance_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Hotels near airport, closest first.

---

## Playbook B: Transit Capsule

**Trigger:** "transit hotel", "中转休息"

```bash
flyai search-hotel --dest-name "{city}" --key-words "机场 太空舱" --sort price_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Capsule/pod hotels near airport for short stays.

---

## Playbook C: Pre-Flight Stay

**Trigger:** "early morning flight", "早班机前一晚"

```bash
flyai search-hotel --dest-name "{city}" --key-words "机场" --sort distance_asc --check-in-date {tonight} --check-out-date {tomorrow}
```

**Output emphasis:** One night before early departure.

---

