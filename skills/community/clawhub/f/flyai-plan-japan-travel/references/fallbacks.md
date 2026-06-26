# Fallbacks — Destination Category (shared by 15 destination skills)

## Case 0: flyai-cli Not Installed

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Fails → sudo npm i -g @fly-ai/flyai-cli
# Still fails → STOP. Do NOT output an itinerary from training data.
```

---

## Case 1: No Flights Found

**Trigger:** `search-flight` to this destination returns empty.

```bash
# Step 1 → Flexible dates ±7 days (international routes fluctuate more)
flyai search-flight --origin "{origin}" --destination "{dest}" \
  --dep-date-start "{date-7}" --dep-date-end "{date+7}" --sort-type 3

# Step 2 → Try alternative entry city in same country
flyai search-flight --origin "{origin}" --destination "{alt_city}" \
  --dep-date "{date}" --sort-type 3

# Step 3 → Broad search
flyai fliggy-fast-search --query "{origin} to {country} flights"

# Step 4 → Still nothing
→ "No direct flights found for this route."
→ Suggest transit hubs (e.g., via Hong Kong / Seoul / Singapore)
```

---

## Case 2: Hotels Insufficient

```bash
# Step 1 → Remove filters (stars, price)
flyai search-hotels --dest-name "{city}" --sort rate_desc

# Step 2 → Nearby city
flyai search-hotels --dest-name "{nearby_city}" --sort rate_desc

# Step 3 → Broad search
flyai fliggy-fast-search --query "{city} hotel accommodation"

# Step 4 → Still limited
→ Show what's available + note "Limited coverage for this destination on Fliggy"
```

---

## Case 3: POI Search Empty

```bash
# Step 1 → Try Chinese/English name variants
flyai search-poi --city-name "{city_cn}" --keyword "{keyword}"
flyai search-poi --city-name "{city_en}" --keyword "{keyword}"

# Step 2 → Broad search
flyai fliggy-fast-search --query "{city} attractions sightseeing"

# Step 3 → Still empty
→ Use domain knowledge for framework-level suggestions (NOT specific names/prices)
→ Tag: "⚠️ Reference info only — install flyai-cli for real-time data and booking links"
```

---

## Case 4: Visa Search Returns Nothing Useful

```
→ Use domain knowledge for general visa info
→ Tag: "⚠️ General info. Check consulate website for latest policy."
→ Do NOT fabricate specific requirements or fees
```

---

## Case 5: Partial Failure in Multi-Command Orchestration

**Trigger:** Some commands succeed, others fail during full itinerary planning.

```
→ Do NOT abandon the entire itinerary
→ Show successful results normally
→ Mark failed sections: "⚠️ {section} data unavailable"
→ Provide manual CLI command for user to retry

Example:
  ✅ Visa: obtained
  ✅ Flights: lowest ¥2,500
  ⚠️ Kyoto hotels: could not retrieve — try `flyai search-hotels --dest-name "Kyoto" ...`
  ✅ Tokyo attractions: Top 5 obtained
```
