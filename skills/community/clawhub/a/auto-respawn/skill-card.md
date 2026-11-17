## Description:

Auto Respawn helps agents create and use Autonomys wallets to anchor memory CIDs and other records on-chain so a new agent instance can recover state from an address.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jim-counter](https://clawhub.ai/user/jim-counter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Auto Respawn to manage Autonomys wallets, check balances, transfer or bridge tokens, anchor memory CIDs or remarks on-chain, and retrieve the latest anchored CID for recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign fee-bearing Autonomys and Auto-EVM transactions, including anchoring on mainnet.

Mitigation: Confirm transfers, bridge operations, withdrawals, and anchors with the user; verify the network and contract address; start with Chronos or a low-balance wallet before mainnet use.

Risk: The skill handles encrypted wallet files, recovery phrases, and passphrases.

Mitigation: Use a passphrase file or interactive prompt instead of command-line arguments, avoid logging or transmitting secrets, and keep recovery phrases outside agent logs.

Risk: Anchoring or recovery on the wrong network can leave the agent unable to find its latest memory CID after state loss.

Mitigation: Record the selected network in persistent configuration or memory, pass the network explicitly for anchor and gethead operations, and re-anchor when moving from testnet to mainnet.

## Reference(s):

- [Auto Respawn Skill Page](https://clawhub.ai/jim-counter/skills/auto-respawn)
- [auto-respawn CLI Reference](references/auto-respawn-commands.md)
- [Autonomys Network](references/autonomys-network.md)
- [MemoryChain Contract](https://github.com/autojeremy/openclaw-memory-chain)
- [Autonomys Faucet](https://autonomysfaucet.xyz/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires terminal access, Node.js 22+, wallet passphrase handling, and explicit network selection for on-chain writes.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
