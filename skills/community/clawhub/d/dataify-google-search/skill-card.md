## Description: <br>
Dataify Google Search helps an agent prepare confirmed Google Search requests for the Dataify Scraper API and return the raw API response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to convert a requested Google web search or SERP crawl into confirmed Dataify Scraper API parameters, execute the request with a Dataify token, and receive the raw search response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search requests and query parameters are sent to Dataify's API. <br>
Mitigation: Install and use the skill only when sending search requests to Dataify is acceptable for the intended data and workflow. <br>
Risk: API tokens may be exposed if passed on the command line or stored plainly in shell startup files. <br>
Mitigation: Provide DATAIFY_API_TOKEN through a secure secret mechanism and avoid echoing or committing token values. <br>
Risk: The skill returns raw API output without summarization or filtering. <br>
Mitigation: Review the raw response before sharing, storing, or using it in downstream decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/dataify-google-search) <br>
- [Dataify Google Search API Reference](references/google_search_api.md) <br>
- [Dataify Scraper API Endpoint](https://scraperapi.dataify.com/request) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, text] <br>
**Output Format:** [Markdown confirmation table, shell command invocation, and raw API response body] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN or an explicitly supplied token before real API calls; returns raw API output without summarization or reshaping.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
