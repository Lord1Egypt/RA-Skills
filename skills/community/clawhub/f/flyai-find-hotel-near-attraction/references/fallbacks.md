# Fallbacks — Hotel Category (shared by 20 hotel skills)

## Case 0: flyai-cli Not Installed

**Trigger:** `flyai --version` returns `command not found`.

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Still fails → sudo npm i -g @fly-ai/flyai-cli
# Still fails → STOP. Tell user to install manually. Do NOT use training data.
```

---

## Case 1: Too Few Hotels Near POI (<3)

**Trigger:** `search-hotels --poi-name` returns < 3 results. Common for natural scenic areas.

```bash
# Step 1 → City-wide search (drop poi-name)
flyai search-hotels --dest-name "{city}" \
  --check-in-date "{in}" --check-out-date "{out}" --sort distance_asc

# Step 2 → Broad search
flyai fliggy-fast-search --query "{city} {poi} hotels"

# Step 3 → Still insufficient
→ Show available results + "Limited lodging near this area."
→ Show city-center options with estimated drive time
```

---

## Case 2: All Over Budget

```bash
# Step 1 → Relax 30%
flyai search-hotels ... --max-price {budget * 1.3} --sort distance_asc

# Step 2 → Try homestays (usually cheaper)
flyai search-hotels ... --hotel-types "民宿" --sort price_asc

# Step 3 → Expand to city-wide
flyai search-hotels --dest-name "{city}" --max-price {budget} --sort price_asc

# Step 4 → Still over → report honestly with suggestions
```

---

## Case 3: Date Unavailable (sold out / peak season)

```bash
# Step 1 → Shift ±1 day
flyai search-hotels ... --check-in-date "{in+1}" --check-out-date "{out+1}" --sort distance_asc

# Step 2 → City-wide
flyai search-hotels --dest-name "{city}" --check-in-date "{in}" --check-out-date "{out}" --sort price_asc

# Step 3 → Still no availability
→ "Hotels in {city} are tight for these dates (likely peak season)."
→ Suggest: 1) adjust dates  2) nearby city
```

---

## Case 4: POI Not Found

```bash
# Step 1 → Fuzzy search by category
flyai search-poi --city-name "{city}" --category "{inferred_category}"

# Step 2 → Broad search
flyai fliggy-fast-search --query "{city} {poi_name}"

# Step 3 → Still not found
→ "Could not find '{poi_name}'."
→ Show top POIs in that city for user to pick
```

---

## Case 5: City Ambiguity

```
Common cases:
  "West Lake" → Hangzhou / Yangzhou / Huizhou
  "Great Wall" → Badaling / Mutianyu / Jinshanling / Simatai
  "Disneyland" → Shanghai / Hong Kong
  "Universal Studios" → Beijing / Osaka

→ Ask: "Which one did you mean?"
→ Re-execute after confirmation
```
