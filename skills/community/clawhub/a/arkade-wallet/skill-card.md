## Description:

Send and receive Bitcoin over Arkade (offchain), onchain (via onboard/offboard), and Lightning. Swap USDC/USDT stablecoins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiero](https://clawhub.ai/user/tiero)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent users use this skill to operate an Arkade wallet, send and receive Bitcoin across Arkade, onchain, and Lightning flows, and request USDC or USDT swap operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence identifies this as a real cryptocurrency wallet and swap integration with irreversible payment actions.

Mitigation: Use only small test amounts and require explicit human approval before send, offboard, Lightning pay, or swap actions.

Risk: The security evidence flags review-worthy private-key handling because the wallet uses a local hot-wallet configuration file.

Mitigation: Protect or avoid the ~/.arkade-wallet/config.json file and do not paste real private keys into shell commands.

Risk: The security evidence notes mutable package execution as a safety gap.

Mitigation: Pin exact package versions before installation or execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tiero/skills/arkade-wallet)
- [Arkade Documentation](https://docs.arkadeos.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local wallet configuration at ~/.arkade-wallet/config.json when the CLI is used.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
