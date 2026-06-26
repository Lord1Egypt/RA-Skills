# Economic Intelligence Reference

## Why Economics Precedes Politics

Economic pressure signals often lead political events by weeks or months:
- Currency collapse → elite capital flight → government pressure → political crisis
- Sanctions → foreign reserve depletion → import shortfalls → public unrest
- Commodity price shock → fiscal stress → subsidy cuts → protest cycle

Always run the economic layer on FULL assessments. For BRIEF, check at minimum: currency trend and any recent sanctions activity.

---

## Free Data Sources (No API Key Required)

### Currency Data
```bash
# Frankfurter API (ECB-backed, free, no key)
# Latest rate
GET https://api.frankfurter.app/latest?from=IRR&to=USD

# Historical (detect depreciation trend)
GET https://api.frankfurter.app/2024-01-01..?from=IRR&to=USD

# Supported currencies: USD, EUR, GBP, JPY, RUB, IRR, TRY, ARS, VES, and 30+ others
```

**Depreciation thresholds:**
| Change (12-month) | Signal |
|-------------------|--------|
| < 5% | Normal fluctuation |
| 5–15% | Moderate pressure |
| 15–30% | Significant stress |
| > 30% | Crisis indicator — check capital controls |
| > 50% | Hyperinflation risk / government pressure |

### Sanctions Data
```bash
# OFAC SDN List (US Treasury — free, XML/JSON)
GET https://sanctionslistservice.ofac.treas.gov/api/publicationsRecords

# OFAC recent actions (RSS)
GET https://home.treasury.gov/policy-issues/office-of-foreign-assets-control-sanctions-programs-and-information

# EU Sanctions Map (JSON export available)
# https://www.sanctionsmap.eu/

# UN Security Council Sanctions Committees
# https://www.un.org/securitycouncil/sanctions/information
```

**Sanctions escalation ladder:**
1. Targeted (individuals, entities) → signal of intent
2. Sectoral (banking, energy, defense) → economic pressure
3. Secondary (third-party restrictions) → isolation escalation
4. Primary + secondary comprehensive → near-total isolation

### Commodity Prices (Conflict-Relevant)
```bash
# World Bank Commodity Data (free)
GET https://api.worldbank.org/v2/en/indicator/PNRG_MBD?format=json

# FRED (US Federal Reserve — free, no key for many series)
GET https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILWTICO  # WTI crude oil
GET https://fred.stlouisfed.org/graph/fredgraph.csv?id=PWHEAMTUSDM  # Wheat price
```

---

## Economic Pressure Indicators by Conflict Type

### State Fragility / Pre-Collapse
| Indicator | Warning Level | Crisis Level |
|-----------|--------------|-------------|
| Foreign reserves | < 3 months imports | < 6 weeks imports |
| Debt service / revenue | > 20% | > 35% |
| Currency depreciation (12m) | > 20% | > 40% |
| Inflation | > 25% | > 100% |
| Import cover (food/fuel) | < 60 days | < 30 days |

### Sanctions Effectiveness
| Indicator | Effective Sanction | Adapted Sanction |
|-----------|-------------------|-----------------|
| Reserve depletion | Rapid | Stabilized via workarounds |
| Trade volume | Declining sharply | New partners found |
| Currency | Rapid depreciation | Stabilized |
| Inflation | Rising | Managed with controls |
| Elite behavior | Capital flight | Capital controls imposed |

### Protest-Enabling Economic Conditions
High correlation between protest onset and:
- Sudden subsidy removal (food, fuel)
- Unemployment spike > 5% within 6 months
- Remittance decline > 20% (diaspora income loss)
- Currency devaluation affecting imported goods prices

---

## Country-Specific Economic Vulnerabilities

### High Oil/Gas Dependency (fiscal breakeven > $70/bbl)
Russia, Iran, Saudi Arabia, Libya, Iraq, Venezuela, Nigeria, Angola
- Below breakeven → fiscal stress → reduced patronage → internal pressure
- Current oil price vs. breakeven is a leading indicator of government stability

