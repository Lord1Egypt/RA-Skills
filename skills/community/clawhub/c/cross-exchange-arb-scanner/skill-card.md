## Description:

Scans live public spot tickers across Coinbase, Kraken, Bitstamp, Gemini, and OKX without API keys to report gross cross-exchange crypto arbitrage spreads for requested symbols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and crypto market operators use this skill to check whether requested spot symbols show a current price gap across major exchanges. The skill is for detection and reporting only, not trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gross spreads can be mistaken for executable arbitrage or trading advice.

Mitigation: Tell users that results exclude trading fees, withdrawal fees, transfer time, and order-book depth, and require independent validation before action.

Risk: The scanner makes live unauthenticated requests to public exchange APIs for user-supplied symbols.

Mitigation: Install only if network access to Coinbase, Kraken, Bitstamp, Gemini, and OKX is acceptable, and treat unavailable exchange responses as incomplete coverage.

Risk: OKX quotes are USDT while the other exchange endpoints are USD.

Mitigation: Call out potential USDT peg noise when comparing OKX prices to USD venues.

## Reference(s):

- [Exchange API notes](artifact/references/notes.md)
- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/cross-exchange-arb-scanner)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Point-in-time public ticker results; no credentials; gross spreads only.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
