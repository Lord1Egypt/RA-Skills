## Description: <br>
API reference for CoinMarketCap exchange endpoints including exchange info, volume, market pairs, historical quotes, and exchange assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryan-cmc](https://clawhub.ai/user/bryan-cmc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to identify the right CoinMarketCap exchange API endpoint, required parameters, authentication header, and response shape for exchange metadata, volume, market pair, historical quote, and asset-reserve workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided CoinMarketCap API key for requests. <br>
Mitigation: Use a limited, revocable API key and avoid exposing the real key in shared logs, prompts, or generated examples. <br>
Risk: CoinMarketCap requests may count against subscription plan limits or rate limits. <br>
Mitigation: Check response credit counts and plan limits before running repeated or broad exchange-data queries. <br>


## Reference(s): <br>
- [CoinMarketCap skill homepage](https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap) <br>
- [Exchange Info and Mapping APIs](references/info.md) <br>
- [Exchange Listings API](references/listings.md) <br>
- [Exchange Quotes API](references/quotes.md) <br>
- [Exchange Market Pairs API](references/market-pairs.md) <br>
- [Exchange Assets API](references/assets.md) <br>
- [Exchange API Use Cases](references/use-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with curl examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided CoinMarketCap API key for live API calls; API usage may count against plan limits.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
