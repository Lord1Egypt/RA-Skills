## Description:

Get an AI signal for one Polymarket market (by its slug) or the current trending markets, through AIProx (aiprox.dev): one POST /api/orchestrate with capability market-data, 50 sats, paid in Bitcoin Lightning (L402 or a LightningProx spend token). Informational only, not financial advice. Use it when the user asks about a specific Polymarket market or trending markets and agrees to pay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec)

### License/Terms of Use:

MIT-0

## Use Case:

People who ask an agent about a specific Polymarket market or currently trending markets can use this skill to request an AI-generated signal and analysis after approving the per-call charge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A call costs 50 sats and sends the market query and payment credential to AIProx; its retention practices were not verified.

Mitigation: Get the user's approval before the call, send only market queries, and use a limited-balance spend token or a per-call Lightning invoice. Do not send secrets or personal data.

Risk: An AI-generated market signal could be mistaken for investment or financial advice.

Mitigation: Present the result as informational only, state that it is not financial advice, and do not place trades or bets on the user's behalf.

## Reference(s):

- [AIProx homepage](https://aiprox.dev)
- [AIProx API endpoint](https://aiprox.dev/api/orchestrate)
- [AIProx documentation](https://aiprox.dev/docs.html)
- [LightningProx top-up](https://lightningprox.com/topup)
- [AIProx trial](https://aiprox.dev/start)

## Skill Output:

**Output Type(s):** [Analysis, JSON]

**Output Format:** [JSON response with a market signal and supporting analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One market or trending-markets request per call; the output is informational and not financial advice.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
