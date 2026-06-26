# Building Code Egress Review

**Domain:** Architecture · Building Code Compliance
**Platforms:** Claude · Codex

## Purpose

Reviews a proposed building design against **IBC 2024 Chapter 10 (Means of Egress)** and produces a structured, defensible egress analysis a registered design professional (architect / engineer of record) and the Authority Having Jurisdiction (AHJ) can review. The analysis covers per-space occupant load, required vs provided egress capacity, number of exits, common path of egress travel, exit access travel distance, dead-end corridor limits, corridor width and rating, accessible means of egress, and any relevant special-occupancy provisions.

The output is always labeled **DRAFT** and is not a code-compliance certification.

## When to Use

- An architect or code consultant doing an early-stage code analysis or coordination check
- A junior architect preparing a §107 code summary sheet for permit submission
- An AHJ plan-review staffer building a structured deficiency list
- A code-of-record reviewer cross-checking egress before stamping a set

## What It Does

1. Collects project, occupancy, building, space, exit, and accessibility data through one-question-at-a-time intake
2. Confirms a scope summary (code edition, construction type, sprinkler / standpipe posture, occupancy approach) before drafting
3. Builds an **Occupant Load Table** per IBC §1004 with cited Table 1004.5 load factors
4. Builds an **Exit Capacity Matrix** (§1005, §1006), a **Travel Distance & Path Matrix** (§1006.2.1, §1017, §1020), and an **Accessible MoE Matrix** (§1009) with section-cited verdicts
5. Runs special-condition checks (Assembly, Group H, Group I-2 / I-3, atrium, mall, storm shelter, high-piled storage) only when applicable
6. Produces a ranked deficiency list with specific design fixes, an unresolved-information list, and an advisory overall verdict labeled **DRAFT — REGISTERED DESIGN PROFESSIONAL AND AHJ REVIEW REQUIRED**

## Notes

This skill produces a **DRAFT egress analysis**, not a code-compliance certification. It does not substitute for the registered design professional's seal, does not bind the Authority Having Jurisdiction, and never resolves AHJ-reserved items (§104.11 alternative materials and methods, performance-based design, occupant-load increases under §1004.5.1, equivalency).

Always cite the IBC section adopted by the AHJ. Where the AHJ adopts NFPA 101 instead of IBC Chapter 10, do not run this skill — it scopes only to IBC 2024 Chapter 10. Sprinkler-dependent egress allowances are gated on the sprinkler system reported by the user.

Do not paste project addresses, owner names, or permit numbers into intake. Use a project codename.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
