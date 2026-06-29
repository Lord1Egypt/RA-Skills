## Description: <br>
Read-only DeFi farming research skill for OpenClaw agents that ranks Trail Heat, simulates farming outcomes with yield decay, audits sybil risk, and streams protocol events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research DeFi farming opportunities, compare protocols, estimate point outcomes, review wallet and protocol risk indicators, and receive read-only guidance before making their own execution decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public wallet addresses, route parameters, and an optional FarmDash API key may be sent to FarmDash. <br>
Mitigation: Use the skill only when that data sharing is acceptable, keep private keys and seed phrases out of the workflow, and provide FARMDASH_API_KEY only for higher-rate features. <br>
Risk: DeFi rankings, simulations, and protocol suggestions may be mistaken for financial advice. <br>
Mitigation: Treat outputs as research, verify protocols and fees independently, and require the user to make any execution decision outside this read-only skill. <br>
Risk: FarmDash go links may involve referral or routing compensation. <br>
Mitigation: Disclose the compensation relationship when presenting a route and include the fee reference so users can compare independently. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-trail-intelligence) <br>
- [Publisher profile](https://clawhub.ai/user/parmasanandgarlic) <br>
- [FarmDash Agent Hub](https://www.farmdash.one/agents) <br>
- [FarmDash OpenAPI schema](https://www.farmdash.one/agents/openapi.yaml) <br>
- [FarmDash MCP configuration](https://www.farmdash.one/.well-known/mcp.json) <br>
- [FarmDash fee structure](https://www.farmdash.one/fees) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown text with tables, risk warnings, route disclosures, and optional setup snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only DeFi research output; Scout tier can be keyless, while optional FARMDASH_API_KEY enables higher-rate Pioneer features.] <br>

## Skill Version(s): <br>
1.0.16 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
