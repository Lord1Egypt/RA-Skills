## Description:

Forecast Analysis Claw helps agents forecast SKU sales from historical CSV or Excel data, calculate replenishment recommendations, and summarize inventory risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

External users, business analysts, and developers use this skill to prepare sales data, run SKU-level or batch demand forecasts, and generate replenishment or stock-risk reports for inventory planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sales spreadsheets and forecast files can contain sensitive business data.

Mitigation: Install and run the skill in an isolated Python environment, keep input and generated files access-controlled, and avoid sharing raw sales data outside approved workflows.

Risk: Untrusted spreadsheet or CSV content may be unsafe to open directly in spreadsheet software.

Mitigation: Review and sanitize generated CSV data before opening it in spreadsheet tools, especially cells that could be interpreted as formulas.

Risk: Promotion forecasting and pushed stockout alerts are partly documented guidance rather than fully implemented automation.

Mitigation: Treat forecasts and replenishment quantities as decision-support outputs and manually review them against business context before purchasing or alerting actions.

## Reference(s):

- [Forecast Models](references/forecast-models.md)
- [Promotion Coefficients](references/promo-coefficients.md)
- [Replenishment Parameters](references/replenishment-params.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and generated CSV or text report outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write cleaned sales data, forecast results, or outlier report CSV files when the bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
