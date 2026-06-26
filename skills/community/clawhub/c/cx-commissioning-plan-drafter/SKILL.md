---
name: cx-commissioning-plan-drafter
description: >
  Use this skill when a commissioning authority (CxA), building commissioning professional,
  MEP engineer, or owner's representative needs to draft a project commissioning plan aligned
  to ASHRAE Guideline 0-2019, LEED v4/v4.1 EA Prerequisite (Fundamental Commissioning), or
  federal/agency commissioning requirements. Covers commissioned systems scope, Cx team roles
  and responsibilities, project schedule, documentation and submittal requirements, functional
  performance test framework, and issues log protocol. Produces a DRAFT Cx Plan for CxA review
  before mechanical and electrical system installation begins.
---

# Commissioning Plan Drafter

Convert project data, Owner's Project Requirements, and system scope information into a structured DRAFT Commissioning Plan aligned to ASHRAE Guideline 0-2019, ready for CxA review before system installation begins.

## Flow

### Phase 1 — Project Identification and Cx Authority

Ask one question at a time. Collect:

- Project name, address, and project number
- Building type and primary use (e.g., Class A office, K-12 school, hospital, data center, laboratory, multifamily, federal facility)
- Gross square footage (conditioned space)
- Project delivery method: design-bid-build, design-build, CM at risk, or integrated project delivery (IPD)
- Owner organization name and Owner's Representative contact (for OPR confirmation)
- CxA organization name and lead CxA name
- Commissioning scope driver: LEED v4/v4.1, ASHRAE Guideline 0 voluntary, federal requirement (GSA, DoD UFC 3-410-11FA), energy code (Title 24 NACM, IECC), or owner-mandated
- Project start date, substantial completion target, and occupancy target

If the commissioning scope driver is LEED, confirm which credit tier is pursued: EA Prerequisite (Fundamental Cx), EA Credit: Enhanced Commissioning, or EA Credit: Enhanced Cx Option 2 (Monitoring-Based Commissioning). Each tier has distinct scope requirements.

### Phase 2 — Owner's Project Requirements (OPR) Summary

The OPR is the foundational document that defines owner intent. Collect or summarize:

- Energy performance goals (e.g., target EUI, ENERGY STAR score, net-zero target)
- Indoor environment quality requirements (thermal comfort ASHRAE 55, IAQ ASHRAE 62.1, lighting levels)
- Reliability and redundancy requirements (e.g., N+1 for critical systems)
- Sustainability certifications required (LEED, WELL, Fitwel, net-zero energy)
- Specific owner operational preferences (BAS vendor, preferred controls platform, service access)
- Expected building lifespan and long-term O&M philosophy

If the OPR has not been formally developed, insert OPR FLAG: The Owner's Project Requirements document must be completed and approved by the Owner before the Cx Plan can be finalized. The CxA is responsible for facilitating OPR development per ASHRAE Guideline 0 Section 5.

### Phase 3 — Systems to Be Commissioned

Present the following standard system categories and ask the user to confirm which apply, add project-specific systems, and note any exclusions:

**HVAC and Mechanical:**
- Air handling units (AHUs), rooftop units (RTUs), heat recovery units
- Variable air volume (VAV) systems and terminal units
- Chilled water system: chillers, cooling towers, pumps, heat exchangers
- Heating hot water system: boilers, pumps, heat exchangers
- Exhaust and ventilation systems
- Humidification and dehumidification systems
- Kitchen exhaust and makeup air
- Cleanroom or laboratory pressurization systems (if applicable)

**Building Automation and Controls:**
- Building Automation System (BAS / BMS / DDC): complete sequences of operation for all commissioned equipment
- Demand-controlled ventilation (DCV)
- Economizer sequences
- BAS integration with fire alarm, security, or lighting (list interfaces)

**Plumbing:**
- Domestic hot water system: water heaters, recirculation, temperature maintenance
- Medical gas systems (if applicable; note AHJ and NFPA 99 requirements separately)

**Electrical:**
- Lighting control systems: occupancy sensors, daylight harvesting, automated shading
- Emergency and standby power: generators, ATS, UPS systems
- Power monitoring and metering systems
- Electric vehicle (EV) charging infrastructure (if applicable)

**Renewable and Specialty:**
- Solar PV system: inverters, monitoring, grid interconnection
- Battery energy storage systems (BESS)
- Heat pump systems (geothermal, air-to-water)
- Data center cooling and power (if applicable)

**Envelope (Enhanced Cx only):**
- Building envelope: air barrier continuity, fenestration, thermal bridging
- Note: Envelope commissioning requires LEED Enhanced Cx or specific owner request

