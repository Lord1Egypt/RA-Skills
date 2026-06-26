# ASHRAE-211 Level 2 Commercial Energy Audit Report

**Platforms:** Claude · Openclaw · Codex
**Domain:** Energy Auditing / Commercial Buildings / Decarbonization

## Purpose

Turns a building profile (occupancy type, vintage, gross floor area, climate zone, schedules, envelope, HVAC / DHW / lighting / plug-load inventory, on-site generation, control system), ≥12 months of utility data (electricity, natural gas, district steam / chilled water / hot water, fuel oil, propane, water), walkthrough findings, and metered / spot-measured equipment data into a DRAFT ASHRAE / ACCA Standard 211 **Level 2** commercial building energy audit report whose structure and content satisfy Normative Annex C (Level 2 mandatory reporting forms): executive summary, building / site description, energy-use baseline with EUI benchmarking, end-use disaggregation, Energy Conservation Measure (ECM) table with engineering-grade savings (±15–25% accuracy), simple payback, NPV, SIR, IRR, lifecycle cost, M&V plan reference per IPMVP, implementation roadmap, financing-options memo, and an unsigned PE / CEA sign-off block — for owner, utility-incentive-program, IRA §179D, NYC LL97, BERDO 2.0, NYSERDA, Title 24, and PACE-underwriter review.

## When to Use

- A Certified Energy Auditor (CEA), Certified Energy Manager (CEM), or Professional Engineer needs to draft an ASHRAE-211 Level 2 report for a commercial, institutional, multifamily, or government building
- A building owner needs to satisfy a utility-incentive-program audit requirement (Con Edison, National Grid, PG&E, SoCalGas, ComEd, Duke, NYSERDA, Energy Trust of Oregon, BC Hydro)
- A 179D consultant needs the baseline + proposed analysis structured for IRA §179D deduction (post-Inflation Reduction Act prevailing-wage / apprenticeship rules confirmed separately)
- A NYC LL97 (Local Law 97 of 2019, as amended) compliance team needs a Level 2 audit to scope ECMs that will land the building below the 2030 and 2035 emissions limits
- A Boston BERDO 2.0, DC BEPS, Denver Energize Denver, Seattle BEPS, St. Louis BEPS, or other Building Performance Standard (BPS) compliance team needs an ECM-by-ECM plan to land the building below the performance threshold
- A PACE / Green Bank / C-PACE lender needs an underwriting-grade audit (SIR ≥ 1.0 typically required) before financing energy upgrades
- A retrocommissioning / RCx team needs the diagnostic baseline before designing measures
- An ESCO / Energy Performance Contracting (ESPC) team needs the M&V-ready baseline and ECM table

## What It Does

