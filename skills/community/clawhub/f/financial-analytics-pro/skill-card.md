## Description:

Financial Analytics Pro helps business owners, financial professionals, and analysts analyze financial data, calculate ratios, forecast cash flow, create visualizations, and generate financial reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacealllc](https://clawhub.ai/user/jacealllc)

### License/Terms of Use:

MIT-0

## Use Case:

Small business owners, financial analysts, accountants, e-commerce operators, investors, and startup teams use this skill to inspect financial statements, calculate ratios, forecast performance, and produce concise reports from local financial data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises bank, brokerage, and accounting integrations that could involve sensitive financial records.

Mitigation: Use local sample or exported data first, avoid connecting live accounts unless the publisher provides clear OAuth, token storage, retention, and revocation details, and treat generated reports and charts as confidential financial records.

Risk: The artifact recommends broad, unpinned package installation for financial analysis dependencies.

Mitigation: Install in a dedicated virtual environment, prefer pinned dependencies or a lockfile, and remove optional packages that are not needed for the intended workflow.

Risk: Financial forecasts, ratios, and reports can be incomplete or misleading if source data is missing, stale, or mapped to unexpected columns.

Mitigation: Review input data, generated calculations, and report outputs before making business, investment, tax, or compliance decisions.

## Reference(s):

- [Financial ratios cheat sheet](references/financial_ratios_cheat_sheet.md)
- [Financial Analytics Pro on ClawHub](https://clawhub.ai/jacealllc/skills/financial-analytics-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, Python code behavior, JSON reports, and generated chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read CSV or Excel financial data and write JSON reports or PNG visualizations when the included analyzer script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
