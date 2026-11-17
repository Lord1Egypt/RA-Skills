## Description:

AI-powered multi-exchange crypto market analysis, arbitrage detection, and trading reports using live data from major exchanges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contrario](https://clawhub.ai/user/contrario)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather cryptocurrency market data, compare exchange pricing, identify arbitrage opportunities, and produce AI-assisted trading analysis reports. It is intended for informational market analysis, not trade execution or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill makes misleading safety claims and uses network and exchange credentials more broadly than users may expect.

Mitigation: Review carefully before installing, use only dedicated read-only exchange keys, and never provide keys with trading or withdrawal permissions.

Risk: The skill sends market data and query text to an external analysis endpoint and verification mode can make live outbound market-data requests.

Mitigation: Avoid putting wallet addresses, secrets, private strategies, or personal data in prompts, and expect live outbound market-data requests during verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/contrario/skills/apex-crypto-intelligence)
- [Publisher profile](https://clawhub.ai/user/contrario)
- [Publisher homepage](https://masterswarm.net)
- [Privacy policy](https://masterswarm.net)
- [External analysis endpoint](https://api.neurodoc.app/aetherlang/execute)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text analysis with optional API response content and report-oriented summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market-analysis narratives, arbitrage summaries, configuration guidance for optional exchange keys, and report content.]

## Skill Version(s):

0.2.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
