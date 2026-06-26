# Playbooks — extended-stay

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Monthly Stay

**Trigger:** "monthly rental", "月租"

```bash
flyai search-hotel --dest-name "{city}" --key-words "长租" --sort price_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Long-stay options, cheapest first.

---

## Playbook B: Serviced Apartment

**Trigger:** "serviced apartment"

```bash
flyai search-hotel --dest-name "{city}" --key-words "服务式公寓" --sort rate_desc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Apartment-style with hotel services.

---

## Playbook C: With Kitchen

**Trigger:** "有厨房的住宿"

```bash
flyai search-hotel --dest-name "{city}" --key-words "厨房" --sort price_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Accommodation with cooking facilities.

---

