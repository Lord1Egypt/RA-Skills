# PLAN.md — competitive-intel skill build
**Status:** IN PROGRESS
**Started:** 2026-03-20
**Classification:** Data fetching / analysis (research pipeline with structured output)
**Scope:** Plugin skill — ClawHub distribution target

---

## Design Decisions

- Two modes: Quick Scan (5–8 sources, inline output) vs Deep Dive (15+ sources, saved to workspace)
- Trust differentiator: every factual claim tagged with evidence tier (HIGH/MEDIUM/LOW/INFERRED)
- No external API dependencies — runs on web_search + web_fetch
- Output format is structured Markdown, not prose paragraphs
- Customer language mining is a first-class section (not an afterthought)
- Example report is DTC-adjacent (fictional adaptogen brand "Rootwell") — demonstrates the skill working for Muhammad's world

## File Plan

```
competitive-intel/
├── PLAN.md                           ← this file
├── SKILL.md                          ← trigger, protocol, gotchas
├── references/
│   ├── report-template.md            ← full output format spec
│   ├── evidence-tiers.md             ← tier definitions + usage rules
│   └── example-report-dtc.md         ← worked DTC example (Rootwell)
└── scripts/
    └── save-report.sh                ← saves output to workspace/research/competitive-intel/
```

## Progress

- [x] PLAN.md
- [x] SKILL.md
- [x] references/report-template.md
- [x] references/evidence-tiers.md
- [x] references/example-report-dtc.md
- [x] scripts/save-report.sh
- [x] Verify: trigger language is precise, not summary
- [x] Verify: gotchas cover the real failure modes (7 gotchas: market size, pricing timestamp, incentivized reviews, missing data as finding, scope creep, feature hallucination, web fetch limits, competitor type ambiguity)
- [x] Verify: example report demonstrates all four evidence tiers (HIGH x2, MEDIUM x20, LOW x1, INFERRED x4)
- [x] Verify: mixed-tier violations fixed ([MEDIUM — INFERRED] → [INFERRED])
- [x] Verify: no dead references — all 3 support files exist
- [x] Verify: save script syntax clean
- [x] Dogfood check: triggers precise, gotchas grounded, example self-demonstrates

- [x] Extended constitution pass: Setup section added
- [x] Extended constitution pass: Tools section added (declarative + fallback)
- [x] Extended constitution pass: Verification section added (checklist + edge case table + pass/fail signal)
- [x] Extended constitution pass: Blast Radius and Hooks documented (explicit decisions, not defaults)
- [x] Read discipline: all files fully read before edits (no truncation; 119→169 lines SKILL.md, 73 ev-tiers, 59 script)
- [x] Untrusted-input: no external content in skill affects execution policy
- [x] Atomicity: changes are targeted additions only; no scope drift

## Status: READY FOR CLAWHUB PUBLISH

## Constraints

- SKILL.md must be tight — protocol and gotchas, no generic best-practice filler
- Description field must tell the model WHEN to invoke, not WHAT the skill does
- No hallucinated data in the example report — all claims must be plausible and clearly staged
- Support files must add leverage, not just bulk
- Do not over-railroad the research protocol — encode structure without locking one brittle path
