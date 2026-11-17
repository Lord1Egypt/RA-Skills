<!-- Copyright (c) 2026 Yang Pengfei / WeChat Official Account "Forklift Veteran". MIT License: see LICENSE.md. -->
# Forklift Maintenance Planning

Applies to relevant electric and IC trucks. Use the actual manufacturer's schedule and current local inspection law. GB/T 44361-2024 is a reference to verify, not a universal schedule. Heavy duty, dust, corrosion, cold stores and multiple shifts may require shorter intervals; do not automatically halve or extend intervals without approval.

## 1. Planning Levels

| Planning level | Illustrative scheduling checkpoint | Responsible role |
|---|---|---|
| Pre-shift | Before use, and after each shift where required | Trained operator |
| Weekly | Weekly / around 50 h | Operator and supervisor |
| Monthly | Monthly / around 200 h | Qualified technician |
| Quarterly | Around 600 h | Qualified specialist |
| Half-year | Around 1200 h | Service provider |
| Annual | Around 2400 h | Service provider / competent inspector |
| Statutory examination | Applicable law and examination scheme | Authorized / competent inspector |

These are planning examples, not prescribed replacement intervals. Follow whichever calendar/hour limit the manual requires. Do not infer a four-year truck inspection interval from an operator certificate renewal period.

## 2. Pre-Shift Checks

- [ ] Tyres/wheels, forks, carriage, mast, chains, guards and restraint.
- [ ] Required lights, horn, warnings, display and interlocks.
- [ ] Service/parking brakes, steering and controls in a safe test area.
- [ ] Fluid/fuel levels per manual and no leaks.
- [ ] Attachment secure; capacity plate valid for configuration.
- [ ] Battery/connector condition; no smoke, heat, swelling or alarms.
- [ ] Route, floor, dock, overhead clearance and pedestrian protection.

Lithium: check SOC/temperature and BMS warnings against approved limits; charger and connector must be undamaged. Lead-acid: inspect cleanliness and electrolyte only as trained, using the correct filling procedure. IC: check oil/coolant, starting, exhaust, cooling and aftertreatment indications.

## 3. Weekly Checks

Inspect tyre wear/pressure, fasteners, fork damage/wear, chains and anchors, mast rollers, hoses, wiring, approved lubrication points, brakes and battery cleanliness. Use model-specific wear limits and tyre markings. Never assume a universal tread depth, chain sag, tyre pressure or friction thickness.

## 4. Monthly Checks

Review oil/filter condition, air/fuel/engine filters, ignition components where applicable, braking travel/return, parking performance, steering play, old DC motor brushes, control connectors, encoders and structural welds. Test only through approved procedures; do not perform a generic 30% slope test or change clearances from generic figures.

## 5. Quarterly Checks

Review scheduled oil/fluid changes, lubrication, chain elongation, fork condition, battery/charger records and critical fastener torque. Replace on the manual's interval or condition limit. Lead-acid specific gravity depends on battery and temperature. Lithium capacity/SOH testing requires an approved procedure, not an arbitrary full 1C discharge.

## 6. Half-Year Checks

Qualified personnel assess hydraulic pressure/leakage, brakes, mast structure, electrical insulation/continuity and safety functions where scheduled. NDT is performed where required by condition, regulation or approved plan. Insulation test voltage and connected electronics isolation must follow the manual. Firmware/BMS changes require approved versions and authorization; they are not mandatory periodic upgrades.

## 7. Annual Service

Perform the specified major service, calibration and safety-function tests, review battery capacity evidence and corrosion, update maintenance records and plan replacements. Do not routinely dismantle a sound engine, transmission, pump or battery solely because one year has passed; use the approved service procedure and condition evidence.

## 8. Statutory Examination

Confirm jurisdiction, truck category, attachment and competent-person scheme. Keep examination and routine maintenance distinct. UK LOLER/PUWER, US OSHA, EU national workplace rules and China's current special-equipment rules have different obligations. Record actual due dates from authoritative requirements and certificates. See `safety-regulation.md` and `international-markets.md`.

## 9. Replacement Planning

| Item | Basis for replacement |
|---|---|
| Oil and coolant | Manual interval, specification and condition analysis |
| Filters | Manual interval, restriction indication and contamination |
| Ignition parts | Engine procedure and condition |
| Brakes | Specified wear and performance limits |
| Tyres | Manufacturer wear marks, damage and operating condition |
| Forks | Approved wear, deformation/crack criteria; competent inspection |
| Chains | Specified elongation, wear, corrosion and damage limits |
| Rollers / seals | Condition, play, leakage and manufacturer criteria |
| Lead-acid / lithium battery | Safety, measured duty-capacity, warranty and manufacturer limits |
| DC brushes | Actual motor's wear limit |

Do not promise a component life from generic operating-hour estimates.

## 10. Record Template

```text
Asset ID / brand / exact model / serial:
Manufactured / commissioned:
Hours / location / duty:
| Date | Service level | Technician | Hours | Checks / measurements | Parts | Defects and action | Next due |
```

## 11. Lubrication Plan

Map approved points: mast/roller locations, chain, carriage, tilt/lift cylinder pivots, steering joints and pedal pivots as applicable. Record lubricant, amount, interval and method. Some bearings are sealed. Chain lubricant must be approved for the chain; do not substitute grease indiscriminately.

## 12. Cost and TCO

Budget consumables, wear parts, labour/travel, examinations, specialist diagnostics, downtime and planned major replacements. Use actual local quotations in the correct currency/tax basis. Avoid unsourced annual savings percentages. Track downtime, repeat faults and maintenance compliance to inform TCO and replacement decisions.

References: `fault-diagnosis.md`, `parts-consumables.md`, `knowledge.md`, `standards.md`, `safety-regulation.md`.