Produce a **Commissioned Systems Matrix**: table with system category, specific equipment, commissioning basis (standard vs. enhanced vs. monitoring-based), and any exclusions with documented rationale.

If the user requests to exclude a system that would normally be required under the commissioning scope driver (e.g., LEED EA Prerequisite requires AHU commissioning), insert an EXCLUSION FLAG with the applicable standard requirement.

### Phase 4 — Commissioning Team: Roles and Responsibilities

Document the Cx team structure. For each role, record the name/organization (or "TBD") and responsibilities:

| Role | Responsibilities |
|---|---|
| Owner / Owner's Rep | Approves OPR, reviews and accepts Cx Plan, resolves scope disputes |
| Commissioning Authority (CxA) | Leads Cx process, develops Cx Plan and FPT protocols, witnesses and documents testing, issues Cx Report |
| Design Engineer of Record (EOR) | Provides Basis of Design (BoD), responds to Cx issues, approves FPT protocols for their discipline |
| General Contractor / CM | Coordinates subcontractor Cx participation, resolves construction-phase issues |
| Mechanical Contractor | Performs pre-functional checks (PFCs), supports FPT execution, corrects deficiencies |
| Electrical Contractor | Same as mechanical for electrical systems |
| Controls Contractor / BAS Vendor | Programs sequences per BoD, performs point-to-point checkout, supports FPT |
| Testing, Adjusting & Balancing (TAB) Contractor | Provides TAB report as prerequisite to FPT; coordinates airflow and hydronic balance |
| Facility Operations Staff | Participates in systems training, receives O&M documentation |

Insert a COORDINATION FLAG for any role listed as TBD — these must be confirmed and documented before system installation begins.

### Phase 5 — Commissioning Schedule

Document Cx activities mapped to the project schedule phases:

**Design Phase (if enhanced or Owner-directed early Cx):**
- OPR development and BoD review: [date range or TBD]
- Design review submittals: [milestone]

**Construction Phase:**
- Cx kickoff meeting: [target date]
- Submittal review (Cx-relevant equipment): [target date]
- Pre-functional checklist (PFC) development: [target date]
- PFC execution window: [start–end dates or by system]
- TAB completion prerequisite: [target date]
- Functional Performance Test (FPT) execution window: [start–end dates]
- Seasonal testing (if required): [date range — note if deferred]

**Occupancy and Post-Occupancy:**
- Systems training for O&M staff: [target date]
- Cx Report completion: [target date]
- Warranty-period follow-up (Enhanced Cx): [10-month review date]

Insert a SCHEDULE FLAG for any FPT window that begins before TAB is confirmed complete — FPTs require balanced airflow and hydronic systems to be valid.

### Phase 6 — Documentation and Submittal Requirements

List all Cx deliverables and the party responsible for each:

| Deliverable | Responsible Party | Due Date |
|---|---|---|
| Owner's Project Requirements (OPR) | CxA (facilitates); Owner (approves) | Before design completion |
| Basis of Design (BoD) | Design EOR | Before construction documents |
| Commissioning Plan | CxA | Before system installation |
| Submittal Review (Cx scope equipment) | CxA | During submittal phase |
| Pre-Functional Checklists (PFCs) | CxA (develops); Contractor (completes) | Before FPT |
| TAB Report | TAB Contractor | Before FPT |
| Functional Performance Test (FPT) Protocols | CxA | Before FPT execution |
| Issues Log | CxA (maintains) | Continuous |
| Systems Training Documentation | Contractors + CxA | Before occupancy |
| O&M Manual Review (Cx scope) | CxA | Before occupancy |
| Commissioning Report | CxA | After FPT completion |
| Deferred/Seasonal Test Report | CxA | Per schedule |

**LEED-specific documentation** (if applicable):
- LEED Online documentation: CxA letter of certification, Cx report upload
- Confirm LEED project registration number and target submittal date

### Phase 7 — Pre-Functional Checklist (PFC) Framework

Pre-functional checklists verify that equipment is installed per contract documents before functional testing begins. Document the PFC approach:

- PFC format: agent-drafted or contractor-submitted with CxA review? Document the project decision.
- PFC trigger: PFCs must be completed and signed by the installing contractor and witnessed by the CxA (or CxA-designated observer) before any FPT is scheduled for that system.
- PFC scope per system type: list the verification categories (installation, startup, controls point-to-point checkout, TAB prerequisite confirmation).
- PFC rejection criterion: any incomplete or failed PFC item that is safety-critical, sequence-critical, or TAB-prerequisite automatically blocks FPT scheduling. Insert NON-NEGOTIABLE: No FPT shall be scheduled for a system with an outstanding CRITICAL PFC deficiency.

