## Description:

Clawdio helps agents transform human voice conversations into structured metadata, semantic markdown reports, and speaker-attributed transcripts for market intelligence, crypto alpha, quote extraction, and sentiment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benschiller](https://clawhub.ai/user/benschiller)

### License/Terms of Use:


## Use Case:

External agents and developers use Clawdio to browse and purchase voice-conversation intelligence reports, then consume structured metadata, semantic markdown reports, and speaker-attributed transcripts for market research, crypto analysis, sentiment review, and quote extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables agents to make paid x402 purchases using USDC on Base Mainnet, and the security summary notes unclear per-purchase consent or spending controls.

Mitigation: Use a dedicated low-balance wallet, require manual approval for each purchase, and avoid wallet-enabled crawling or autonomous self-discovery.

Risk: Purchased artifacts can include transcripts, speaker identities, Twitter handles, avatars, quotes, sentiment, and market analysis.

Mitigation: Treat returned transcripts and participant metadata as sensitive personal data; review, redact, and limit redistribution according to the intended use.

Risk: Repeat access may require repurchase if artifacts are not saved after a transaction.

Mitigation: Store purchased metadata, reports, transcripts, and transaction records in an approved location immediately after purchase.

## Reference(s):

- [Clawdio Skill Page](https://clawhub.ai/benschiller/skills/clawdio)
- [Clawdio API and Homepage](https://clawdio.vail.report)
- [Coinbase AgentKit](https://docs.cdp.coinbase.com/agentkit)
- [Coinbase CDP SDK](https://docs.cdp.coinbase.com/)
- [x402 Protocol](https://www.x402.org/)

## Skill Output:

**Output Type(s):** [text, guidance, shell commands, configuration, code, markdown, JSON]

**Output Format:** [Markdown instructions with shell commands, JavaScript examples, JSON response examples, and generated report or transcript markdown from the API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Purchased API responses include metadata, structured markdown reports, speaker-attributed markdown transcripts, and transaction information.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
