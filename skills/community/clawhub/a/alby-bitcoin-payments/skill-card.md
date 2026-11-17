## Description:

Teaches agents how to use @getalby/cli to operate a bitcoin lightning wallet via Nostr Wallet Connect (NIP-47), including sending and receiving payments, checking balances, creating invoices, converting fiat and sats, handling paid HTTP 402 requests, discovering paid API services, and paying supported on-chain crypto or stablecoin addresses by swapping from a bitcoin balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rolznz](https://clawhub.ai/user/rolznz)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to let an agent interact with an Alby-compatible bitcoin lightning wallet for wallet setup, balance checks, invoices, payments, fiat/sats conversion, paid HTTP 402 requests, and paid service discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent ongoing authority to operate a real bitcoin wallet.

Mitigation: Use a low-balance or budget-limited wallet and require explicit confirmation for every payment, swap, or paid fetch.

Risk: Connection secrets may be exposed if pasted into chat, logs, or command history.

Mitigation: Prefer named or file-based credentials, never print or read secret contents, and revoke any secret that was exposed.

Risk: The skill executes an npm-distributed CLI through npx.

Mitigation: Pin and verify the CLI or install source before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rolznz/skills/alby-bitcoin-payments)
- [Alby](https://getalby.com)
- [Alby CLI](https://github.com/getAlby/cli)
- [Nostr Wallet Connect](https://nwc.dev)
- [402index](https://402index.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce payment, wallet, invoice, fetch, and service-discovery command guidance; user confirmation is required for payment or swap actions.]

## Skill Version(s):

1.3.8 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
