# Fallbacks — Flight Category (shared by 15 flight skills)

## Case 0: flyai-cli Not Installed

**Trigger:** `flyai --version` returns `command not found`.

```bash
# Step 1 → Auto-install
npm i -g @fly-ai/flyai-cli

# Step 2 → Verify
flyai --version

# Step 3 → Permission issue
sudo npm i -g @fly-ai/flyai-cli

# Step 4 → Still fails
→ STOP. Do NOT answer with training data.
→ Tell user: "Please run `npm i -g @fly-ai/flyai-cli` manually. Requires Node.js ≥18."
```

---

## Case 1: No Results (empty response)

**Trigger:** `search-flight` returns 0 results.

```bash
# Step 1 → Expand dates ±3 days
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date-start "{date-3}" --dep-date-end "{date+3}" --sort-type 3

# Step 2 → Include connecting (remove journey-type)
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date "{date}" --sort-type 3

# Step 3 → Fallback to broad search
flyai fliggy-fast-search --query "{origin} to {destination} flights"

# Step 4 → Still nothing
→ "No flights available on this route for the selected dates."
→ Suggest: 1) nearby departure city  2) alternative dates  3) train/rail
```

---

## Case 2: Too Many Results (>15)

**Trigger:** Overwhelming results, user has no filters.

```
→ Show Top 5 by current sort
→ Ask ONE filter question: "Do you prioritize price, duration, or direct flights?"
→ Re-search with added parameter
```

---

## Case 3: All Results Over Budget

**Trigger:** User has a budget, all results exceed it.

```bash
# Step 1 → Relax budget 30%
flyai search-flight ... --max-price {budget * 1.3} --sort-type 3

# Step 2 → Try red-eye
flyai search-flight ... --dep-hour-start 21 --sort-type 3

# Step 3 → Flexible dates
flyai search-flight ... --dep-date-start "{date-3}" --dep-date-end "{date+3}" --sort-type 3

# Step 4 → Still over
→ "Lowest available: ¥{min}, ¥{diff} over your budget."
→ Suggest: 1) adjust dates  2) connecting flights  3) train alternative
```

---

## Case 4: Ambiguous City Name

**Trigger:** City maps to multiple airports.

```
Common ambiguities:
  "Tokyo" → NRT (Narita) / HND (Haneda)
  "Shanghai" → PVG (Pudong) / SHA (Hongqiao)
  "Beijing" → PEK (Capital) / PKX (Daxing)
  "Osaka" → KIX (Kansai) / ITM (Itami)
  "Seoul" → ICN (Incheon) / GMP (Gimpo)

→ Try search with city name first
→ If ambiguous results → ask user which airport
```

---

## Case 5: Invalid Date

**Trigger:** Date is in the past or < 2 hours from now.

```
→ Do NOT execute search
→ "This date has already passed."
→ Auto-search tomorrow:
  flyai search-flight --origin "{o}" --destination "{d}" \
    --dep-date "{tomorrow}" --sort-type 3
```
