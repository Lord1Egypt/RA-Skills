## Description: <br>
Provides fundamental equity analysis and peer ranking using structured scoring across business quality, balance-sheet safety, cash flow, valuation, sector adjustments, and confidence modifiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NickFiorani](https://clawhub.ai/user/NickFiorani) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to analyze one or more public stock tickers, compare peers, choose a best pick, and produce fundamentals-based verdicts with confidence, risks, valuation justification, and sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may produce decisive stock opinions using public market data and news. <br>
Mitigation: Treat outputs as educational, verify cited financial data independently, and avoid using the output as personalized investment advice. <br>
Risk: Financial analysis can be affected by stale, missing, or conflicting public data. <br>
Mitigation: Use the playbook's data quality scorecard, source hierarchy, and confidence caps; mark unavailable metrics as NA instead of fabricating values. <br>
Risk: Users could expose sensitive financial or account information while requesting analysis. <br>
Mitigation: Do not provide brokerage credentials, private account details, or non-public information. <br>


## Reference(s): <br>
- [Fundamental Stock Analysis Playbook](artifact/references/playbook.md) <br>
- [ClawHub skill page](https://clawhub.ai/NickFiorani/fundamental-stock-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis with ticker verdicts, scorecards, peer rankings, news links, and source attribution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Educational and informational output; no machine-readable JSON block; stale, missing, or conflicting data must be called out with confidence adjustments.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
