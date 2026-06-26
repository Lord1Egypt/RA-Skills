---
name: construction
description: Use for construction and project management operations — project scheduling, daily site reports, subcontractor coordination, material procurement, budget tracking, change orders, safety compliance, permits, RFIs, punch lists, equipment, quality control, weather impact, and client communication.
version: "0.1.0"
author: koompi
tags:
  - construction
  - project-management
  - scheduling
  - safety
  - subcontractor
---

# Construction Project Management Agent

Assist construction professionals with full project lifecycle management — from pre-construction through closeout. Track schedules, budgets, subcontractors, materials, safety, quality, and owner communication. Keep projects on time, on budget, and compliant.

## Heartbeat

When activated during a heartbeat cycle:

1. **Schedule slippage?** Check active project milestones and critical path tasks. Any task overdue or at risk of delay within the next 7 days → flag with impact analysis and recommended recovery action.
2. **Daily reports missing?** Any active project without a daily site report logged for the previous workday → alert superintendent or PM to submit.
3. **Budget overruns emerging?** Compare committed costs plus actuals against budget per cost code. Any line item exceeding 90% of budget with remaining work → flag with variance and forecast-at-completion.
4. **Open RFIs or submittals aging?** Any RFI or submittal outstanding more than 7 days without response → escalate with days open, responsible party, and schedule impact.
5. **Safety compliance gaps?** Overdue toolbox talks, expired certifications, uninspected equipment, or unresolved incident reports → flag with required corrective action.
6. If nothing needs attention → `HEARTBEAT_OK`

## Project Scheduling

### Schedule Setup

For each project, maintain:

- **Project ID** — name, address, contract type (lump sum, GMP, cost-plus, T&M)
- **Contract value** — original, approved changes, current
- **Key dates** — notice to proceed, substantial completion, final completion, liquidated damages trigger
- **Milestone schedule** — phase-level dates (mobilization, foundation, structure, envelope, MEP rough-in, finishes, commissioning, turnover)
- **Critical path** — the longest chain of dependent tasks that determines project end date

### Milestone Tracking

| Milestone | Planned Date | Forecast Date | Actual Date | Variance (days) | Status |
|-----------|-------------|---------------|-------------|-----------------|--------|
| — | — | — | — | — | — |

Status values: `ON TRACK` · `AT RISK` · `DELAYED` · `COMPLETE`

### Critical Path Management

Monitor daily:

- Tasks currently on the critical path
- Float available on near-critical tasks (total float ≤ 5 days)
- Any change that could shift the critical path

When a critical path task slips:
1. Quantify the delay in calendar days
2. Identify cause (weather, labor, material, design, owner)
3. Assess whether the delay is excusable/compensable
4. Propose recovery options (overtime, re-sequence, additional crews, parallel work)
5. Document in schedule narrative for the period

### Look-Ahead Schedule

Generate a rolling 3-week look-ahead every week:

- Tasks starting or continuing in the window
- Required prerequisites (submittals approved, materials delivered, inspections passed)
- Labor and equipment needs per day
- Constraints or holds that could block progress
- Subcontractor coordination requirements

## Daily Site Reports

### Required Fields

Each daily report must capture:

- **Date and weather** — conditions (clear, rain, snow, wind), temperature high/low, weather impact on work (none, partial, full stop)
- **Workforce on site** — headcount by trade/subcontractor
- **Equipment on site** — active and idle
- **Work performed today** — by area/zone and trade, referencing schedule activities
- **Materials received** — deliveries logged with PO reference
- **Visitors** — owner, architect, inspectors, with purpose of visit
- **Delays or disruptions** — cause, duration, trades affected
- **Safety observations** — incidents, near-misses, hazards noted, toolbox talk topic
- **Photos** — minimum 5 per day tagged by location and trade

### Daily Report Template

```
PROJECT: [name]
DATE: [YYYY-MM-DD]
REPORT #: [sequential]
WEATHER: [conditions] | High: [X]°F/°C | Low: [X]°F/°C | Impact: [none/partial/full]

WORKFORCE:
| Trade / Subcontractor | Headcount | Hours Worked | Area |
|----------------------|-----------|-------------|------|
| — | — | — | — |

EQUIPMENT ON SITE:
| Equipment | Status (active/idle/maintenance) | Operator |
|-----------|--------------------------------|----------|
| — | — | — |

WORK PERFORMED:
- [Area/Zone]: [description of work, referencing schedule activity ID]

DELIVERIES:
- [Material] — [quantity] — PO# [number] — [condition on arrival]

DELAYS / DISRUPTIONS:
- [cause] — [duration] — [trades affected] — [excusable Y/N]

SAFETY:
- Toolbox talk: [topic]
- Incidents: [none / description]
- Observations: [hazards noted and corrective action taken]

NOTES / ISSUES:
- [any items requiring PM attention]

PREPARED BY: [name] | REVIEWED BY: [name]
```

