# USDA Plant Hardiness Zones

## Zone Overview

The USDA Hardiness Zone Map divides the US into 13 zones based on average annual minimum winter temperatures. Each zone is a 10°F range, subdivided into "a" and "b" halves (5°F each).

| Zone | Avg Min Winter Temp (°F) | Avg Min Winter Temp (°C) |
|------|--------------------------|--------------------------|
| 1    | Below -50                | Below -45.6              |
| 2    | -50 to -40               | -45.6 to -40             |
| 3    | -40 to -30               | -40 to -34.4             |
| 4    | -30 to -20               | -34.4 to -28.9           |
| 5    | -20 to -10               | -28.9 to -23.3           |
| 6    | -10 to 0                 | -23.3 to -17.8           |
| 7    | 0 to 10                  | -17.8 to -12.2           |
| 8    | 10 to 20                 | -12.2 to -6.7            |
| 9    | 20 to 30                 | -6.7 to -1.1             |
| 10   | 30 to 40                 | -1.1 to 4.4              |
| 11   | 40 to 50                 | 4.4 to 10                |
| 12   | 50 to 60                 | 10 to 15.6               |
| 13   | 60 to 70                 | 15.6 to 21.1             |

---

## US Regions by Zone (General)

### Zone 3–4 (Northern US / Canada border)
- Minnesota, Wisconsin, North Dakota, Montana, northern Maine, parts of Alaska
- Very short growing season (90–120 frost-free days)
- Last frost: May 1–May 15 | First frost: Sep 15–Oct 1

### Zone 5 (Upper Midwest / Northeast)
- Illinois, Indiana, Ohio, Pennsylvania, upstate New York, parts of New England
- Growing season ~150 frost-free days
- Last frost: Apr 1–Apr 15 | First frost: Oct 1–Oct 15

### Zone 6 (Mid-Atlantic / Central US)
- Virginia, Maryland, New Jersey, Missouri, Kansas, Colorado foothills
- Growing season ~165 frost-free days
- Last frost: Mar 15–Apr 1 | First frost: Oct 15–Nov 1

### Zone 7 (Upper South / Pacific Northwest)
- Tennessee, North Carolina, northern Georgia, Arkansas, Oklahoma, Oregon coast, Washington state
- Growing season ~180+ frost-free days
- Last frost: Mar 1–Mar 15 | First frost: Nov 1–Nov 15

### Zone 8 (South / West Coast)
- Georgia, Alabama, Mississippi, Louisiana (north), Texas (central), Pacific Coast
- Growing season ~200+ frost-free days
- Last frost: Feb 15–Mar 1 | First frost: Nov 15–Dec 1

### Zone 9 (Deep South / California central valley)
- Florida (north), Louisiana, Texas (coast/south), California (central valley), Arizona (low desert)
- Growing season ~250+ frost-free days
- Last frost: Jan 30–Feb 15 | First frost: Dec 1–Dec 15

### Zone 10–11 (Tropical / Subtropical)
- South Florida, Hawaii, southern California coast, southern tip of Texas
- Year-round growing possible; frost rare to nonexistent

---

## Approximate Last Frost Dates by Zone

Used by planting_guide.py for scheduling calculations.

```json
{
  "3":  {"last_frost": "05-15", "first_frost": "09-15"},
  "4":  {"last_frost": "05-01", "first_frost": "10-01"},
  "5":  {"last_frost": "04-15", "first_frost": "10-15"},
  "6":  {"last_frost": "04-01", "first_frost": "11-01"},
  "7":  {"last_frost": "03-15", "first_frost": "11-15"},
  "8":  {"last_frost": "03-01", "first_frost": "12-01"},
  "9":  {"last_frost": "02-15", "first_frost": "12-15"},
  "10": {"last_frost": "01-30", "first_frost": null},
  "11": {"last_frost": null,    "first_frost": null}
}
```

---

## How to Find Your Zone

1. Visit: https://planthardiness.ars.usda.gov/
2. Enter your ZIP code
3. Or use the general guide above based on your state/region

Zones are a starting point — microclimates, elevation, proximity to water, and urban heat islands all affect actual growing conditions. Always observe your local conditions.

---

## Zone Tips

- **Zones 3–5:** Focus on cold-hardy crops; use season extenders (row covers, cold frames, hoop houses)
- **Zones 6–7:** Most common range; wide variety of crops feasible spring through fall
- **Zones 8–9:** Two growing seasons possible (spring and fall); summer heat limits some cool-season crops
- **Zones 10–11:** Reversed calendar for some crops; cool-season crops in "winter" months
