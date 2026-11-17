## Description:

Monitor and analyze market-moving catalysts including earnings, FDA decisions, economic data releases, and corporate events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[collierking](https://clawhub.ai/user/collierking)

### License/Terms of Use:


## Use Case:

External users and market-focused agents use CatalystWatch to monitor upcoming and recent catalysts for tickers, sectors, or watchlists and summarize likely market impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a CatalystWatch API key and may use optional watchlist tickers.

Mitigation: Install only if you trust the CatalystWatch data provider, provide the key through the expected environment variable, and avoid sharing sensitive watchlists unless appropriate.

Risk: Catalyst summaries may influence financial decisions.

Mitigation: Treat the output as informational and verify market data, event timing, and expected impact independently before making trades or investment decisions.

## Reference(s):

- [CatalystWatch on ClawHub](https://clawhub.ai/collierking/skills/catalystwatch)
- [collierking ClawHub profile](https://clawhub.ai/user/collierking)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text summaries with configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CATALYSTWATCH_API_KEY for CatalystWatch data access; CATALYSTWATCH_WATCHLIST may provide default tickers.]

## Skill Version(s):

0.0.2 (source: server evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
