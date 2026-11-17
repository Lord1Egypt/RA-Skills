## Description:

Analyze Twitter Spaces and voice conversations to extract market intelligence, crypto alpha, sentiment analysis, speaker-attributed insights, structured reports, transcripts, and machine-readable metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benschiller](https://clawhub.ai/user/benschiller)

### License/Terms of Use:


## Use Case:

External agents, developers, and market researchers use this skill to browse and purchase structured intelligence from Twitter Spaces and long-form voice discussions, especially for crypto markets, AI trends, sentiment analysis, and speaker-attributed claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages wallet-backed purchases, and the security summary flags unclear user confirmation and spending controls.

Mitigation: Use a dedicated low-balance wallet, require explicit approval before each purchase, and validate the endpoint, network, price, and payment terms before signing.

Risk: CDP or wallet secrets could be exposed through source control, prompts, or logs during integration.

Mitigation: Store wallet credentials in a secret manager or environment variables, keep them out of source control, and redact them from logs and shared transcripts.

Risk: Repeat access requires repurchase if purchased reports and transaction metadata are not retained.

Mitigation: Persist purchased artifacts, transaction hashes, and catalog identifiers in an approved storage location after each purchase.

## Reference(s):

- [API Reference](references/API-REFERENCE.md)
- [Integration Guide](references/INTEGRATION.md)
- [Clawdio API](https://clawdio.vail.report)
- [ClawHub Skill Page](https://clawhub.ai/benschiller/skills/clawdio-twitter)
- [x402 Protocol](https://www.x402.org/)
- [Coinbase AgentKit Documentation](https://docs.cdp.coinbase.com/agentkit)
- [Coinbase CDP Documentation](https://docs.cdp.coinbase.com/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown, JSON]

**Output Format:** [Markdown guidance with curl and JavaScript examples; purchased API responses are JSON containing Markdown reports and transcripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Purchasing requires network access and an x402-compatible wallet funded with USDC on Base Mainnet.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
