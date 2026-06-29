## Description: <br>
Predicts short-term direction and magnitude for on-exchange A-share ETFs by weighting the top holdings, analyzing component-stock technical signals and funds flow, and cross-checking against the ETF's own indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bianchunhui](https://clawhub.ai/user/bianchunhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to generate structured ETF market-analysis reports for A-share ETFs, including top-holding breakdowns, weighted short-term predictions, ETF signal cross-checks, confidence levels, and risk reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Short-term ETF predictions may be interpreted as personalized trading advice. <br>
Mitigation: Present the output as market analysis only, keep the investment-advice disclaimer visible, and encourage users to verify data before acting. <br>
Risk: ETF holdings and weights can be stale or drift from reported top-holding data. <br>
Mitigation: Verify current holdings and market data before relying on the weighted calculation, especially around reporting updates or major events. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bianchunhui/etf-holdings-predictor) <br>
- [Publisher profile](https://clawhub.ai/user/bianchunhui) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Structured Markdown report with tables and concise risk reminders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ETF code or name input and presents weighted prediction, ETF cross-check, confidence, and trading-risk context.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
