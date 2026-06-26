# 8D Corrective Action Report

**Platforms:** Claude · Openclaw · Codex
**Domain:** Manufacturing

## Purpose

Drafts a complete Eight Disciplines (8D) corrective action report for a manufacturing nonconformance, supplier defect, internal scrap event, or customer complaint. Covers the full D0–D8 sequence used by OEM-mandated complaint handling under IATF 16949, including emergency response action, containment, 5-Why root cause analysis, and the corrective-vs-preventive action matrix with verification dates.

## When to Use

- Customer complaint or warranty escalation requiring a formal 8D response (Ford, VW, Stellantis, BMW, Toyota and other automotive / aerospace / medical-device OEMs)
- Internal nonconformance reports (NCRs) and high-PPM scrap events
- Supplier corrective action requests (SCAR) issued by a Tier 1 or OEM customer
- Recurrence of a previously closed defect — re-opening or escalating an existing 8D
- IATF 16949 / AS9100 / ISO 13485 problem-solving evidence for audit

## What It Does

**Phase 1: Scope and Intake**
1. Collects the trigger (customer complaint / internal NCR / SCAR / recurrence), reporting customer, part/program, affected lots, observed defect, current containment status, and any safety/regulatory implications
2. Confirms the team (D1) by role rather than name and verifies the problem-statement quantification (PPM, ppk impact, parts affected) before drafting
3. Tags every input as Confirmed / Assumed / Unknown and refuses to proceed if safety, regulatory, or recall risk is unclear

**Phase 2: Root Cause and Containment**
4. Drafts D0 (emergency response action) and D3 (interim containment) with quantities, locations, and effective-from dates
5. Builds a 5-Why chain for both the technical cause (why the defect occurred) and the systemic / detection cause (why the system did not prevent or detect it)
6. Maps each Why to an evidence type (measurement data, process record, FMEA reference, control plan line) and flags any Why that is asserted without evidence

**Phase 3: Corrective Action and Verification**
7. Produces D5 permanent corrective actions tied 1:1 to the root causes, with owners, target dates, and a measurable effectiveness criterion
8. Produces D6 implementation evidence prompts and D7 systemic preventive actions (FMEA update, control plan update, lessons-learned share)
9. Closes with D8 team recognition and a 6- and 8-month effectiveness check schedule
10. Runs a quality-gate checklist (no root cause skipped to symptom, no preventive action recycled from corrective, no missing verification date) before the report is considered submittable

## Output

A complete 8D report (D0–D8) with a problem-statement quantification block, a 5-Why technical and systemic chain, a corrective-vs-preventive action matrix, and a verification schedule. Marked **DRAFT** and explicitly requires sign-off by the quality engineer of record and the customer-quality representative before transmittal.

## Notes

The skill never invents measurement data, FMEA RPN numbers, control-plan references, or PPM. Every quantitative claim must be supplied by the user or marked Unknown. It does not generate safety-critical or recall recommendations on its own — if the trigger has safety or recall potential, it stops and instructs the user to escalate to the customer-quality and legal/regulatory teams before continuing.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.