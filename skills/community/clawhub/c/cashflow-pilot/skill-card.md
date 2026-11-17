## Description:

现金流领航 helps small and medium business owners manage income and expenses, import bills, generate cash-flow reports, track receivables and payables, and forecast future cash flow in Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjing5024064](https://clawhub.ai/user/hanjing5024064)

### License/Terms of Use:

MIT-0

## Use Case:

External small and medium business owners use this skill to maintain a local cash-flow ledger, import CSV bill data, review monthly reports, manage receivables and payables, and generate short-horizon cash-flow forecasts. It is intended for Chinese-language bookkeeping assistance and management insight, not audited accounting advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive business financial records are stored locally as plaintext JSON files.

Mitigation: Use a private CFP_DATA_DIR on an encrypted disk and avoid shared or synced folders for business records.

Risk: Imported CSV text can affect generated Markdown or Mermaid reports.

Mitigation: Review imported CSV data and generated reports before sharing or relying on them.

Risk: Cash-flow forecasts are based on historical data and may be inaccurate for business decisions.

Mitigation: Treat forecasts as planning support and compare them with current business context before making financial commitments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanjing5024064/skills/cashflow-pilot)
- [Cashflow report templates](artifact/references/report-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Chinese Markdown reports, tables, Mermaid chart blocks for paid features, JSON-backed local ledger files, and inline shell commands for bundled Python scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional CFP_SUBSCRIPTION_TIER and CFP_DATA_DIR environment variables; free and paid tiers expose different reporting, import, reminder, and forecasting features.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
