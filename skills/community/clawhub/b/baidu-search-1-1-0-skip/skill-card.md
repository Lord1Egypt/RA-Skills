## Description: <br>
Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lulu-owo](https://clawhub.ai/user/lulu-owo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve live web search results from Baidu for current information, documentation, and research tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and filters are sent to Baidu under the configured BAIDU_API_KEY. <br>
Mitigation: Avoid including secrets in queries and use a limited-purpose Baidu API key where possible. <br>
Risk: The skill depends on the local Python requests package and a valid BAIDU_API_KEY. <br>
Mitigation: Confirm dependencies and credentials are available before deployment. <br>


## Reference(s): <br>
- [Baidu AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>
- [ClawHub skill page](https://clawhub.ai/lulu-owo/baidu-search-1-1-0-skip) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON array of Baidu search reference objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, and BAIDU_API_KEY; supports recency, resource type, site, blocked-site, and safe-search filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
