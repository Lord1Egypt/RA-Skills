# GHG Corporate Inventory Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Carbon Accounting — GHG Protocol / CSRD ESRS E1 / IFRS S2 / SBTi / CDP

## Purpose

A corporate GHG inventory drafting partner for sustainability leads, ESG analysts, climate-disclosure officers, environmental managers, and CFO-office reporting staff. Turns the legal-entity structure, energy bills, fleet data, refrigerant logs, supplier spend, and value-chain activity into a structured DRAFT GHG inventory aligned to:

- **GHG Protocol Corporate Accounting and Reporting Standard** (Revised Edition, WBCSD / WRI)
- **GHG Protocol Corporate Value Chain (Scope 3) Standard**
- **GHG Protocol Scope 2 Guidance** (location-based + market-based dual reporting; 2026 consultation update tracked)
- **IPCC AR6 GWP100** values (with the AR5 / AR4 prior-period flag where applicable)
- **CSRD ESRS E1** (Climate Change), **IFRS S2** (ISSB), **SBTi** target validation, **CDP** Climate Change disclosure, **SEC Climate Rule** (where in force / partially stayed), **TCFD** legacy frame
- **EU Omnibus** Wave-1 / Wave-2 timeline expectations as of the 2026 reporting cycle

## When to Use

- Building a first-time corporate GHG inventory for a single reporting year
- Updating a recurring annual inventory with a documented base-year recalculation policy
- Preparing the GHG inventory underpinning CSRD ESRS E1, IFRS S2, SBTi target validation, CDP submission, SEC climate disclosure, or PCAF financed-emissions reporting
- Recalculating a base year after a structural change (acquisition, divestiture, outsourcing / insourcing, methodology change, error correction)
- Producing the assurance-ready packet for a limited or reasonable-assurance engagement (ISAE 3410, ISAE 3000)
- Drafting the Scope 3 screening rationale to defend "immaterial" exclusions to assurance providers, SBTi, and CDP scorers

## What It Does

**Phase 1: Scope and reporting frame**
1. Captures user role (sustainability lead, ESG analyst, climate-disclosure officer, environmental manager, controller, treasurer, ERM lead), reporting entity, reporting year, and currency
2. Captures every disclosure surface the inventory must serve (CSRD ESRS E1, IFRS S2, SBTi target validation, CDP, SEC climate rule, TCFD legacy, voluntary report, PCAF financed-emissions, supplier RFI)
3. Confirms scope OUT (no assurance provided by this skill; no net-zero claim made; no offset / carbon-credit retirement decision; no internal-carbon-price calibration)

**Phase 2: Consolidation approach + boundaries**
4. Walks the GHG Protocol consolidation choice: **equity-share** vs **financial control** vs **operational control** — with the rationale for the chosen approach and the implication for joint ventures, leased assets, franchises, and minority interests
5. Defines organizational boundary (entity list with ownership / control / lease structure) and operational boundary (facilities, fleet, IT, leased real estate, contracted manufacturing)
6. Builds the base-year and base-year recalculation policy with structural-change triggers (acquisition / divestiture / outsourcing / insourcing / methodology change / error correction) and a "significance threshold" (default ≥5% of total emissions; configurable)

**Phase 3: Scope 1 (direct emissions)**
7. Builds the Scope 1 inventory across stationary combustion (boilers, generators, CHP, furnaces), mobile combustion (fleet, off-road, marine, rail, aviation), fugitive (refrigerants per Kigali Amendment HFCs, SF6, CH4 leaks, fire-suppression), process emissions (industrial-process category per IPCC 2006 / 2019 refinement), and biogenic CO2 (reported separately, not added to gross Scope 1)
8. Anchors every Scope 1 line to activity data (units, source), an emission factor with named source (EPA EFs, Defra / DESNZ, IEA, IPCC AR6 GWP100, supplier-specific), and a data-quality tier
9. Treats refrigerants by GWP100 from IPCC AR6 (default) with the prior-edition GWP flag where required

**Phase 4: Scope 2 (purchased energy)**
10. Builds Scope 2 dual reporting: **location-based** (using the grid-average emission factor — eGRID, IEA, AIB / European Residual Mix, country-specific) and **market-based** (using contractual instruments — RECs, GOs, EACs, PPAs, supplier-specific factors)
11. Refuses to report market-based Scope 2 without the Scope 2 Quality Criteria (instrument tracking, vintage, geography matching, exclusive claim, residual mix for the unbacked portion)
12. Captures the contractual-instrument register (REC / GO / EAC / PPA / VPPA) with vintage, geography, MWh, and retirement record
13. Captures purchased steam / heat / cooling separately with the supplier-specific factor

