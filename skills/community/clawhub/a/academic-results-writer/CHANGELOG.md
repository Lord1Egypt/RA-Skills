# Changelog

## v1.2.1 — Chinese Localization (2026-05-26)

- README.md fully localized to Chinese.
- SKILL.md description localized to Chinese.
- Public version: 1.2.1.

## v1.2.0 — Stable Release (2026-05)

- Stable release with all v1.1-patch4-cleanup-bridge-file rules consolidated.
- Added file-output mode for long target-paper adaptation, Module H bridge workflows, and truncation recovery.
- Added preferred handling for Module H Writer Transfer Packet from paper-results-reverse-engineer v3.0+.
- Default output: standard-depth; full audit-depth on user request.
- All source-integrity, anti-plagiarism, and statistical guardrails retained.
- Public version: 1.2.0 | Internal version: academic-results-writer-v1.2.0-stable

---

## v1.1 (2026-05-17) — Target-Paper Results Style Adaptation Mode

- Added Target-paper Results Style Adaptation Mode, including:
  - Target Results style profiling (§19)
  - Design-match checks
  - Structure-only transfer
  - Source-integrity rules (§20)
  - Anti-plagiarism guardrails
- Enhanced reverse-engineer v3.0 integration with risk flag rule.

### v1.1-patch1
- Added target-paper risk extraction rule, transferable-vs-risky style distinction, derived-statistic source rule, EEG–behavior wording reinforcement for target-paper mode.

### v1.1-patch2
- Added no-assumed-target-metadata rule, no-placeholder-table/figure-in-direct-Results rule, target-mode variable translation rule, cross-sectional mediation statistical-effect prefix rule.

### v1.1-patch3
- Added strict target-source resolution and fail-closed rule, input decontamination rule, minimum evidence rule for target Results extraction, gating rule for 8-section format.

### v1.1-patch4
- Added remote-source clarity, partial target extraction limits, design-incompatible target fallback, anti-test-context carryover rule.

### v1.1-patch4-cleanup
- Refined default output depth, strengthened pre-to-post wording in sleep EEG Results, clarified Figure/Table reference exceptions, added Chinese statistical-format consistency rule.

### v1.1-patch4-cleanup-bridge
- Added preferred handling for Module H Writer Transfer Packet from paper-results-reverse-engineer v3.0-bridge.

### v1.1-patch4-cleanup-bridge-file
- Added file-output mode for long target-paper adaptation, Module H bridge workflows, design-incompatible fallback outputs, full audit outputs, and truncation recovery.

---

## v1.0 (2026-05-17) — Initial Release

- Initial release with write-from-statistics, revise-draft, table-to-results, figure-to-results, audit-only, journal-style capabilities.
- Statistical reporting templates for t-test, ANOVA, regression, mediation/moderation, LMM, chi-square, meta-analysis, sleep EEG, fMRI/EEG, and qualitative studies.
- Chinese and English academic writing templates.
- Figure/Table narrative templates.
- Results vs Discussion boundary rules.
- Certainty continuum (strongest → weakest phrasing).
- Quality checklist and Do-Not rules.

### v1.0-patch1
- Added pre-post sleep wording guardrail, derived marginal mean rule, warning against compressed omnibus-statistic expressions.

### v1.0-patch2
- Added figure error-bar terminology rule (SD/SE/CI distinction).

### v1.0-patch3
- Added Revision Mode source-boundary rule and missing-statistics handling (A/B/C classification).

### v1.0-patch4
- Refined Revision Mode: moved null-result meta-explanations out of formal Results draft; added missing-control-wording rule and partial-design-information handling.

### v1.0-patch5
- Added bootstrap-count source rule, no-unsolicited-citation rule, mediation magnitude wording rule, variable-translation fidelity rule.

### v1.0-patch6
- Added figure visual-language source rule (no visual claims without actual image).

### v1.0-patch7
- Added meta-analysis wording guardrails for trim-and-fill adjusted effect significance, robustness under I² ≥ 50%, and Q-test/random-effects interpretation; upgraded to hard-self-check level.

### v1.0-patch8
- Added EEG–behavior correlation wording guardrail; LMM dummy-coding interpretation rule, marginal simple-slope wording rule, predicted-effect wording guardrail.
