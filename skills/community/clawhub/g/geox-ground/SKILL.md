---
name: geox-ground
description: Earth-domain reasoning grounding for arifOS. Activate when: (1) any claim involves geology, wells, seismic, basin interpretation, petrophysics, Earth materials, or subsurface reasoning; (2) questions about geological structures, formations, rock properties, fluid dynamics, or basin modeling; (3) Arif asks about geoscience topics. GEOX is the Large Earth Model layer — it forces physics-over-narrative, real-data-over-elegant-fiction, and explicit OBS/DER/INT/SPEC separation. NOT optional decoration.
metadata: {"openclaw": {"emoji": "🌍"}}
---

# GEOX Ground — Grounded Earth Reasoning Layer

GEOX exists to force the agent to reason through **physics, material constraints, real data, and explicit uncertainty** when the task touches the physical Earth.

## The GEOX Habit

When any Earth-domain claim is made, the agent must:

1. **Separate epistemic levels** — never conflate observation with interpretation
2. **Invoke physics first** — appeal to material constraints, not narrative
3. **Preserve uncertainty** — don't paper over unknowns with confident language
4. **Ground in real data** — wells, seismic, logs, samples beat inference

## Epistemic Labels

Prefix every Earth-domain claim with a label:

| Label | Meaning | Example |
|---|---|---|
| `OBS` | Direct observation | "Wireline log shows 2150m TVD" |
| `DER` | Derived from data | "Porosity computed from density log" |
| `INT` | Interpretation | "This structure likely contains hydrocarbons" |
| `SPEC` | Speculation | "Possibly a turbidite fairway" |

**Never present `INT` as `OBS`. Never present `SPEC` as `INT`.**

## When This Skill Activates

- Geology, geophysics, petrophysics, basin modeling
- Well logs, seismic interpretation, formation evaluation
- Rock properties, fluid contacts, pressure regimes
- Structural geology, stratigraphy, sedimentology
- Questions with words: "formation", "reservoir", "trap", "seal", "source", "pay", "porosity", "permeability", "saturation", "pressure", "depth", "structure"

## GEOX Decision Rules

1. **Physics over narrative** — "The seal capacity must exceed the column height" beats "it looks like a good trap"
2. **Real wells over hand-wavy synthesis** — cite actual data points
3. **Uncertainty bands required** — for any quantitative claim, provide a range
4. **Hold conditions** — if data is insufficient for a confident interpretation, say so and label it `SPEC`
5. **No false precision** — 2150m ± 5m is fine; 2150.342m is fraud if you only measured to nearest 5m

## Anti-Error Patterns

❌ "This is definitely a turbidite reservoir."
✅ "The seismic character in this interval (OBS: chaotic, moderate amplitude) is consistent with turbidite deposits (INT), but could also be mass-transport deposits (DER from amplitude vs frequency analysis). Confidence: LOW."

❌ "The well found commercial hydrocarbons."
✅ "The MDT tool recovered gas-cut mud (OBS) indicating mobile gas (DER: pressure gradient 0.65 psi/m). Pay thickness net pay cutoffs pending final log analysis."

## References

- GEOX epistemic label guide: `references/epistemic-labels.md`
- Common hold conditions in geoscience: `references/hold-conditions.md`
