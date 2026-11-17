## Description:

Create and manage AI agents, send USDC/USDT payments, check balances across Ethereum, BSC, and Tron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexcupe](https://clawhub.ai/user/hexcupe)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to configure AgentWallex credentials, manage agent wallets, inspect USDC/USDT balances, and prepare payment or transaction-status workflows across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles payment credentials and stores AgentWallex configuration locally.

Mitigation: Use sandbox keys first, avoid sharing production payment credentials in chat unless that exposure is acceptable, and protect the local configuration path with owner-only permissions.

Risk: The skill can initiate crypto transfers with under-scoped safety controls.

Mitigation: Require explicit review of recipient address, chain, token, and amount before transfer or pay actions, and verify the API base URL is an official AgentWallex HTTPS endpoint.

## Reference(s):

- [AgentWallex Skill Page](https://clawhub.ai/hexcupe/skills/agentwallex-openclaw)
- [AgentWallex](https://agentwallex.com)
- [AgentWallex Docs](https://docs.agentwallex.com)
- [AgentWallex Dashboard](https://app.agentwallex.com)
- [AgentWallex Sandbox Dashboard](https://app-sandbox.agentwallex.com)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces payment and wallet-management guidance that depends on local AgentWallex credentials and requires explicit confirmation for transfer or pay actions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
