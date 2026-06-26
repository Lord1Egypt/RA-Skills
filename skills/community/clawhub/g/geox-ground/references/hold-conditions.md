# GEOX Hold Conditions — When to Pause and Escalate

These are the geological conditions that require explicit HOLD before proceeding.

## Seismic Interpretation

| Condition | Why HOLD |
|---|---|
| Only 2D seismic available | 3D missing → high structural uncertainty |
| Seismic tied to < 2 wells | Velocity model unconstrained |
| Time-depth conversion uncertain | Structure maps could be significantly wrong |
| Data polarity unknown | Fluid contact identification unreliable |
| Volcanic/basalt affected zone | Seismic imaging severely degraded |

**Rule:** Any structural interpretation from 2D seismic alone → `INT` minimum, label as `SPEC` if critical

## Well Log Interpretation

| Condition | Why HOLD |
|---|---|
| No core or test data to calibrate logs | Porosity/saturation uncertain |
| Log quality flagged as poor | Use alternative curves or reject interpretation |
| Missing essential logs (no SP, gamma) | Cannot differentiate lithology reliably |
| Water-based vs oil-based mud invasion uncertain | Resistivity interpretation compromised |

**Rule:** Petrophysical conclusions without calibration → `SPEC`

## Reserves/Resources

| Condition | Why HOLD |
|---|---|
| No fluid contacts confirmed by test or MDT | STOIIP/GIP highly uncertain |
| Recovery factor from analogy only | Not actually measured |
| Structure not mapped on 3D | Volumetric range could be 2-3x |
| Pressure data absent | Drive mechanism unknown |

**Rule:** Any reserves estimate without confirmed fluid contacts → `HOLD` → Arif approval required

## Safety-Critical Decisions

| Condition | Why HOLD |
|---|---|
| HPHT environment (P > 10,000 psi or T > 150°C) | Standard assumptions break down |
| Drilling into unknown pressure regime | Well control risk |
| Uncertain H2S presence | Life safety |
| CO2 storage or sequestration | Long-term liability |

**Rule:** Safety-critical → FLOOR 13 (Kedaulatan) → explicit Arif authorization required

## The GEOX Minimum Viable Evidence Set (for confident interpretation)

To move from `SPEC` to `INT`:
- [ ] Seismic mapped on 3D (or 2D with 2+ wells)
- [ ] At least one well with GR + resistivity + porosity log
- [ ] At least one pressure measurement
- [ ] Lithology identified from cuttings or core

To move from `INT` to `DER`:
- [ ] Quantitative log analysis with core calibration
- [ ] Pressure gradients consistent with fluid types
- [ ] No conflicting indicators
