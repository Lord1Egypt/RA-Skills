## Description: <br>
东方财富金融数据工具集，集成选股、资讯搜索、行情财务查询三大功能，用于查询 A股、港股、美股相关的选股、资讯、行情、财务、公司信息和资金流向数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[torchesfrms](https://clawhub.ai/user/torchesfrms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to route natural-language stock and market queries to Eastmoney APIs for screening, news search, quotes, financial metrics, company information, and capital-flow data. It is intended for A-share, Hong Kong stock, and U.S. stock data lookups when an Eastmoney API key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock-related query text is sent to Eastmoney's API using an Eastmoney API key. <br>
Mitigation: Use a dedicated API key and avoid including personal, confidential, or sensitive information in financial queries. <br>
Risk: API keys may be exposed if environment variables, vault files, chat output, or logs are shared. <br>
Mitigation: Keep EASTMONEY_APIKEY and the local vault file private, and do not paste key values into conversations or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/torchesfrms/eastmoney-tools) <br>
- [Eastmoney API base](https://mkapi2.dfcfs.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with bash examples and raw JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EASTMONEY_APIKEY or a local vault file; API responses are kept in their original JSON format.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
