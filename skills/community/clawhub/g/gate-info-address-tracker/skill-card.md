## Description: <br>
Address tracker and analysis for on-chain addresses, including address profile lookup, transaction history, and fund-flow tracing through Gate-Info MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect an on-chain address, summarize wallet labels, balances, risk signals, DeFi positions, large transactions, and fund flows when Gate-Info MCP access is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried wallet addresses and inferred chain details are sent to the Gate-Info MCP provider. <br>
Mitigation: Use the skill only for addresses the user is comfortable querying through that provider, and avoid using it for harassment or personal tracking. <br>
Risk: The skill may deepen analysis for labeled, high-balance, or risk-flagged addresses even when the user asks a broad lookup question. <br>
Mitigation: Ask explicitly for a basic lookup when limited analysis is desired, and treat labels, risk scores, and flow summaries as provider-supplied signals rather than definitive identity claims. <br>
Risk: Fund-flow tracing can be unavailable or incomplete. <br>
Mitigation: Report missing fund-flow data plainly and avoid fabricating transaction edges, values, or ownership conclusions. <br>


## Reference(s): <br>
- [Gate Address Tracker MCP Specification](references/mcp.md) <br>
- [Scenarios & Prompt Examples](references/scenarios.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/gate-info-address-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown address analysis report with tables, fund-flow summaries, risk notes, and missing-data notices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only Gate-Info MCP lookups; depth and value thresholds vary by address size and user intent.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
