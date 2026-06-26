## Description: <br>
Computes 25+ profitability, liquidity, leverage, efficiency, and growth ratios from QBO data and produces a 9-tab Excel workbook with scoring, DuPont decomposition, Altman Z-Score, trend charts, trend-reversal detection, CDC logging, and Month-End Close integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting and finance teams use this skill to generate financial ratio analysis for a QBO-connected client, including profitability, liquidity, leverage, efficiency, growth, DuPont, Altman Z-Score, benchmarking, and trend-reversal analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workbooks and cache files can contain sensitive client accounting data. <br>
Mitigation: Install only in an approved environment and store or delete generated files according to organizational data-handling rules. <br>
Risk: Running against the wrong QBO client slug or account can produce misleading reports or expose client data. <br>
Mitigation: Confirm the QBO client slug/account before running the skill. <br>
Risk: The skill invokes a local Python pipeline script to process financial data. <br>
Mitigation: Verify that the referenced local Python script is trusted before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/financial-ratios) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash invocation examples and generated Excel workbook and JSON cache files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces FinancialRatios_{slug}_{YYYY_MM}.xlsx and .cache/financial-ratios/{slug}.json; outputs can contain sensitive client accounting data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
