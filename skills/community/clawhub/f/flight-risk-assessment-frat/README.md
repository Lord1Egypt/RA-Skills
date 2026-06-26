# Flight Risk Assessment (FRAT)

**Platforms:** Claude · Openclaw · Codex
**Domain:** Aviation

## Purpose

Runs a pre-flight Flight Risk Assessment Tool (FRAT) for a single planned flight using the FAA Safety Team's PAVE (Pilot, Aircraft, enVironment, External pressures) framework plus IMSAFE pilot self-assessment, scoring every item with rationale, mapping the total to Green / Yellow / Red, recommending mitigations per identified hazard, naming the appropriate dispatch authority, and producing a defensible FRAT log for the operator's Safety Management System (SMS). The output supports — but never replaces — the pilot-in-command's go / no-go decision.

## When to Use

- Pre-flight planning for any Part 91, Part 135, Part 137, Part 141, public-use, or business-aviation flight
- Single-pilot operations where a structured second opinion is valuable
- Operators preparing for FAA Part 135 SMS compliance (mandatory by 28 May 2027)
- Air-medical, air-tour, and helicopter operations integrating FRAT into a dispatch workflow
- Flight schools standardizing student-pilot risk awareness
- After a change in conditions (weather, MEL, fatigue, schedule) when a fresh FRAT is needed
- Post-flight debrief or training exercises reconstructing risk reasoning

## What It Does

**Phase 1: Flight & Operator Context**
1. Captures operator, regulation part, mission type, planned route, departure / arrival / alternate(s), and ETD
2. Confirms whether this is an initial FRAT or a re-FRAT triggered by changed conditions

**Phase 2: Pilot (P) — IMSAFE and Currency**
3. Walks IMSAFE — Illness, Medication, Stress, Alcohol, Fatigue, Eating
4. Captures certificate level, ratings, total time, time-in-type, recent experience (30 / 60 / 90 days), instrument currency, dual within 90 days, WINGS phase, BFR / 61.58 / 135.293 currency

**Phase 3: Aircraft (A)**
5. Captures aircraft type, equipment (IFR / GPS / autopilot / weather-data / TAWS / TCAS / icing), MEL / CDL items deferred, fuel load and reserve plan, weight & balance margin

**Phase 4: enVironment (V)**
6. Captures departure / en-route / destination / alternate weather (ceiling, visibility, wind, crosswind, gusts, convective, icing, turbulence, IFR / MVFR / VFR), terrain, density altitude, day / night / twilight, NOTAMs, TFRs

**Phase 5: External Pressures (E) and Scoring**
7. Captures passenger expectations, business / schedule pressure, family / personal pressure, get-home-itis indicators, and reputational pressure
8. Scores each PAVE category with rationale, computes the total, maps to Green / Yellow / Red
9. Produces a mitigation plan per identified hazard and a dispatch-authority recommendation (PIC alone / Chief Pilot consult / Director of Operations consult / Cancel)
10. Names the re-FRAT triggers — what conditions require running this assessment again
11. Always labels the output **"DRAFT — FINAL GO / NO-GO IS THE PILOT-IN-COMMAND'S DECISION"**

## Output

A FRAT log with flight identifiers, scored PAVE breakdown, IMSAFE self-assessment, total score with risk color, named hazards, per-hazard mitigations, dispatch-authority recommendation, re-FRAT triggers, and a mandatory review banner.

## Notes

This skill **drafts** a Flight Risk Assessment to support — never replace — the pilot-in-command's go / no-go decision under 14 CFR §91.3, §91.103, §91.13, the operator's General Operations Manual, and applicable Part 135 / 121 / 137 / 141 rules. The skill does not file flight plans, does not dispatch the flight, does not retrieve weather (the user provides current sources), and does not opine on airworthiness — those determinations belong to the PIC, dispatcher, chief pilot, director of operations, and maintenance personnel as applicable. No personal identifying information about passengers is collected. The skill never minimizes a hazard to "get the flight out"; if the user pushes for a Green when items score Yellow / Red, the skill holds the assessment and re-states the mitigation gap.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
