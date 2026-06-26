## Description: <br>
BitoPro Market Intel provides public crypto market indicators, BitoPro-listed coin data, listing specs, and relevant news filtered to BitoPro spot coins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bitopro](https://clawhub.ai/user/bitopro) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to answer BitoPro-focused crypto market-intelligence questions, including sentiment, global market indicators, BitoPro-listed coin rankings, public BTC/ETH holdings, listing catalog details, and filtered crypto news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: English news snippets may be sent to Google Translate and cached. <br>
Mitigation: Use the translation feature only for public news content and avoid submitting confidential or account-specific information. <br>
Risk: Users may confuse market intelligence with trading authority. <br>
Mitigation: Do not provide exchange trading credentials to this skill; use it only for public market and news data, not account actions or order placement. <br>
Risk: Public market-data endpoints can rate limit shared-IP usage. <br>
Mitigation: Configure the optional CoinGecko Demo API key when shared-IP rate limits would affect reliability. <br>


## Reference(s): <br>
- [BitoPro Skill Hub](https://clawhub.ai/bitopro/bitopro-skill-hub) <br>
- [Coin Mapping Reference](references/coin-mapping.md) <br>
- [Endpoint Reference](references/endpoints.md) <br>
- [News Categories Reference](references/news-categories.md) <br>
- [CoinGecko Demo API Key Dashboard](https://www.coingecko.com/en/developers/dashboard) <br>
- [BitoPro Public API](https://api.bitopro.com/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries, tables, and concise natural-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Strictly scoped to BitoPro-listed spot coins; may include translated public news snippets and public market-data citations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata); artifact frontmatter reports 1.4.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
