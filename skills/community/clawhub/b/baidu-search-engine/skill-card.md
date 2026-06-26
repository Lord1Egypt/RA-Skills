## Description: <br>
Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve live Baidu web search results for documentation lookup, current information, and research topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu's Qianfan API and the submitted request body is echoed in command output. <br>
Mitigation: Avoid submitting secrets or highly sensitive text in the query field, and handle terminal output or logs as potentially containing user queries. <br>
Risk: The skill requires BAIDU_API_KEY in the runtime. <br>
Mitigation: Provide the key through environment management and avoid hard-coding it in prompts, scripts, or checked-in files. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/cgxxxxxxxxxxxx/baidu-search-engine) <br>
- [Baidu Qianfan AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON search references printed to stdout, with status and error text when applicable.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and python3; accepts query, count, and freshness request fields.] <br>

## Skill Version(s): <br>
1.1.4 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
