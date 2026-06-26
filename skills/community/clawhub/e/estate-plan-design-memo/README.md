# Estate Plan Design Memo

**Platforms:** Claude · Openclaw · Codex
**Domain:** Estate Planning — Trust & Estate Strategy

## Purpose

An estate-plan design partner for licensed estate planning attorneys, trust officers, paralegals, and law students. Turns a structured client intake (family, asset inventory by title, residency, goals, tax posture, existing documents) into a DRAFT *design memo* that recommends the document set, asset-titling and beneficiary-designation moves, fiduciary nominations, and federal / state / GST tax flags — the strategy artifact that comes **before** the will, trust, or POA is drafted.

## When to Use

- Building the strategy memo before an initial design meeting with a new estate planning client
- Re-designing a plan after a major life event (marriage, divorce, birth, death, move to a new state, business sale, inheritance)
- Reviewing an existing plan against a new federal estate-tax exemption, state-inheritance-tax rule, or SECURE Act / SECURE 2.0 beneficiary-designation impact
- Standardizing the design rationale a partner expects to see from an associate before any document drafting starts
- Preparing a client-meeting agenda with the open questions a lawyer must resolve before drafting

## What It Does

**Phase 1: Intake**
1. Captures attorney role, client residency state(s), domicile facts, and any non-US connections
2. Captures family structure: marital status, spouse(s), children (minor, adult, special needs, from prior relationships), grandchildren, dependents, pets, intentional exclusions
3. Captures asset inventory **by title** (sole, JTWROS, tenancy-by-entirety, community-property, trust-titled, beneficiary-designated, business interest) with approximate fair-market value
4. Captures income-tax character of retirement and IRD assets (traditional vs. Roth IRA/401(k), inherited IRA, NUA stock, deferred comp, annuities)
5. Captures goals: control during life, control after death, asset protection, tax minimization, charity, blended-family fairness, special-needs preservation, business succession
6. Captures existing documents and prior gifts (lifetime gift-tax exemption used, GST allocations, 529s, ILITs in force)
7. Restates the facts with **Confirmed / Assumed / Unknown** tags and shows the headline metrics (gross estate, probate vs. non-probate split, state-tax exposure) before recommending anything

**Phase 2: Design**
8. Recommends a **document set** (will-only / pour-over will + revocable trust / SLAT / ILIT / QPRT / GRAT / charitable trust / dynasty trust / special-needs trust / POA / advance directive / HIPAA authorization) tied to the goals and tax posture
9. Recommends **titling and beneficiary-designation** moves to align assets with the plan (retitle, fund the trust, update IRA / 401(k) / life-insurance / TOD / POD beneficiaries, watch SECURE 2.0 10-year rule)
10. Recommends **fiduciary nominations** (executor, successor trustee, guardian, healthcare agent, agent under POA) with successor depth and compensation notes

**Phase 3: Tax flags and risk**
11. Flags federal estate-tax exposure against the current exemption with use-it-or-lose-it sunset alerts
12. Flags GST allocation issues and dynasty-trust eligibility by situs state
13. Flags state estate / inheritance tax exposure (e.g., MA, OR, WA, NY, MN, IL, MD, NJ, PA, CT, RI, VT, HI, ME, DC) by domicile and real-property situs
14. Flags IRD / SECURE 2.0 stretch-loss issues for non-spouse beneficiaries
15. Flags portability / DSUE election needs for surviving spouses

**Phase 4: Output**
16. Produces the DRAFT design memo using the structure in `SKILL.md`
17. Runs the self-check rubric and lists failures back to the attorney
18. Produces an "open questions for client" list — items that must be resolved before drafting begins

## Output

A DRAFT memo with:

- Engagement and disclaimer header (DRAFT — LICENSED ESTATE ATTORNEY MUST REVIEW)
- Client snapshot (family, residency, headline metrics)
- Goals (verbatim from client, ranked)
- Recommended document set with rationale per document
- Asset-titling and beneficiary-designation action table (asset, current title / beneficiary, recommended title / beneficiary, rationale)
- Fiduciary slate (role, primary, successors, compensation note)
- Federal estate, GST, state-tax flags table
- SECURE 2.0 and IRD considerations
- Evidence matrix (every recommendation → fact → source)
- Open questions for client
- Open questions for attorney (research, citations, jurisdictional confirmation)

## Safety

This skill drafts a **design memo for an attorney**, not a final estate plan and not legal advice to the client. Every output is labeled **DRAFT — LICENSED ESTATE ATTORNEY MUST REVIEW**. The skill never drafts will, trust, POA, or directive language; never gives tax advice without the named-attorney's review; never recommends specific investment products or insurance carriers; never executes any document; never opines on the validity of an existing document without attorney review of the original. State-specific rules vary — the skill will name its jurisdictional assumptions and flag every item that requires the attorney to confirm against current state statute and case law. Client personally identifiable information and asset values are treated as confidential and are never written to external services.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
