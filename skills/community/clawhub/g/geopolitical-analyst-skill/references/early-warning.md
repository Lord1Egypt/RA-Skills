# Early Warning System

## Purpose

Detect situations that will become crises before they appear in news feeds. Most conflicts and political crises are predictable 6–24 months before they erupt if the right structural indicators are monitored.

The Political Instability Task Force (PITF) — funded by the US government, peer-reviewed — identified the combinations that most reliably precede instability. This reference documents those indicators and their open-source proxies.

---

## The PITF Core Model

Two structural conditions together predict instability onset better than any other combination:

### Condition 1: Regime Type — The "Anocracy" Risk Zone

| Polity Score | Regime Type | Instability Risk |
|-------------|------------|-----------------|
| +6 to +10 | Full democracy | LOW |
| +1 to +5 | Partial democracy | MEDIUM |
| -5 to 0 | **Anocracy** | **HIGHEST** — 3× more likely than full democracy |
| -10 to -6 | Full autocracy | MEDIUM (more stable than anocracy) |

**Anocracy** = partial democracy with incomplete institutions, where competitive elections exist alongside significant authoritarian practices. This is the most unstable zone — not dictatorship.

**Source (free):** Polity5 dataset — www.systemicpeace.org/polityproject.html

### Condition 2: Ethnic Factionalism

Present when: a dominant ethnic/sectarian group controls state institutions at the expense of other groups, AND the marginalized group(s) have political organization.

**Combined risk:** Anocracy + ethnic factionalism = highest instability predictor globally. Alone, each condition doubles risk. Together, they multiply it.

---

## Secondary Early Warning Indicators

These indicators add predictive value when primary conditions are met:

### 1. Infant Mortality Rate (IMR) as State Capacity Proxy
- IMR > 40 per 1,000 live births → significant state capacity failure
- IMR > 75 → severe state capacity failure; conflict zone risk elevated
- **Source:** UNICEF State of the World's Children (annual, free)
- **Why it works:** IMR captures government delivery of basic services across the whole country — hard to fake, hard to politically manipulate

### 2. Neighborhood Effect
- Countries **bordering active conflict** have 5× higher instability risk than baseline
- The mechanism: refugee flows, arms trafficking, armed group sanctuary, economic disruption, political contagion
- **Apply:** When analyzing a conflict, always check bordering countries' stability status

### 3. Elite Fragmentation Signals
Visible before public collapse:
- High-profile defections from ruling party/military
- Purges of senior officials (indicates leader perceives threat from within)
- Factional public disagreements in previously unified government
- Sudden retirement/resignation of security chiefs
- State media tone shift toward internal scapegoating

### 4. Security Force Cohesion
The most important single variable for whether a government survives a crisis:
- **Unified security force** → government likely survives protest/coup attempt
- **Fractured security force** (ethnic splits, factional loyalty, non-payment) → government vulnerable even to moderate opposition

**Detection signals:**
- Reports of non-payment to soldiers/police
- Security force units refusing orders
- Ethnic composition of key security units vs. population
- Parallel security forces established (indicator: leader doesn't trust main military)

### 5. Economic Grievance Accumulation
Not economic crisis alone — the *combination* of economic stress and blocked political channels:
- Youth unemployment > 25% + restricted political participation = volatile combination
- Subsidy removal + no compensation mechanism = protest trigger
- Inflation affecting food + fuel simultaneously = mass mobilization threshold

### 6. Leadership Succession Uncertainty
Particularly destabilizing in non-democratic systems when:
- Leader is aging, ill, or recently incapacitated
- No established succession mechanism
- Multiple factions are openly positioning
- No constitutional framework for transfer

---

## Leading Indicators by Crisis Type

### Pre-Coup Indicators (6–18 months before)
- Military officers making political statements (breaking institutional norm)
- Civilian government attempting to change military leadership for political reasons
- Civilian leaders creating parallel security structures
- Military budget cuts or non-payment
- Regional military commanders building autonomous local relationships
- Foreign military training/equipment shifting to one faction

### Pre-Mass Protest / Revolution (3–12 months before)
- Previous protest cycle was suppressed but not addressed
- Economic shock (subsidy cut, currency devaluation, unemployment spike)
- Opposition figure imprisoned or exiled → becomes focal point
- Networked civil society organizations forming coalitions
- Diaspora funding and organizational support increasing
- Commemorative date approaching (anniversaries of previous protests/events)

### Pre-Civil War (12–36 months before)
- Ethnic/sectarian armed incidents increasing in frequency
- State withdrawing from peripheral regions (policing, services)
- Armed opposition group successfully testing state response
- External patron beginning material support to opposition group
- Refugees from neighboring conflict providing recruitment pool
- Anocracy + factionalism conditions present (PITF model)

### Pre-Interstate Conflict (6–18 months before)
- Repeated border incidents without resolution
- Military modernization/procurement spike in one party
- Alliance commitments being publicly reaffirmed (signaling)
- Economic interdependence declining between parties
- Back-channel communication channels going quiet
- Domestic political pressure requiring "action" on the dispute

---

## Free Data Sources for Early Warning

| Indicator | Source | Update Frequency |
|-----------|--------|-----------------|
| Polity5 scores (regime type) | systemicpeace.org | Annual |
| Fragile States Index | fundforpeace.org/fsi | Annual |
| ND-GAIN Country Index (climate vulnerability) | gain.nd.edu | Annual |
| ACLED conflict trends | acleddata.com | Daily |
| UNHCR displacement data | unhcr.org/data | Monthly |
| UNODC crime/instability data | unodc.org/unodc/data-and-analysis | Annual |
| World Bank governance indicators | worldbank.org/governance | Annual |
| Freedom House (political rights) | freedomhouse.org | Annual |
| IMF Article IV reports (economic stress) | imf.org | Annual per country |
| UNICEF IMR data | unicef.org/statistics | Annual |

---

## Early Warning Assessment Format

When running proactive monitoring (not reactive analysis), output:

```markdown
## ⚠️ Early Warning Assessment: [COUNTRY] — [DATE]

**Monitoring basis:** [Why this country is being watched]

### Structural Risk Profile
- Regime type (Polity score if available): [score/type]
- Ethnic factionalism: PRESENT / ABSENT / PARTIAL
- PITF combined risk: LOW / ELEVATED / HIGH
- Neighboring conflicts: [list or none]
- Neighborhood effect: YES / NO

### Active Precursor Indicators
[Numbered list of specific observable signals currently present]

### Missing Triggers
[What conditions are not yet present that would significantly elevate risk]

### Timeline Estimate
[Based on precursor pattern, estimated window: IMMINENT (<3mo) / NEAR (<12mo) / MEDIUM (1-3yr) / WATCH]

### Key Observable
[Single most important development that would confirm or deny the trajectory]

### Confidence: HIGH / MEDIUM / LOW
[Basis for confidence level]
```

---

## Calibration Notes

Early warning models are probabilistic, not deterministic:
- PITF model correctly identifies ~75% of instability onsets at 2-year horizon
- ~25% false positive rate at the threshold used above
- Absence of indicators does NOT mean absence of risk — black swans occur

**Honest statement every early warning assessment should include:**
> "These indicators assess structural risk factors, not certainty of outcome. Most high-risk situations do not result in acute crises. This assessment identifies elevated probability, not prediction."
