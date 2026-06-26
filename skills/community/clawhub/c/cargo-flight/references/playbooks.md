# Playbooks — cargo-flight

> CLI command sequences only. Knowledge is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| sort-type | `--sort-type` | Default: **2** (recommended) |
| journey-type | `--journey-type` | Optional: 1=direct, 2=connecting |

---

## Playbook A: Recommended Cargo Route

**Trigger:** User says "air cargo", "空运", "货运航班".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
```

**Output:** Recommended flights suitable for cargo shipping.

---

## Playbook B: Cheapest Cargo Route

**Trigger:** User says "cheapest air freight", "最便宜空运", "经济货运".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
```

**Output:** Cheapest available flights for cargo consideration.

---

## Playbook C: Fastest Cargo Route

**Trigger:** User says "fastest shipping", "最快空运", "急件".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 4
```

**Output:** Shortest duration flights for urgent cargo.

---

## Playbook D: Direct Cargo Route

**Trigger:** User says "direct cargo flight", "直飞货运", "不中转货运".

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 1 --sort-type 2
```

**Output:** Direct flights preferred for cargo safety.
