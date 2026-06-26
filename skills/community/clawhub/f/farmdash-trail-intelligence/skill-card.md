## Description: <br>
Read-only DeFi farming research skill for OpenClaw agents. Ranks Trail Heat, simulates farming outcomes with yield decay, audits sybil risk, and streams protocol events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External DeFi researchers and agent operators use this skill to compare protocols, simulate farming outcomes, monitor protocol events, and assess public-wallet sybil risk without executing transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public wallet addresses and route-sizing parameters may be sent to FarmDash when research tools are used. <br>
Mitigation: Use only public wallet data, avoid entering secrets, and review whether sending those public identifiers fits the user's privacy expectations. <br>
Risk: FarmDash route links may involve referral, affiliate, or routing compensation. <br>
Mitigation: Disclose the commercial relationship, link fee details when a FarmDash route is shown, and encourage users to verify canonical protocol destinations independently. <br>
Risk: DeFi research outputs, route quotes, and projected rewards can be mistaken for execution instructions or guaranteed financial outcomes. <br>
Mitigation: Present outputs as research, include uncertainty and downside warnings, and require a separate explicit execution path for any transaction. <br>
Risk: Users may accidentally provide private keys, seed phrases, signed messages, or transaction approvals to a research workflow. <br>
Mitigation: Refuse secret or signing material and remind users that this skill is read-only and does not need wallet write permissions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/parmasanandgarlic/skills/farmdash-trail-intelligence) <br>
- [FarmDash agent hub](https://www.farmdash.one/agents) <br>
- [FarmDash MCP configuration](https://www.farmdash.one/.well-known/mcp.json) <br>
- [FarmDash OpenAPI specification](https://www.farmdash.one/agents/openapi.yaml) <br>
- [FarmDash fee disclosure](https://www.farmdash.one/fees) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown research summaries with structured tables, warnings, and optional links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only DeFi research outputs; no transaction signing or execution] <br>

## Skill Version(s): <br>
1.0.15 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
