# Climate & Resource Stress Reference

## Why Resource Stress Drives Conflict

Climate and resource pressures are increasingly **primary drivers** of conflict — not secondary background context. They operate on slower timescales than political events but often create the structural conditions that political events ignite.

Key pathways:
```
Water scarcity → agricultural failure → food insecurity → displacement
→ competition for arable land → intercommunal violence → state fragility

Desertification → pastoral migration → herder-farmer conflict
→ armed escalation → state unable to manage → insurgency space opens

Climate migration → receiving community pressure → ethnic tension
→ political mobilization → violence or political crisis

Resource revenue → state dependency → price shock → fiscal crisis
→ reduced service delivery → legitimacy crisis → political instability
```

---

## Data Sources (Free, No Key Required)

### Climate Vulnerability
```bash
# ND-GAIN Country Index — overall climate vulnerability + readiness
# Best single composite index for country-level climate risk
https://gain.nd.edu/our-work/country-index/rankings/

# INFORM Risk Index (EU-funded, free)
# Combines hazard, vulnerability, and coping capacity
https://drmkc.jrc.ec.europa.eu/inform-index/

# IPCC Sixth Assessment Report — regional projections
https://www.ipcc.ch/report/ar6/
```

### Water Stress
```bash
# WRI Aqueduct Water Risk Atlas (free, no key)
https://www.wri.org/aqueduct

# UN-Water Global Analysis and Assessment
https://www.unwater.org/publications

# FAO AQUASTAT (country-level water data)
https://www.fao.org/aquastat
```

### Food Security
```bash
# IPC (Integrated Food Security Phase Classification) — real-time global
https://www.ipcinfo.org/

# FEWS NET (US government famine early warning)
https://fews.net/

# FAO GIEWS (Global Information and Early Warning System)
https://www.fao.org/giews/
```

### Land/Resource Conflict
```bash
# ACLED environment/resource conflict tag (filter event_type)
https://acleddata.com

# Land Matrix (land grabbing data)
https://landmatrix.org/
```

---

## Conflict-Resource Risk Matrix

### Water Conflict Typology

| Conflict Type | Driver | Typical Actors | Example |
|--------------|--------|---------------|---------|
| Inter-state water dispute | Transboundary river, dam construction | State vs. state | Ethiopia-Egypt-Sudan (Nile/GERD) |
| Herder-farmer conflict | Water hole/grazing competition | Community vs. community | Sahel, Horn of Africa |
| Urban water crisis | Infrastructure failure + population growth | State vs. population | Pakistan, MENA cities |
| Hydropower vs. downstream | Dam changes river flow regime | State vs. state/community | Mekong (China vs. SE Asia) |

### Food-Conflict Correlation

IPC Phase classifications (apply to FIPS or administrative regions):
| Phase | Definition | Conflict Implication |
|-------|-----------|---------------------|
| 1 — Minimal | Food secure | Baseline |
| 2 — Stressed | Coping without severe depletion | Increased migration risk |
| 3 — Crisis | Moderate acute malnutrition | Significant displacement driver |
| 4 — Emergency | Emergency food assistance required | Active conflict driver, armed group recruitment pool |
| 5 — Famine | Mass death | State legitimacy collapse accelerant |

**Key correlation:** Phase 3–4 conditions in a region with existing armed conflict → conflict intensification. Phase 3–4 in peaceful region → conflict onset risk elevated.

---

## High-Risk Resource Conflicts (Active 2024–2026)

### Nile Basin (Ethiopia, Egypt, Sudan, others)
**Core issue:** Grand Ethiopian Renaissance Dam (GERD) affects Nile flow to Egypt and Sudan
**Egypt position:** Dam threatens existential water security (90%+ of water from Nile)
**Ethiopia position:** Sovereign right to develop own resources; GERD is development necessity
**Sudan position:** Divided — benefits from flood regulation, concerned about flow reduction
**Legal framework:** 1929 Nile Waters Agreement (contested by upstream states as colonial-era), no binding multilateral treaty
**Escalation risk:** Egypt has made military threat statements. Ethiopia is unlikely to stop filling. Sudan is a potential flashpoint.
**Watch:** GERD filling schedule, Egyptian military posture, regional mediation attempts

### Mekong River (China vs. Lower Mekong States)
**Core issue:** Chinese upstream dams alter flow patterns, fisheries, sediment transport
**Affected:** Thailand, Laos, Cambodia, Vietnam
**Power asymmetry:** China upstream, no binding international water law applies
**Complicating factor:** Laos and Cambodia heavily economically dependent on China
**Watch:** Mekong water level data, ASEAN positions, US Mekong initiatives

### Sahel Water-Climate-Conflict System
**Core dynamic:** 10–20% rainfall decline + population growth → traditional pastoral routes disrupted → herder-farmer conflict → armed group exploitation of communal divisions → state fragility
**Affected:** Mali, Burkina Faso, Niger, Chad, Nigeria (northern), Sudan (Darfur)
**Not separable from:** Political instability, coup cycle, foreign military presence (French, Russian/Africa Corps, US)
**Watch:** Annual rainfall data, IPC food security phases, ACLED herder-farmer conflict events

### Arctic (Russia, US, Canada, Norway, Denmark/Greenland)
**Core dynamic:** Ice retreat opens new shipping routes (Northern Sea Route) and resource extraction (oil, gas, minerals)
**Russia position:** Asserts sovereign jurisdiction over Northern Sea Route
**Western position:** International waters / freedom of navigation
**Watch:** Ice extent data (NSIDC), Russian Arctic military installations, resource extraction agreements

---

## Climate as Conflict Multiplier

Climate stress rarely causes conflict directly. It multiplies existing tensions:

```
Existing condition          + Climate stressor          = Elevated risk

Ethnic land tension         + Drought                   = Herder-farmer violence
Political exclusion         + Crop failure              = Protest/uprising
Weak state capacity         + Flood displacement        = IDP conflict
Armed group presence        + Food insecurity           = Recruitment pool

No existing tension         + Climate stress            = Migration, adaptation (not conflict)
```

**Analytical rule:** Climate stress without pre-existing political/ethnic/economic tension rarely produces conflict. Always identify the political pre-condition before attributing conflict to climate.

---

## Resource Revenue and Governance

For resource-dependent states (oil, gas, minerals > 30% of GDP):

**Dutch Disease pattern:**
1. Resource boom → currency appreciation → manufacturing uncompetitive → economic monoculture
2. Price shock → fiscal crisis → sudden service/subsidy cuts → political instability
3. Revenue fluctuation creates patronage dependency → political system designed around resource distribution

**Resource curse indicators:**
- High resource revenue share of GDP
- Low tax base from non-resource sector
- Patronage-based political system
- Weak rule of law outside capital
- High inequality despite resource wealth

**Conflict implication:** Resource-cursed states are more vulnerable to civil conflict when prices fall and patronage networks can no longer be maintained.

**Key states:** Nigeria, Angola, DRC (minerals), Libya, Iraq, Venezuela, South Sudan — monitor fiscal breakeven vs. current commodity prices.

---

## Climate Assessment Integration Template

Add to FULL assessments when relevant:

```markdown
### Resource & Climate Layer

**Water stress level (WRI Aqueduct):** HIGH / MEDIUM / LOW / MINIMAL
**Food security status (IPC phase, if available):** Phase 1–5 by region
**Climate vulnerability (ND-GAIN):** Score and ranking
**Active resource disputes:** [list or none]
**Climate-conflict pathway:** [Which pathway, if any, is active: water/food/land/revenue]
**Conflict multiplier assessment:** [Is climate stress amplifying existing tensions, or is it an independent driver?]
```
