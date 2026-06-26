## Description: <br>
Analyzes A-share stocks for ST, delisting, accounting, cash-flow, leverage, audit, and related financial risk signals using cn-stock-data and current web evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzswk](https://clawhub.ai/user/yzswk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to screen A-share companies for financial distress, ST warning, and delisting-risk signals before relying on investment research or follow-up analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation phrases can cause generic safety or risk questions to trigger investment-style analysis. <br>
Mitigation: Require a stock, ticker, or company context before relying on the output, and prefer narrower activation phrases or disambiguation. <br>
Risk: Financial data can lag disclosures or be unavailable, which may make risk conclusions incomplete. <br>
Mitigation: State the reporting period used, disclose missing data, and avoid fabricating unavailable figures. <br>
Risk: Outputs may be mistaken for investment advice. <br>
Mitigation: Present results as reference analysis only and preserve the skill's caution that it does not constitute investment advice. <br>


## Reference(s): <br>
- [A Share Risk Alert release page](https://clawhub.ai/yzswk/a-share-risk-alert) <br>
- [A-share risk alert guide](references/risk-alert-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown risk report or brief summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formal mode includes company context, risk-signal analysis, risk level, ST/delisting assessment, and cautions; brief mode summarizes risk level, triggered signals, and conclusion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
