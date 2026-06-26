# Emergency After-Action Report

**Platforms:** Claude · Openclaw · Codex
**Domain:** Emergency Management

## Purpose

Turns evaluator notes, hotwash highlights, controller logs, and participant feedback into a HSEEP-aligned DRAFT After-Action Report and Improvement Plan (AAR/IP) for one exercise (discussion-based or operations-based) or one real-world incident. Produces Core-Capability performance ratings, an analysis narrative tied to exercise objectives, a SMART Improvement Plan matrix, and a Lessons Learned section.

**The output is always DRAFT.** The exercise director, lead evaluator, exercise sponsor, or incident commander must review every rating, every finding, and every corrective action — and sign the AAR/IP — before it is distributed.

## When to Use

- Post-exercise AAR for any HSEEP-defined exercise (seminar, workshop, tabletop, game, drill, functional, full-scale)
- Real-world incident AAR for an emergency-management agency, healthcare coalition, school / campus, utility, or transit system
- Grant-funded exercise documentation (HSGP, EMPG, PHEP, HPP, UASI, SHSP) where HSEEP compliance is required
- Hospital / healthcare-coalition exercise documentation supporting CMS, Joint Commission, or TJC emergency preparedness compliance
- Exercise-evaluator quality-control review of an AAR drafted by a participating agency
- Cross-jurisdictional exercise where multiple agencies must agree on findings before publication

## What It Does

**Phase 1: Scope the AAR**
1. Collects exercise / incident metadata: name, type, dates, sponsor, jurisdiction(s), participating organizations
2. Collects exercise objectives and the Core Capabilities each objective targeted
3. Collects scenario summary (and operational period for real-world incidents)
4. Confirms whether the AAR/IP is HSEEP-required (grant-funded) and whether classification controls apply (e.g., FOUO, CUI)

**Phase 2: Evidence Intake**
5. Logs evaluator observations against Exercise Evaluation Guides (EEGs) — capability targets, critical tasks, observed performance
6. Logs hotwash and participant-feedback themes
7. Logs controller logs, MSEL injects executed / not executed, and unanticipated branches
8. Tags every observation with the Core Capability, the capability target, the responsible org, and a strength / area-for-improvement label

**Phase 3: Rate and Analyze**
9. Rates each Core Capability using the standard four-level HSEEP rubric: Performed without Challenges (P), Performed with Some Challenges (S), Performed with Major Challenges (M), Unable to be Performed (U)
10. Writes a structured analysis section for each Core Capability: Strengths → Areas for Improvement → root cause (using the "5 Whys" or a barrier-analysis approach)
11. Cross-checks ratings against evidence — never rates a capability above the supporting observations

**Phase 4: Improvement Plan and Final Packet**
12. Drafts each corrective action as a SMART statement and maps it to a Core Capability and capability element (planning, organization, equipment, training, exercise — POETE)
13. Assigns a primary responsible organization, POC, start date, and completion date
14. Produces a Lessons Learned summary, an executive summary, and an Improvement Plan matrix
15. Lists unresolved-information items and any classification handling notes

## Output

A DRAFT HSEEP AAR/IP with: Executive Summary, Core Capabilities ratings table, Analysis of Core Capabilities (one section per capability), Conclusion / Lessons Learned, Improvement Plan matrix (one row per corrective action), and Appendices index (Improvement Plan stand-alone, Participant Feedback Summary, Acronyms, Exercise Schedule, Exercise Participants, References). All sections labeled `DRAFT — for exercise-director / incident-commander review and sign-off`.

## Notes

This skill never publishes an AAR or distributes it to participants. It never assigns ratings unsupported by evidence in the session, never invents critical-task names, and never assigns corrective actions to organizations the user has not confirmed are willing to own them. It does not handle classified, Law Enforcement Sensitive, or Protected Health Information beyond what the user explicitly provides — and it never includes PHI, attendee personal identifiers, or sensitive operational details in any external lookup or example.

It defaults to HSEEP-aligned language and the four-level capability rating rubric. Where the sponsor uses an older or alternate scheme (e.g., a custom three-level scale), it preserves the sponsor's scheme but maps each rating back to the HSEEP rubric in a side column.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
