## Description: <br>
Tracks public U.S. congressional stock trades, highlights concentrated buying and anomaly signals, and helps relate trading activity to committee and policy context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goatdeesign](https://clawhub.ai/user/goatdeesign) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to fetch public congressional stock-trade data and generate structured reports on holdings concentration, unusual trading patterns, and possible policy context. Outputs should be treated as research leads and not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public congressional trade disclosures can be delayed or incomplete, so results may not reflect current holdings or exact transaction values. <br>
Mitigation: Disclose the reporting delay, verify important records against public sources, and avoid treating the output as real-time market data. <br>
Risk: Anomaly and policy-catalyst interpretations may be incorrect or overstated if used as financial conclusions. <br>
Mitigation: Present interpretations as research leads, include the non-investment-advice disclaimer, and independently verify material conclusions. <br>
Risk: The skill fetches public web data and can write local output files when a path is selected. <br>
Mitigation: Run it only in an environment where outbound public-data requests and local report-file creation are acceptable. <br>


## Reference(s): <br>
- [Analysis Framework](references/analysis_framework.md) <br>
- [Committee Industry Map](references/committee_industry_map.md) <br>
- [Capitol Trades](https://www.capitoltrades.com/trades) <br>
- [ClawHub Skill Page](https://clawhub.ai/goatdeesign/congress-stock-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Analysis] <br>
**Output Format:** [Markdown reports with structured tables; optional JSON or CSV from the data-fetch script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write report or data files locally when an output path is selected.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
