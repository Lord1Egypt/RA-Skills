# Commercial Appraisal Narrative Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Real-Property Appraisal

## Purpose

Drafts a USPAP 2026–2027 (effective January 1, 2026) narrative appraisal report for an income-producing commercial real-property assignment. Covers engagement intake, subject identification, inspection log, market and neighborhood analysis, highest-and-best-use four-tests analysis (as-vacant and as-improved), the three approaches to value (Sales Comparison, Income Capitalization with direct capitalization and DCF, Cost — or an explicit exclusion justification), reconciliation of value indications, final value opinion, USPAP-compliant certification, assumptions and limiting conditions, and an addenda package.

**The output is always DRAFT.** A state-Certified General appraiser (or the assignment's signing appraiser of equivalent license class) must verify every comparable, adjustment, capitalization rate, discount rate, market-rent comparable, expense comparable, depreciation deduction, and reconciliation, and the appraiser must personally sign the certification before the report is delivered to the client or any intended user.

## When to Use

- A state-Certified General appraiser is preparing a narrative appraisal report for an income-producing commercial property (office, retail, industrial, multifamily 5+ units, mixed-use, self-storage, hospitality, special-purpose)
- A junior appraiser or trainee is drafting a narrative report under the direct supervision of a state-Certified General appraiser
- A review appraiser is evaluating a third-party narrative report for USPAP compliance and reconciling its conclusions with file evidence
- A lender, special servicer, or counsel needs a USPAP-compliant narrative skeleton for an assignment that will be assigned to an external appraiser
- An assignment requires both an as-is value and a prospective value upon completion of construction or stabilization, and the workflow must distinguish the two effective dates

## What It Does

**Phase 1: Engagement Intake**
1. Captures the client and the intended user(s), the intended use of the report, the type of value (market value, market value subject to extraordinary assumptions, prospective market value upon completion, prospective market value upon stabilization, liquidation value, disposition value, insurable value), the effective date(s) of value, the date of report, the property rights appraised (fee simple, leased fee, leasehold), and any jurisdictional exception or hypothetical condition
2. Defines the scope of work consistent with the USPAP Scope of Work Rule — the extent of property inspection, the extent of research, the approaches considered and applied, and the rationale for any approach excluded

**Phase 2: Property and Market Context**
3. Identifies the subject: street address, legal description, parcel ID(s), site dimensions, zoning, building dimensions, year built, gross / rentable / leasable / usable area, parking, current occupancy, current rent roll summary
4. Tabulates the three-year prior-sales history and any current listing or option contract, per USPAP Standards Rule 1-5
5. Builds a market and neighborhood analysis: regional / metropolitan / submarket; demographic and economic drivers; supply and demand for the property type; vacancy, absorption, rent, sale-price trends; and a sub-market conclusion that supports the Highest-and-Best-Use analysis

**Phase 3: Highest-and-Best-Use Analysis**
6. Runs the four-tests highest-and-best-use analysis (legally permissible, physically possible, financially feasible, maximally productive) twice — **as-vacant** and **as-improved** — and reconciles them. Where the conclusions differ, names the implication for the value opinion.

**Phase 4: Approaches to Value**
7. **Sales Comparison Approach.** Selects comparable sales; tabulates each comp's transaction details (sale date, price, financing terms, conditions of sale, market conditions, expenditures after purchase, physical characteristics, location, use); builds the adjustment grid (sale-price adjustments by element, sequence per USPAP-aligned standard); applies the adjustments; reconciles to a value indication with a rationale that names the most-similar comp(s)
8. **Income Capitalization Approach — Direct Capitalization.** Builds the pro-forma income statement: potential gross income (PGI) by lease, vacancy and collection loss (V&C), other income, effective gross income (EGI), operating expenses (with each expense reconciled to comparables or market norms), reserves for replacement (where required), net operating income (NOI). Selects the overall capitalization rate (OAR) with the comp-sale-derived, debt-coverage-ratio (DCR / band-of-investment), or surveyed-rate basis. Reports the capitalized value indication
9. **Income Capitalization Approach — DCF.** Builds the lease-by-lease rollover schedule with rent steps, market-rent on rollover, downtime, tenant-improvement allowance, leasing commissions, free rent, expense growth, capital reserve, V&C, terminal-year NOI, terminal capitalization rate, transaction costs, present-value discount rate, IRR, and NPV. States the source of every input (lease abstract, market rent comp, V&C survey, OpEx comp, broker survey, RERC / PwC / Situs cap-rate survey, capital-market-derived discount rate)
10. **Cost Approach.** Estimates site value (using the Sales Comparison Approach, allocation, extraction, ground-rent capitalization, subdivision-development, or land-residual technique — naming which); estimates reproduction or replacement cost new (RCN) using a stated source (Marshall & Swift, RSMeans, RLB, builder cost, or other); deducts physical, functional, and external depreciation by source; adds site improvements at depreciated cost; computes the indicated value
11. **If an approach is excluded**, drafts the Standards-Rule 2-2(a)(viii) exclusion justification per USPAP — what approach was considered, why it was not necessary for credible results, and the basis for excluding it

**Phase 5: Reconciliation and Final Value**
12. Reconciles the value indications from each applied approach with explicit weight or qualitative emphasis on the approach most reflective of buyer behavior for the property type. States the reconciled value indication, the rounded value opinion, and any extraordinary assumption or hypothetical condition affecting the value

**Phase 6: Certification, Assumptions, Addenda**
13. Drafts the USPAP-compliant certification (paraphrased to reflect the assignment) and the appraiser's signature block — UNSIGNED in the DRAFT — including the appraiser's state-Certified General license number (or trainee under a supervisor) and a contributing-appraiser disclosure where applicable
14. Drafts the Assumptions and Limiting Conditions section and the Extraordinary Assumptions / Hypothetical Conditions list per USPAP Standards Rule 2-2(a)
15. Builds the addenda: subject photos, comparable-sale photos, location map, plat / survey, zoning map, flood map, rent roll / lease abstracts, three-year operating statements, market rent comparables, comparable-sale data sheets, contract / listing / option (where applicable), engagement letter, and the signing appraiser's qualifications and license

## Output

A DRAFT USPAP 2026–2027 narrative appraisal report with: letter of transmittal; table of contents; certification block (unsigned); summary of salient facts and conclusions; assumptions and limiting conditions; extraordinary assumptions / hypothetical conditions; scope of work; property identification and rights appraised; three-year sales-history disclosure; market and neighborhood analysis; site description; improvements description; highest-and-best-use analysis (as-vacant and as-improved); Sales Comparison Approach; Income Capitalization Approach (direct capitalization and DCF); Cost Approach (or Standards-Rule 2-2(a)(viii) exclusion justification); reconciliation of value indications; final value opinion (with rounding rationale); addenda — labeled `DRAFT — for state-Certified General appraiser review, certification, and signature`.

## Notes

This skill never issues a signed appraisal report, never affirms a value opinion without the signing appraiser's verification, and never blends two property-rights bases (fee simple vs. leased fee) silently. The skill always distinguishes between Hypothetical Conditions (assumed facts contrary to known facts) and Extraordinary Assumptions (assumed facts the appraiser does not know but believes plausible). The skill always cross-checks Standards Rule 1-5 (prior-sales-and-listing disclosure for the prior three years) and Standards Rule 2-2(a)(viii) (exclusion justification when an approach is not applied).

It treats subject identifiers, rent rolls, lease abstracts, operating statements, client identity, intended-user identity, and client-confidential information as confidential assignment work product. It does not paste subject addresses, owner identities, transaction terms, or rent / expense data into examples or external lookups. It does not transmit assignment data to any service the user has not authorized.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
