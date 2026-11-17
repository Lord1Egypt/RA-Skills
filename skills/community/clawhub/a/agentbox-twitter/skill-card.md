## Description:

Twitter/X research via paid API: search tweets with 50+ operators, fetch tweets with threads/replies/quotes, get user profiles with tweets/followers/following.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search Twitter/X posts, inspect tweet context, and retrieve user profile activity through a paid x402 API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic paid API calls can create unexpected cumulative USDC costs when searches are repeated or paginated.

Mitigation: Use specific queries, set deliberate result limits, and review pagination before requesting additional pages.

Risk: Twitter/X API requests can fail for invalid parameters, missing records, payment requirements, or upstream API errors.

Mitigation: Check returned HTTP errors and adjust query syntax, tweet or user references, payment setup, and retry posture before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tenequm/skills/agentbox-twitter)
- [Twitter/X paid API base endpoint](https://twitter.x402.agentbox.fyi)
- [Twitter/X search endpoint](https://twitter.x402.agentbox.fyi/search)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Guidance]

**Output Format:** [Markdown guidance with x402_payment request examples and JSON-shaped API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each API request costs $0.003 USDC; pagination or repeated searches can increase total cost.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
