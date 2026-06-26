# Geotechnical Investigation Report Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Geotechnical Engineering

## Purpose

Drafts a subsurface (geotechnical) investigation report for a single building, infrastructure, or earthwork site. Covers project description and proposed loading, site geology and regional-hazard scan, field exploration (boreholes, cone penetration tests, test pits, SPT N-values, refusal depths, groundwater observations), ASTM-aligned laboratory testing, subsurface conditions narrative, ASCE 7 seismic site class determination, foundation and earthwork recommendations (allowable bearing pressures, settlement estimates, lateral earth pressures, retaining walls, slabs-on-grade, pavements, deep foundations, dewatering), construction-phase considerations, ASFE-style limitations, and appendices for boring logs, lab data, and a site / boring-location plan.

**The output is always DRAFT.** A licensed Geotechnical Engineer of Record (GER) must verify every soil description, lab value, parameter selection, recommendation, and citation, and physically stamp and seal the report before it is issued to the design team, owner, or building department.

## When to Use

- Pre-design subsurface investigation for a building (residential, commercial, industrial, institutional), bridge, retaining structure, embankment, dam, pipeline, or pavement
- Owner's geotechnical due-diligence report for site acquisition (distinct from a Phase I Environmental Site Assessment)
- Update or re-issue of a prior geotechnical report when the proposed structure or loading changes
- Foundation-design support during schematic / design-development / construction-document phases
- Review of a third-party geotechnical report by an owner, lender, or design-team peer reviewer
- Junior staff engineer or report-production team drafting under a GER's supervision

## What It Does

**Phase 1: Project and Site Setup**
1. Captures project name, owner, design team, address (with lat / lon and parcel ID), proposed structure type and dimensions, anticipated column / wall / footing loads, anticipated cut-and-fill grading, intended pavement type, and any code or jurisdictional driver (IBC year, ASCE 7 edition, local DOT, FAA, AREMA, USACE)
2. Captures site geology and regional-hazard scan: published geologic mapping, regional groundwater conditions, regulatory floodplain, expansive / collapsible / liquefiable / corrosive soil indicators, karst, mining subsidence, landslide history, fault proximity (for ASCE 7 seismic and California Alquist-Priolo)

**Phase 2: Field Exploration**
3. Logs every exploration point with location (station / offset or lat / lon), surface elevation, depth, equipment, casing / drilling-method, sampler type, SPT N-values (raw and corrected to N1,60 or N1,60cs), CPT tip / sleeve / pore-pressure profiles, refusal depth, and observed-groundwater depth at completion and after stabilization
4. Tabulates sample inventory (sample number, depth, recovery, sampler, USCS classification, in-situ test, lab assignment)

**Phase 3: Laboratory Testing**
5. Tabulates lab results with the controlling ASTM standard (D2487, D2488, D4318, D6913, D7928, D2216, D2435, D2166, D2850, D4767, D1557, D698, D4546, D5333, D4972, D1883 CBR, D3080, D2980) — distinguishing field visual-manual descriptions (D2488) from laboratory USCS classifications (D2487)

**Phase 4: Subsurface Conditions and Seismic**
6. Builds the subsurface narrative: stratigraphy by exploration zone or by elevation, depth to bedrock or refusal, depth to and seasonal fluctuation of groundwater, perched-water indicators, hazardous-soil indicators (organic, expansive, collapsible, liquefiable, sulfate-bearing, corrosive)
7. Determines ASCE 7 Site Class (A–F) with the explicit basis (V̄s, N̄, S̄u, or field judgement); records when a Site Class F assumption forces a site-specific response analysis

**Phase 5: Conclusions and Recommendations**
8. Drafts foundation recommendations across all applicable systems: shallow spread / strip / mat foundations (allowable / factored bearing, minimum embedment, frost / temperature considerations, settlement estimate with method cited, footing-on-fill criteria), deep foundations (drilled shaft / micropile / driven-pile axial and lateral capacity, downdrag, group effects), and ground-improvement options (over-excavation and replacement, deep dynamic compaction, stone columns, soil-cement, rigid inclusions) when shallow foundations are not viable
9. Drafts lateral earth pressure recommendations (at-rest, active, passive, seismic increment), retaining-wall design parameters, drainage requirements, slabs-on-grade subgrade and vapor-retarder recommendations, pavement subgrade and section recommendations (asphalt and PCC) with the controlling design method (AASHTO, ME-PDG, agency procedure), and earthwork-and-compaction recommendations (D1557 95% / 98% per element, lift thickness, moisture window, suitable / unsuitable fill criteria, oversize, slope inclinations, surface drainage)
10. Drafts construction-phase considerations: dewatering, temporary excavation and shoring (OSHA 1926 Subpart P soil-type, sloping / benching, shielding / shoring), groundwater control during construction, observation and testing services to be provided by the GER

**Phase 6: Limitations, References, and Packet Assembly**
11. Records ASFE-style limitations (project-specific report; not for re-use; subsurface variations; subsurface variability; report is interpretive; observation services recommended) and design-team-reliance / construction-team-reliance language
12. Builds the appendices: Site / Boring-Location Plan; Boring Logs; Lab Test Results; ASCE 7 Site Class look-up; ASTM standards table; Limitations / Reliance Statement; Symbol Legend (USCS, sampler, groundwater)

## Output

A DRAFT geotechnical investigation report with: cover page, table of contents, sections 1–10 (Project Description; Site & Geology; Field Exploration; Lab Testing; Subsurface Conditions; Seismic Considerations; Conclusions & Recommendations; Construction Considerations; Limitations; References), appendices (site / boring-location plan, boring logs, lab data, ASCE 7 Site Class look-up, ASTM standards table, limitations / reliance statement, symbol legend), and unsigned stamp / seal block — labeled `DRAFT — for Geotechnical Engineer of Record review, stamp, and seal`.

## Notes

This skill never issues a stamped or sealed report, never determines code compliance (only a licensed GER stamping the report does), never invents soil descriptions, lab values, SPT N-values, groundwater observations, or any boring-log content, and never recommends a foundation system without the field and lab data to support the recommendation. The skill flags every data gap (e.g., no groundwater observation at completion, no Atterberg limits on fine-grained samples) and surfaces it in the limitations section. Seismic site class beyond field judgement requires an explicit V̄s, N̄, or S̄u basis; where the basis is unavailable, the report flags the assumption and recommends a confirmatory measurement.

It treats subsurface data, boring logs, lab data, and proposed-loading information as confidential project work product. It does not paste owner identifiers, parcel-specific findings, or confidential design loads into examples or external lookups. It does not transmit project data to any service the user has not authorized.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
