## Description:

Bridge tokens from one chain to another without swapping. Simplified cross-chain transfer where the output token is the same as the input token. Use when the user wants to move tokens between chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to move the same token between supported blockchains without performing a swap. It guides token, amount, source chain, destination chain, and optional recipient handling before delegating bridge execution and reporting results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports irreversible crypto transfer workflows through a delegated executor.

Mitigation: Use it only where wallet signing requires clear human confirmation for token, amount, chains, recipient, fees, and final broadcast.

Risk: The documented install commands can resolve mutable remote content.

Mitigation: Install a pinned, reviewed version or commit before using the skill in a wallet-connected environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/bridge-tokens)
- [Publisher profile](https://clawhub.ai/user/wpank)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown bridge report with transaction identifiers, fee, settlement, and safety status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Uniswap chain and token lookup tools and delegates execution to a cross-chain executor agent.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
