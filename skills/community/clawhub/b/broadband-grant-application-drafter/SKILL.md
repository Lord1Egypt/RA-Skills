---
name: broadband-grant-application-drafter
description: >
  Use this skill when an ISP, rural electric cooperative, municipality, tribal
  organization, or broadband office needs to draft a grant application narrative
  for federal or state broadband funding programs including BEAD, USDA ReConnect,
  E-Rate, or state broadband grant programs. Covers service area definition,
  technology selection, deployment plan, cost structure, and affordability plan.
  Produces a DRAFT narrative for applicant and legal review before submission.
---

# Broadband Grant Application Drafter

Converts project facts — applicant information, service area, technology choice, deployment timeline, and cost estimates — into a structured grant application narrative for federal and state broadband funding programs. Outputs a DRAFT for applicant, engineering, and legal counsel review before submission.

## Flow

Ask one question at a time. Wait for the user's answer before moving to the next step.

### Step 1 — Program Identification

Ask:
- Which grant program is this application for? (e.g., BEAD, USDA ReConnect Round 4+, E-Rate, FCC Emergency Connectivity Fund, state broadband office program — specify state and program name)
- What is the application deadline?
- Is this a subgrantee application (to a state broadband office) or a direct federal application?

Look up the program's key eligibility requirements based on the user's answer and state them explicitly before proceeding. Flag any eligibility questions that the applicant must confirm:
- **BEAD:** Applicants must be ISPs, utilities, cooperatives, local governments, or non-profits; fiber is the default technology; locations served must be confirmed unserved or underserved per the NTIA Fabric
- **ReConnect:** Applicants must be entities providing service to rural areas with fewer than 400,000 people that are currently unserved (less than 25/3 Mbps or no service)
- **E-Rate:** Applicants must be eligible schools or libraries; funding is for connectivity and equipment, not infrastructure build-out

### Step 2 — Applicant Profile

Collect:
- Legal entity name and type (ISP, co-op, municipality, tribal government, non-profit, etc.)
- State of incorporation / organization
- FCC Registration Number (FRN) and SAM.gov registration status
- Years of broadband deployment experience and any prior federal or state broadband grants received
- Current service territory (states and counties served)

### Step 3 — Service Area Definition

Collect:
- Geographic area to be served (county, census tracts, or specific communities — name and state)
- Number of locations to be served (locations, not households; BEAD uses the NTIA Fabric definition)
- Confirmation of unserved / underserved status for the proposed locations:
  - Source used (NTIA Fabric, FCC National Broadband Map, state challenge data, or independent survey)
  - Current maximum download/upload speeds available at these locations
- Any anchor institutions in the service area (schools, libraries, healthcare facilities, public safety)

If the applicant has not confirmed unserved/underserved status against program-required data sources, flag this as a **prerequisite that must be resolved before drafting the application narrative**.

### Step 4 — Technology Selection

Collect:
- Proposed technology (fiber-to-the-premises FTTP, fixed wireless access FWA, hybrid fiber-wireless, cable, other)
- Planned download / upload speeds to be delivered (must meet program minimums — confirm against the program identified in Step 1)
- Scalability: can the network be upgraded to 1 Gbps / 1 Gbps symmetric without replacing the core infrastructure?
- Last-mile topology and middle-mile access plan

For BEAD applications: confirm that fiber is proposed or document the specific technical justification for an alternative technology under the program's exception process.

### Step 5 — Deployment Plan

Collect:
- Phase structure: how many deployment phases, what geography per phase, and why this sequencing
- Milestone schedule: key milestones with estimated dates (engineering complete, permits obtained, construction start, service activation, project closeout)
- Permitting strategy: make-ready process, pole attachment, ROW coordination, tribal land considerations
- Workforce plan: in-house versus contracted construction, workforce development commitments if required by program

### Step 6 — Cost Structure

Collect:
- Total project capital cost (estimated)
- Cost per passing (total capex ÷ total locations to be served)
- Cost breakdown by category: construction (civil, trenching, aerial, make-ready), materials (fiber, electronics, CPE), engineering, permitting, project management, contingency
- Operating costs: Year 1 O&M estimate
- Matching funds: amount, source, and confirmation status (committed vs. anticipated)
- Grant amount requested

Flag if cost per location appears outside the typical range for the technology type and geography — ask the user to confirm or provide a justification narrative.

### Step 7 — Affordability and Adoption Plan

