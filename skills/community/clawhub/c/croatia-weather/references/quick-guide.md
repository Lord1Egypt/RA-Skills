# DHMZ Quick Guide — Which Command to Run

> **Source of truth for all DHMZ XML feed URLs and data structure:**
> https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici
>
> If any feed stops working, returns errors, or the XML structure changes, visit the page above
> to check for updated URLs or schema changes. Then update `{baseDir}/scripts/dhmz.py` accordingly.

---

## Decision Table

| User asks about... | Command(s) | Why |
|---|---|---|
| "What's the weather?" / "weather at home" | `current` then `forecast` | Current conditions + what's coming |
| "Weather in [Croatian city]" | `current [city]` then `forecast [city]` | Fuzzy matches city name |
| "Weather in [European city]" | `europe [city]` | Non-Croatian European city |
| "Is it going to rain?" | `forecast` + `precip` | Check forecast + current rain |
| "This week's weather" | `forecast` | 7-day overview |
| "Detailed forecast for tomorrow" | `forecast3` | 3-hourly breakdown |
| "What's the outlook / next few days" | `outlook` | 3-day text summary |
| "Any weather warnings?" | `warnings` | CAP alerts for 3 days |
| "Is there a storm / bura?" | `warnings` + `adriatic` | Warnings + maritime wind |
| "Heat wave?" | `heatwave` + `bio` | 5-day heat indicator + biometeo |
| "Cold wave / frost risk?" | `coldwave` + `frost` | Cold wave + ground frost |
| "Should I water my garden?" | `frost` + `soil` + `precip` + `agro` | Ground frost, soil state, rain, agro advice |
| "When to plant / sowing?" | `soil` + `frost` + `agro` + `agro7` | Soil temps, frost, agro bulletin |
| "Is it safe to sail?" | `adriatic` + `maritime` + `warnings` + `sea` | Nautical forecast + wind warnings + sea state |
| "Sea temperature?" | `sea` | Adriatic coastal stations |
| "Can I swim?" | `sea` + `current [coastal city]` | Sea temp + air temp |
| "UV / sunburn risk?" | `uvi` | Hourly UV index |
| "Snow?" | `snow` + `current` | Snow depth + conditions |
| "River levels / flooding?" | `hydro` + `rivers` | River levels + flood alerts + temps |
| "River temperature for fishing?" | `rivers` | 19 river stations |
| "Fire danger?" | `fire` | FWI index for 35+ stations |
| "Health / biometeo / allergies?" | `bio` | 3-day biometeo forecast |
| "Is this normal for this time of year?" | `climate [city]` | 125-year monthly averages |
| "How much rain this year?" | `climate-rain [year]` | Monthly precipitation totals |
| "Compare to historical average" | `climate [city]` + `current [city]` | Climate norm vs actual |
| "Full weather report" | `full` | Combined overview |
| "What stations are available?" | `stations` | Lists all station names |
| "Weather in Belgrade / Vienna / etc." | `europe [city]` | European capitals |

---

## Common Combinations

### Quick check (home station)
```bash
python3 {baseDir}/scripts/dhmz.py current
python3 {baseDir}/scripts/dhmz.py forecast
```

### Comprehensive briefing
```bash
python3 {baseDir}/scripts/dhmz.py full
```

### Farmer / gardener
```bash
python3 {baseDir}/scripts/dhmz.py frost
python3 {baseDir}/scripts/dhmz.py soil
python3 {baseDir}/scripts/dhmz.py agro
python3 {baseDir}/scripts/dhmz.py agro7
```

### Sailor / coastal trip
```bash
python3 {baseDir}/scripts/dhmz.py warnings
python3 {baseDir}/scripts/dhmz.py adriatic
python3 {baseDir}/scripts/dhmz.py maritime
python3 {baseDir}/scripts/dhmz.py sea
```

### Safety check (storms, floods, extreme temps)
```bash
python3 {baseDir}/scripts/dhmz.py warnings
python3 {baseDir}/scripts/dhmz.py heatwave
python3 {baseDir}/scripts/dhmz.py coldwave
python3 {baseDir}/scripts/dhmz.py hydro
```

### Climate research / comparison
```bash
python3 {baseDir}/scripts/dhmz.py climate zagreb_maksimir
python3 {baseDir}/scripts/dhmz.py climate-rain 2025
```

---

## Feed Update Schedule

| Feed type | Update frequency |
|---|---|
| Current conditions | Every 1–3 hours |
| Forecasts (7d, 3d) | Twice daily (~00:00 and ~12:00 UTC) |
| Warnings (CAP) | As needed (event-driven) |
| Heat/cold wave | Daily |
| Biometeo | Daily |
| Precipitation, snow, temps | Daily (at 08:00 UTC observation) |
| UV index | Continuous (hourly readings) |
| Sea temperature | Hourly |
| River temperature | Hourly |
| Soil temperature | Daily |
| Agro bulletin | Weekly |
| Agro 7-day data | Weekly |
| Hydrological forecast | Daily |
| Fire danger | Daily |
| Climate averages | Static (annual updates) |
| Annual precipitation | Monthly updates |

---

## Troubleshooting

If a feed returns an error or unexpected data:

1. **Check the source page:** https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici
2. Verify the URL is still correct
3. Try fetching the raw XML: `curl -s "[URL]" | head -20`
4. If the XML structure changed, update the parsing in `{baseDir}/scripts/dhmz.py`
5. Seasonal feeds may return empty data (e.g., snow depth in summer, UV at night)

### Known quirks
- **Snow depth** returns empty in summer — this is normal, not an error
- **Heat wave** returns all 🟢 in winter — normal
- **Cold wave** returns all ⚪ in summer — normal
- **Sea temperature** stations report at varying times; some columns may be `-`
- **River temperature** latest reading may be `None` if sensor hasn't reported yet — script takes last valid value
- **Climate precipitation** uses `,` as decimal separator in source (`203,6`); script converts to `.`
- **Climate averages** contain HTML entities in row labels (e.g., `&#8804;`); these are display-only
- **Forecast station names** use underscores (`Slavonski_Brod`), current conditions use spaces
