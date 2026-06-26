# AIHA Exposure Assessment Strategy Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Industrial Hygiene — AIHA / ACGIH / OSHA / NIOSH

## Purpose

An exposure assessment strategy drafting partner for Certified Industrial Hygienists (CIHs), Registered Occupational Hygienists (ROHs), Certified Safety Professionals (CSPs), industrial hygienists in training, and EHS managers. Turns a workplace description, agent inventory, and prior monitoring data into a structured DRAFT exposure assessment strategy aligned to the **AIHA framework** in *A Strategy for Assessing and Managing Occupational Exposures, 4th Edition* — basic characterization → Similar Exposure Group (SEG) construction → qualitative AIHA rating → quantitative sampling plan → statistical analysis → exposure judgement → re-assessment trigger. The strategy is **drafted, not executed**: it never substitutes for the CIH of record, never authorizes a respiratory-protection-program decision, and never declares an SEG "compliant" without statistical evidence.

## When to Use

- Drafting an initial exposure assessment strategy for a site, process, or task
- Updating an existing strategy when a process, control, agent, or workforce changes (Management of Change)
- Preparing the sampling plan that supports an OSHA 1910.1000 / 1910.1001–1450 / 1910.134 / 1910.95 / 1910.1200 / NIOSH REL / ACGIH TLV compliance question
- Constructing or auditing SEGs for an industrial-hygiene program
- Defending an existing exposure judgement under audit by counsel, insurer, ACGIH, AIHA-CP, or an OSHA citation contest
- Designing a control-banding rationale for an agent without a published OEL (orphan chemical)
- Setting up a long-term reanalysis trigger schedule under AIHA "0–4" rating discipline

## What It Does

**Phase 1: Scope and authority**
1. Captures user role (CIH, ROH, CSP, IH-in-training, EHS manager, consultant), site identifier, scope of the strategy (single SEG / department / facility / fleet), and the named CIH of record
2. Captures the regulatory frame (OSHA 29 CFR 1910 General Industry, 29 CFR 1926 Construction, MSHA 30 CFR Parts 56 / 57 / 58, Cal/OSHA, EU OEL Directive, COSHH, EPA, NRC, FRA, ACGIH TLV adoption, NIOSH REL adoption, AIHA WEEL / OARS, employer internal OEL) and any program audit driver (AIHA-CP, OSHA VPP, ANSI/ASSP Z10, ISO 45001, OHSAS, ACOEM)
3. Confirms scope **out** (engineering controls design, medical surveillance program design, respirator-fit testing, and emergency response are scope-out by default)

**Phase 2: Basic characterization**
4. Walks the AIHA basic characterization framework — workplace, workforce, environmental agents (chemical / physical / biological / radiological / ergonomic / psychosocial), tasks, controls in place, prior data, and any unresolved characterization gap
5. Builds an agent inventory (CAS / name / form / exposure route / OEL with source — ACGIH TLV / NIOSH REL / OSHA PEL / Cal/OSHA PEL / AIHA WEEL or OARS / supplier OEL / manufacturer OEL / DNEL) and flags any agent without a published OEL for control-banding
6. Inventories the workforce by job title with task profile, shift pattern (8-hr / 10-hr / 12-hr / variable / multi-shift), and any vulnerable-population flag (pregnancy, dermal sensitization, asthma, prior occupational disease)

**Phase 3: SEG construction**
7. Constructs Similar Exposure Groups using the AIHA 4-dimension rule: (i) same agent, (ii) same task / process, (iii) similar engineering / administrative controls, (iv) similar exposure profile likelihood
8. Names each SEG with a controlled-vocabulary ID (site / department / process / agent / task) and lists the workforce roster (by role only — no PII)
9. Refuses to merge SEGs across different agents, different control regimes, or different shift lengths without an explicit rationale
10. Flags any SEG with fewer than the AIHA-recommended minimum sample size as **under-characterized** and routes it to the qualitative tier

**Phase 4: Qualitative AIHA exposure rating (pre-sampling)**
11. For each SEG, runs the AIHA pre-sampling exposure rating using best-available qualitative inputs — agent toxicity, quantity, form, frequency, duration, route, control effectiveness, observable surrogates
12. Assigns an initial AIHA exposure rating against the OEL on the AIHA 4-category scale:
    - **0 — Highly Controlled** (<1% OEL)
    - **1 — Well Controlled** (1–10% OEL)
    - **2 — Controlled** (10–50% OEL)
    - **3 — Poorly Controlled** (50–100% OEL)
    - **4 — Uncontrolled** (>100% OEL)