**Phase 5: Scope 3 (value-chain emissions) — 15-category screening**
14. Runs the 15-category Scope 3 screen with the GHG Protocol decision tree per category:

    - **Upstream:**
      1. Purchased goods and services
      2. Capital goods
      3. Fuel- and energy-related activities not included in Scope 1 or 2 (WTT, T&D losses, fuel-supply-chain)
      4. Upstream transportation and distribution
      5. Waste generated in operations
      6. Business travel
      7. Employee commuting (including remote-work where material)
      8. Upstream leased assets

    - **Downstream:**
      9. Downstream transportation and distribution
      10. Processing of sold products
      11. Use of sold products (including the **expected-lifetime use phase** — direct-use for energy-using products; indirect-use for inputs)
      12. End-of-life treatment of sold products
      13. Downstream leased assets
      14. Franchises
      15. Investments (financed emissions per PCAF where applicable)

15. For each category, documents an **inclusion / exclusion / immateriality** decision with a quantitative justification (default screen: any category > 5% of total emissions is included; ≤5% may be excluded with a documented spend / activity-screen estimate)
16. Refuses "immaterial — out of scope" without a quantitative screen
17. Anchors each included category to a calculation method (**spend-based**, **average-data**, **hybrid**, or **supplier-specific**) per the Scope 3 *Technical Guidance for Calculating Scope 3 Emissions*

**Phase 6: GWP, biogenic, removals, and offsets**
18. Locks GWP source (IPCC AR6 GWP100 default; AR5 / AR4 only when the prior period was reported under that edition and a recalculation is not yet due)
19. Reports biogenic CO2 separately (not added to gross Scope 1)
20. Reports removals (biogenic sequestration, geological CCS, BECCS, DAC) separately with permanence rating and the **gross emissions / removals / net** triplet
21. Treats offsets / carbon credits as **outside the inventory** — never netted into Scope 1 / 2 / 3; only reported in a separate offset register with project ID, vintage, registry (Verra, Gold Standard, CDM, ART TREES, ACR, CAR), and retirement record

**Phase 7: Data-quality matrix**
22. Builds a data-quality matrix per category with the GHG Protocol pedigree-matrix dimensions: **technology**, **temporal**, **geographical**, **completeness**, **reliability** — scored 1 (best) to 5 (worst); aggregate uncertainty estimate per category and total

**Phase 8: Restatements and comparatives**
23. Applies the recalculation policy to all prior-period comparatives where a structural-change trigger fires, and produces a restated comparatives table with the change description, magnitude, and rationale
24. Flags every restatement for assurance review

**Phase 9: Disclosure-surface alignment**
25. Maps the inventory line-by-line to:
    - **ESRS E1-6** disclosure requirements (gross Scope 1, gross Scope 2 location-based and market-based, gross Scope 3 by category, total gross)
    - **IFRS S2** climate-related disclosures
    - **SBTi** target-setting baseline requirements (1.5°C alignment, 40% Scope 3 trigger, FLAG sector overlay, near-term + long-term targets, BVCM commitment)
    - **CDP** Climate Change 2026 scorecard line items
    - **SEC climate rule** (where in force / partially stayed; flag the stay status)
26. Lists every reconciliation difference between the GHG Protocol inventory and the financial perimeter (consolidation differences, equity-method differences, partial-year acquisitions) for the controller's tie-out

**Phase 10: Assurance-readiness self-check + sign-off**
27. Runs the assurance-readiness self-check (ISAE 3410, ISAE 3000) and lists failures before delivering the DRAFT
28. Produces an unsigned reporting-officer + assurance-provider review block, an evidence index, and an unresolved-questions list

## Output

A DRAFT corporate GHG inventory packet with:

- Header (reporting entity, reporting year, currency, consolidation approach, organizational and operational boundary, base-year, recalculation policy)
- Scope 1 table (stationary, mobile, fugitive, process, biogenic — separated)
- Scope 2 dual table (location-based + market-based + contractual-instrument register)
- Scope 3 15-category table with inclusion / exclusion / immateriality justification and method
- Removals register (separate from inventory)
- Offset register (separate from inventory)
- Data-quality matrix per category with pedigree dimensions and aggregate uncertainty
- Restated comparatives table
- Disclosure-surface alignment matrix (ESRS E1-6, IFRS S2, SBTi, CDP, SEC)
- Reconciliation to financial perimeter
- Assurance-readiness self-check output
- Evidence index (every activity-data row to source document and emission-factor source)
- Unsigned reporting-officer + assurance-provider review block
- Unresolved-information list

## Safety

This skill drafts a **GHG inventory**, not an assured statement, a net-zero claim, an SBTi-validated target, a CDP score, an ESRS E1 audited disclosure, or an SEC filing. Every output is labeled **DRAFT — REPORTING OFFICER + ASSURANCE PROVIDER MUST REVIEW**. The agent never adopts an emission factor without a named source, never substitutes spend-based for activity-based where activity data is available without flagging the trade-off, never nets offsets into Scope 1 / 2 / 3, never makes a net-zero claim, and never substitutes for an assurance engagement. Personally identifiable employee data (commute mode, home address, individual travel records) and supplier confidential data are summarized — never pasted verbatim. The inventory enforces the GHG Protocol Scope 2 dual-reporting rule, the Scope 3 15-category screen, and the IPCC AR6 GWP100 default.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
