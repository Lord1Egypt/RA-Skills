## Description:

CryptoWatch helps agents check cryptocurrency prices, market rankings, and manual price alerts using CoinGecko data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gztanht](https://clawhub.ai/user/gztanht)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to retrieve current cryptocurrency prices, compare market movement, and maintain local threshold alerts. The outputs are informational only and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented npx install command may fetch an unpinned remote npm package that does not clearly match the reviewed artifact.

Mitigation: Pin the npm package to a reviewed version and verify the package identity and checksum before running it.

Risk: The skill makes outbound requests to CoinGecko and depends on availability, rate limits, and returned market data quality.

Mitigation: Run it in an environment where CoinGecko access is expected, handle rate-limit failures, and treat returned prices as informational rather than financial advice.

Risk: Price alerts are stored locally and require manual execution or external scheduling to check thresholds.

Mitigation: Use a reviewed scheduler if continuous checks are required and protect the local alert configuration file from unwanted modification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gztanht/skills/cryptowatch)
- [Publisher profile](https://clawhub.ai/user/gztanht)
- [CoinGecko API](https://www.coingecko.com/en/api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local JSON alert file when alert commands are used.]

## Skill Version(s):

1.0.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