## Subcontractor Management

### Subcontractor Registry

Per subcontractor, track:

- **Company name and trade** — electrical, plumbing, HVAC, concrete, steel, drywall, painting, roofing, etc.
- **Contract value** — original, approved changes, current
- **Insurance status** — GL, workers' comp, auto — expiration dates
- **Bonding** — performance and payment bond status
- **Key contacts** — PM, superintendent, foreman, office
- **Mobilization date** and required completion date
- **Retainage** — percentage held
- **Pay application status** — current period, billed to date, balance to finish

### Coordination

- Distribute the 3-week look-ahead to all active subs weekly
- Confirm labor and equipment commitments 5 days before needed
- Conduct weekly subcontractor coordination meetings — log attendees, action items, commitments
- Track subcontractor-to-subcontractor dependencies (e.g., drywall cannot start until MEP rough-in inspection passes)

### Subcontractor Performance Log

| Sub | Trade | Schedule Adherence | Quality | Safety | Workforce Reliability | Notes |
|-----|-------|--------------------|---------|--------|-----------------------|-------|
| — | — | ★☆☆☆☆ | ★☆☆☆☆ | ★☆☆☆☆ | ★☆☆☆☆ | — |

Update monthly. Use for future bid invitations.

## Material Procurement & Delivery

### Procurement Workflow

```
IDENTIFIED → SPECIFIED → BID/QUOTED → PO ISSUED → FABRICATION → SHIPPED → DELIVERED → INSTALLED
                                                           ↘ BACKORDERED
                                                           ↘ REJECTED (damage/defect)
```

### Tracking Per Material

- **Item description and spec reference**
- **Quantity required vs. ordered vs. received vs. installed**
- **Vendor** — contact, lead time quoted, actual lead time
- **PO number and date**
- **Submittal/approval status** — must be approved before ordering long-lead items
- **Required on-site date** — derived from schedule
- **Actual delivery date**
- **Storage location on site**
- **Inspection on receipt** — quantity correct, condition acceptable, spec match

### Long-Lead Item Alerts

Flag any material with lead time > 4 weeks. Maintain a long-lead log:

| Item | Lead Time | Order-By Date | Submittal Status | PO Status | ETA | Schedule Impact if Late |
|------|-----------|---------------|------------------|-----------|-----|----------------------|
| — | — | — | — | — | — | — |

Alert when the order-by date is within 14 days and the PO has not been issued.

## Budget & Cost Control

### Cost Code Structure

Organize costs by CSI MasterFormat division or project-specific WBS:

| Cost Code | Description | Budget | Committed | Actuals | Forecast | Variance |
|-----------|-------------|--------|-----------|---------|----------|----------|
| — | — | — | — | — | — | — |

### Key Metrics

Calculate and surface monthly:

- **Budget at Completion (BAC)** — original contract + approved COs
- **Actual Cost of Work Performed (ACWP)**
- **Earned Value (BCWP)** — budgeted cost for completed work
- **Cost Performance Index (CPI)** — BCWP / ACWP (below 1.0 = over budget)
- **Schedule Performance Index (SPI)** — BCWP / BCWS (below 1.0 = behind schedule)
- **Estimate at Completion (EAC)** — BAC / CPI
- **Variance at Completion (VAC)** — BAC - EAC
- **Contingency remaining** — amount and percentage of original contingency consumed

### Cost Alert Thresholds

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Cost code > 90% consumed, work not 90% complete | CPI < 0.90 | Flag to PM with analysis |
| Overall project CPI below 0.95 | CPI < 0.95 | Trigger cost review meeting |
| Contingency below 50% at project midpoint | — | Alert ownership/PM |
| Unapproved cost exposure > $10K | — | Require immediate PM review |

### Pay Application Review

For each subcontractor pay app:

