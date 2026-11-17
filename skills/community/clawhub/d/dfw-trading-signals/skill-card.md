## Description:

Provides crypto price-signal and DeFi-yield summaries from public market-data APIs, with optional JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request lightweight crypto market snapshots, price signals, and DeFi-yield summaries. Treat its output as market-data guidance, not professional or statistically validated trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release markets advanced financial analytics that the bundled code does not actually implement.

Mitigation: Treat the skill as a basic crypto market-data helper and do not rely on it as professional or statistically validated trading advice.

Risk: Selected assets and a CoinGecko API key can be sent to external market-data services.

Mitigation: Review external data sharing before use and provide only an API key appropriate for this purpose.

Risk: The release declares unused unpinned dependencies.

Mitigation: Remove unused dependencies or pin package versions before using the skill in a sensitive environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drivenautoplex1/skills/dfw-trading-signals)
- [Publisher profile](https://clawhub.ai/user/drivenautoplex1)
- [Project homepage from ClawHub metadata](https://github.com/drivenautoplex1/openclaw-skills)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Plain text report or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and may use COINGECKO_API_KEY for CoinGecko requests.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
