# Playbooks — flyai-plan-japan-travel

> CLI command sequences. Use domain knowledge from SKILL.md for parameter mapping only.

---

## Playbook A: Multi-City Itinerary (default)

**Trigger:** User wants a multi-city Japan trip.

**Prerequisites:** origin city + dates + days collected.

```bash
# 1. Visa
flyai fliggy-fast-search --query "Japan visa"

# 2. Outbound flight
flyai search-flight --origin "{origin}" --destination "{entry_city}" \
  --dep-date "{day1}" --sort-type 3

# 3. Return flight
flyai search-flight --origin "{exit_city}" --destination "{origin}" \
  --dep-date "{dayN}" --sort-type 3

# 4. Hotels per city (split by itinerary)
flyai search-hotels --dest-name "{city1}" \
  --check-in-date "{day1}" --check-out-date "{dayX}" --sort rate_desc
flyai search-hotels --dest-name "{city2}" \
  --check-in-date "{dayX}" --check-out-date "{dayY}" --sort rate_desc

# 5. Attractions per city (category from user interest mapping)
flyai search-poi --city-name "{city1}" --category "{mapped_category}"
flyai search-poi --city-name "{city2}" --category "{mapped_category}"
```

**Enrichment:** Add transport between cities (use Shinkansen timing from domain knowledge), JR Pass recommendation.

---

## Playbook B: Single-City Deep Dive

**Trigger:** User specifies one city ("Tokyo 3 days", "Kyoto deep dive").

```bash
flyai search-flight --origin "{origin}" --destination "{city}" \
  --dep-date "{day1}" --sort-type 3
flyai search-flight --origin "{city}" --destination "{origin}" \
  --dep-date "{dayN}" --sort-type 3

flyai search-hotels --dest-name "{city}" \
  --check-in-date "{day1}" --check-out-date "{dayN}" --sort rate_desc

# Multiple categories to fill each day
flyai search-poi --city-name "{city}" --poi-level 5
flyai search-poi --city-name "{city}" --category "{interest_1}"
flyai search-poi --city-name "{city}" --category "{interest_2}"
```

---

## Playbook C: Budget Trip

**Trigger:** User says "budget", "cheap", "save money", "穷游".

```bash
# Cheapest flight (try multiple entry cities)
flyai search-flight --origin "{origin}" --destination "Osaka" \
  --dep-date "{day1}" --sort-type 3
flyai search-flight --origin "{origin}" --destination "Tokyo" \
  --dep-date "{day1}" --sort-type 3

# Flexible dates
flyai search-flight --origin "{origin}" --destination "{cheaper_city}" \
  --dep-date-start "{day1-3}" --dep-date-end "{day1+3}" --sort-type 3

# Budget hotels
flyai search-hotels --dest-name "{city}" --max-price 400 --sort price_asc \
  --check-in-date "{day1}" --check-out-date "{dayN}"

# Free/cheap attractions
flyai search-poi --city-name "{city}" --category "宗教场所"
flyai search-poi --city-name "{city}" --category "城市观光"
```

**Enrichment:** Note budget tips from domain knowledge (fly into Osaka = cheaper, stay in Osaka instead of Kyoto = 30% savings, etc.)

---

## Playbook D: Themed Trip

**Trigger:** User has a specific theme (cherry blossom, skiing, onsen, etc.)

```bash
# Flexible dates matching season
flyai search-flight --origin "{origin}" --destination "{city}" \
  --dep-date-start "{season_start}" --dep-date-end "{season_end}" --sort-type 3

# Theme attractions
flyai search-poi --city-name "{city}" --category "{theme_category}"
flyai search-poi --city-name "{city}" --keyword "{theme_keyword}"

# Theme hotels
flyai search-hotels --dest-name "{city}" \
  --key-words "{theme_keyword}" --sort rate_desc

# Supplementary
flyai fliggy-fast-search --query "{city} {theme} travel"
```

**Category/keyword mapping by theme:**
| Theme | `--category` | `--keyword` |
|-------|-------------|-------------|
| Cherry blossom | — | "樱花" or "cherry blossom" |
| Onsen | `温泉` | "温泉" or "onsen" |
| Skiing | `滑雪` | "ski" |
| Autumn foliage | `自然风光` | "红叶" or "maple" |
| Anime/pop culture | `文创街区` | "anime" or "秋叶原" |
