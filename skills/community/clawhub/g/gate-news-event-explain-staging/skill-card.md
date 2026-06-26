## Description: <br>
Explains why a crypto asset pumped or dumped by linking recent events, market snapshots, and on-chain context into an attribution report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to explain abnormal crypto price moves with a concise event attribution report. It is intended for read-only market commentary and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto market explanations can overstate causality when events, market data, or on-chain signals are incomplete. <br>
Mitigation: Treat the report as market commentary, preserve uncertainty, and avoid buy, sell, or hold recommendations. <br>
Risk: The skill depends on Gate News and Gate Info MCP servers being available and trusted in the agent environment. <br>
Mitigation: Confirm the required MCP servers and shared runtime rule files are present and trusted before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-news-event-explain-staging) <br>
- [Gate News EventExplain MCP Specification](references/mcp.md) <br>
- [Scenarios and prompt examples](references/scenarios.md) <br>
- [Gate.com](https://www.gate.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown attribution report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only synthesis using event, market, and on-chain context; includes uncertainty language when no single trigger is clear.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
