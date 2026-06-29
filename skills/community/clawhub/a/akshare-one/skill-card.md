## Description: <br>
Akshare One is an MCP-based stock-data connector for China market data, including historical prices, real-time quotes, news, financial statements, insider trading data, financial metrics, and trading-day time information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve China stock market data through the XiaoBenYang API. It helps agents answer market-data questions by routing requests to tools for prices, news, financial statements, insider trading, and related metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a XiaoBenYang API key and stores it in plaintext in a local .env file. <br>
Mitigation: Use a limited or revocable API key, keep .env out of source control, and rotate or delete the key when the skill is no longer needed. <br>
Risk: The security summary notes leftover Gaokao and school-search wording that may confuse users about the skill's purpose. <br>
Mitigation: Review prompts and tool descriptions before deployment so user-facing guidance reflects the stock-data workflow. <br>


## Reference(s): <br>
- [Akshare One on ClawHub](https://clawhub.ai/cainingnk/akshare-one) <br>
- [XiaoBenYang API key site](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, guidance] <br>
**Output Format:** [Markdown responses summarizing raw JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a XiaoBenYang API key; returned data depends on the upstream API and requested market symbol.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
