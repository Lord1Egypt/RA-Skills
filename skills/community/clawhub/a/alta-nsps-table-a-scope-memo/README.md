# ALTA/NSPS Table A Scope Memo

**Platforms:** Claude · Openclaw · Codex
**Domain:** U.S. Land Surveying — ALTA/NSPS Land Title Surveys (2026 standards, effective 2026-02-23)

## Purpose

A scope-setting partner for licensed Professional Land Surveyors (PLS), title-company underwriters, lender counsel, commercial real-estate attorneys, and developer project managers commissioning a **2026 ALTA/NSPS Land Title Survey** under the **Minimum Standard Detail Requirements for ALTA/NSPS Land Title Surveys** adopted by the American Land Title Association (ALTA) and the National Society of Professional Surveyors (NSPS), effective **February 23, 2026**. Produces a **scope-of-services memo** that pins down the Table A selections, state-mandatory items, written-agreement provisions (notably **Item 15**), fee-impact notes, and follow-up questions for the client, lender, and title insurer **before site work begins** — so the survey delivered matches the survey the lender, title insurer, and buyer actually need.

## When to Use

- Commissioning an ALTA/NSPS Land Title Survey for an acquisition, refinance, construction loan, development, ground lease, or 1031 exchange
- Confirming Table A item selections **before** the PLS mobilizes a field crew and incurs cost
- Bridging the 2026 edition's changes against an older request form, lender survey-requirements memo, or title-company "preferred Table A" template
- Reconciling state-statute / administrative-rule **mandatory items** (e.g., monumentation under Item 1 in states where it is statutorily required) with the lender's negotiated list
- Drafting the **Item 15** written-agreement language among surveyor, client, lender, and title insurer for items with limitations / preconditions
- Producing the **client / lender / title-insurer follow-up question set** the surveyor must clear before fieldwork

## What It Does

**Phase 1: Transaction and property posture**
1. Captures property address, county, state, parcel ID(s), parcel count, gross area, approximate boundary length, anticipated easements, current improvements, and intended improvements
2. Captures transaction type — acquisition, refinance, construction loan, development, ground lease, 1031, fund-level acquisition, REIT acquisition, portfolio refinance
3. Captures the parties — buyer / borrower, seller (if any), lender, title-insurance underwriter, title agent, owner's-policy beneficiary, lender's-policy beneficiary
4. Confirms the **survey will be certified as a "2026 ALTA/NSPS Land Title Survey"** — older editions are not the current standard

**Phase 2: Title-record intake**
5. Captures the most recent **title commitment** Schedule A legal description and Schedule B-II exceptions (easements, restrictive covenants, encroachments, leases, rights-of-way) — exception by exception
6. Identifies adjoining-record-owner research need (per current standard)
7. Captures lender's and title-insurer's specific survey requirements (lender memo, underwriter checklist, special endorsements such as ALTA 9, 17, 18, 19, 22, 25, 28-series)

**Phase 3: Table A item-by-item selection**
8. Walks Table A items **1 through 20** in order with the user (selected / not selected / state-mandatory / negotiated wording) and records:
   - Why selected (lender, title-insurer endorsement requirement, owner request, state law)
   - Why not selected (cost, not material to transaction, deferred to a separate study)
   - State-mandatory status (if any) — e.g., monumentation under Item 1 is statutorily required in many states and is therefore not optional
   - Special wording or scope-limitation requested
   - Fee impact estimate (relative — `+`, `++`, `+++`)
9. Captures any **negotiated additional item** as **21(a), 21(b), 21(c)…** with explicit wording (Table A standard practice — additional items beyond the first 20 are numbered 21(a), 21(b), etc., with negotiated wording explained)
10. **Item 15** triggers the **written-agreement requirement** among surveyor, client, lender, and title insurer: the skill produces a written-agreement boilerplate and a face-of-plat notes block; if the parties cannot agree, the skill flags Item 15 as **not deliverable**

**Phase 4: Deliverables and certifications**
11. Captures deliverables — number of signed/sealed prints, electronic format(s), CAD format (DWG / DGN), GIS format (Shapefile / GeoJSON), georeferencing CRS (state-plane / UTM / project-defined), legal-description Word document, ASCII coordinate file
12. Captures certification block — exact certificate language is fixed by the 2026 Standards; the certificate **only** lists parties who are entitled to rely on the survey (buyer / lender / title insurer / agent / others named pre-fieldwork)
13. Captures field-data, mapping, and report due dates and the relationship between survey closing and transaction closing

**Phase 5: Pre-fieldwork follow-up question set**
14. Generates the follow-up question set the PLS must clear before mobilization — open Schedule B-II questions, ambiguous easement language, lender endorsement specifics, state-mandatory items, Item 15 written-agreement signatures, certification party list, and access / right-of-entry logistics

**Phase 6: 2026-edition compliance audit**
15. Runs a compliance audit that the scope memo:
   - Names the standard as "2026 ALTA/NSPS Land Title Survey" (not 2021 or older)
   - Accommodates 2026-edition changes to Table A wording, definitions, documentation, fieldwork standards, and reporting
   - Captures state-mandatory items as **not optional** in states that mandate them
   - Identifies Item 15 written-agreement requirement when Item 15 is selected
   - Identifies certification parties **before** fieldwork (post-fieldwork addition of certification parties is not permitted by the Standards)

## Output

A scope-of-services memo with:

- Transaction-and-property summary
- Standard-edition confirmation ("2026 ALTA/NSPS Land Title Survey")
- Table A item-by-item selection table (Item 1 through 20 + any negotiated 21(a)..(n))
- State-mandatory items flagged
- Item 15 written-agreement boilerplate (when selected)
- Deliverables and CRS table
- Certification party list (pre-fieldwork)
- Schedule B-II exception-by-exception treatment
- Lender / title-insurer endorsement crosswalk (ALTA 9 / 17 / 18 / 19 / 22 / 25 / 28-series)
- Fee-impact summary (relative)
- Pre-fieldwork follow-up question set
- 2026-edition compliance audit
- PLS sign-off block

## Safety

This skill drafts a scope memo, **not** the survey itself. Every output is labeled **DRAFT — LICENSED PROFESSIONAL LAND SURVEYOR (PLS) MUST REVIEW AND SIGN BEFORE FIELDWORK**. The skill never issues, signs, seals, or certifies a survey, never represents to a lender or title insurer that fieldwork has occurred, and never alters a legal description. The skill defers to the licensed PLS on professional judgment, fieldwork procedure, and state-specific monumentation, recordation, and licensure rules. The certification block is governed by the current Standards and lists only parties identified **before** fieldwork; the skill flags any attempt to add certification parties post-fieldwork. The skill does not modify title-commitment Schedule A or B language; it scopes how the surveyor will treat each exception on the face of the plat.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
