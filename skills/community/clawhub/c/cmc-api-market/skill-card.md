## Description: <br>
API reference for CoinMarketCap market-wide endpoints including global metrics, fear/greed, indices, trending topics, and charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryan-cmc](https://clawhub.ai/user/bryan-cmc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent users use this skill to choose CoinMarketCap market-wide API endpoints, authentication patterns, parameters, and example requests for crypto market overview, sentiment, indices, charting, community, content, and utility workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CMC API keys may be exposed if copied into chat logs, source code, or shared command history. <br>
Mitigation: Store the API key in an environment variable or secret manager and avoid pasting live keys into prompts or examples. <br>
Risk: The /v1/key/info endpoint can reveal account quota, plan, and usage details. <br>
Mitigation: Call /v1/key/info only when account usage details are needed and avoid sharing its responses outside trusted contexts. <br>
Risk: Community and content endpoints may return social posts, comments, or news that need source-aware review before use in analysis. <br>
Mitigation: Treat community/content results as input evidence and review them before using them for recommendations or decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bryan-cmc/cmc-api-market) <br>
- [CoinMarketCap skills repository](https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap) <br>
- [Common Use Cases](references/use-cases.md) <br>
- [Global Metrics API Reference](references/global-metrics.md) <br>
- [Fear and Greed Index API Reference](references/fear-greed.md) <br>
- [Market Indices API Reference](references/indices.md) <br>
- [Community API Reference](references/community.md) <br>
- [Content API Reference](references/content.md) <br>
- [K-Line Charts API Reference](references/kline.md) <br>
- [Tools API Reference](references/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance, API call examples] <br>
**Output Format:** [Markdown with endpoint tables, inline bash examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [References CoinMarketCap API endpoints that require an X-CMC_PRO_API_KEY header.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
