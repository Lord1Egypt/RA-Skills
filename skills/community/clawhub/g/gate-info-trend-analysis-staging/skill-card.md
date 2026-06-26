## Description: <br>
Performs read-only single-coin crypto trend and technical analysis using Gate Info market data, including K-line data, indicators, multi-timeframe signals, and market snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce a structured technical analysis report for one cryptocurrency from read-only Gate market data and standard technical indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Technical analysis may be mistaken for investment advice or a price prediction. <br>
Mitigation: Treat results as informational, avoid trade instructions or specific price predictions, and include limitations and risk warnings. <br>
Risk: Missing, stale, or unavailable market-data tool results can weaken the analysis. <br>
Mitigation: Disclose unavailable data, label timeframes and indicator settings, and downgrade confidence when inputs are incomplete. <br>
Risk: The skill depends on Gate Info market-data MCP tools being available in the current agent environment. <br>
Mitigation: Confirm the required Gate Info MCP server before use and return a clear unavailable-data response when tools fail. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-info-trend-analysis-staging) <br>
- [Gate Info TrendAnalysis MCP Specification](references/mcp.md) <br>
- [Scenarios and Prompt Examples](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown 7-section technical analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only output with timeframe labels, indicator settings, data availability notes, and informational risk warnings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
