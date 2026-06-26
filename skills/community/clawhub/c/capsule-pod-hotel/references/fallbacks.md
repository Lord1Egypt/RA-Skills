# Fallbacks — Hotel Category

## Case 0: flyai-cli Not Installed

```bash
npm i -g @fly-ai/flyai-cli && flyai --version
# Still fails → STOP. Do NOT answer with training data.
```

## Case 1: Too Few Hotels (<3)

```bash
# Drop poi-name/keywords, search city-wide
flyai search-hotel --dest-name "{city}" --sort rate_desc
# Broad search
flyai keyword-search --query "{city} hotels"
```

## Case 2: All Over Budget

```bash
# Relax 30%
flyai search-hotel ... --max-price {budget*1.3}
# Try homestays
flyai search-hotel ... --hotel-types "民宿" --sort price_asc
```

## Case 3: Date Unavailable (peak season)

```bash
# Shift ±1 day
flyai search-hotel ... --check-in-date "{in+1}" --check-out-date "{out+1}"
# City-wide
flyai search-hotel --dest-name "{city}" --sort price_asc
```

## Case 4: POI Not Found

```bash
# Fuzzy search
flyai search-poi --city-name "{city}" --category "{inferred}"
# Broad
flyai keyword-search --query "{city} {poi_name}"
```

## Case 5: Parameter Conflict

```bash
flyai search-hotel --dest-name "{city}" --sort rate_desc
flyai keyword-search --query "{city} hotels"
```

## Case 6: API Timeout

```
Retry once → Simplify → Report honestly.
```