Collect:
- Subscriber pricing plan: monthly rate for qualifying broadband service at program-required speeds
- Low-income affordability program: participation in ACP successor program, Lifeline, or state equivalent; description of reduced-rate offering
- Digital equity measures: device access programs, digital literacy partnerships, community outreach plan
- Adoption barrier analysis: which populations in the service area face barriers beyond physical access (cost, devices, skills)

### Step 8 — DRAFT Narrative Assembly

Assemble the DRAFT application narrative using the Output Format below. Label clearly:

```
DRAFT — Requires Applicant, Engineering, and Legal Counsel Review
Program: [program name]
Applicant: [legal entity name]
Date: [date]
```

Flag any information gaps with `[INFORMATION NEEDED — DO NOT SUBMIT WITH THIS PLACEHOLDER]`.

## Key Rules

- **Always** identify and state the specific grant program's eligibility rules before drafting narrative sections.
- **Never** present cost estimates as binding, certified, or final — always label them "PRELIMINARY ESTIMATES."
- **Always** confirm the applicant's SAM.gov and FRN registration status is current before drafting — unregistered applicants cannot receive federal funds.
- **Never** assert that locations are unserved or underserved without the applicant confirming the data source and program-required methodology.
- **Always** flag BEAD fiber-first requirements; do not draft an alternative-technology justification without the applicant providing the specific technical basis.
- **Always** include an affordability / adoption plan — it is required by BEAD and most state programs.
- **Always** label the output DRAFT and include a reviewer sign-off block.
- **Ask one question at a time**; intake may span multiple sessions.
- This skill produces a narrative draft only — it does not submit to any portal, generate FCC Form filings, or interact with any government system.

## Output Format

Produce a structured Markdown document with the following sections:

```
# Broadband Grant Application Narrative — DRAFT

**Program:** [program name]
**Applicant:** [legal entity name]
**Application deadline:** [date]
**Status:** DRAFT — Requires Applicant, Engineering, and Legal Counsel Review
**Prepared:** [date]

---

## Executive Summary

[3–5 sentence overview: who the applicant is, where the project is, how many locations will be served, what technology will be deployed, and what the total project cost and grant request are.]

## Section 1: Applicant Qualifications

[Narrative: legal entity, type, years of experience, prior grants, current service territory, relevant technical capacity.]

## Section 2: Project Area and Need

[Narrative: geographic area, number of unserved/underserved locations, current speed availability, data source and methodology used to confirm unserved/underserved status, anchor institutions.]

## Section 3: Technical Approach

[Narrative: technology selected, planned speeds, network architecture, scalability to 1 Gbps symmetric, middle-mile access plan.]

*For BEAD applications: fiber-first confirmation or alternative-technology exception justification.*

## Section 4: Deployment Plan

[Narrative: phased deployment timeline, milestone schedule table, permitting strategy, workforce plan.]

### Milestone Schedule

| Milestone | Target Date |
|-----------|-------------|
| Engineering complete | |
| Permits obtained | |
| Construction start | |
| 25% locations activated | |
| 50% locations activated | |
| 100% locations activated | |
| Project closeout | |

## Section 5: Project Budget

[Narrative: total project cost, cost per location, cost category breakdown, matching funds source and status.]

### Budget Summary

| Category | Estimated Cost |
|----------|---------------|
| Civil construction | |
| Materials (fiber, electronics, CPE) | |
| Engineering and design | |
| Permitting and ROW | |
| Project management | |
| Contingency (recommended 10–15%) | |
| **Total Project Cost** | |
| Less: Matching Funds | |
| **Grant Amount Requested** | |

*All figures are PRELIMINARY ESTIMATES. Final costs must be validated by a licensed engineer and reviewed by legal counsel before submission.*

## Section 6: Affordability and Adoption Plan

[Narrative: subscriber pricing, low-income program participation, digital equity measures, adoption barrier analysis, community outreach plan.]

---

## Open Items and Information Needed

[List all [INFORMATION NEEDED] placeholders with responsible party and due date.]

## Reviewer Sign-Off

| Role | Name | Date | Initials |
|------|------|------|----------|
| Applicant Authorized Official | | | |
| Network Engineer | | | |
| Grant/Legal Counsel | | | |

*This narrative is a DRAFT. Do not submit to any grant portal or share with the funding agency until all open items are resolved and all sign-offs are obtained.*
```

## Feedback

If this skill did not meet your needs or you encountered a workflow it does not cover, share your feedback at: https://github.com/archlab-space/Open-Skill-Hub/issues

Surface this link only when the user expresses an unmet need or dissatisfaction — never in normal interactions.
