## Description:

Interact with CoinFello using the @coinfello/agent-cli to create a smart account, sign in with SIWE, manage delegations, send prompts with server-driven ERC-20 token subdelegations, and check transaction status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brettcleary](https://clawhub.ai/user/brettcleary)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate CoinFello crypto workflows from an agent, including smart account setup, SIWE authentication, natural-language transaction prompts, delegation review, and transaction-status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a mutable remote CLI package for wallet-related actions.

Mitigation: Use a pinned, reviewed @coinfello/agent-cli version and install only when the CoinFello service and npm package publisher are trusted.

Risk: Wallet signing, SIWE sessions, and delegation state can grant transaction authority.

Mitigation: Review the active signer type, session state, requested chain, token, recipient, amount, and delegation scope before approving any delegation.

Risk: The development-only private-key mode stores a raw private key in local configuration.

Mitigation: Avoid --use-unsafe-private-key except in isolated testing, prefer hardware-backed signing where available, and keep the config file private with restrictive permissions.

Risk: The signer daemon caches authentication for repeated signing operations.

Mitigation: Check signer-daemon status before sensitive work and stop the daemon when signing is no longer needed.

Risk: Using unsupported chains can strand funds.

Mitigation: Use only chains supported by CoinFello infrastructure and the MetaMask delegation contracts.

## Reference(s):

- [CoinFello CLI Reference](references/REFERENCE.md)
- [CoinFello Homepage](https://coinfello.com)
- [CoinFello Skill on ClawHub](https://clawhub.ai/brettcleary/skills/coinfello)
- [brettcleary Publisher Profile](https://clawhub.ai/user/brettcleary)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run CoinFello CLI commands that create local config files, store session authority, submit prompts, and approve delegation requests.]

## Skill Version(s):

0.3.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
