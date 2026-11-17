## Description:

Banana Farmer provides stock and crypto momentum scanning, ticker analysis, portfolio briefs, market pulse, sector trends, performance tracking, and risk alerts through Python scripts backed by the Banana Farmer API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamandjarvis](https://clawhub.ai/user/adamandjarvis)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and analysts use this skill to query Banana Farmer market signals, compare tickers, build watchlists, and review portfolio or sector momentum for research. It supports decision support only and is not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested tickers and portfolio holding symbols to bananafarmer.app using a Banana Farmer API key.

Mitigation: Install only if this data sharing is acceptable; keep BF_API_KEY scoped to Banana Farmer and review the provider's terms and privacy policy before using the trial-key signup flow.

Risk: Market signals may be mistaken for investment advice.

Mitigation: Treat outputs as research data only and have a qualified human review any financial decision.

Risk: Signals can be stale or delayed during market hours.

Mitigation: Run the health check and verify data freshness before relying on time-sensitive analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adamandjarvis/skills/banana-farmer)
- [Banana Farmer Homepage](https://bananafarmer.app)
- [Banana Farmer Developers](https://bananafarmer.app/developers)
- [Tiingo Market Data Source](https://tiingo.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON from Python CLI scripts, often summarized by the agent in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BF_API_KEY; some endpoints may require a higher API tier.]

## Skill Version(s):

1.9.0 (source: ClawHub release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
