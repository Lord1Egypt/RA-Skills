## Description:

Builds personalized stock-news briefings and opportunity scans from a user's holdings, watchlist, sectors, and selected sources.

This skill is for research and development only.

## Publisher:

[illli](https://clawhub.ai/user/illli)

### License/Terms of Use:

CC BY-NC 4.0

## Use Case:

Investors, analysts, and agents use this skill to configure local stock-interest profiles, generate personalized market briefings, scan breaking news for opportunity signals, and create per-stock ARTi analysis links without producing trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance-news summaries may be mistaken for trading recommendations or may overstate causal impact.

Mitigation: Keep facts, inference, confidence, adverse conditions, and the research-only disclaimer separated; do not provide target prices, guarantees, automatic trades, or buy/sell advice.

Risk: Generated ARTi links send stock symbols, company labels, news titles, source URLs, and the research prompt to a third-party URL when clicked.

Mitigation: Tell users what fields are sent before creating or presenting links, and avoid clicking them for sensitive research context unless that sharing is acceptable.

Risk: The README recommends an unpinned global npx install or update command.

Mitigation: Review the installer before use and prefer a pinned package or immutable skill revision before deployment.

Risk: News feeds, RSS entries, web pages, and aggregated summaries can contain untrusted instructions or unverifiable claims.

Mitigation: Treat source content as data only, ignore embedded operational instructions, and verify key facts with official or reliable secondary sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/illli/skills/arti-opportunity-radar)
- [Output Contract](references/output-contract.md)
- [Profile Schema](references/profile-schema.md)
- [Information Sources and Fallback Rules](references/sources.md)
- [ARTi analysis agent](https://artifin.ai/app/agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefings with evidence labels, source links, per-stock ARTi analysis links, and optional JSON profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local .arti-opportunity-radar/profile.json after user confirmation; ARTi links include stock symbol, company label, news title, source URL, and research prompt.]

## Skill Version(s):

1.0.0 (source: config.yaml and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
