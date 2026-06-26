## Description: <br>
Generates weekly monitoring reports for US retail brokerages and the broader trading ecosystem, including equity and options volume, broker operating metrics, crypto markets, exchange share, and prediction markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sarahwang94712](https://clawhub.ai/user/sarahwang94712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to generate or update weekly brokerage and trading-ecosystem monitoring reports covering IBKR, SCHW, HOOD, FUTU, market volume, crypto, and prediction-market indicators. It can also update a structured Excel workbook when the user supplies one. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated financial data, citations, or market interpretations may be incorrect, stale, or unsuitable for a user's decision-making context. <br>
Mitigation: Review generated financial data, citations, and assumptions before relying on the report. <br>
Risk: The workflow writes report and workbook outputs and may update a user-provided Excel workbook copy. <br>
Mitigation: Use a copy of any workbook and confirm before running the full workflow when the request is only a simple market question. <br>
Risk: Some market and broker sources refresh on different weekly, monthly, or quarterly cadences, so parts of a report may carry forward prior data. <br>
Mitigation: Check the data coverage table and carried-forward markers before treating a section as newly refreshed. <br>


## Reference(s): <br>
- [Report Template](report-template.md) <br>
- [Excel Database Structure](excel-structure.md) <br>
- [Metrics by Broker](metrics-by-broker.md) <br>
- [Dashboard Data Schema](dashboard-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Analysis, Guidance] <br>
**Output Format:** [Markdown report and Excel workbook outputs, with concise chat guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a weekly report and, when a workbook is provided, appends rows to a 16-sheet Excel database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
