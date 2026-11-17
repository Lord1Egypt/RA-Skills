## Description:

Compute and report 25+ financial ratios from QBO data, producing a 9-tab Excel workbook with traffic-light scoring, DuPont decomposition, Altman Z-Score, 6-month trend charts, trend-reversal detection, CDC logging, and Month-End Close pipeline integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting and finance agents use this skill to run financial ratio analysis for QBO-connected clients, including profitability, liquidity, leverage, efficiency, growth, benchmark, trend, DuPont, and Altman Z-Score reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Excel workbooks may contain sensitive client financial records.

Mitigation: Write reports only to protected output directories and avoid synced or shared Desktop locations unless sharing is intended.

Risk: The .cache/financial-ratios CDC cache may retain client ratio history and prior-run financial values.

Mitigation: Secure or clear the cache according to the organization's financial-record retention policy.

## Reference(s):

- [Financial Ratio Analysis Skill Page](https://clawhub.ai/samledger67-dotcom/skills/financial-ratios)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated Excel workbook output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces FinancialRatios_{slug}_{YYYY_MM}.xlsx and maintains a .cache/financial-ratios/{slug}.json CDC cache.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
