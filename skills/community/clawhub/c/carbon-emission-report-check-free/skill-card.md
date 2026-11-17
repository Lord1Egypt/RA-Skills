## Description:

A free local checker that recalculates and cross-checks six China ETS emissions-report fields, cites source lines and numbers, and declines conclusions when required input is missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Energy, EHS, finance, and reporting teams at key emitting entities use this skill before third-party verification to check copied emissions-report tables for arithmetic and consistency issues. It helps agents run local checks on activity data, emission factors, oxidation rates, subtotals, unit conversions, duplicate rows, and missing fields.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may overread the output as a formal audit, regulatory determination, or verification opinion.

Mitigation: Treat results as table-internal arithmetic and consistency checks; keep third-party verification and regulatory review in the workflow.

Risk: Missing headers, blank fields, unsupported units, or malformed copied table text can prevent a reliable check.

Mitigation: Provide the full table header and data rows in the expected copied-text or JSON format; when input is insufficient, the skill reports missing material instead of making a finding.

Risk: The free version intentionally omits five checks available only in the complete edition.

Mitigation: Review the listed checks not run before relying on the result, especially prior-year comparisons, official factor-basis checks, quota comparisons, cross-version checks, and facility-by-scope summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/carbon-emission-report-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON emitted by a local Node.js runner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source lines and numeric values; insufficient input returns missing-field guidance instead of a conclusion.]

## Skill Version(s):

1.0.8 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
