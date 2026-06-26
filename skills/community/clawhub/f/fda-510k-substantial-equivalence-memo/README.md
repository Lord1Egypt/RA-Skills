# FDA 510(k) Substantial Equivalence Memo

**Platforms:** Claude · Openclaw · Codex
**Domain:** Medical-Device Regulatory Affairs — FDA 510(k) Premarket Notification

## Purpose

A drafting partner for regulatory-affairs specialists, RA managers, quality-systems teams, and consulting submission writers preparing the **Section 10 Substantial Equivalence (SE) Comparison** for a U.S. FDA **510(k)** premarket notification (Traditional, Abbreviated, or Special) under **21 CFR Part 807 Subpart E**. Turns the subject device file, intended-use statement, candidate predicate device(s), and performance data into a structured **SE comparison memo** that satisfies the FDA CDRH "**510(k) Program: Evaluating Substantial Equivalence in Premarket Notifications [510(k)]**" Decision-Making Flowchart — intended use → technological characteristics → "different questions of safety and effectiveness" (DQSE) → performance-data bridging → SE decision.

## When to Use

- Drafting Section 10 of a Traditional, Abbreviated, or Special 510(k) submission
- Re-drafting an SE comparison after receiving an FDA **Additional Information (AI)** hold letter under 21 CFR § 807.87(l)
- Re-drafting an SE comparison after a **Not Substantially Equivalent (NSE)** determination, with predicate-selection rework
- Selecting and justifying a **primary predicate** (and optional **reference device** for performance data) and avoiding **split-predicate** errors
- Internal RA / QA review of an SE comparison before eSTAR / eCopy submission via the CDRH Portal or CDER / CBER gateway
- Preparing an SE comparison for a **De Novo-to-510(k)** follow-on or a **post-clearance modification** that triggers a new 510(k) under the "Deciding When to Submit a 510(k) for a Change to an Existing Device" guidance

## What It Does

**Phase 1: Submission posture and product profile**
1. Captures submission type (Traditional / Abbreviated / Special), regulation number, product code, review center (CDRH or CBER), classification (Class I / II / III with 510(k) requirement), and any pre-submission (Q-Sub) feedback
2. Captures subject device name, model(s), indications for use, intended use, intended user, intended environment, and intended patient population
3. Captures known FDA-recognized consensus standards, special controls, and applicable mandatory performance-testing guidance (biocompatibility, sterilization, electrical safety, EMC, cybersecurity, software, human factors, MR-compatibility)

**Phase 2: Predicate selection and eligibility**
4. Captures candidate primary predicate(s) — 510(k) number(s), clearance date, product code, regulation, manufacturer, indications for use
5. Audits each candidate for **legally marketed** status (cleared, grandfathered, reclassified, or 513(f)(2) De Novo) and for "**convenience predicate**" red flags
6. Confirms a **single primary predicate** with the same intended use; allows a **reference device** only for performance-data bridging, not for changing the intended-use comparison
7. Blocks **split-predicate** constructions where intended use comes from one predicate and technological characteristics from another

**Phase 3: SE Decision-Making Flowchart**
8. **Step 1 — Intended Use.** Compares the subject IFU to the predicate IFU word-for-word; flags any new indication, new patient population, new anatomy, new disease state, new use environment, new contraindication change as a potential new intended use → NSE risk
9. **Step 2 — Technological Characteristics.** Builds a side-by-side comparison table covering design, materials, energy source / type / output, performance specs, principles of operation, packaging, sterilization method, shelf life, biocompatibility patient-contact category, software level of concern / documentation level, cybersecurity posture, human-factors use scenarios
10. **Step 3 — Different Questions of Safety and Effectiveness (DQSE).** For each technological difference, analyzes whether the difference raises **different** questions of safety and effectiveness; if yes → NSE risk (consider De Novo or PMA); if no → proceeds to Step 4
11. **Step 4 — Performance Data.** Identifies the performance testing needed to demonstrate the subject is **as safe and effective as** the predicate despite the technological differences — bench, biocompatibility, sterilization validation, software V&V, cybersecurity, electrical safety / EMC, animal, clinical (only if needed)
12. Maps each performance-data element to an applicable FDA-recognized consensus standard or device-specific guidance

**Phase 4: Drafting**
13. Drafts Section 10 in the FDA expected order: Subject Device Description → Predicate Device Description → Indications for Use Comparison → Technological Characteristics Comparison Table → DQSE Analysis → Performance Data Summary → SE Conclusion
14. Produces an Indications for Use comparison sub-section that uses the **exact** subject and predicate IFU text (no paraphrase)
15. Produces the Substantial Equivalence Conclusion paragraph in the format FDA reviewers expect

**Phase 5: AI-letter / NSE red-flag audit**
16. Runs a red-flag audit covering convenience predicate, paraphrased IFU, glossed-over technological differences, unsupported "minor difference" claims, missing standard recognition, missing software documentation level, missing cybersecurity per the 2023 omnibus authority, missing biocompatibility per ISO 10993-1 / FDA modified matrix, missing human-factors evaluation
17. Cross-checks against common AI / NSE deficiency patterns from FDA CDRH refuse-to-accept (RTA) checklists and Decision Summary public records

## Output

A DRAFT Section 10 memo packet with:

- Submission posture block (submission type, product code, regulation, center)
- Predicate-eligibility audit (legally marketed status, single primary predicate confirmed, no split predicate, reference device declared and scoped)
- Indications for Use comparison (subject IFU vs predicate IFU — verbatim)
- Technological Characteristics Comparison Table (side-by-side, every meaningful attribute)
- DQSE Analysis (each difference → same / different questions, justified)
- Performance-Data Bridging Plan (test type → standard / guidance → acceptance criterion)
- Substantial Equivalence Conclusion paragraph
- AI-letter / NSE red-flag audit
- RA / QA / clinical / engineering review and sign-off block
- Unresolved-information list

## Safety

This skill drafts a regulatory submission section, **not** a filing. Every output is labeled **DRAFT — RA / QA REVIEW REQUIRED BEFORE FDA SUBMISSION**. The skill never submits to FDA, never logs into eSTAR / CDRH Portal / CDER NextGen / ESG, and never communicates with FDA reviewers. The skill enforces FDA-recognized consensus standards by **number and version** rather than approximations, refuses to fabricate predicate K-numbers, IFU text, or test data, and treats subject-device design and clinical data as confidential under the institution's quality system. The skill flags potential **De Novo** or **PMA** pathways when the SE analysis surfaces a new intended use, a new technological characteristic raising different questions of safety and effectiveness, or a Class III preamendment device with no eligible predicate.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
