## Description:

Monitors configured crypto wallet addresses and retrieves live market prices to generate a basic portfolio overview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to add wallet addresses, refresh cryptocurrency prices, and produce command-line portfolio summaries. It is best suited for lightweight tracking, not authoritative balance, profit/loss, alerting, or financial decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate its ability to monitor actual wallet balances, portfolio holdings, profit/loss, or alerts.

Mitigation: Use it only as a lightweight prototype unless the implementation is corrected and validated against authoritative balance and transaction sources.

Risk: Wallet addresses are stored in a home-directory JSON file.

Mitigation: Review local storage behavior before deployment and avoid adding sensitive or unnecessary wallet identifiers.

Risk: The script contacts CoinGecko for market prices.

Mitigation: Confirm that outbound network access to CoinGecko is acceptable for the deployment environment.

## Reference(s):

- [Crypto Holdings Monitor on ClawHub](https://clawhub.ai/sxliuyu/skills/crypto-holdings-monitor)
- [CoinGecko Simple Price API](https://api.coingecko.com/api/v3/simple/price)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Command-line text with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores configured wallet addresses in a home-directory JSON file and contacts CoinGecko for market prices.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