### Phase 8 — Functional Performance Test (FPT) Framework

Document the FPT approach without writing full test scripts (full FPT protocols are developed separately per system):

- FPT authoring responsibility: CxA develops all FPT protocols with EOR review and approval
- FPT execution method: manual testing, trend-log review, or automated testing via BAS (specify project preference)
- Witness requirement: CxA witnesses all FPTs; contractor responsible party must be present
- Failure protocol: any failed FPT result is logged in the Issues Log; contractor corrects deficiency; re-test is performed and documented; CxA closes the issue only after successful re-test
- Seasonal testing plan: list any sequences that require deferred testing (e.g., economizer testing in summer, heating sequences in winter) and document deferred test schedule

Insert a TEST SCOPE NOTE: FPT protocols will test each system's sequences of operation against the approved BoD. Tests will include, at minimum: startup/shutdown sequences, occupied/unoccupied mode transitions, setpoint response, alarm and fault conditions, emergency shutdown, and any system integration sequences listed in the Commissioned Systems Matrix.

### Phase 9 — Issues Log Protocol

Document the issues management process:

- Issues Log format: spreadsheet or commissioning software (name platform if specified)
- Issue fields: issue number, date identified, system, description, priority (Critical / High / Medium / Low), responsible party, target resolution date, resolution description, CxA close-out date
- CRITICAL priority definition: safety hazard, life safety system failure, or sequence failure that prevents occupancy
- Issue escalation path: unresolved CRITICAL issues escalate to Owner's Rep and EOR within 24 hours
- Issues Log distribution: shared with Owner's Rep, GC, and relevant subcontractors at weekly Cx meetings during construction phase

### Phase 10 — DRAFT Commissioning Plan Assembly

Produce the DRAFT Cx Plan with:

1. **Header**: Project name, address, project number, building type, GSF, CxA organization, plan date, document version, status: **DRAFT — PENDING CxA REVIEW**
2. **Project Overview**: Delivery method, commissioning scope driver, project schedule summary
3. **Owner's Project Requirements Summary**: Energy goals, IEQ requirements, reliability requirements, OPR FLAG if not yet completed
4. **Commissioned Systems Matrix**: Table of all systems in scope, basis, and exclusions
5. **Cx Team Roles and Responsibilities**: Table from Phase 4
6. **Commissioning Schedule**: Phase-mapped milestone table
7. **Documentation and Submittal Requirements**: Deliverables table
8. **Pre-Functional Checklist Framework**: PFC approach, trigger, and blocking criteria
9. **Functional Performance Test Framework**: Authoring, execution, failure protocol, seasonal testing
10. **Issues Log Protocol**: Format, fields, escalation, distribution
11. **CxA Review Block**:

```
DRAFT — PENDING CxA REVIEW AND OWNER ACCEPTANCE

Lead CxA: _______________________
CxA Organization: _______
CxA Certification (BCxP / CxA / CBCP): _______
Date of Review: _______
Acceptance status: [ ] ACCEPTED  [ ] ACCEPTED WITH REVISIONS  [ ] REQUIRES REVISION
Revisions required: _______

Owner / Owner's Representative acceptance: _______________________
Date: _______
```

## Key Rules

- Always label the output: **DRAFT — PENDING CxA REVIEW AND OWNER ACCEPTANCE**.
- Never produce complete FPT protocols or detailed test scripts — these are separate deliverables developed by the CxA per system.
- If the OPR has not been developed, insert an OPR FLAG and do not proceed past Phase 2 until the user confirms whether to continue with a placeholder.
- If a system is excluded that is required by the commissioning scope driver, always insert an EXCLUSION FLAG.
- No FPT shall be scheduled until TAB is confirmed complete — insert a SCHEDULE FLAG if this sequence appears at risk.
- Ask one question at a time. Do not present all phases as a single intake form.
- This skill produces planning documentation only. The CxA is responsible for all professional judgments, system-specific FPT protocols, and the final Cx Report.
- LEED-specific requirements depend on the target credit tier — confirm the credit tier before documenting the commissioning scope.

## Output Format

The DRAFT Cx Plan is formatted as a professional technical document with:
- Numbered sections matching the assembly structure above
- Tables for the Commissioned Systems Matrix, Cx team roles, schedule milestones, and deliverables
- FLAG blocks for OPR, schedule risks, exclusions, and missing information
- CxA and Owner acceptance sign-off block at the end

Target length: 4–8 pages depending on project complexity and number of commissioned systems.

## Feedback

If a user expresses an unmet need, requests a feature not covered by this skill, or is dissatisfied with the output, surface this link: https://github.com/archlab-space/Open-Skill-Hub/issues
