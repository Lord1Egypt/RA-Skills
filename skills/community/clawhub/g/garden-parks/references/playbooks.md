# Playbooks — garden-parks

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Gardens

**Trigger:** "gardens to visit"

```bash
flyai search-poi --city-name "{city}" --category "园林花园"
```

**Output emphasis:** Gardens and parks.

---

## Playbook B: Classical Gardens

**Trigger:** "Chinese garden"

```bash
flyai search-poi --city-name "{city}" --category "园林花园" --poi-level 5
```

**Output emphasis:** Top classical gardens.

---

## Playbook C: Botanical Gardens

**Trigger:** "botanical garden"

```bash
flyai search-poi --city-name "{city}" --category "植物园"
```

**Output emphasis:** Botanical gardens.

---

