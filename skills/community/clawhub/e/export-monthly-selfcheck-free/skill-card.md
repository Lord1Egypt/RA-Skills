## Description:

A Chinese-language, local-only checker for copied or exported foreign-trade accounting tables that performs deterministic monthly checks for export rebate calculations, export declaration and FX collection reconciliation, and foreign-currency settlement exchange gains or losses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

Proprietary

## Use Case:

Finance and treasury staff use this skill during monthly close or reconciliation to check copied table data for arithmetic consistency, totals, duplicates, missing values, and reproducible source-backed findings. It supports review of three free-version checks and does not replace tax, accounting, foreign-exchange, or compliance judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic consistency checks as tax, accounting, foreign-exchange, or compliance advice.

Mitigation: Treat results as reproducible table checks only, and have qualified reviewers confirm rates, policies, source documents, and filing decisions.

Risk: The skill does not read ERP exports, XLSX files, bank PDFs, or online tax and FX data directly.

Mitigation: Provide copied or exported table text with recognizable headers, and verify source-system records separately when direct file or online data review is required.

Risk: The free release omits some related checks, including export rebate document consistency and import tax calculation checks.

Mitigation: Review the reported checks_not_run and checks_out_of_scope fields before relying on coverage, and perform separate review for omitted checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/export-monthly-selfcheck-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Chinese-language text or JSON check report with findings, per-check status, summaries, and missing-input guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided table text or JSON input; no network access, API key, registration, or hidden privileged behavior is indicated by the security evidence.]

## Skill Version(s):

1.0.53 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
