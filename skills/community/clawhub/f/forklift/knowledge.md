<!-- Copyright (c) 2026 Yang Pengfei / WeChat Official Account "Forklift Veteran". MIT License: see LICENSE.md. -->
# Forklift Knowledge Base

Reference topics: truck types, selection, batteries, drives, hydraulics, masts, economics and applications. Exact model specifications require `models-spec-retrieval.md`; current law/status requires `standard-retrieval.md`. Do not invent figures from memory.

## 1. Truck Types

| Common US industry class | Description | Applications |
|---|---|---|
| I | Electric motor rider trucks | Manufacturing and indoor handling |
| II | Electric narrow-aisle trucks | Reach, order picking and high-bay storage |
| III | Electric motor hand / hand-rider trucks | Pallet transport and stacking |
| IV | IC trucks with cushion tyres | Suitable prepared surfaces, subject to ventilation |
| V | IC trucks with pneumatic tyres | Suitable outdoor handling |
| VI | Electric and IC tractors | Towing |
| VII | Rough-terrain forklift trucks | Appropriate construction/outdoor applications |

This US industry classification is not the complete ISO 5053-1 taxonomy. ISO 5053 and GB/T 6104 provide terminology/classification; select the correct type definitions. Other products include telehandlers, container handlers, platform trucks, automated trucks and explosion-protected trucks.

## 2. Selection Questions

Electric trucks offer low local emissions and noise; IC trucks can suit appropriate outdoor duty and refuelling infrastructure. Compare actual workload, ventilation, emissions law, energy supply, gradients, temperature, cost and service. Electric trucks are not maintenance-free.

| Factor | Lithium-ion | Lead-acid |
|---|---|---|
| Charging | Opportunity/fast charging if approved | Often longer charge/cooling window; design-dependent |
| Maintenance | No routine watering, but inspect BMS, connections and cooling | Flooded types require approved watering and care |
| Purchase | Often higher initial cost | Often lower initial cost |
| Cold operation | Approved temperature and heating limits matter | Cold reduces available capacity too |
| Suitability | High utilization where infrastructure supports it | Can suit lower-duty operations with charging time |

Cycle life, charge time and temperature ranges depend on chemistry, depth of discharge, warranty conditions and model. Do not state one range as guaranteed. Select cargo capacity from the actual residual-capacity plate, including load centre, height and attachment effects.

## 3. Battery and Charging

Follow the battery manufacturer's SOC window, storage SOC, inspection and recharge schedule. A generic 20-80% operating band or 40-60% storage band is only a planning example, not universal instruction. Avoid long storage at unsuitable SOC/temperature.

Reduced runtime, SOC jumps, abnormal charge current/voltage, temperature differences and BMS warnings require assessment. Smoke, swelling, smell or rapid heating require stop-use and emergency escalation.

Use only an approved compatible charger with correct voltage, chemistry, communication, connector and charge profile. Do not substitute a lead-acid charger for lithium. Charging power must match battery acceptance, connector and site supply; do not assume all trucks have an onboard charger or automotive charging protocol.

## 4. Motors and Controls

AC induction and permanent-magnet motors are common; older DC motors may need brush maintenance. AC is not a guarantee of a fixed efficiency gain. Permanent magnets can offer efficiency/torque advantages but suitability depends on the drive and duty.

Controller suppliers include Curtis, ZAPI, Sevcon and regional suppliers. Voltage/current/motor type/software/CAN compatibility are model-specific. Obtain the serial-specific approved configuration rather than replacing by brand alone.

## 5. Hydraulics

Gear, piston and vane pumps differ in pressure, flow, efficiency, noise and cost. Select oil viscosity, additives, low-temperature performance and food-grade requirements from the manual. H1 registration concerns incidental food contact; it does not establish universal equipment compatibility.

Slow lift checks: actual load and capacity → oil level/temperature → filter restriction → qualified relief/pump/valve/cylinder testing. Never set a generic 16-18 MPa pressure to overcome an overload. Oil change intervals follow the manual, duty and condition analysis.

## 6. Mast and Attachments

Two-stage, three-stage and full-free-lift masts offer different lowered height, lift, visibility and capacity. Stage count alone does not establish free lift or maximum height. Verify doorway/container clearance and overhead space.

Attachments include sideshift, fork positioners, paper-roll/drum/bale clamps, rotators, push-pulls, tipping devices and approved lifting attachments. Attachment weight and offset reduce residual capacity. Ordinary forks are not an approved personnel platform.

## 7. Braking

Trucks may use dry friction, wet-disc, hydraulic, mechanical or electromagnetic systems depending on design. Regeneration can recover energy but savings vary by duty. It does not replace service or parking brakes. Inspect all systems per the manufacturer schedule.

## 8. TCO

```text
TCO = purchase + infrastructure + energy + maintenance + training + insurance
      + downtime + financing + disposal - residual value
```

Use comparable operating hours, load cycles, temperature, tariffs, fuel prices, currency and tax basis. Include battery replacement and local service. A historic China-market example cannot establish a current UK/EU/US price or a universal lithium advantage. See `selection-guide.md`.

## 9. Noise, Emissions and Applications

Measure noise using the stated method and assess worker exposure; do not assume every electric truck is below one noise threshold. IC emissions requirements depend on engine, market and use. Indoor IC operation requires an actual air-quality/ventilation assessment and applicable law.

| Scenario | Candidate approach |
|---|---|
| Cold store | Rated low-temperature electric/other approved truck, condensation and charging controls |
| Ports | Heavy counterbalance, container handler or reachstacker matched to duty |
| Food / pharma | Hygiene-compatible truck, attachment and fluids |
| Hazardous area | Complete approved explosion-protected configuration |
| E-commerce | Pallet trucks, reach/stackers or justified automation |
| High bay | Reach/VNA with verified floor, aisle and residual capacity |
| Rough terrain | Suitable rough-terrain truck/telehandler and trained operator |

## 10. Misconceptions

Lithium trucks still need brake, mast, hydraulic, tyre and electrical maintenance. Same nominal tonnage does not guarantee the same residual capacity. Fast charging is safe only within the approved battery/charger limits. AGVs suit assessed repeatable workflows, not every task. Battery cycle count cannot be compared directly with an entire IC truck's life.

## 11. Research at Answer Time

Verify exact model figures, current quotations, measured consumption, warranty, service coverage, legal requirements and market statistics. Use `international-markets.md` for UK, EU, US, Canada, Australia and Japan sources. Record region, date, configuration and URL.
