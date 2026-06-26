# Playbooks — flyai-find-hotel-near-attraction

> CLI sequences only. Domain knowledge in SKILL.md is for parameter mapping — never answer without executing.

## Quick Reference

| Parameter | Flag | This Skill |
|-----------|------|-----------|
| POI name | `--poi-name` | **Always required** |
| Distance sort | `--sort distance_asc` | **Always enabled** |
| Accommodation type | `--hotel-types` | Match to POI type (see below) |
| Keywords | `--key-words` | For special facilities ("pool", "温泉") |

---

## Playbook A: City Landmarks (West Lake, Forbidden City, Bund)

```bash
flyai search-poi --city-name "{city}" --keyword "{poi}"
flyai search-hotels --dest-name "{city}" --poi-name "{poi}" \
  --check-in-date "{in}" --check-out-date "{out}" --sort distance_asc
```

**Enrichment:** Recommend hotels within 1km (walking distance).

---

## Playbook B: Ancient Towns (Wuzhen, Lijiang, Fenghuang)

```bash
flyai search-poi --city-name "{city}" --keyword "{town}"

# Prefer inns (客栈) for ancient towns
flyai search-hotels --dest-name "{town}" --poi-name "{town}" \
  --hotel-types "客栈" --sort distance_asc

# If < 3 results, expand to all types
flyai search-hotels --dest-name "{town}" --poi-name "{town}" \
  --sort distance_asc
```

**Enrichment:** Note "staying inside the scenic area offers the best experience."

---

## Playbook C: Theme Parks (Disney, Universal Studios)

```bash
flyai search-poi --city-name "{city}" --keyword "{park}"
flyai search-hotels --dest-name "{city}" --poi-name "{park}" \
  --sort distance_asc

# Bonus: search tickets
flyai fliggy-fast-search --query "{city} {park} tickets"
```

**Enrichment:** Flag official partner hotels if identifiable from results.

---

## Playbook D: Natural Scenic Areas (Zhangjiajie, Jiuzhaigou)

```bash
flyai search-poi --city-name "{city}" --keyword "{park}"
flyai search-hotels --dest-name "{city}" --poi-name "{park}" \
  --sort distance_asc

# If < 3 → expand to city-wide
flyai search-hotels --dest-name "{city}" --sort distance_asc
```

**Enrichment:** Split output into "Near park" vs "City center" sections with estimated drive time.
