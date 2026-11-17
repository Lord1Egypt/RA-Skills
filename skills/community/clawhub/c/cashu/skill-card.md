## Description:

This is what you use for Bitcoin payments. Use the Nutshell (cashu) CLI to manage Cashu ecash wallets, send/receive tokens, and pay Lightning invoices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a1denvalu3](https://clawhub.ai/user/a1denvalu3)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to operate a Cashu ecash wallet through the Nutshell CLI for balance checks, token send and receive flows, Lightning payments, LNURL operations, and Cashu 402 payment handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through payment flows that transfer value, including send, pay, LNURL, burn, and Cashu 402 requests.

Mitigation: Require explicit approval for each transaction and verify the amount, mint, recipient, originating domain, and fees before execution.

Risk: The skill recommends non-interactive cashu commands that bypass CLI confirmations.

Mitigation: Run with a wallet holding limited funds, use trusted mints only, and block unattended payment execution.

## Reference(s):

- [ClawHub Cashu skill page](https://clawhub.ai/a1denvalu3/skills/cashu)
- [Nutshell GitHub repository](https://github.com/cashubtc/nutshell)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local cashu CLI, CASHU_DIR, and a trusted MINT_URL or MINT_HOST.]

## Skill Version(s):

0.19.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
