## Description:

Scan Reddit for trending stocks and sentiment spikes using the ApeWisdom API (free). Use this to find "meme stocks", retail momentum, and sentiment shifts on r/wallstreetbets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stuhorsman](https://clawhub.ai/user/stuhorsman)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to fetch ApeWisdom Reddit sentiment rankings, identify trending stock or crypto tickers, and compare top mentions with 24-hour chatter spikes for informational market-sentiment review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to ApeWisdom for live market-sentiment data.

Mitigation: Install only where network access to ApeWisdom is acceptable and prefer explicit least-privilege network permission metadata.

Risk: Market-sentiment rankings can be mistaken for investment recommendations.

Mitigation: Treat results as informational signals rather than financial advice and validate decisions against independent sources.

Risk: The HTTP request does not set an explicit timeout.

Mitigation: Run in an environment where stalled commands can be interrupted, or add a request timeout before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stuhorsman/skills/apewisdom)
- [ApeWisdom API Endpoint](https://apewisdom.io/api/v1.0/filter)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands; scanner output is a JSON array of ranked ticker records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output returns up to 20 results; spike sorting filters out entries with 10 or fewer mentions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
