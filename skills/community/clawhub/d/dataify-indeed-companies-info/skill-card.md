## Description: <br>
Collect Indeed company information through Dataify Scraper API by creating collection tasks from Indeed company list URLs, keywords, industries and states, or company URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to configure and submit Dataify Scraper API tasks that collect Indeed company profile information from list URLs, keywords, industry and location filters, or specific company URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Indeed company URLs, keywords, industries, locations, task metadata, and account-authenticated requests to Dataify. <br>
Mitigation: Install only if this data sharing is acceptable for the account and use case, and confirm parameters before each API call. <br>
Risk: The skill handles a Dataify API token and may receive one through command-line arguments or local environment configuration. <br>
Mitigation: Prefer a scoped DATAIFY_API_TOKEN environment variable, avoid passing tokens with --token when possible, never echo tokens, and review any permanent shell-profile storage before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-indeed-companies-info) <br>
- [Publisher profile](https://clawhub.ai/user/dataify-server) <br>
- [Dataify Indeed Companies Info API Reference](references/indeed_companies_info_api.md) <br>
- [Dataify Scraper API builder endpoint](https://scraperapi.dataify.com/builder?platform=1) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration guidance] <br>
**Output Format:** [Markdown confirmation tables, command examples, and task status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Dataify API token and submits Indeed collection parameters to Dataify after user confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