### High Food Import Dependency
Egypt (50%+ wheat imports), Lebanon, Yemen, Somalia, North Africa generally
- Global wheat/grain price spikes directly → subsidy cost increase → government fiscal pressure
- Egypt: $1 increase in wheat price = ~$150M additional annual subsidy cost

### Remittance-Dependent Economies
Lebanon, Jordan, El Salvador, Philippines, Mexico
- Remittances > 10% of GDP = diaspora conditions matter for domestic stability
- Diaspora mobilization (protest, funding, information) amplifies local movements

### High External Debt (dollarized)
Argentina, Lebanon, Pakistan, Sri Lanka, Ghana, Zambia
- Dollar appreciation → debt servicing costs increase → fiscal crisis accelerates

---

## Elite Capital Flight Indicators

When elite capital flight begins, government pressure is real even if publicly denied:

**Detectable signals:**
- Luxury real estate purchases in Dubai, London, Turkey by nationals of stressed country
- Offshore banking flows (BIS data — published quarterly with lag)
- Cryptocurrency adoption spikes (informal capital controls workaround)
- Airline routes from capital city to financial hubs increasing
- Sudden increase in residency/citizenship-by-investment applications from country

---

## Economic Coercion & Evasion Patterns

Economic coercion is practiced by multiple actors. The following documents known patterns across all parties — both the imposition of economic pressure and the adaptation responses.

### Unilateral Sanctions & Economic Measures (Imposed Outside UN Framework)

The US, EU, UK, and their allies impose significant unilateral economic measures not authorized by the UN Security Council. Target states and many international law scholars contest the legality of these measures under international law. This is analytically relevant context.

| Imposing Actor | Instrument | Notable Targets | Contested Legality |
|---------------|-----------|----------------|-------------------|
| United States | OFAC SDN / sectoral sanctions | Iran, Russia, Cuba, Venezuela, North Korea, Syria | Widely contested outside Western bloc |
| European Union | EU Sanctions Map designations | Russia, Belarus, Iran, Syria | Less contested; UN-aligned in many cases |
| United States | Secondary sanctions (penalize third parties) | Any entity trading with primary targets | Strongly contested — claimed extraterritorial overreach |
| United States | SWIFT exclusion (via pressure on SWIFT) | Iran (2012), Russia (2022) | Contested as weaponization of financial infrastructure |

### Adaptation & Evasion Networks (Response to Economic Pressure)

| Party Under Pressure | Primary Adaptation Mechanism | Key Routes |
|---------------------|----------------------------|-----------|
| Iran | Trade through intermediary companies; barter arrangements | UAE free zones, Turkey, Iraq, China |
| Russia (post-2022) | Re-export through third countries; alternative payment systems (MIR, CIPS) | Central Asia, Turkey, China, UAE |
| North Korea | Maritime transfers, cyber operations for revenue | China border, offshore networks |
| Venezuela | Commodity swaps; Chinese/Russian barter trade | Caribbean, China, Russia |
| Myanmar | Regional trade networks | China, Thailand, ASEAN |
| Cuba | Long-term adaptation to US embargo (60+ years) | Russia, China, Venezuela, EU (partial) |

### Note on Western Economic Statecraft
The US dollar's reserve currency status, US control of SWIFT-adjacent infrastructure, and the extraterritorial reach of US secondary sanctions give the United States asymmetric economic coercion capability compared to other states. This structural advantage is analytically relevant when assessing economic pressure dynamics — a US-led sanctions campaign has different enforcement reach than a Russian or Chinese economic measure.

---

## Economic ↔ Political Correlation Matrix

| Economic Event | Political Response (typical lag) |
|---------------|----------------------------------|
| Currency crisis onset | Elite defection signals: 2–8 weeks |
| Subsidy removal | Street protests: 1–4 weeks |
| Sanctions comprehensive | Import shortfalls: 3–6 months |
| Reserve depletion (< 6 weeks cover) | IMF approach / default declaration: 2–8 weeks |
| Hyperinflation onset (> 50%/month) | Political crisis: 1–3 months |
| Debt default | Government resignation / restructuring: 1–6 months |
