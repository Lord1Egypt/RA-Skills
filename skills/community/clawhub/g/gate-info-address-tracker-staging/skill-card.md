## Description: <br>
Analyzes on-chain addresses with Gate-Info read-only tools to produce address profiles, holdings, risk notes, transaction history, and conditional fund-flow tracing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to inspect public blockchain addresses, summarize balances and labels, assess risk signals, and trace high-value transaction flows when the request or address profile warrants deeper analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A simple address lookup may expand into deeper transaction and fund-flow tracing when labels, balance, or risk flags trigger deep mode. <br>
Mitigation: Ask for Basic Mode or explicitly request no fund-flow tracing when only an address profile is needed. <br>
Risk: On-chain labels and fund-flow relationships may be incomplete or probabilistic. <br>
Mitigation: Present ownership, risk, and fund-flow conclusions as source-labeled observations and avoid definitive claims about natural persons. <br>


## Reference(s): <br>
- [Gate Address Tracker MCP Specification](references/mcp.md) <br>
- [Scenarios and Prompt Examples](references/scenarios.md) <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-info-address-tracker-staging) <br>
- [Publisher profile](https://clawhub.ai/user/gaixianggeng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown address analysis reports with tables, summaries, and explicit missing-data or risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Gate-Info MCP queries; deep tracing is conditional on user intent, known labels, high balance, or risk flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
