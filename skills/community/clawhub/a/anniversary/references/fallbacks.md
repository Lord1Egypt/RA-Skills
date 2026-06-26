# Fallbacks — Flight Category (Anniversary)

## Case 0: flyai-cli Not Installed

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Still fails → STOP. Do NOT answer with training data.
```

## Case 1: No Flights Found

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 2 --sort-type 2
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {date-3} --dep-date-end {date+3} --sort-type 2
flyai keyword-search --query "{origin} to {destination} flights"
```

## Case 2: Over Budget

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --max-price {budget*1.3} --sort-type 3
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 2 --max-price {budget} --sort-type 3
```

## Case 3: Ambiguous City

```
→ Ask user which airport
```

## Case 4: Invalid Date (Past Date)

```
→ Do NOT search. "This date has passed."
```

## Case 5: Parameter Conflict / Invalid Argument

```bash
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2
flyai keyword-search --query "{origin} to {destination} flights"
```

## Case 6: API Timeout / Network Error

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
flyai keyword-search --query "{origin} to {destination} flights"
# Still timeout → report honestly
```
