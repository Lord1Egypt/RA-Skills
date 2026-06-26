# Playbooks — ancient-town-explorer

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Ancient Towns

**Trigger:** "ancient town"

```bash
flyai search-poi --city-name "{city}" --category "古镇古村"
```

**Output emphasis:** Ancient towns and villages.

---

## Playbook B: Water Towns

**Trigger:** "water town"

```bash
flyai search-poi --city-name "{city}" --keyword "水乡"
```

**Output emphasis:** Jiangnan water villages.

---

## Playbook C: Ethnic Villages

**Trigger:** "ethnic village"

```bash
flyai search-poi --city-name "{city}" --keyword "古村"
```

**Output emphasis:** Minority ethnic villages.

---

