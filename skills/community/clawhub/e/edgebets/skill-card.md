## Description:

AI-powered sports betting simulations with Monte Carlo analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cannedoxygen](https://clawhub.ai/user/cannedoxygen)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use EdgeBets to browse sports games, request daily picks or track records, and run paid Monte Carlo simulations for NBA, NFL, MLB, and MLS betting analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid simulations can spend real USDC from a Solana mainnet wallet.

Mitigation: Use only a small, dedicated wallet and require manual confirmation of the exact amount, recipient, network, and quote before each payment.

Risk: A long-lived private key in SOLANA_PRIVATE_KEY can expose wallet funds if mishandled.

Mitigation: Avoid connecting a main wallet, rotate credentials when needed, and keep only the funds required for intended simulations in the configured wallet.

Risk: Price information is inconsistent across the artifact, which may confuse payment expectations.

Mitigation: Confirm the current quote, simulation price, and charged amount before approving any Solana transaction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cannedoxygen/skills/edgebets)
- [Publisher Profile](https://clawhub.ai/user/cannedoxygen)
- [EdgeBets Website](https://edgebets.fun)
- [EdgeBets API Documentation](https://api.edgebets.fun/api/v1/x402)
- [EdgeBets OpenAPI Spec](https://api.edgebets.fun/api/v1/x402/openapi.json)
- [npm Package](https://www.npmjs.com/package/edgebets-sdk)
- [x402 Protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript and TypeScript code examples, shell commands, and structured simulation summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sports game lists, win probabilities, projected scores, edge analysis, daily pick summaries, track records, balance checks, and wallet setup guidance.]

## Skill Version(s):

1.0.4 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
