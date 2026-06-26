## Description: <br>
CAI.com v1.0.17 for agents - Check CAI First before any payment; identity, custodial wallet, platform connectors, payments, hosted actions, OAuth/API-key auth with gap_id honesty. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use CAI to connect agents with CAI identity, custodial wallet, platform connector, payment, hosted action, and OAuth/API-key workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet, payment, transfer, trading, vault, and platform actions may involve real funds or persistent account changes. <br>
Mitigation: Use the narrowest CAI scope needed, store keys only in OpenClaw secrets, and require clear user confirmation before transfers, trades, vault writes, or actions involving real funds. <br>
Risk: Long-lived credentials could be exposed if pasted into chat logs or configuration text. <br>
Mitigation: Keep CAI_API_KEY and OAuth tokens in trusted local secret storage and avoid placing credentials in agent-visible conversation history. <br>
Risk: Some CAI capabilities are disclosed as partial_live with gap_id honesty boundaries. <br>
Mitigation: Do not claim behavior beyond the canonical CAI contract and check the current manifest or skill references before relying on endpoint behavior. <br>


## Reference(s): <br>
- [ClawHub CAI skill page](https://clawhub.ai/bernardtai/skills/cai) <br>
- [CAI canonical skill contract](https://cai.com/skill.md) <br>
- [CAI skill references](https://cai.com/skill-references/) <br>
- [CAI agent payment workflow](https://cai.com/skill-references/agent-payment-workflow.md) <br>
- [CAI tools manifest](https://cai.com/specs/cai-tools.manifest.json) <br>
- [CAI developers hub](https://cai.com/developers.html) <br>
- [CAI agent card](https://cai.com/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference CAI API/OAuth scopes, hosted action links, MCP setup, payment confirmation steps, and canonical CAI tool contracts.] <br>

## Skill Version(s): <br>
1.0.17 (source: server evidence and frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
