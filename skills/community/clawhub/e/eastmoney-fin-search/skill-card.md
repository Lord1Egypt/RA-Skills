## Description: <br>
Searches Eastmoney financial-news sources for time-sensitive market information, including news, announcements, research reports, policies, trading rules, event context, and impact analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QQK000](https://clawhub.ai/user/QQK000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, developers, and financial analysts use this skill to retrieve current, source-filtered financial information for market research, securities news, announcements, policy updates, and event-specific analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial search queries are sent to Eastmoney's external API. <br>
Mitigation: Avoid confidential trading, due-diligence, or sensitive business wording in queries. <br>
Risk: The skill requires MX_APIKEY for API access. <br>
Mitigation: Store MX_APIKEY only as a protected environment variable in trusted runtime environments. <br>
Risk: Search results are saved as local TXT and JSON files. <br>
Mitigation: Delete saved output files when local financial search history should not be retained. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/QQK000/eastmoney-fin-search) <br>
- [Eastmoney News Search API Endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Terminal text plus saved TXT and JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MX_APIKEY and sends query text to Eastmoney's API.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
