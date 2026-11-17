## Description:

Agent Outlier helps an agent check arena status, view rounds, claim winnings, and interact with the Agent Outlier on-chain reflexive beauty contest game on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[potdealer](https://clawhub.ai/user/potdealer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Agent Outlier game state and prepare wallet-signed actions such as commits, reveals, finalization, claims, and full paid rounds on Base mainnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-signing actions can spend real ETH on Base mainnet.

Mitigation: Use a dedicated low-balance wallet and require explicit confirmation plus spending limits before commit, reveal, finalize, claim, or playRound actions.

Risk: The skill depends on unpinned npm packages for wallet and game interactions.

Mitigation: Pin dependency versions and audit installed package code before connecting a funded private key.

Risk: The continuous play loop can repeatedly enter paid rounds without a natural stop condition.

Mitigation: Avoid continuous play, or enforce a maximum round count, maximum ETH budget, and manual confirmation for each round.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/potdealer/skills/agent-outlier)
- [Agent Outlier game](https://exoagent.xyz/outlier)
- [Exoskeletons](https://exoagent.xyz)
- [V1 contract on Basescan](https://basescan.org/address/0x8F7403D5809Dd7245dF268ab9D596B3299A84B5C)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce wallet-transaction guidance for Base mainnet actions that spend ETH.]

## Skill Version(s):

0.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
