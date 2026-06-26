## Description: <br>
Access aggregated China export trade statistics sourced from China General Administration of Customs public data, compiled and served through the doumaotong.com REST API. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[findhappy7](https://clawhub.ai/user/findhappy7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, students, and small business users can query China export metrics by HS code, destination market, monthly trend, product ranking, and recent historical records for reference and baseline market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to doumaotong.com and the provider may log IP addresses, paths, request parameters, and timestamps. <br>
Mitigation: Use the skill only when sharing trade-research query details with doumaotong.com is acceptable; do not send sensitive business plans or private identifiers in query parameters. <br>
Risk: The API serves third-party aggregated data with a typical 1-2 month lag and is not a direct government data source. <br>
Mitigation: Verify important or high-stakes figures against China Customs Statistics or UN Comtrade before relying on them. <br>
Risk: The skill states that no credentials are required, despite the release being tagged as requiring sensitive credentials. <br>
Mitigation: Do not provide API keys, tokens, login credentials, or other secrets if prompted while using these endpoints. <br>


## Reference(s): <br>
- [China Customs Statistics](http://stats.customs.gov.cn/indexEn) <br>
- [doumaotong.com API base URL](https://doumaotong.com) <br>
- [UN Comtrade Database](https://comtradeplus.un.org/) <br>
- [UN Comtrade API Documentation](https://comtradeapi.un.org/docs/v1) <br>
- [U.S. Trade.gov HS Codes Reference](https://www.trade.gov/harmonized-system-hs-codes) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with REST endpoint examples and JSON response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes read-only GET endpoints that return export data with code and data fields.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
