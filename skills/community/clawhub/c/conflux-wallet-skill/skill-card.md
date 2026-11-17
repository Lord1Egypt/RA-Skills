## Description:

Self-sovereign EVM wallet for AI agents that can create a local wallet, check balances, send ETH or ERC20 tokens, swap tokens, and interact with smart contracts across Base, Conflux eSpace, Ethereum, Polygon, Arbitrum, and Optimism without cloud custody or API keys.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[pana](https://clawhub.ai/user/pana)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent create and operate a local EVM wallet, inspect balances, prepare transfers, request swap quotes, execute confirmed swaps, and interact with smart contracts across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage real crypto funds and execute transfers, swaps, approvals, and contract writes.

Mitigation: Start with negligible funds and require independent verification of recipient, token contract, chain, amount, and gas cost before approving any transaction.

Risk: The reviewed package can bootstrap by downloading and installing unpinned GitHub source and dependencies.

Mitigation: Pin, inspect, and scan the GitHub source and dependencies before running npm install or executing wallet commands.

Risk: Local private key exposure or accidental wallet reinitialization can cause loss of funds.

Mitigation: Protect ~/.cfx-wallet.json, never share private keys, avoid reinitializing funded wallets, and move funds to a new wallet if a key may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pana/skills/conflux-wallet-skill)
- [Publisher profile](https://clawhub.ai/user/pana)
- [Project homepage from ClawHub metadata](https://github.com/conflux-fans/conflux-wallet-skill)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Conflux eSpace explorer](https://evm.confluxscan.org)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are expected to use --json where available so the agent can parse results and present transaction details before user confirmation.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
