## Description:

Generates a concise Chinese daily crypto market briefing by searching current BTC/ETH market data, major events, funding-rate opportunities, and optional Feishu delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcy891](https://clawhub.ai/user/pcy891)

### License/Terms of Use:

MIT-0

## Use Case:

External users and crypto market operators use this skill to request a daily Chinese-language briefing that summarizes BTC/ETH conditions, recent crypto events, funding-rate observations, and concise action guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send generated crypto briefing content to a hardcoded Feishu recipient, creating an external disclosure risk.

Mitigation: Return the briefing in chat by default, require explicit confirmation before any external send, and resolve the Feishu recipient from the current verified user configuration.

Risk: Crypto prices, funding rates, and event summaries can become stale or unavailable during briefing generation.

Mitigation: Use only current search results for numeric market data and state that data is unavailable instead of fabricating prices, rates, or event details.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown briefing with tables, bullets, and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses search-derived market data and should avoid inventing prices, rates, or event details when current data is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
