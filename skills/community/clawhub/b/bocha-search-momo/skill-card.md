## Description: <br>
博查 AI 搜索工具，调用 https://api.bocha.cn 进行网页搜索，返回带摘要的中文结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justaboyhai-wq](https://clawhub.ai/user/justaboyhai-wq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to run Bocha web searches from an agent workflow and receive summarized Chinese search results. It is intended for query-and-result retrieval, not for private data handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Bocha's external API. <br>
Mitigation: Avoid searching for secrets or sensitive private text, and use the skill only when sending the query to Bocha is acceptable. <br>
Risk: The Bocha API key can be stored in a local configuration file. <br>
Mitigation: Use a dedicated Bocha API key, protect the local config file, and do not commit the key or config file to a repository. <br>


## Reference(s): <br>
- [Bocha Search skill page](https://clawhub.ai/justaboyhai-wq/bocha-search-momo) <br>
- [Bocha website](https://www.bocha.cn) <br>
- [Bocha open platform](https://open.bocha.cn) <br>
- [Bocha Web Search API documentation](https://bocha.com/documents/web-search-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text search results with title, URL, and summary fields; setup guidance uses shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Bocha API key stored in a local config file or provided through BOCHA_API_KEY; search result count defaults to 5 and supports 1-10 results.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
