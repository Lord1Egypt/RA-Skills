## Description: <br>
Uses the CSTCloud Web Search API to let an agent search the web with a CSTCLOUD_API_KEY and return titles, URLs, sources, and summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shcw0405](https://clawhub.ai/user/shcw0405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give an OpenClaw agent CSTCloud-backed web search, especially when they want a provider reachable from China and configured through a single API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to CSTCloud as an external provider. <br>
Mitigation: Avoid putting secrets, private internal information, or sensitive personal data in search queries. <br>
Risk: The skill requires a CSTCLOUD_API_KEY and command-line tools to function. <br>
Mitigation: Configure the API key in the agent environment and verify bash, curl, and jq are available before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shcw0405/cstcloud-web-search) <br>
- [CSTCloud Uni-API service](https://uni-api.cstcloud.cn) <br>
- [CSTCloud web search endpoint](https://uni-api.cstcloud.cn/v1/web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text search results with titles, URLs, sources, snippets, and command-line status messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a search query and an optional result count from 1 to 10; requires bash, curl, jq, and CSTCLOUD_API_KEY.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
