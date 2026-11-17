## Description:

Purchases Api3 data feed subscriptions from market.api3.org.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api3dao](https://clawhub.ai/user/api3dao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to select an Api3 dAPI feed and chain, get a subscription quote, execute an on-chain purchase, and optionally read the deployed reader proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses WALLET_MNEMONIC to sign a live blockchain transaction for a data feed subscription.

Mitigation: Use only a dedicated low-balance wallet and independently inspect the transaction details before approving the purchase step.

Risk: A valuable recovery phrase could be exposed if stored casually in the skill directory or shared with the agent.

Mitigation: Keep production wallet secrets out of the skill directory and avoid sharing the mnemonic directly in chat.

Risk: The read-data-feed step can target an unintended contract if the reader proxy address is malformed or untrusted.

Mitigation: Run that step only after validating the proxy address as a 42-character hexadecimal Ethereum address that starts with 0x.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/api3dao/skills/api3-data-feed-purchase)
- [Api3 Market](https://market.api3.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks and summarized command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pnpm, ts-node, and WALLET_MNEMONIC for purchase execution.]

## Skill Version(s):

0.7.0 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
