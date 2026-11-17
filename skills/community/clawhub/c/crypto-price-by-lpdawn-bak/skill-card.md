## Description:

Retrieves real-time USD prices and 24-hour percentage changes for major cryptocurrencies such as BTC, ETH, DOGE, SOL, and LTC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robertstarry-gif](https://clawhub.ai/user/robertstarry-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer cryptocurrency price questions by querying Binance through ccxt and returning a concise price response. It is suited for quick market lookups, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Binance through ccxt for each price lookup.

Mitigation: Deploy only in environments where outbound exchange API calls are allowed and expected.

Risk: Returned cryptocurrency prices are live market data and may be unavailable, delayed, or unsuitable for financial decisions.

Mitigation: Present results as informational lookups, handle API failures clearly, and avoid treating output as financial advice.

Risk: Responses may be in Chinese, which can affect user comprehension in other locales.

Mitigation: Confirm that the target agent or user workflow accepts Chinese-language responses or translate them before presentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robertstarry-gif/skills/crypto-price-by-lpdawn-bak)
- [Publisher profile](https://clawhub.ai/user/robertstarry-gif)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text response with cryptocurrency price and 24-hour percentage change]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to BTC when no symbol is supplied; responses may be in Chinese and depend on live Binance availability.]

## Skill Version(s):

1.0.0 (source: server evidence, artifact frontmatter, and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