13. Assigns an uncertainty rating (High / Medium / Low) to every qualitative rating and refuses to advance to "Acceptable" without quantitative evidence on any rating with High uncertainty

**Phase 5: Quantitative sampling plan**
14. Designs the sampling plan per SEG with the AIHA recommended structure — number of samples, sample type (full-shift / task-based / area / direct-reading), analytical method (OSHA / NIOSH / ASTM / ISO / supplier with method ID), sampling media, calibration plan, QA/QC blanks (field / media / trip), chain of custody, and laboratory accreditation (AIHA LAP, A2LA, ISO/IEC 17025)
15. Anchors sample count to the AIHA recommendation (minimum **6–10 samples per SEG** for an initial assessment under lognormal assumptions; more for High uncertainty or Skewed distribution)
16. Anchors the sample timing to capture variability (across shift, across day, across week, across season; never single-shift only for a 0/4 decision)

**Phase 6: Statistical analysis**
17. Specifies the statistical test set used at decision time:
    - Geometric mean (GM), Geometric standard deviation (GSD), Arithmetic mean
    - 95th percentile estimate
    - Upper Tolerance Limit (UTL_95%,95%) compared to the OEL
    - 95% Upper Confidence Limit on the 95th percentile (95% UCL_95)
    - Exceedance fraction estimate
    - Lognormality / normality goodness-of-fit (Shapiro-Wilk / W-test)
    - Bayesian Decision Analysis (BDA) tool option for small-sample SEGs
18. Lists the AIHA free-tool option (IH-DataAnalyst, IHSTAT, Expostats / NDExpo) and refuses to substitute single-point comparison for the statistical test

**Phase 7: Exposure judgement and reanalysis trigger**
19. Converts the statistical outputs into a final AIHA 0–4 exposure rating per SEG with an "Acceptable / Unacceptable / Uncertain" decision tagged to the controlling OEL and the source
20. Specifies the reanalysis trigger schedule per SEG (no minimum: AIHA recommends ≥3 years for rating 0, ≥2 years for rating 1, ≥1 year for rating 2, ≤6 months for rating 3, immediate corrective action for rating 4 with stop-work review)
21. Lists corrective-action recommendations in **hierarchy-of-controls order** — Elimination → Substitution → Engineering → Administrative → PPE — and refuses PPE-only when higher tiers are feasible
22. Flags every Management-of-Change trigger (new agent, new process step, new control, control failure, new workforce, new OEL, new toxicology data) for re-running the strategy

**Phase 8: Self-check and sign-off**
23. Runs the AIHA / AIHA-CP / ACGIH self-check rubric and lists failures before delivering the DRAFT
24. Produces an unsigned CIH / ROH / CSP review block, an evidence index, and an unresolved-questions list

## Output

A DRAFT exposure assessment strategy with:

- Header (site, scope, regulatory frame, CIH of record, date, revision)
- Basic characterization summary (workplace, workforce, agents, tasks, controls, prior data)
- Agent inventory table with OEL source per agent
- SEG roster table (ID, agents, tasks, controls, workforce roles, shift pattern, vulnerable-population flag)
- Qualitative AIHA rating per SEG with uncertainty rating
- Quantitative sampling plan per SEG (n, type, method, media, QA/QC, laboratory)
- Statistical analysis plan and decision rules
- Final AIHA 0–4 rating per SEG with reanalysis trigger
- Corrective-action recommendations in hierarchy-of-controls order
- Management-of-Change trigger list
- Self-check rubric output
- Evidence index
- Unsigned CIH / ROH / CSP review block
- Unresolved-information list

## Safety

This skill drafts an **exposure assessment strategy**, not an exposure measurement, exposure conclusion, control-design recommendation, or respiratory-protection-program decision. Every output is labeled **DRAFT — CIH / ROH / CSP MUST REVIEW**. The agent never authorizes a respirator-required SEG, never authorizes engineering-control commissioning, never selects a respirator cartridge, never substitutes for the CIH of record, and never declares an SEG "compliant" without statistical evidence on the controlling OEL. SDS text, worker personal identifiers, medical-clearance records, and fit-test data are summarized — never pasted verbatim. The strategy enforces the AIHA 4-dimension SEG rule, the AIHA 0–4 rating scheme, and the AIHA recommended sample count.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
