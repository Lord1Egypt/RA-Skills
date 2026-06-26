# GEOX Epistemic Labels — Usage Guide

## The Four Labels

### OBS — Direct Observation
**Definition:** Something measured, recorded, or directly observed. No inference.

Examples:
- "Wireline gamma ray log shows 85 API at 2150m MD"
- "Core sample recovered from 2240-2245m shows medium-grained sandstone"
- "MDT tool recorded pressure of 3500 psi at 2100m TVD"

**Use when:** You have the actual data point. Cite the measurement tool/method.

---

### DER — Derived from Data
**Definition:** Computed or inferred from OBS using established methods. Mathematical or empirical transformation.

Examples:
- "Porosity computed from density log = 22% (DER: 𝜙 = (𝜌ma - 𝜌b)/(𝜌ma - 𝜌f))"
- "Water saturation Sw = 35% from Archie equation (DER: using a=1, m=n=2, Rt=15 ohm-m)"
- "TVD from MD using average deviation factor 0.98"

**Use when:** You applied a formula, method, or transformation to OBS data.

---

### INT — Interpretation
**Definition:** Professional judgment applied to DER + contextual knowledge. Not a direct measurement.

Examples:
- "This porosity-permeability relationship suggests reservoir-quality rock (INT)"
- "The flat spot on the seismic amplitude is interpreted as a fluid contact (INT)"
- "The structural high is likely a four-way closure suitable for trapping hydrocarbons (INT)"

**Use when:** Reasoning, experience, or geological context is applied beyond the raw data.

---

### SPEC — Speculation
**Definition:** An idea that is plausible but not supported by direct evidence. Low confidence.

Examples:
- "This could be a turbidite sandstone fairway (SPEC)"
- "Possibly the source rock is Ordovician in age (SPEC)"
- "May have been affected by late-stage tectonic inversion (SPEC)"

**Use when:** Proposing hypotheses, exploring possibilities, or filling data gaps with informed guesses.

---

## Composite Labels

In practice, chains often combine:

```
OBS → DER → INT → SPEC
```

Example:
1. OBS: "Density log values 2.35-2.45 g/cc across interval"
2. DER: "Porosity 18-24% computed from density"
3. INT: "Reservoir-quality sandstones based on porosity-permeability transform"
4. SPEC: "Likely transgressive systems tract within a third-order sequence"

---

## Confidence Calibration

| Label | Approximate Confidence | Typical Evidence |
|---|---|---|
| OBS | 95-100% | Direct measurement |
| DER | 80-95% | Established formula applied correctly |
| INT | 50-80% | Professional judgment, multiple indicators |
| SPEC | 10-50% | Plausible but unconfirmed |

**If you're unsure → SPEC. Never promote SPEC to INT without evidence.**
