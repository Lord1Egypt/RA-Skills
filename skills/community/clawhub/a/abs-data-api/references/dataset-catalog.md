# ABS Data API — Dataset Catalog

Curated reference for the most commonly queried ABS datasets available via the Data API.
IDs verified against the ABS API (2025). All IDs use `agencyID=ABS`.

## How to Use

1. Find the dataflow `ID` below
2. Run: `abs_query.py <ID> <key> [--latest]`
3. Consult [sdmx-patterns.md](sdmx-patterns.md) to construct dimension keys

---

## Consumer Prices

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| CPI, inflation, consumer prices | `CPI` | 2.0.0 | Consumer Price Index | 6401.0 | Quarterly; all groups + sub-groups; all capital cities. Updated Nov 2025: new dimension structure; version confirmed 2.0.0 |
| monthly CPI, monthly inflation | `CPI_M` | 1.2.0 | Monthly CPI Indicator | 6484.0 | Monthly; released Nov 2025 as ongoing series (no longer experimental) |
| monthly CPI housing | `CPI_H` | 1.0.0 | Monthly CPI — Housing | 6484.0 | Monthly; housing-specific CPI component; added Nov 2025 |
| CPI quarterly | `CPI_Q` | 1.0.0 | Consumer Price Index Quarterly | 6401.0 | Quarterly (deprecated; prefer CPI) |
| CPI weights, expenditure weights | `CPI_WEIGHTS` | 1.0.0 | CPI Weights | 6401.0 | Expenditure class weights |

---

## Wages & Earnings

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| WPI, wage price index, wage growth | `WPI` | 1.2.0 | Wage Price Index | 6345.0 | Quarterly; private + public sector; all industries |

---

## Producer Prices

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| PPI, producer prices, input prices | `PPI` | 1.1.3 | Producer Price Indexes by Industry | 6427.0 | Quarterly |
| PPI final demand | `PPI_FD` | 1.1.0 | Producer Price Indexes, Final Demand | 6427.0 | Quarterly; stage-of-production approach |

---

## Property Prices

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| RPPI, residential property price index, house prices | `RPPI` | 1.0.0 | Residential Property Price Index | 6416.0 | Quarterly; eight capital cities |
| dwelling values state, RES_DWELL_ST | `RES_DWELL_ST` | 1.0.0 | Residential Dwellings: Values by State | 6416.0 | Quarterly; mean price and number of dwellings |
| dwelling medians GCCSA | `RES_DWELL` | 1.0.0 | Residential Dwellings: Medians by GCCSA | 6416.0 | Quarterly; unstratified medians and transfer counts |

---

## Labour Force

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| LF, labour force, unemployment, employment, participation rate | `LF` | 1.0.0 | Labour Force | 6202.0 | Monthly; headline estimates by state |
| LF by age | `LF_AGES` | 1.0.0 | Labour Force: Age Groups | 6202.0 | Monthly; detailed age groups |
| underemployment, underutilisation | `LF_UNDER` | 1.0.1 | Labour Force - Underemployment & Underutilisation | 6202.0 | Monthly |
| hours worked, full-time part-time | `LF_HOURS` | 1.0.0 | Labour Force: Hours Worked | 6202.0 | Monthly |
| LF education, educational attendance | `LF_EDU` | 1.0.0 | Labour Force Educational Attendance | 6202.0 | Monthly |

---

## Job Vacancies

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| JV, job vacancies, open positions | `JV` | 1.0 | Job Vacancies | 6354.0 | Quarterly; by sector and industry |

---

## National Accounts / GDP

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| GDP, national accounts aggregates, ANA_AGG | `ANA_AGG` | 1.0.0 | National Accounts Key Aggregates | 5206.0 | Quarterly; top-level GDP and aggregates |
| GDP expenditure, household consumption, ANA_EXP | `ANA_EXP` | 1.0.0 | National Accounts — GDP (Expenditure) | 5206.0 | Quarterly |
| GDP income, compensation of employees, ANA_INC | `ANA_INC` | 1.0.0 | National Accounts — GDP (Income) | 5206.0 | Quarterly |
| GDP production, GVA, gross value added, ANA_IND_GVA | `ANA_IND_GVA` | 1.0.0 | National Accounts — GDP (Production/GVA) | 5206.0 | Quarterly; by industry |
| state final demand, SFD | `ANA_SFD` | 1.0.0 | National Accounts — State Final Demand | 5206.0 | Quarterly; by state |

---

## Population Estimates (ERP)

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| ERP quarterly, quarterly population | `ERP_Q` | 1.0.0 | Quarterly Population Estimates (ERP) | 3101.0 | Quarterly; by state, sex, age |
| ERP SA2, population SA2 | `ERP_ASGS2021` | 1.0.0 | ERP by SA2 (ASGS 2021+) | 3218.0 | Annual; ASGS Edition 3, 2001 onwards |
| ERP LGA, population LGA 2024 | `ABS_ANNUAL_ERP_LGA2024` | 1.0.0 | ERP by LGA (2024 edition) | 3218.0 | Annual; LGA, age and sex; uses 2024 LGA boundaries |
| ERP SA2 ASGS2016 | `ERP_ASGS2016` | 1.0.0 | ERP by SA2 (ASGS 2016) | 3218.0 | Annual; ASGS 2016, 2001–2021 |
| ERP country of birth | `ERP_COB` | 1.0.0 | ERP by Country of Birth | 3412.0 | Annual; country of birth, age, sex |

