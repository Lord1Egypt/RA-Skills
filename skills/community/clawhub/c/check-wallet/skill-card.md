## Description:

Query OpenAnt wallet addresses and on-chain balances for SOL, ETH, SPL tokens, and USDC using read-only CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to check OpenAnt wallet addresses, inspect on-chain balances, and troubleshoot insufficient-balance errors before wallet-related actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes an unpinned remote CLI package in an authenticated wallet context.

Mitigation: Pin @openant-ai/cli to a reviewed release and run it with minimal filesystem, environment, and network access.

Risk: Wallet addresses and balances may be displayed automatically.

Mitigation: Ask before showing full addresses or balances and redact sensitive wallet details when a full value is not required.

## Reference(s):

- [ClawHub skill page for Check Wallet](https://clawhub.ai/ant-1984/skills/check-wallet)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and JSON CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands append --json for structured output from the OpenAnt CLI.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
