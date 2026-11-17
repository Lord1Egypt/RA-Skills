## Description:

Agentic X402 enables agents to make x402 payments for gated APIs and content, fetch paid resources, check wallet balances, and create payment links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ya7ya](https://clawhub.ai/user/ya7ya)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to configure a dedicated EVM wallet, inspect balances, pay for x402-gated web resources, fetch paid content, and create payment links for gated content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically spend cryptocurrency when paying for or fetching x402-gated resources.

Mitigation: Use a dedicated low-balance wallet, test on testnet first, prefer dry-run or manual review for new URLs, and avoid unattended pay or fetch flows for untrusted URLs.

Risk: The skill requires a raw EVM private key and may store it in an environment file.

Mitigation: Keep the key out of agent transcripts, terminal logs, screenshots, and shell history; restrict file permissions; and store backups only in a secure password manager or encrypted file.

Risk: Server security evidence reports that advertised payment limits are not reliably enforced.

Mitigation: Limit wallet funding to the maximum acceptable loss and avoid untrusted automatic payment flows until payment-limit enforcement is fixed.

## Reference(s):

- [x402 Protocol Docs](https://docs.x402.org/)
- [npm: agentic-x402](https://www.npmjs.com/package/agentic-x402)
- [x402 GitHub](https://github.com/coinbase/x402)
- [Base Network](https://base.org/)
- [21.cash](https://21.cash)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Terminal text, JSON responses, and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet addresses, balances, transaction hashes, payment link details, and fetched paid content.]

## Skill Version(s):

0.2.6 (source: SKILL.md metadata, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
