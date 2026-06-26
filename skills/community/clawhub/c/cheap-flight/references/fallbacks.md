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

**Trigger:** `search-flight` returns 0 results.

```bash
# Step 1 → Expand dates ±3 days
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date-start "{date-3}" --dep-date-end "{date+3}" --sort-type 3

# Step 2 → Include connecting flights (remove --journey-type if set to 1)
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date "{date}" --sort-type 3

# Step 3 → Broad keyword search as fallback
flyai keyword-search --query "{origin} to {destination} flights"

# Step 4 → Still nothing → suggest nearby cities or rail
```

## Case 2: All Over Budget

```bash
# Step 1 → Relax budget 30%
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date "{date}" --max-price {budget*1.3} --sort-type 3

# Step 2 → Try red-eye
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date "{date}" --dep-hour-start 21 --sort-type 3

# Step 3 → Flexible dates
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date-start "{date-3}" --dep-date-end "{date+3}" --sort-type 3

# Step 4 → Consider train alternative
flyai search-train --origin "{o}" --destination "{d}" \
  --dep-date "{date}" --sort-type 3
```

## Case 3: Ambiguous City Name

```
Common multi-airport cities:
  "Tokyo" → NRT (Narita) / HND (Haneda)
  "Shanghai" → PVG (Pudong) / SHA (Hongqiao)
  "Beijing" → PEK (Capital) / PKX (Daxing)
  "Osaka" → KIX (Kansai) / ITM (Itami)
  "Seoul" → ICN (Incheon) / GMP (Gimpo)

→ Try search with city name first (CLI handles mapping)
→ If ambiguous results → ask user which airport
```

## Case 4: Invalid Date

```
→ Do NOT execute search. "This date has already passed."
→ Auto-search tomorrow:
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date "{tomorrow}" --sort-type 3
```

## Case 5: Parameter Conflict / Invalid Argument

**Trigger:** CLI returns error containing "invalid", "conflict", or non-zero exit code.

```bash
# Step 1 → Retry with minimum required params only
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 3

# Step 2 → Fallback to keyword search
flyai keyword-search --query "{origin} to {destination} cheap flights"

# Step 3 → Report error honestly with raw command for debugging
```

## Case 6: API Timeout / Network Error

**Trigger:** CLI hangs >30s or returns network error.

```bash
# Step 1 → Retry once
flyai search-flight --origin "{o}" --destination "{d}" \
  --dep-date "{date}" --sort-type 3

# Step 2 → Simplify query
flyai keyword-search --query "{origin} to {destination} flights"

# Step 3 → Report timeout honestly. Do NOT substitute with training data.
```
