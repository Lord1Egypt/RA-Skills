## Description: <br>
Screens A-share and Hong Kong-listed stocks using technical indicators, capital-flow signals, and fundamentals, with multi-factor filtering and ranked results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tingdall](https://clawhub.ai/user/tingdall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to screen A-share and Hong Kong-listed equities against technical, capital-flow, and fundamental criteria, then produce ranked stock-selection results for research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock-screening results may be mistaken for investment advice. <br>
Mitigation: Present rankings as research support only and advise users to verify data and make independent decisions. <br>
Risk: Market data or screening signals may be stale, incomplete, or inaccurate. <br>
Mitigation: Require independent verification of prices, fundamentals, and capital-flow data before relying on results. <br>
Risk: Broad trigger wording such as general requests to find something may activate the stock-screening workflow unintentionally. <br>
Mitigation: Confirm the user intends a stock-screening task before applying screening criteria. <br>
Risk: Users may disclose brokerage credentials or private account details while discussing stock screening. <br>
Mitigation: Do not request or accept brokerage credentials, account access, or private account information. <br>


## Reference(s): <br>
- [Screening Criteria](artifact/references/screening-criteria.md) <br>
- [ClawHub Release Page](https://clawhub.ai/tingdall/china-stock-screener) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown tables with ranked screening results and per-stock rationale] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should be treated as research support and not as financial advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
