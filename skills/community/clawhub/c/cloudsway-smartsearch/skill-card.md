## Description: <br>
Performs real-time web searches to retrieve up-to-date online information, news, research data, and fact-checking results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prismheart](https://clawhub.ai/user/prismheart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI agents and LLM systems use this skill to search the web for current information, news, research sources, documentation, and fact checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and API usage are sent to Cloudsway. <br>
Mitigation: Avoid sending secrets, private customer data, or highly sensitive topics in search requests. <br>
Risk: The CLOUDSWAYS_AK API key is required to use the service. <br>
Mitigation: Store the key securely and avoid exposing it in shared logs, screenshots, or troubleshooting output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/prismheart/cloudsway-smartsearch) <br>
- [Cloudsway homepage](https://cloudsway.ai) <br>
- [Cloudsway SmartSearch API endpoint](https://aisearchapi.cloudsway.net/api/search/smart) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [JSON search results with titles, URLs, snippets, dates, and optional extracted page text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLOUDSWAYS_AK, curl, and jq; query, count, freshness, pagination, and content extraction options are supplied as JSON input.] <br>

## Skill Version(s): <br>
1.0.6 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
