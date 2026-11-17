## Description:

AWP Skill helps agents work with Agent Work Protocol operations across Base, Ethereum, Arbitrum, and BSC, including onboarding, staking, allocations, worknet management, governance, and queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kilb](https://clawhub.ai/user/kilb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to onboard AWP wallets, query protocol state, and prepare or run AWP worknet, staking, allocation, binding, and governance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet setup and transaction-signing workflows can affect funds or protocol positions.

Mitigation: Use only a dedicated AWP work wallet, avoid storing personal assets in it, and confirm every transaction or signature request before execution.

Risk: External repository based setup can change after publication.

Mitigation: Verify the awp-wallet repository or pin a trusted release before running install.sh.

Risk: Worknet skill installs may rely on repositories that later change.

Mitigation: Review trusted-namespace worknet skill installs before deployment and scan them again when versions change.

## Reference(s):

- [AWP Skill on ClawHub](https://clawhub.ai/kilb/skills/awp)
- [Publisher Profile](https://clawhub.ai/user/kilb)
- [AWP Skill Repository](https://github.com/awp-core/awp-skill)
- [AWP Wallet Repository](https://github.com/awp-core/awp-wallet)
- [AWP JSON-RPC API](https://api.awp.sh/v2)
- [API Reference](references/api-reference.md)
- [Protocol Reference](references/protocol.md)
- [Staking Commands](references/commands-staking.md)
- [Worknet Commands](references/commands-worknet.md)
- [Governance Commands](references/commands-governance.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, JSON API payloads, and script invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local scripts and user wallet/session state when guiding AWP protocol operations.]

## Skill Version(s):

1.7.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
