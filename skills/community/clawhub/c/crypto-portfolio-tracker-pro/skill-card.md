## Description:

Crypto Portfolio Tracker Pro provides basic cryptocurrency portfolio tracking, CoinGecko price lookup for a sample portfolio, and local price alert recording.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to track cryptocurrency holdings, estimate portfolio value changes, and record price alerts. Users should review the shipped behavior before connecting real accounts or storing sensitive financial configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release describes broader exchange, wallet, analytics, and report capabilities than the shipped code appears to provide.

Mitigation: Validate the actual artifact behavior before relying on the skill for financial decisions, operational monitoring, or portfolio reporting.

Risk: The configuration shape includes plaintext fields for exchange API keys, API secrets, Telegram bot tokens, wallet addresses, and other sensitive financial metadata.

Mitigation: Keep live secrets and sensitive wallet data out of the included config unless they have been moved to safer storage and access controls.

Risk: Running the portfolio tracker can contact an external market data service.

Mitigation: Confirm that CoinGecko API use is acceptable for the deployment environment before executing the tracking script.

## Reference(s):

- [Configuration reference](references/config.json)
- [CoinGecko API](https://api.coingecko.com/api/v3)
- [ClawHub skill page](https://clawhub.ai/dagangtj/skills/crypto-portfolio-tracker-pro)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or terminal text with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local alert records and may contact CoinGecko when the portfolio tracking script is run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
