## Description: <br>
Analyze charts, OHLC bars, candlestick sequences, and trading context using Al Brooks style price action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ovels](https://clawhub.ai/user/ovels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders, analysts, and agent users use this skill to classify chart context, identify Brooks-style setups near the hard right edge, and decide whether a setup is actionable, watch-only, or no trade. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce discretionary market commentary that may be mistaken for personalized financial advice or an execution system. <br>
Mitigation: Treat outputs as chart-analysis guidance only, review conclusions independently, and do not use the skill as an automated trading or account-access system. <br>
Risk: Chart screenshots or analyst notes may expose private account details. <br>
Mitigation: Remove account identifiers, balances, positions, and other sensitive details before sharing inputs with the agent. <br>
Risk: Implicit invocation may apply the skill to trading-analysis prompts when the user expected a general response. <br>
Mitigation: Disable implicit invocation when the skill should run only after it is explicitly named. <br>


## Reference(s): <br>
- [Core Concepts](references/core_concepts.md) <br>
- [Market Context Checklist](references/market_context_checklist.md) <br>
- [Setup Taxonomy](references/setup_taxonomy.md) <br>
- [Entries And Exits](references/entries_and_exits.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown analysis with an optional JSON block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stable labels for market phase, Always In bias, setup status, direction, trade style, and confidence when structured output is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
