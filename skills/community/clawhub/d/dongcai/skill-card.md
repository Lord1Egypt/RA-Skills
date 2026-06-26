## Description: <br>
东方财富妙想资讯搜索 helps agents search financial news, announcements, research reports, policy updates, trading rules, and event analysis through an Eastmoney-related search service while reducing reliance on stale or non-authoritative sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinsutianxing](https://clawhub.ai/user/kevinsutianxing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial-analysis agents use this skill to retrieve current, query-relevant financial information such as news, announcements, research reports, policy updates, trading rules, and event analysis. It is intended for workflows where timely external financial context is needed before answering a user question. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a locally stored MX_APIKEY and sends financial search queries to an external search service. <br>
Mitigation: Use the skill only when that data flow is acceptable, store the API key in an environment variable, avoid committing credentials, and rotate the key if exposure is suspected. <br>
Risk: The shell script interpolates the query directly into a JSON request body, which may fail or behave unexpectedly for unusual query text such as embedded quotes. <br>
Mitigation: Use simple query text or improve JSON escaping before relying on queries that contain special characters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kevinsutianxing/dongcai) <br>
- [Eastmoney-related financial news search API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and plain text or JSON API response content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an MX_APIKEY environment variable and network access to the external search endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