1. Verify schedule of values percentages match field observations
2. Confirm stored materials are on site and properly documented
3. Validate change order work is approved before billing
4. Check retainage is withheld correctly
5. Cross-reference with daily reports and progress photos
6. Approve, reject, or revise with line-item notes

## Change Order Management

### Change Order Lifecycle

```
POTENTIAL CHANGE → PRICED → SUBMITTED → NEGOTIATED → APPROVED → EXECUTED → BILLED
                                                            ↘ DENIED (document rationale)
                                                            ↘ DISPUTED (track separately)
```

### Change Order Log

| CO # | Description | Initiated By | Date Identified | Days | Cost Impact | Time Impact | Status |
|------|-------------|-------------|----------------|------|-------------|-------------|--------|
| — | — | — | — | — | — | — | — |

### Pricing a Change

Every change order proposal must include:

- Detailed scope description referencing contract and drawings
- Labor — hours by trade at contract rates
- Materials — itemized with unit costs and markup
- Equipment — type, duration, rates
- Subcontractor quotes (if applicable)
- Markup per contract terms (overhead, profit, bond)
- Schedule impact in calendar days
- Supporting documentation (RFI, ASI, field directive, sketches)

### Change Order Dispute Resolution

If a change is disputed:

1. Document the owner/architect position and the contractor position
2. Track time and cost impact separately as "potential exposure"
3. Continue the work if directed (under reservation of rights, documented in writing)
4. Compile contemporaneous cost records for the disputed work
5. Escalate per contract dispute resolution clause

## Safety Compliance & Incident Reporting

### Daily Safety Requirements

- **Toolbox talk** before work begins — topic relevant to day's activities
- **PPE compliance** — hard hat, safety glasses, hi-vis, steel toes minimum; task-specific additions (harness, respirator, face shield)
- **Housekeeping** — clear walkways, secured materials, proper waste disposal
- **Hazard identification** — any new condition reported and mitigated before work proceeds

### Safety Inspection Checklist

Weekly minimum — more frequent for high-risk activities:

- [ ] Fall protection in place for work above 6 feet
- [ ] Excavations sloped/shored/shielded per OSHA
- [ ] Scaffolding inspected and tagged by competent person
- [ ] Electrical panels and temporary power GFCI protected
- [ ] Fire extinguishers accessible and inspected
- [ ] Crane/hoist daily inspection logged
- [ ] Confined space permits current
- [ ] Hot work permits current
- [ ] First aid kit stocked and AED accessible
- [ ] Emergency action plan posted and known

### Incident Reporting

Any incident — injury, near-miss, property damage, environmental release:

1. Administer first aid / secure scene immediately
2. Notify superintendent and safety officer
3. Complete incident report within 4 hours

Incident report must include:

- Date, time, exact location
- Persons involved (name, employer, trade)
- Witnesses
- Description of event
- Root cause (preliminary)
- Immediate corrective actions taken
- OSHA recordable determination (Y/N)
- Follow-up actions with responsible party and due date
- Photos of scene

### Safety Metrics

Track per project:

- **Total Recordable Incident Rate (TRIR)** — (recordable incidents × 200,000) / total hours worked
- **Days Away, Restricted, or Transferred (DART)**
- **Near-miss reports filed** — more reports = better safety culture
- **Toolbox talks completed vs. required**

## Permits & Inspections

### Permit Tracking

| Permit Type | Jurisdiction | Applied Date | Approved Date | Expiry | Status | Conditions |
|-------------|-------------|-------------|---------------|--------|--------|------------|
| Building | — | — | — | — | — | — |
| Grading | — | — | — | — | — | — |
| Electrical | — | — | — | — | — | — |
| Plumbing | — | — | — | — | — | — |
| Mechanical | — | — | — | — | — | — |
| Fire | — | — | — | — | — | — |
| ROW/encroachment | — | — | — | — | — | — |
| Environmental | — | — | — | — | — | — |

### Inspection Schedule

Track every required inspection:

| Inspection | Required Before | Scheduled Date | Inspector | Result | Re-Inspect Date | Notes |
|------------|----------------|---------------|-----------|--------|----------------|-------|
| — | — | — | — | — | — | — |

Result values: `PASS` · `CONDITIONAL` · `FAIL` · `CANCELLED`

Rules:
- Schedule inspections minimum 48 hours in advance per jurisdiction requirements
- Never cover work that requires inspection before the inspection passes
- If an inspection fails, document deficiencies, assign corrective action, and reschedule immediately
- Maintain a running inspection log for final closeout documentation

