## Description:

Finance Tools helps agents run local CSV-based finance analysis workflows, including income and expense summaries, financial ratios, trends, category rollups, budget comparisons, year-over-year analysis, and forecasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cqdev-ai](https://clawhub.ai/user/cqdev-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this skill to analyze local finance or transaction CSV files and select commands for budgeting, ratios, trends, categories, growth analysis, and forecasts. Outputs should be treated as analytical support, not financial or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted or untrusted CSV values could make terminal output misleading.

Mitigation: Use trusted or sanitized CSV files and review the displayed results before acting on them.

Risk: Automatic column detection can select the wrong amount, date, category, budget, or actual column.

Mitigation: Inspect the CSV headers and validate the detected mapping against the source data before relying on summaries, ratios, or forecasts.

Risk: Forecasts and financial ratios may be mistaken for professional financial advice.

Mitigation: Treat outputs as decision support only and review important conclusions with appropriate accounting, finance, or business expertise.

Risk: The artifact is primarily documented and presented in Chinese, which may affect review by users who do not read Chinese.

Mitigation: Have a qualified reader verify commands, warnings, and output labels before operational use in non-Chinese-language workflows.

## Reference(s):

- [ClawHub Finance Tools skill page](https://clawhub.ai/cqdev-ai/skills/finance-tools)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and terminal-output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided CSV files; results depend on automatic column detection and user review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact files describe 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
