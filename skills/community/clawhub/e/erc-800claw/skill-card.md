## Description:

The OpenClaw entry point for ERC-8004 agent identity and reputation. Register agents on-chain, query identities, give and receive feedback ratings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[primer-dev](https://clawhub.ai/user/primer-dev)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use ERC-800Claw to register on-chain agent identities, query ERC-8004 identity and reputation data, and submit feedback ratings on Ethereum mainnet or Sepolia.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger real blockchain writes using a wallet private key for registration or feedback.

Mitigation: Use a dedicated low-balance wallet, prefer Sepolia first, and require the agent to show the network, action, gas estimate, and transaction summary before any transaction is signed.

Risk: Private keys can be exposed if pasted into chat, logs, or command output.

Mitigation: Use environment variables or a secure secret store, and do not display PRIVATE_KEY values in agent responses.

Risk: The agent may install or invoke an unintended SDK package if dependencies are not scoped carefully.

Mitigation: Verify the package name, version, and publisher before installation or execution.

## Reference(s):

- [ERC-800Claw on ClawHub](https://clawhub.ai/primer-dev/skills/erc-800claw)
- [ERC-8004 Protocol](https://8004.org)
- [EIP-8004](https://eips.ethereum.org/EIPS/eip-8004)
- [ERC-800Claw npm package](https://npmjs.com/package/erc-800claw)
- [ERC-800Claw PyPI package](https://pypi.org/project/erc-800claw)
- [Primer Systems](https://primer.systems)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that read from or write to Ethereum networks; wallet-backed actions require PRIVATE_KEY and gas.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
