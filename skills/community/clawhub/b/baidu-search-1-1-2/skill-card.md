## Description: <br>
Search the web using Baidu AI Search Engine (BDSE) for live information, documentation, or research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeayoo](https://clawhub.ai/user/jeayoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve current Baidu web search results through a Python command when an answer needs live information, documentation, or research material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu using the configured BAIDU_API_KEY. <br>
Mitigation: Avoid secrets or confidential terms in queries and use a dedicated API key with appropriate limits. <br>
Risk: The helper depends on the Python requests package and network access to Baidu's API. <br>
Mitigation: Install dependencies from trusted sources and run the skill only in environments where Baidu API access is expected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jeayoo/baidu-search-1-1-2) <br>
- [Baidu AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands] <br>
**Output Format:** [JSON search results printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; supports query, count from 1 to 50, and freshness filters using date ranges or pd, pw, pm, py.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
