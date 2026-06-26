## Description: <br>
Uses Eastmoney Miaoxiang financial search to retrieve current financial information such as news, announcements, research reports, policies, trading rules, event details, and impact analysis from more authoritative sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search financial-market queries against Eastmoney's API and receive current, finance-focused search results. It is suited for stock, sector, macro, policy, event-impact, news, announcement, and research-report lookups where stale or low-authority sources would be risky. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial search text is sent to Eastmoney's external API. <br>
Mitigation: Avoid confidential client, portfolio, or nonpublic business information in queries unless policy explicitly allows sharing it with the API provider. <br>
Risk: Result files are saved locally and may persist after the agent run. <br>
Mitigation: Use the default output directory or a deliberate output path you control, and remove saved .txt and .json files when they are no longer needed. <br>
Risk: The skill requires an API key in MX_APIKEY. <br>
Mitigation: Keep MX_APIKEY only in trusted execution environments and do not expose it in prompts, logs, or frontend code. <br>


## Reference(s): <br>
- [Eastmoney Miaoxiang financial search API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search) <br>
- [ClawHub skill page](https://clawhub.ai/zhouhuihui008/eastmoney-fin-search-1-0-5) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Terminal text plus saved .txt and .json files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MX_APIKEY, sends query text to Eastmoney's API, and writes results to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json reports 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
