## Description: <br>
Searches the web using Baidu AI Search Engine (BDSE) for live information, documentation, or research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15914355527](https://clawhub.ai/user/15914355527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to run Baidu web searches from Python-backed workflows when they need live web, documentation, or research results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu and may consume the user's Baidu API quota. <br>
Mitigation: Use only queries that are appropriate for the user's policy and monitor use against the configured Baidu API quota. <br>
Risk: Search queries may contain secrets, personal data, or confidential internal terms. <br>
Mitigation: Do not submit sensitive content unless organizational policy explicitly allows sending it to Baidu. <br>
Risk: The embedded artifact metadata does not exactly match the registry metadata. <br>
Mitigation: Verify the package identity and registry entry before installing or deploying this release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/15914355527/baidu-search-v2) <br>
- [Baidu AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text] <br>
**Output Format:** [JSON search results written to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY; accepts a required query, optional count from 1 to 50, and optional freshness filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
