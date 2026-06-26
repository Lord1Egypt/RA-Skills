# Playbooks — food-tour

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Food Tour

**Trigger:** "food tour in {city}"

```bash
flyai search-poi --city-name "{city}" --category "市集"
flyai keyword-search --query "美食 {city}"
```

**Output emphasis:** Comprehensive food exploration.

---

## Playbook B: Street Food

**Trigger:** "street food {city}"

```bash
flyai search-poi --city-name "{city}" --keyword "小吃街"
```

**Output emphasis:** Street food hotspots.

---

## Playbook C: Cooking Class

**Trigger:** "cooking class {city}"

```bash
flyai keyword-search --query "烹饪课程 {city}"
```

**Output emphasis:** Cooking class experiences.

---

## Playbook D: Fine Dining

**Trigger:** "Michelin {city}"

```bash
flyai keyword-search --query "米其林餐厅 {city}"
```

**Output emphasis:** Top-rated restaurants.

---

