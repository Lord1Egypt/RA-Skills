# ABS SDMX Dimension Patterns

This reference covers common dimension codes and key construction patterns
for frequently used ABS datasets.

---

## Universal Dimension Patterns

These dimensions appear across most ABS datasets with consistent codes.

### FREQ — Frequency
| Code | Meaning |
|---|---|
| `M` | Monthly |
| `Q` | Quarterly |
| `A` | Annual |
| `S` | Semi-annual |

### TSEST — Type of Adjustment
| Code | Meaning |
|---|---|
| `10` | Original (unadjusted) |
| `12` | Seasonally adjusted |
| `20` | Seasonally adjusted (some datasets) |
| `30` | Trend |

### SEX_ABS — Sex
| Code | Meaning |
|---|---|
| `1` | Male |
| `2` | Female |
| `3` | Persons (total) |

### REGION — Geographic Region (State/Territory)
| Code | Meaning |
|---|---|
| `AUS` | Australia (national total) |
| `1` | New South Wales |
| `2` | Victoria |
| `3` | Queensland |
| `4` | South Australia |
| `5` | Western Australia |
| `6` | Tasmania |
| `7` | Northern Territory |
| `8` | Australian Capital Territory |
| `9` | Other Territories |

Sub-regional codes (used in ERP and census datasets):
- SA2: 9-digit codes (e.g. `101051539` = Adelaide City)
- SA3: 5-digit codes (e.g. `10102` = Adelaide City)
- SA4: 3-digit codes (e.g. `101` = Adelaide)
- LGA: 5-digit codes (ABS LGA codes)

---

## Dataset-Specific Dimension Keys

### CPI (Consumer Price Index) — v2.0.0

Dimension order: `MEASURE . INDEX . TSEST . REGION . FREQ`

**MEASURE**
| Code | Meaning |
|---|---|
| `1` | Index numbers |
| `2` | Percentage change from previous period |
| `3` | Percentage change from previous year |
| `6` | Contribution to % pts change from previous period |
| `7` | Contribution to Annual % pts change |

**INDEX (selected)**
| Code | Meaning |
|---|---|
| `10001` | All groups CPI |
| `999901` | All groups CPI, seasonally adjusted |
| `20001` | Food and non-alcoholic beverages |
| `20002` | Alcohol and tobacco |
| `20003` | Clothing and footwear |
| `20004` | Furnishings, household equip. and services |
| `20005` | Transport |
| `20006` | Health |
| `115522` | Rents |
| `131197` | All groups CPI excluding food and energy |
| `104122` | All groups CPI excluding 'volatile items' |

**REGION (capital cities)**
| Code | Meaning |
|---|---|
| `50` | Australia |
| `1` | Sydney |
| `2` | Melbourne |
| `3` | Brisbane |
| `4` | Adelaide |
| `5` | Perth |
| `6` | Hobart |
| `7` | Darwin |
| `8` | Canberra |

Example keys:
- `1.10001.10.50.Q` = Index numbers, All groups, Original, Australia, Quarterly
- `3.10001.10.50.Q` = % change year ago, All groups, Original, Australia, Quarterly
- `1.10001.10.1.Q` = Index numbers, All groups, Original, Sydney, Quarterly

---

### LF (Labour Force) — v1.0.0

Dimension order: `MEASURE . SEX_ABS . REGION . INDUSTRY . TSEST . FREQ`

**MEASURE**
| Code | Meaning |
|---|---|
| `1` | Employed, total |
| `2` | Employed, full-time |
| `3` | Unemployment rate |
| `4` | Unemployed, total |
| `5` | Labour force, total |
| `6` | Participation rate |
| `7` | Not in labour force |

**INDUSTRY**: `15` = All industries

Example keys:
- `3.3.AUS.15.20.M` = Unemployment rate, Persons, Australia, All industries, Seasonally adjusted, Monthly
- `6.3.AUS.15.20.M` = Participation rate, Persons, Australia, All industries, Seasonally adjusted, Monthly
- `1.3.1.15.20.M` = Employment, Persons, NSW, All industries, Seasonally adjusted, Monthly

---

### WPI (Wage Price Index) — v1.2.0

Dimension order: `MEASURE . SECTOR . INDUSTRY . TSEST . FREQ`

**MEASURE**
| Code | Meaning |
|---|---|
| `1` | Index Numbers |
| `2` | % change prev quarter |
| `3` | % change year ago |

**SECTOR**
| Code | Meaning |
|---|---|
| `1` | Private |
| `2` | Public |
| `3` | All |

**INDUSTRY**: `1599` = Total all industries (common across ABS)

Example: `1.3.1599.20.Q` = Index numbers, All sectors, Total, Seasonally adjusted, Quarterly

---

### ERP_Q (Quarterly Population Estimates) — v1.0.0

Dimension order: `MEASURE . REGION . SEX . AGE . FREQ`

**MEASURE**: `ERP` = Estimated Resident Population

**AGE**: `TOT` = All ages

Example: `ERP.3.3.TOT.Q` = ERP, Queensland, Persons, All ages, Quarterly

---

### RT (Retail Trade) — v1.0.0

Dimension order: `MEASURE . INDUSTRY . REGION . TSEST . FREQ`

**MEASURE**: `RETAIL_TURN` = Retail Turnover

**INDUSTRY**
| Code | Meaning |
|---|---|
| `TOT` | Total (all industries) |
| `A` | Food |
| `B` | Household goods |
| `C` | Clothing, footwear, personal |
| `D` | Department stores |
| `E` | Other retailing |
| `F` | Cafes, restaurants, takeaway |

Example: `RETAIL_TURN.TOT.AUS.20.M` = Total turnover, All industries, Australia, Seasonally adjusted, Monthly

---

### ANA_AGG (National Accounts Aggregates) — v1.0.0

Dimension order: `MEASURE . SECTOR . PRICES . TSEST . FREQ`

**PRICES**
| Code | Meaning |
|---|---|
| `10` | Current prices |
| `20` | Chain volume measures |

**TSEST**: `20` = Seasonally adjusted; `30` = Trend

Example: `GDP.TOT.20.20.Q` = GDP, Chain volume, Seasonally adjusted, Quarterly
(Check DSD for exact MEASURE and SECTOR codes; use `all` key first to discover)

---

## Building Keys: Step-by-Step

1. **Discover dimension order** — fetch DSD:
   ```
   GET /datastructure/ABS/{ID}/{VERSION}?references=codelist
   ```
   Read `data.dataStructures[0].dataStructureComponents.dimensionList.dimensions`

2. **Find valid codes** — each dimension links to a codelist with valid IDs

3. **Construct key** — join one code per dimension with `.`
   - Use empty string for "wildcard" on a dimension: `1..20.Q` = all INDEX values

4. **Test with `all`** first — always works, then narrow down

---

## Time Period Formats

| Frequency | Format | Example |
|---|---|---|
| Monthly | `YYYY-MM` | `2024-03` |
| Quarterly | `YYYY-QN` | `2024-Q1` |
| Annual | `YYYY` | `2024` |
| Semi-annual | `YYYY-SN` | `2024-S1` |

Range parameters: `?startPeriod=2020-Q1&endPeriod=2024-Q4`

---

## Geographic Lookups

For SA2/SA3/SA4/LGA codes, refer to:
- ABS ASGS correspondence files: `https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3`
- ABS MapStats for browsing geographic boundaries
- The ERP_ASGS2021 DSD codelists contain all valid SA2 codes
