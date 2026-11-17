## Description:

Crypto Tracker Cn helps agents retrieve cryptocurrency market data, sentiment, DeFi metrics, technical indicators, gas information, and related learning guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check crypto prices, market sentiment, DeFi rankings, yield comparisons, gas fees, and basic technical indicators. The skill also includes Chinese-language education and strategy material plus optional local portfolio, alert, and financial tracking commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio, alert, and tracking commands can store holdings, purchase prices, transaction descriptions, or budget details in plaintext local files.

Mitigation: Avoid entering sensitive financial details unless plaintext local storage is acceptable; on shared machines, use a private data directory with restrictive permissions or avoid those commands.

Risk: Market indicators, DeFi yields, and strategy guidance may be mistaken for investment advice.

Mitigation: Treat outputs as educational market information, verify important data independently, and keep human review in the loop before making financial decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain1/skills/crypto-tracker-cn)
- [BytesAgain Homepage](https://bytesagain.com)
- [CoinGecko API](https://api.coingecko.com/api/v3)
- [DefiLlama API](https://api.llama.fi)
- [Alternative.me Fear & Greed API](https://api.alternative.me/fng)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and tabular command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands may create local JSON or log files for portfolio, alert, or tracking data.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
