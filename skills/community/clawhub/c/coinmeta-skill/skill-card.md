## Description: <br>
Fetches latest cryptocurrency newsflashes and articles from the CoinMeta API with keyword search and pagination support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[semithin](https://clawhub.ai/user/semithin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve CoinMeta cryptocurrency newsflashes and article summaries, search by keyword, paginate results, and format API responses for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and request parameters are sent to CoinMeta's external API. <br>
Mitigation: Use only non-sensitive queries and configure COINMETA_API_KEY deliberately for CoinMeta lookups. <br>
Risk: CoinMeta responses are third-party cryptocurrency news data and may be incomplete or outdated. <br>
Mitigation: Treat returned news as informational and verify important market claims against authoritative sources before acting. <br>


## Reference(s): <br>
- [CoinMeta-Skill on ClawHub](https://clawhub.ai/semithin/coinmeta-skill) <br>
- [CoinMeta API](https://api.coinmeta.com) <br>
- [Newsflash List Endpoint](https://api.coinmeta.com/open/v1/newsflash/list) <br>
- [Newsflash Search Endpoint](https://www.coinmeta.com/open/v1/newsflash/search) <br>
- [Article Search Endpoint](https://api.coinmeta.com/open/v1/article/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style text with curl examples and formatted CoinMeta API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses COINMETA_API_KEY and sends page, size, and keyword values to CoinMeta endpoints.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
