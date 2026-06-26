## Description: <br>
查询加密货币快讯。触发场景：查询币圈快讯、获取加密货币新闻、crypto news、币圈资讯。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[semithin](https://clawhub.ai/user/semithin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve CoinMeta cryptocurrency news flashes and perform keyword searches for crypto news updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses COINMETA_API_KEY for CoinMeta news queries, which may expose quota, billing, or account access if mishandled. <br>
Mitigation: Use a scoped or rotatable CoinMeta API key where available, store it only in the expected environment variable, and monitor key usage. <br>
Risk: CoinMeta responses can include HTML content and external crypto-news text that may be unsuitable for direct display or decision-making. <br>
Mitigation: Strip HTML as the artifact specifies, present retrieved news as source content, and avoid treating crypto-news summaries as financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/semithin/coinmeta-api) <br>
- [CoinMeta API base URL](https://api.coinmeta.com) <br>
- [CoinMeta newsflash list endpoint](https://api.coinmeta.com/open/v1/newsflash/list) <br>
- [CoinMeta newsflash search endpoint](https://www.coinmeta.com/open/v1/newsflash/search) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with curl examples and formatted crypto-news summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires COINMETA_API_KEY and curl; supports page, size, and keyword parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
