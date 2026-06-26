## Description: <br>
Searches Eastmoney financial information sources for timely news, announcements, research reports, policies, trading rules, event details, and impact analysis so agents can avoid stale or non-authoritative finance references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and financial-analysis agents use this skill to retrieve current Eastmoney-sourced financial information for company, sector, macro, policy, market-event, and risk-analysis questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User queries are sent to Eastmoney's external API. <br>
Mitigation: Avoid confidential or regulated information in search queries and use the skill only when Eastmoney is an acceptable external data processor. <br>
Risk: The skill requires an Eastmoney API key in the runtime environment. <br>
Mitigation: Use a dedicated API key where possible, keep it in EASTMONEY_APIKEY, and avoid exposing it in prompts, logs, or client-side contexts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/eastmoney-financial-search-1-0-2) <br>
- [Eastmoney Skills API key page](https://marketing.dfcfs.com/views/finskillshub/indexuNdYscEA?appfenxiang=1) <br>
- [Eastmoney news search API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EASTMONEY_APIKEY and sends the user's query to Eastmoney's external API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
