# Fallbacks — Flight Category

## Case 0: flyai-cli Not Installed

**Trigger:** `flyai --version` returns `command not found`.

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Fails → sudo npm i -g @fly-ai/flyai-cli
# Still fails → STOP. Do NOT answer with training data.
```

## Case 1: No Flights Found

```bash
# Step 1 → Expand dates ±3 days
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start "{date-3}" --dep-date-end "{date+3}" --sort-type 3
# Step 2 → Include connecting flights
flyai search-flight --origin "{o}" --destination "{d}" --dep-date "{date}" --sort-type 3
# Step 3 → Broad search
flyai keyword-search --query "{origin} to {destination} flights"
# Step 4 → Suggest nearby cities or rail
```

## Case 2: All Over Budget

```bash
# Relax budget 30%
flyai search-flight ... --max-price {budget*1.3} --sort-type 3
# Try red-eye
flyai search-flight ... --dep-hour-start 21 --sort-type 3
# Flexible dates
flyai search-flight ... --dep-date-start "{date-3}" --dep-date-end "{date+3}" --sort-type 3
```

## Case 3: Ambiguous City

```
"Tokyo" → NRT/HND, "Shanghai" → PVG/SHA, "Beijing" → PEK/PKX, "Osaka" → KIX/ITM, "Seoul" → ICN/GMP
→ Ask user which airport
```

## Case 4: Invalid Date

```
→ Do NOT search. "This date has passed."
→ Auto-search tomorrow
```

## Case 5: Parameter Conflict / Invalid Argument

```bash
# Retry with minimum required params only
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 3
# Fallback to broad search
flyai keyword-search --query "{origin} to {destination} flights"
```

## Case 6: API Timeout / Network Error

```bash
# Retry once → Simplify query → Report honestly. Do NOT substitute with training data.
```