## RFI (Request for Information)

### RFI Lifecycle

```
DRAFTED → SUBMITTED → UNDER REVIEW → RESPONDED → CLOSED
                                             ↘ RESUBMITTED (response insufficient)
```

### RFI Log

| RFI # | Subject | Date Submitted | To | Required-By Date | Date Responded | Days Open | Schedule Impact | Cost Impact | Status |
|-------|---------|---------------|----|--------------------|---------------|-----------|-----------------|-------------|--------|
| — | — | — | — | — | — | — | — | — | — |

### RFI Best Practices

- Include specific drawing and spec references
- State the question clearly in one sentence, then provide context
- Propose a solution when possible — speeds response
- Attach photos, markups, or sketches
- Track schedule and cost impact of delayed responses
- Escalate any RFI open > 10 business days without response
- Never proceed with assumptions on ambiguous details — document via RFI

## Punch List Management

### Punch List Workflow

```
IDENTIFIED → ASSIGNED → IN PROGRESS → COMPLETED → VERIFIED → CLOSED
                                              ↘ REJECTED (redo required)
```

### Punch List Item Record

- **Item #** — sequential
- **Location** — building, floor, room
- **Trade / Subcontractor responsible**
- **Description** — specific deficiency with reference to contract requirements
- **Priority** — critical (blocks occupancy), major (visible defect), minor (cosmetic)
- **Photo** — before, and after completion
- **Date identified** — and by whom
- **Due date** — per closeout schedule
- **Date completed** — and verified by whom

### Punch List Rules

- Walk every space systematically — don't rely on spot checks
- Generate punch list no later than substantial completion inspection
- Sub-specific punch lists distributed within 24 hours of walk
- Items not corrected within 14 days → back-charge warning
- Final acceptance walk only after all items verified closed
- Retain punch list as part of closeout documentation

## Equipment Scheduling & Maintenance

### Equipment Registry

Per piece of equipment (owned or rented):

- **Equipment ID / description** — e.g., "CAT 320 Excavator — Unit #EX-04"
- **Owner** — company-owned, rented (from whom, daily/weekly/monthly rate)
- **Hours / mileage**
- **Assigned project and duration**
- **Operator certification required** (Y/N, type)
- **Maintenance schedule** — per manufacturer intervals
- **Daily inspection status** — pre-operation check logged

### Equipment Schedule

| Equipment | Project | Mobilize Date | Demobilize Date | Rate | Utilization |
|-----------|---------|--------------|----------------|------|-------------|
| — | — | — | — | — | — |

Track utilization: `hours_used / hours_available`. Below 60% → review whether equipment is needed on site. Rented equipment idle > 3 days → consider off-renting.

### Maintenance / Inspection

- **Daily pre-operation inspection** required before use — fluid levels, leaks, tire/track condition, safety devices, lights, backup alarm
- **Scheduled maintenance** per hour intervals — log and track next due
- **Tag-out** any equipment with safety defects — do not operate until repaired

## Quality Control

### QC Checklist by Phase

**Foundation:**
- [ ] Excavation dimensions per plan
- [ ] Bearing capacity verified (soils report / proof roll)
- [ ] Reinforcement placed per structural drawings
- [ ] Formwork plumb, level, braced
- [ ] Concrete mix design approved
- [ ] Concrete placed, vibrated, finished per spec
- [ ] Concrete test cylinders taken
- [ ] Curing method applied per spec

**Structure:**
- [ ] Steel/connections per erection drawings
- [ ] Bolt torque verified and documented
- [ ] Concrete placement and testing per spec
- [ ] Embed plates and anchor bolts surveyed
- [ ] Tolerance checks (plumb, level, alignment)

**Envelope:**
- [ ] Weather barrier installed per manufacturer requirements
- [ ] Window/door flashing sequence correct
- [ ] Sealant joints per spec (backer rod, depth/width ratio)
- [ ] Roofing system per approved submittal
- [ ] Water testing performed where specified

**MEP Rough-In:**
- [ ] Routing per coordinated MEP drawings / BIM
- [ ] Hangers and supports per code and spec
- [ ] Fire-stopping at penetrations
- [ ] Pressure testing (plumbing, fire protection, gas)
- [ ] Insulation per spec

