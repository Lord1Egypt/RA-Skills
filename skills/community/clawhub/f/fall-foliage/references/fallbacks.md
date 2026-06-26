# Fallbacks — Seasonal/Special Category

## Case 0: flyai-cli Not Installed

```bash
npm i -g @fly-ai/flyai-cli && flyai --version
# Still fails → STOP. Do NOT answer with training data.
```

## Case 1: Seasonal Data Not Available

```bash
flyai search-poi --city-name "{city}" --poi-level 5
flyai fliggy-fast-search --query "{city} travel"
```

## Case 2: Event/Festival Not Found

```bash
flyai fliggy-fast-search --query "{city} {month} events"
```

## Case 3: Partial Failure

```
→ Show available data, mark missing sections
```

## Case 4: API Timeout

```
Retry once → Simplify → Report honestly.
```
