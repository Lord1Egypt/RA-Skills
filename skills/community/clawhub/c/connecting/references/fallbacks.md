# Fallbacks — Flight Category (Connecting)

## Case 0: flyai-cli Not Installed

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Still fails → STOP. Do NOT answer with training data.
```

## Case 1: No Connecting Flights Found

```bash
# Step 1 → Remove journey-type filter (include direct)
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
# Step 2 → Try flexible dates ±3 days
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start "{date-3}" --dep-date-end "{date+3}" --journey-type 2 --sort-type 3
# Step 3 → Try different transfer city
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
# Step 4 → Keyword search
flyai keyword-search --query "{origin} to {destination} connecting flights"
```

## Case 2: All Connecting Flights Over Budget

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 2 --max-price {budget*1.3} --sort-type 3
# Try including direct flights for comparison
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --max-price {budget} --sort-type 3
```

## Case 3: Ambiguous City

```
→ Ask user which airport
```

## Case 4: Invalid Date

```
→ Do NOT search. "This date has passed."
```

## Case 5: Parameter Conflict

```bash
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 3
flyai keyword-search --query "{origin} to {destination} flights"
```

## Case 6: API Timeout

```bash
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 3
flyai keyword-search --query "{origin} to {destination} flights"
# Still timeout → report honestly.
```
