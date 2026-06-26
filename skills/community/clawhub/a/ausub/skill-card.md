## Description: <br>
AUSUB uses Tushare gold ETF market data and rule-based indicators to generate bounded dynamic dollar-cost averaging suggestions with rationale and risk notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juryory](https://clawhub.ai/user/juryory) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use AUSUB to fetch Tushare daily data for a gold ETF, evaluate rule-based market states, and produce disciplined periodic investment suggestions. It is intended as an execution aid with explicit risk reminders, not as a guarantee of returns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires TUSHARE_TOKEN and uses it to access Tushare. <br>
Mitigation: Install it only in an environment where exposing that token to this skill and Tushare is acceptable. <br>
Risk: Local user memory files may contain investment preferences or other personal financial context. <br>
Mitigation: Keep memory files private and avoid persisting sensitive income, expense, deposit, or savings details unless truly needed. <br>
Risk: The tushare dependency can affect data access and behavior over time. <br>
Mitigation: Review or pin the tushare package before use in managed environments. <br>
Risk: Investment suggestions could be misunderstood as guaranteed returns or personalized financial advice. <br>
Mitigation: Present outputs as disciplined dollar-cost averaging assistance, preserve risk notes, avoid leverage, and require user confirmation before saving plan changes. <br>


## Reference(s): <br>
- [Gold long-term return reference](references/gold-long-term-return.md) <br>
- [AUSUB ClawHub page](https://clawhub.ai/juryory/ausub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text reports and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include market summaries, indicator summaries, suggested multipliers, suggested amounts, trigger details, explanations, and risk notes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
