## Description:

Bifrost SLPx liquid staking via @bifrostio/slpx-cli: query vToken rates, APY, TVL, holders, and protocol information, and manage vETH balance, mint, redeem, and claim flows on supported EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bifrost-io](https://clawhub.ai/user/bifrost-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Bifrost SLPx liquid-staking data and prepare vETH mint, redeem, claim, balance, and status workflows through the Bifrost CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask an agent to run mutable npm package code while preparing wallet transactions.

Mitigation: Use a pinned and independently reviewed @bifrostio/slpx-cli version before installation or execution.

Risk: Mint, redeem, and claim workflows may broadcast transactions on behalf of the configured signing wallet.

Mitigation: Require the pre-broadcast checklist, explicit user approval, and independent verification of chain, amount, contract, and calldata before broadcast.

Risk: Persistent plaintext signing-key setup can expose wallet credentials if reused or stored in shared shell configuration.

Mitigation: Prefer a hardware wallet, isolated signer, or low-value operational wallet; do not use a primary wallet key or paste secrets into chat.

## Reference(s):

- [Bifrost SLPx CLI package](https://www.npmjs.com/package/@bifrostio/slpx-cli)
- [Command reference](references/commands.md)
- [Supported tokens and chains](references/tokens-and-chains.md)
- [Pre-broadcast checklist](references/pre-tx-checklist.md)
- [Error codes](references/errors.md)
- [Signing key setup](references/private-key-env.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and summaries of JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CLI JSON output as the grounding source; transaction broadcasts require checklist review and explicit user approval.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
