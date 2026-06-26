## Description: <br>
Virtual Mastercards for AI agents: crypto payments, USDC wallet setup, and autonomous virtual payment card management through x402 on Stellar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ASGCompute](https://clawhub.ai/user/ASGCompute) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use ASG Card to let MCP-capable agents create, fund, inspect, freeze, and unfreeze virtual Mastercard cards paid with USDC on Stellar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent real spending power through wallet-backed card creation and funding. <br>
Mitigation: Install only when that behavior is intended, use a dedicated Stellar wallet, and keep only limited USDC available. <br>
Risk: Virtual card details, including PAN and CVV, can be exposed by tool output. <br>
Mitigation: Require approval before sensitive card tools run and prevent card details from being logged, remembered, or sent through Telegram unless that exposure is accepted. <br>
Risk: Plaintext wallet secrets or high-value keys could be exposed through local configuration. <br>
Mitigation: Avoid storing high-value private keys in plaintext configs and use a purpose-limited wallet for agent activity. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ASGCompute/agentcard) <br>
- [ASG Card Documentation](https://asgcard.dev/docs) <br>
- [ASG Card Website](https://asgcard.dev) <br>
- [ASG Card SDK on npm](https://npmjs.com/package/@asgcard/sdk) <br>
- [Technical Overview](TECHNICAL_OVERVIEW.md) <br>
- [Security Policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown instructions with inline shell commands and MCP tool responses as JSON-like text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can expose wallet status, payment actions, and sensitive virtual card details when tools are invoked.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata; artifact SKILL.md frontmatter says 1.0.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