**Phase 1: Intake and ASHRAE-211 Level Confirmation**
1. Confirms requester role (CEA / CEM / PE / BEMP / owner's rep / 179D consultant / ESCO), audit level (Level 1 preliminary, Level 2 energy survey + engineering-grade analysis, Level 3 detailed investment-grade) — and acknowledges that Level 2 requires ≥12 months utility data, on-site survey, end-use disaggregation, engineering-grade ECM analysis with ±15–25% accuracy, and Annex C reporting forms
2. Captures the building profile — building type per ASHRAE-211 occupancy categories, year built / years renovated, gross floor area (ft² / m²), conditioned area, parking and unconditioned-area breakdown, ASHRAE climate zone (1A–8 + worldwide), schedules, occupancy density, operating hours, principal end uses

**Phase 2: Utility Data Analysis and EUI Benchmarking**
3. Tabulates 12+ months bill-by-bill for each fuel (electricity kWh / kW, natural gas therms / Dth, district steam / CHW / HW, fuel oil gallons, propane gallons, water gal / kgal / m³) with the rate schedule, time-of-use windows, and demand charges
4. Performs weather-normalization with HDD / CDD from a named NOAA / Environment Canada / national weather station and a stated base-temperature method (typical 65°F / 18.3°C; sensitivity tested) and produces site EUI and source EUI in kBtu/ft²/yr (or kWh/m²/yr), three-year trend, and ENERGY STAR Portfolio Manager 1–100 score where eligible
5. Disaggregates end use (HVAC heating, HVAC cooling, fans, pumps, lighting interior, lighting exterior, plug loads, refrigeration, DHW, vertical transportation, process, on-site generation) using a calibrated engineering method (not just the Portfolio Manager default) and flags anomalies (rate-schedule errors, abnormal load factor, unexplained baseload, peak-demand drift, weather-not-explained variance)

**Phase 3: Building / Site Description and Load Profile**
6. Catalogues the envelope (assemblies, U-values, SHGC, infiltration estimate), HVAC primary (chiller, boiler, DX, VRF, district), HVAC secondary (AHU, VAV, FCU, RTU, fan coil, baseboard), DHW (water heater, boiler, heat pump, instantaneous), lighting (interior LPD W/ft² by space type, exterior LPD W/ft², controls), plug loads (workstation / kitchen / data closet / lab / specialty), vertical transportation (elevators, escalators), process loads, on-site generation (solar PV kW DC / kW AC, CHP, battery storage), BAS architecture (BACnet / Modbus / proprietary, named platform), and metering (utility, sub-meter, smart-meter interval data, BMS trend data)
7. Builds the load profile (annual, monthly, weekday vs weekend, peak day with 15-minute or hourly granularity) where the data supports it

**Phase 4: ECM Identification and Engineering-Grade Analysis**
8. Identifies ECMs from the walkthrough, end-use breakdown, BAS trend review, and discipline checklists — categorized by ASHRAE-211 ECM families: envelope, HVAC, DHW, lighting, plug loads, controls, retrocommissioning, on-site generation, electrification, water, behavior
9. Analyzes each ECM with the Annex C minimum content: scope, baseline, proposed, savings calculation method (bin method / regression / hourly simulation / DOE-2 / EnergyPlus / OpenStudio / IES-VE / Trane TRACE / Carrier HAP / spreadsheet), savings in native units (kWh, therms, gallons, kBtu) and demand savings (kW), $ savings at the marginal rate (with rate-schedule basis stated), interactive effects with other ECMs (avoids double-counting), installed cost (with source — Means / RSMeans / vendor quote / parametric), simple payback (yr), NPV (with stated discount rate and analysis period), Savings-to-Investment Ratio (SIR), IRR, lifecycle cost (LCC), non-energy benefits (productivity, IAQ, IEQ, code-compliance, brand), M&V Option per IPMVP (A retrofit-isolation key parameter, B retrofit-isolation all parameter, C whole-facility, D calibrated simulation), implementation risk (Low / Medium / High), sequencing dependency with other ECMs, electrification / decarbonization flag, and emissions impact (kg CO₂e/yr — with the grid-emissions factor source named, e.g. eGRID subregion)
10. Cross-checks every ECM against the **interactive-effects rule**: lighting LED reductions reduce internal gain, which reduces cooling load (savings) and increases heating load (penalty) — the bundle is netted, not stacked

**Phase 5: Implementation Roadmap and Financing Options**
11. Sequences ECMs into Tier 1 (no-cost / low-cost / operational / RCx — typically <2-year payback), Tier 2 (capital — typically 2–7-year payback), Tier 3 (deep retrofit / electrification — typically 7–20-year payback) with a stated phasing rationale that accounts for end-of-life replacement, BAS upgrades, façade work, asbestos / lead abatement, and tenant displacement
12. Catalogues financing options — utility rebates and prescriptive / custom incentives (named program), IRA §179D deduction (post-IRA prevailing-wage / apprenticeship confirmation flagged), IRA §48 Investment Tax Credit and the Domestic Content / Energy Community / Low-Income bonus adders, IRA §45L for residential portions where applicable, PACE / C-PACE, Green Bank / state low-interest loans, on-bill financing, performance contracting / ESPC / ESCO, GSA / federal facility funding, BPS-related financing (NYC, Boston, DC, Denver, Seattle, St. Louis BPS programs), tax-exempt-entity direct-pay election (where applicable) — naming each program and the next step to confirm eligibility

**Phase 6: Annex C Conformance Check, Assembly, Sign-off, Open Questions**
13. Self-checks against ASHRAE-211 Normative Annex C Level 2 mandatory reporting forms — every required field complete, every ECM rendered in the prescribed format, the EUI tables and end-use breakdown in the prescribed format, the executive summary in the prescribed format
14. Assembles the executive summary (≤2 pages — building, baseline EUI vs benchmark, total identified savings energy / $ / emissions / payback range, top-N ECM recommendations, financing snapshot), the body, appendices (utility bill log, weather normalization, end-use disaggregation method, ECM calculations, M&V plan reference, code-compliance summary), and an unsigned PE / CEA sign-off block
15. Lists open questions (data not received, equipment nameplate not legible, BAS read-only access pending, occupant survey pending) and an evidence index that cross-references every utility bill, equipment nameplate photograph, BAS trend, spot-measurement log, and vendor quote

## Output

A draft Level 2 audit packet consisting of (a) an executive summary (≤2 pages); (b) the Annex-C-conformant body (intake, utility analysis, building description, ECM table, implementation roadmap, financing memo, self-check); (c) the ECM table with engineering-grade per-ECM analysis; (d) appendices (utility bill log, weather normalization, end-use method, ECM calculations, M&V plan, code-compliance summary); (e) the unsigned PE / CEA sign-off block; (f) a numbered evidence index; (g) an open-questions list — all marked **DRAFT — FOR OWNER, UTILITY-INCENTIVE-PROGRAM, BPS-COMPLIANCE-TEAM, AND PE / CEA REVIEW**.

## Notes

This skill **drafts** an ASHRAE-211 Level 2 audit report to support — never replace — the licensed Professional Engineer, Certified Energy Auditor, or Certified Energy Manager who will sign and seal the report. The skill does not stamp or seal, does not bind the building owner to any ECM, does not warrant that the building will achieve any specific BPS / LL97 / BERDO / BEPS / Title 24 compliance result, does not certify §179D eligibility (which depends on prevailing-wage and apprenticeship verification outside the audit), does not commit the utility to any incentive amount, does not perform the M&V (Option A/B/C/D per IPMVP) — only references the plan to do so. The skill follows ASHRAE-211 mandatory Annex C forms for Level 2 — Level 1 (preliminary) and Level 3 (investment-grade) are scoped separately and the skill will flag and stop if the user requests a level the skill is not currently configured to draft.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
