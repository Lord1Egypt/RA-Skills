# Crop Nutrient Management Plan

**Domain:** Agriculture · Agronomy & Conservation Planning
**Platforms:** Claude · Codex

## Purpose

Drafts a field-by-field **Nutrient Management Plan (NMP)** aligned to **NRCS Conservation Practice Standard 590** and the **4R Nutrient Stewardship** framework (Right Source, Right Rate, Right Time, Right Placement). The plan covers operation and field inventory, crop rotation, realistic yield goals, soil-test and manure-analysis interpretation, per-field nutrient budgets for N / P₂O₅ / K₂O with cited credits, the state P-Index or P-threshold result (where regulatory), 4R application decisions with setbacks, a recordkeeping log template, and a contingency adjustment table.

The output is always labeled **DRAFT — CCA / NRCS TSP / STATE-APPROVED PLANNER REVIEW AND SIGN-OFF REQUIRED** and is not a signed or submitted plan.

## When to Use

- A CCA or NRCS-certified TSP preparing a 590-aligned plan for CSP or EQIP
- A state-approved planner drafting under a state nutrient-management law (PA Act 38, MD NM Law, Chesapeake Bay states, Iowa, Wisconsin ATCP 50, Ohio H2Ohio, California ILRP, …)
- An agronomy consultant supporting a CAFO permittee with manure-based plans
- A 4R Plus / 4R Verified record-of-decision drafted for voluntary stewardship reporting
- An agronomic-only (non-regulatory) plan where the operator wants a defensible budget

## What It Does

1. Gates the session on planner role, reviewing planner, plan use (CSP / EQIP / CAFO / state regulation / 4R / agronomic-only), state, and LGU recommendation system
2. Walks one-question-at-a-time intake of operation, fields, rotation, yield goal, soil tests, manure / biosolids analyses, commercial fertilizer plan, sensitive-area features, conservation practices in place, state P-Index method, and recordkeeping format
3. Confirms a scope summary with the planner before drafting
4. Builds a per-field × year **Nutrient Budget** for N, P₂O₅, and K₂O with cited LGU crop-demand recommendations, soil-test credits, manure first-year-available coefficients, legume credits, and residual credits
5. Runs the **state P-Index or P-threshold** rule and outputs a P-Risk Table when the plan use is regulatory
6. Builds a **4R Application Plan** with Right Source / Right Rate / Right Time / Right Placement and a per-field setbacks block
7. Outputs a **Recordkeeping Log template** and a **Contingency Adjustment Table** for in-season deviations
8. Runs a gap and accuracy check (state supplement cited, LGU recs cited, soil-test method, soil-test validity, manure-analysis recency, realistic yield goal, P-based vs N-based, application-condition restrictions, sensitive-area setbacks, draft labeling) and appends an Unresolved Information list

## Notes

This skill produces a **DRAFT NMP**, not a signed plan. It does **not** certify CSP / EQIP / CAFO / state-program compliance, **does not** opine on permitting, and **does not** include pesticide / herbicide / restricted-use product recommendations.

State 590 supplements, LGU recommendations, and P-Index / P-threshold rules vary substantially. The skill cites them when the planner supplies them and flags them as Unresolved when they are not. Soil-test interpretation depends on the method (Bray-P1 / Mehlich-3 / Olsen for P; NH₄OAc / Mehlich-3 for K); cross-method substitution is forbidden.

No producer name, farm name, parcel ID, GPS coordinate, address, FSA tract / farm / field number, or NPDES permit number should be pasted into intake. Use an operation codename.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
