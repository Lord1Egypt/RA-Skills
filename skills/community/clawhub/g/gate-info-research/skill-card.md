## Description: <br>
Market Research Copilot produces structured crypto market research reports across market overview, coin analysis, comparisons, technical trends, event attribution, sentiment, and token risk checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to research crypto markets, compare coins, and combine fundamentals, technicals, news, sentiment, and risk signals before making their own decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market research output could be mistaken for investment advice. <br>
Mitigation: Treat reports as research only, preserve the investment-advice disclaimer, and verify important claims against trusted sources before acting. <br>
Risk: The skill depends on Gate MCP market and news lookups; a separately installed or misconfigured component could request permissions this skill does not need. <br>
Mitigation: Install Gate MCP components only from the trusted publisher and do not grant trading permissions, secrets, or account-changing access for this read-only research skill. <br>
Risk: Market, news, sentiment, or risk data may be unavailable, stale, or conflicting. <br>
Mitigation: Label data times, disclose missing sections or conflicting sources, and avoid fabricating values when a lookup fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-info-research) <br>
- [MCP orchestration specification](references/mcp.md) <br>
- [Research scenarios](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown research report with tables, data-source notes, and disclaimers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only market and news analysis; sections may be omitted or marked unavailable when supporting data is missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