---

## Births, Deaths, Natural Change

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| births, birth rate, registered births | `BIRTHS_SUMMARY` | 1.0.0 | Registered Births Summary | 3301.0 | Annual; by state/territory, 1975+ |
| births monthly by age of mother | `BIRTHS_MON_OCC_AGE_MOTHER` | 1.0.0 | Monthly Births by Age of Mother | 3301.0 | Monthly; experimental; released 2025 |
| births age of mother, fertility by age | `BIRTHS_AGE_MOTHER` | 1.0.0 | Births by Age of Mother | 3301.0 | Annual |
| births age of father | `BIRTHS_AGE_FATHER` | 1.0.0 | Births by Age of Father | 3301.0 | Annual |
| deaths, death rate, mortality | `DEATHS_AGESPECIFIC_OCCURENCEYEAR` | 1.0.0 | Deaths by Year of Occurrence | 3302.0 | Annual; age-specific death rates |
| deaths registration year | `DEATHS_AGESPECIFIC_REGISTRATIONYEAR` | 1.0.0 | Deaths by Year of Registration | 3302.0 | Annual |
| life expectancy | `LIFE_TABLE_STATE` | 1.0.0 | Life Tables by State/Territory | 3302.0 | Annual |

---

## Migration

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| NOM, net overseas migration, overseas arrivals | `NOM_CY` | 1.0.0 | Net Overseas Migration (Calendar Year) | 3412.0 | Annual; by state, age, sex |
| NOM financial year | `NOM_FY` | 1.0.0 | Net Overseas Migration (Financial Year) | 3412.0 | Annual |
| NIM, interstate migration | `NIM_CY` | 1.0.0 | Interstate Migration (Calendar Year) | 3101.0 | Annual; by state |
| NIM financial year | `NIM_FY` | 1.0.0 | Interstate Migration (Financial Year) | 3101.0 | Annual |

---

## International Trade in Goods & Services

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| ITGS, international trade goods, exports imports | `ITGS` | 1.2.0 | International Trade in Goods | 5368.0 | Monthly; total merchandise trade |
| merchandise exports | `MERCH_EXP` | 1.0.0 | Merchandise Exports by Commodity (SITC) | 5368.0 | Monthly; by commodity and country |
| merchandise imports | `MERCH_IMP` | 1.0.0 | Merchandise Imports by Commodity (SITC) | 5368.0 | Monthly; by commodity and country |
| trade services country calendar year | `TRADE_SERV_CNTRY_CY` | 1.0.0 | Trade in Services by Country (Calendar Year) | 5368.0 | Annual |
| trade services country financial year | `TRADE_SERV_CNTRY_FY` | 1.0.0 | Trade in Services by Country (Financial Year) | 5368.0 | Annual |
| trade services state | `TRADE_SERV_STATE_CY` | 1.0.0 | Trade in Services by State (Calendar Year) | 5368.0 | Annual |

---

## Retail Trade

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| RT, retail trade, retail sales, retail turnover | `RT` | 1.0.0 | Retail Trade | 8501.0 | **DISCONTINUED** — final release June 2025, no longer updated. Use `HSI_M` or `BUSINESS_TURNOVER` instead |
| monthly business turnover | `BUSINESS_TURNOVER` | 1.3.0 | Monthly Business Turnover Indicator | 8501.0 | Monthly; by industry division. Preferred replacement for discontinued RT |
| HSI monthly, household spending indicator | `HSI_M` | 1.0.0 | Household Spending Indicator (Monthly) | 8501.0 | Monthly; replacement series for retail trade from mid-2025; broader coverage |

---

## Housing Finance / Lending

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| LEND_HOUSING, housing finance, lending indicators, mortgages | `LEND_HOUSING` | 1.1 | Lending Indicators Housing Finance | 5601.0 | Monthly; new loan commitments |

---

## Building Activity

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| building activity, construction activity, dwelling approvals, commencements | `BUILDING_ACTIVITY` | 1.0.0 | Building Activity | 8752.0 | Quarterly; commencements, completions, work done |

---

## Survey Microdata / Table Collections

| Terms | ID | Version | Name | Cat No. | Notes |
|---|---|---|---|---|---|
| ABS survey unit table 2024 | `ABS_SU_TABLE_2024` | 1.0.0 | ABS Survey Unit Table 2024 | — | Cross-sectional survey data; 2024 edition |

---

## Notes

- Full dataflow list: `https://data.api.abs.gov.au/rest/dataflow/ABS` (1,200+ dataflows)
- Versions are accurate as of 2025-11; run `abs_cache.py refresh` for the latest
- Use `abs_cache.py search <term>` for fuzzy search across all 1,200+ dataflows
- Catalogue numbers link to ABS publications at `https://www.abs.gov.au/statistics`
- **Discontinued datasets** (as of mid-2025): `RT` (Retail Trade) — use `HSI_M` or `BUSINESS_TURNOVER`
