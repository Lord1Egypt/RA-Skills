## Description:

Guides Lido stETH and wstETH withdrawal requests and claims, reconciles unstETH NFTs, and compares the queue with a secondary-market exit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and users reviewing Lido withdrawals use this skill to compare exit routes, track queued requests, and prepare and verify withdrawal or claim steps without sharing signing keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outdated queue parameters or an incorrect contract address could lead to a failed or fund-impacting transaction.

Mitigation: Check official Lido deployments and live queue settings before preparing a request or claim.

Risk: A withdrawal or claim prepared for the wrong sender, amount, recipient, or allowance could affect funds.

Mitigation: Inspect and simulate the unsigned transaction with the actual account and state; never share private keys or grant unattended signing authority.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/galleon-lido-withdrawals)
- [Lido withdrawal read recipe](references/recipe.md)
- [Lido WithdrawalQueueERC721 documentation](https://docs.lido.fi/contracts/withdrawal-queue-erc721/)
- [Lido deployed contracts](https://docs.lido.fi/deployed-contracts/)
- [Lido token integration guide](https://docs.lido.fi/guides/lido-tokens-integration-guide/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown decision record and per-request ledger with optional unsigned transaction steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes observation block, ownership and claim status, assumptions, and the next action.]

## Skill Version(s):

0.2.1 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