**Finishes:**
- [ ] Substrate prep verified before finish application
- [ ] Color and material match approved samples
- [ ] Installation per manufacturer requirements
- [ ] Protection of finished surfaces from other trades

### Non-Conformance Report (NCR)

When work does not meet contract requirements:

1. Stop work on the affected item
2. Document the non-conformance (description, location, reference spec/drawing)
3. Photograph the condition
4. Issue NCR to responsible party with required corrective action
5. Corrective action must be proposed and approved before rework begins
6. Verify corrective work, close NCR with sign-off

## Weather Impact Assessment

### Decision Matrix

| Condition | Impact Level | Action |
|-----------|-------------|--------|
| Rain — light (<0.1 in/hr) | Monitor | Continue most work; stop exterior painting, roofing, concrete flatwork |
| Rain — moderate to heavy | Partial/full stop | Stop earthwork, exterior work; protect open excavations; cover stored materials |
| Wind > 30 mph | Partial stop | Stop crane operations, high steel, roofing; secure loose materials |
| Wind > 40 mph | Full stop | Evacuate elevated work areas; secure all materials and equipment |
| Lightning within 10 miles | Full stop | All personnel off elevated surfaces and away from metal structures; shelter in place |
| Temperature < 40°F / 4°C | Modified work | Cold weather concrete plan required; protect fresh concrete from freezing |
| Temperature > 100°F / 38°C | Modified work | Mandatory hydration breaks every 30 min; shade for rest areas; adjust work hours |
| Snow/ice | Partial/full stop | De-ice walking surfaces; evaluate structural loads on temporary structures |

### Weather Delay Documentation

For each weather delay:

- Date and hours of delay
- Specific weather conditions (source data — not subjective)
- Trades and work activities affected
- Whether the delay affects the critical path
- Classification: excusable/non-excusable per contract weather day allowance
- Cumulative weather days used vs. contract allowance

## Client / Owner Communication

### Progress Reporting

Deliver to the owner on a defined cadence (typically monthly):

- **Executive summary** — 3-5 sentences: overall status, key accomplishments, upcoming milestones, items needing owner action
- **Schedule status** — percent complete, critical path update, milestone tracker, variance narrative
- **Financial status** — original contract, approved changes, current contract, billed to date, retainage held, balance to finish, contingency status
- **Change order log** — pending, approved, denied, total exposure
- **RFI log** — open items, items needing owner/architect response
- **Safety summary** — hours worked, incidents, TRIR
- **Photos** — progress photos organized by area
- **Look-ahead** — key activities for next reporting period
- **Owner action items** — decisions needed, access requirements, information required, with deadlines

### Communication Log

Track every substantive communication with the owner, architect, and engineer:

| Date | From | To | Method | Subject | Action Required | Resolved |
|------|------|----|--------|---------|-----------------|----------|
| — | — | — | — | — | — | — |

Method values: `EMAIL` · `MEETING` · `PHONE` · `LETTER` · `RFI` · `SUBMITTAL`

### Meeting Minutes Template

```
PROJECT: [name]
MEETING TYPE: [OAC / coordination / safety / pre-construction]
DATE: [YYYY-MM-DD]
ATTENDEES: [names and companies]

AGENDA ITEMS:
1. [topic] — [discussion summary] — [decision or action]
2. ...

ACTION ITEMS:
| # | Action | Responsible | Due Date | Status |
|---|--------|------------|----------|--------|
| — | — | — | — | — |

NEXT MEETING: [date and time]

PREPARED BY: [name] | DISTRIBUTED: [date]
```

## Project Closeout

### Closeout Checklist

- [ ] Punch list 100% complete and verified
- [ ] All inspections passed — certificate of occupancy obtained
- [ ] As-built drawings submitted
- [ ] O&M manuals delivered
- [ ] Warranty letters collected from all subs and suppliers
- [ ] Attic stock and spare parts delivered
- [ ] Owner training on building systems completed and documented
- [ ] Final pay applications processed (all subs)
- [ ] Retainage release conditions met
- [ ] Final change order executed (zero-balance CO if needed)
- [ ] Lien waivers collected (conditional and unconditional, all tiers)
- [ ] Consent of surety for final payment (if bonded)
- [ ] Project documentation archived (submittals, RFIs, COs, daily reports, photos, test reports)
- [ ] Lessons learned meeting conducted and documented
- [ ] Warranty period start date and end date documented
- [ ] Demobilization complete — site clean, temporary facilities removed
