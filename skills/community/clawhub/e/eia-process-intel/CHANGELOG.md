# Changelog

All notable changes to this skill are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/), adheres to [Semantic Versioning](https://semver.org/).

## [0.3.0] - 2026-09-10

From a single-case evidence chain to a **recallable, evolvable, cross-case-reusable evidence-chain engine**: three research moves that were already happening implicitly are now explicit protocols. Methodology unchanged.

### Added
- **Credibility evolution protocol**: every high-risk field carries prior (grading table) → in-case evidence (status tag) → mandatory posterior (maintained / upgraded / downgraded, with deciding evidence). The prior table moves only on ≥2 independent case confirmations or a hard counter-example — single-case posteriors never edit it.
- **Anomaly-loop protocol**: four anomaly classes (validation conflict / mapping miss / caliber self-inconsistency / unexpected process-equipment combination) trigger bounded backtracking — hypotheses named, backtrack target named, every loop ends in a written artifact, 3-loop cap before escalating to an open DD question.
- **Cross-case aggregation**: three standard grep/join queries per engagement (capacity-vs-equipment ratio, per-process emission intensity, same-equipment fingerprint). Strict two-layer write rule — aggregation output lands in `cross-case-results.md` (fact layer); the mapping library updates only on stable patterns or clear counter-examples (judgment layer). Aggregation results are data, not knowledge.

### Changed
- Acceptance/verification monitoring reports (竣工验收监测报告) added to the external-source list — actual emissions, monitored load, actual-vs-budgeted investment; higher cross-validation value than the EIA filing itself.
- Mean-load power check added to capacity back-calculation (declared kWh ÷ declared hours vs the line's minimum configured load).

### Verified
- Field-calibrated end-to-end against a real acceptance report (nanoimprint track, 2026-09-10): ledger schema unchanged; grading table, mapping seed and recipes exercised; posterior, anomaly loop and aggregation protocols distilled from that run.

## [0.2.0] - 2026-09-10

### Changed
- SKILL.md rebuilt as an English-primary playbook following high-download skill patterns (analysis of the top-25 by downloads on ClawHub): trigger-style frontmatter description with numbered use-when scenarios, "When to Use" situation/action table up top, field-credibility grading table + threshold-hugging signatures + interest-review questions + cross-validation recipes pulled forward from references into the main body. Methodology unchanged — form only.
- Frontmatter slimmed to single-language (English) description; Chinese trigger keywords kept inline for matchability. Added clawdbot metadata (emoji).
- Removed the `en/` mirror — the root SKILL.md is now the English document; Chinese deep-dive references kept as-is.

## [0.1.3] - 2026-09-09

### Changed
- Republished fresh after deleting the ClawHub slug (registry retained the 0.1.2 version number, so this clean release carries 0.1.3). Content identical to 0.1.2: fully fictionalized worked example, no confidential case references anywhere in the package or its history.

## [0.1.2] - 2026-09-09

### Changed
- Worked example fully fictionalized: the demo no longer references any real company or filing (compliance — the original case reference is confidential). Example files renamed to `format-demo-ir-detector*.md`; all identifiers replaced with fictional placeholders.
- Public repository history rewritten to a single clean commit; pre-0.1.2 tags removed, so the confidential case reference does not remain in public git history.
- ClawHub slug deleted and republished fresh, clearing the immutable pre-0.1.2 registry versions that still contained the original example.

## [0.1.1] - 2026-09-09

### Changed
- SKILL.md now opens with an English overview (positioning, pointer to `en/SKILL.md`) so the ClawHub/GitHub landing view leads bilingual instead of Chinese-only. Runtime workflow unchanged.

## [0.1.0] - 2026-09-09

### Added
- Six-phase workflow: acquire → structured extraction → gaming review → cross-validation → inference → ledger booking
- Field credibility grading table (v1 prior): capacity / product mix / emissions = high risk; equipment count / physical info = low risk, used as trust anchors; threshold-hugging signature checklist; three interest-review questions
- Cross-validation recipes: capacity (cycle-time / material / energy methods), yield back-calculation from material balance (material-balance method), emission back-calculation, product-mix inference from hazardous-waste fingerprints; external source list (discharge permit platform, hazwaste manifests, penalty records, prospectuses, customs)
- Minimal ontology ledger schema v0.1: 8 entities, 8 relations (incl. gaming_trace), JSONL format with provenance (file + page + verbatim quote), game_risk and status tags per fact, failed-query-driven schema evolution
- Process→equipment mapping seed for semiconductor / IR detector / nanoimprint tracks (~22 rows, uncertain entries marked 【to verify】)
- Bilingual documentation (Chinese primary, full English mirror under `en/`)
- Worked format demo using a fictionalized IR-detector case (all numbers explicitly marked illustrative)
