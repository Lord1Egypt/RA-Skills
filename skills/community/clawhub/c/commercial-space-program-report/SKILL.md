---
name: commercial-space-program-report
description: >
  Use this skill when an interior designer, architect, project manager, or owner's
  representative needs to convert a client brief and functional requirements into a
  structured commercial space program. Covers department inventory, headcount projections,
  net area assignments with benchmark basis, functional adjacency matrix, and a
  design-guide narrative. Produces a DRAFT space program for design-team and client
  review before schematic design begins.
---

# Commercial Space Program Report

Convert a client's organizational structure, headcount projections, and functional requirements into a structured space program — the prerequisite document that defines every room type, net area, occupancy, and adjacency before any schematic floor plan is drawn.

## Flow

1. **Project intake** — Confirm: project name, project type (office, healthcare outpatient, retail, hospitality, education, mixed-use, other), gross building area or lease area if known, location, scope (new construction, tenant improvement, or renovation), and the client's primary goals and constraints (budget tier, density target, flexibility requirements, planned growth timeline). Ask one question at a time if the client brief is incomplete.

2. **Organizational inventory** — Build a complete department or functional-group roster. For each group, confirm: group name, primary activities, current headcount, projected headcount at 3 years and 5 years, reporting relationship or adjacency preference, and any known special requirements (secure access, clinical infrastructure, heavy equipment, AV-intensive, server or IDF, lab utilities, quiet zone, etc.).

3. **Room type catalog** — For each group, enumerate all room types needed, including: private enclosed offices, open workstations, small meeting rooms (2–4 persons), medium conference rooms (6–10 persons), large conference or board rooms (12+ persons), phone and focus rooms, reception and lobby, break rooms and pantries, storage and file rooms, server or IDF rooms, accessible restrooms (if within scope), specialty rooms (clinic rooms, labs, studios, trading floors, etc.), and back-of-house or service spaces.

4. **Net area assignment** — For each room type, assign a net usable area in SF or m². State the standard or benchmark used for every assignment: choose from GSA space planning criteria, BOMA occupancy standards, ANSI/BIFMA workspace guidelines, IBC/ADA occupancy minimums, published healthcare room-size standards (FGI Guidelines), or client-stated standard. If no standard applies, state "Engineering Judgment" and the basis. Flag any room where occupancy load or ADA clearance has not yet been confirmed.

5. **Adjacency matrix** — For each major group or space category, score functional adjacency preference against all other groups using a 1–5 scale:
   - 1 = Must-Adjacent (operational necessity)
   - 2 = Preferred-Adjacent (efficiency gain)
   - 3 = Neutral
   - 4 = Preferred-Separate (noise, privacy, or workflow)
   - 5 = Must-Separate (security, infection control, regulatory)
   Produce a complete matrix table with scores and a brief rationale for any 1 or 5 rating.

6. **Program totals and efficiency ratio** — Sum net usable areas by group and by space category (Enclosed Private, Open Collaborative, Conference and Meeting, Support and Storage, Amenity and Wellness, Specialty). Compute the total Net Usable Area (NUA). If gross area is known, compute the load factor (Gross ÷ Net) and flag if outside the typical 1.10–1.40 range for commercial interiors.

7. **Special systems and finish requirements** — List any known special infrastructure needs and the generic finish-quality tier (Class A, Class B, or Class C) appropriate for each space type. Examples: raised access floor, lab gas and exhaust, clinical hand-washing, high-density mobile shelving, acoustically rated partitions, dedicated HVAC zones, AV infrastructure density.

8. **Open items and design-guide narrative** — List all unresolved program questions with an owner assigned where possible. Write a 1–2 paragraph design-guide narrative summarizing the program intent, key adjacency priorities, flexibility requirements, growth strategy, and any client preferences the design team should carry into schematic design.

9. **DRAFT report assembly** — Compile all sections into the structured output below. Mark the document **DRAFT — NOT FOR PERMIT OR CONSTRUCTION**. Include an unsigned Designer Review block.

## Key Rules

- Always mark the output DRAFT — NOT FOR PERMIT OR CONSTRUCTION.
- Never represent net area assignments as code-compliant final specifications; final compliance review by a licensed architect is required.
- State the benchmark or standard used for every room-type area assignment; do not assign areas without a stated basis.
- If headcount data is incomplete, generate the program with clearly flagged TBD placeholders rather than estimating.
- Ask one clarifying question at a time; confirm each group's headcount and requirements before proceeding to the next.
- Flag any room type where ADA/ABA clearance, occupant load, or lease restriction may affect the assigned area.

## Output Format

```
COMMERCIAL SPACE PROGRAM REPORT — DRAFT
Project: [name]
Project Type: [type]
Location: [city, state]
Scope: [new construction / TI / renovation]
Date: [YYYY-MM-DD]
Prepared for: [role only]

────────────────────────────────────────
PROGRAM SUMMARY
────────────────────────────────────────
Total Net Usable Area (NUA): [SF / m²]
Gross Area (if known):       [SF / m²]
Load Factor:                 [ratio or "TBD"]
Headcount (current / projected 5yr): [X / Y]
Area per Person (NUA basis): [SF or m² per person]

────────────────────────────────────────
ORGANIZATIONAL INVENTORY
────────────────────────────────────────
Group | Current HC | 3yr HC | 5yr HC | Primary Activities | Special Requirements

────────────────────────────────────────
ROOM CATALOG AND NET AREAS
────────────────────────────────────────
Group → Room Type | Count | Unit Area (SF/m²) | Total Area | Standard / Benchmark | Flags

[Subtotal per group]

────────────────────────────────────────
PROGRAM TOTALS BY CATEGORY
────────────────────────────────────────
Category                  | Total SF (m²) | % of NUA
Enclosed Private          |               |
Open Collaborative        |               |
Conference and Meeting    |               |
Support and Storage       |               |
Amenity and Wellness      |               |
Specialty                 |               |
──────────────────────────|───────────────|─────────
TOTAL NET USABLE AREA     |               | 100%

────────────────────────────────────────
FUNCTIONAL ADJACENCY MATRIX (1=Must-Adjacent → 5=Must-Separate)
────────────────────────────────────────
[Group A vs. Group B | Score | Rationale for 1 or 5]

────────────────────────────────────────
SPECIAL SYSTEMS AND FINISH REQUIREMENTS
────────────────────────────────────────
Space / Room Type | System or Requirement | Finish Tier (A/B/C)

────────────────────────────────────────
OPEN ITEMS
────────────────────────────────────────
1. [item | Owner | Target date]
2. [item]

────────────────────────────────────────
DESIGN-GUIDE NARRATIVE
────────────────────────────────────────
[1–2 paragraphs summarizing program intent, adjacency priorities, flexibility strategy,
and growth accommodation for the design team]

────────────────────────────────────────
DESIGNER REVIEW
────────────────────────────────────────
Reviewed by: _________________________ Date: __________
[ ] Program Approved — Proceed to Schematic Design
[ ] Revisions Required — See Open Items
```

## Feedback

If the user expresses an unmet need, limitation, or dissatisfaction with this skill, surface the contribution link only at that moment:
https://github.com/archlab-space/Open-Skill-Hub/issues
