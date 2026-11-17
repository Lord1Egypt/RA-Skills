<!-- Copyright (c) 2026 Yang Pengfei / WeChat Official Account "Forklift Veteran". MIT License: see LICENSE.md. -->
# Forklift Selection Guide

Select operating environment → actual load and capacity → power system, then brand/configuration. All dimensions, residual capacity, battery performance and prices require model- and market-specific confirmation.

## 1. Decision Path

```text
Mainly indoors → electric counterbalance / reach / pallet / VNA as required
Mainly outdoors → assess surface, gradient, weather, duty and charging
Heavy outdoor / no charging → compare approved IC and electric alternatives
Mixed duty → assess protection, tyres, charging and ventilation

Rack height: low → counterbalance or stacker; high → reach/VNA subject to capacity
Aisle: wide → counterbalance; restricted → reach/articulated/VNA after layout check
Single shift with charging window → compare lead-acid and lithium TCO
Multiple shifts → assess opportunity charging, battery exchange and infrastructure
Cold store → manufacturer-rated truck and battery, heating/condensation controls
Hazardous area → complete approved explosion-protected configuration
```

Height bands such as below 4 m, 4-8 m and above 8 m, and aisle bands such as above 3.5 m, 2.5-3.5 m and below 2.5 m, are preliminary screening only. Actual stacking aisle depends on truck, pallet orientation, load and clearance; obtain the manufacturer's layout data.

## 2. Application Matrix

| Industry | Priorities | Candidate types / brands to investigate |
|---|---|---|
| Cold chain | Temperature, hygiene, condensation | Approved cold-store electric; Heli, Hangcha and regional suppliers |
| Food / beverage | Hygiene, noise, indoor air | Electric counterbalance, suitable attachments/fluids |
| Pharmaceuticals | Cleanliness and controlled environment | Electric with compatible cleaning/materials |
| Electronics | ESD and cleanliness | Specifically approved ESD configuration |
| Automotive | Continuous duty and line supply | Electric counterbalance, tow tractors or suitable heavy trucks |
| Ports | Weather, load, ground and containers | Heavy forklifts/container handlers: Kalmar, Hangcha, LiuGong and others |
| E-commerce | Frequent pallet movement and standard routes | Pallet trucks, stackers, reach trucks, AGV/AMR where justified |
| Steel / building materials | Heavy loads and long goods | Rated heavy counterbalance or multidirectional equipment |
| Chemical | Hazard classification | Approved explosion-protected truck; chemistry alone is insufficient |
| Manufacturing | Shift pattern and mixed duty | 2-3.5 t class as an initial range, subject to actual load chart |
| Wholesale | Outdoor loading and service access | Suitable electric, diesel or LPG, subject to air-quality rules |
| High-bay logistics | Lift height, aisle and floor | Reach/VNA: Linde, Jungheinrich, Crown, Toyota and others |

For UK, EU, US and other regional product ranges and service websites, use `international-markets.md`. Verify local model availability rather than importing a China-market recommendation unchanged.

## 3. Capacity

Specify cargo mass, dimensions, centre of gravity, required height, attachment mass/offset, pallet and dynamic conditions. Use the truck's configuration-specific residual-capacity plate. Nominal tonnage alone is insufficient. A planning margin does not authorize exceeding the plate.

Do not estimate capacity by a universal percentage per metre of lift or per 100 mm of load centre. Obtain the manufacturer's chart for the actual mast/attachment. Typical shopping ranges span 1-1.6 t for light work, 2-3.5 t for general industry, 5-10 t for heavy handling and 16 t+ for specialist work; these are not guaranteed allowable cargo weights.

## 4. Configuration Checklist

- [ ] Fork length, section, mounting class and approved load.
- [ ] Mast stages, free lift, lowered height, overhead clearance and lift height.
- [ ] Rated/residual capacity at actual load centre and height.
- [ ] Battery energy/voltage, motor or engine, duty-cycle evidence.
- [ ] Approved charger, electricity supply, cable route and installation.
- [ ] Tyres, floors, gradients, weather/ingress protection.
- [ ] Overhead guard, restraint, warning devices and required safety systems.
- [ ] Sideshift, fork positioner, clamps, push-pull or other approved attachment.
- [ ] Cold-store, food-grade, ESD or explosion-protected specification where required.
- [ ] Weighing, cameras, fleet management and automation interfaces where useful.

Lithium checks: chemistry, usable kWh, duty, charge rate, BMS compatibility, thermal management, warranty, service and end-of-life support. For example 80 V × 300-500 Ah gives nominal 24-40 kWh; usable energy differs. Do not assume automotive CCS/CHAdeMO compatibility or universal 30/80 kW chargers.

## 5. Contract Terms

Itemize truck, battery, charger, attachment and installation. Specify acceptance tests, actual warranty years/hours/cycles and battery capacity conditions, local registration/conformity documentation, training, parts delivery, service response/radius, software access, replacement truck and residual-value/trade-in terms. Warranty figures are negotiated, not universal industry guarantees.

## 6. Five-Year TCO

```text
TCO = purchase + installation + energy + maintenance + training + insurance
      + downtime + financing/disposal - residual value
Electric energy = operating hours × measured kWh/h × electricity tariff
IC fuel = operating hours × measured L/h × fuel price
Maintenance = parts + labour + inspections + planned replacements
```

Use comparable duty, currency, tax treatment and reporting period. Account for infrastructure, battery replacement, time-of-use charges and service availability. Illustrative China-market estimates are not current UK/EU/US quotations; do not assert lithium always has lower TCO.

## 7. Common Mistakes

Oversizing wastes capital and manoeuvrability; undersizing creates overload risk. Other errors include assuming lithium is always cheaper, ignoring charging space/power, attachment derating/cost, remote service delays, operator training, floor loading or rack clearance. Do not use unsourced percentages for fault causation.

## 8. Recommendation Template

```text
Scenario: <cargo / load centre / lift / aisle / temperature / shifts / market>
Candidate category and capacity: <subject to approved residual-capacity chart>
Power: <evidence-based choice>
Mast / attachment / tyres / safety: <actual configuration>
Local candidates: <verified regional models and dealer support>
Infrastructure and compliance: <requirements to confirm>
Budget: <dated local quotations, currency, taxes and inclusions>
TCO assumptions / uncertainties: <explicit>
Sources: <official specifications, dates and URLs>
```

References: `brands.md`, `models-spec-retrieval.md`, `standards.md`, `safety-regulation.md`, `used-forklift-evaluation.md`.
