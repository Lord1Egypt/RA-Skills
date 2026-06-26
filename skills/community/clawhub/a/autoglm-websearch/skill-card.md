## Description: <br>
Uses the AutoGLM Web Search API to search the web, retrieve current information, and return page snippets that can be summarized with source references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyfujian](https://clawhub.ai/user/flyfujian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a task needs web search, current information, webpage snippets, and cited source links through AutoGLM. It is best suited to workflows that can safely send search terms to the AutoGLM service and use a local token service for authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to the third-party AutoGLM Web Search API. <br>
Mitigation: Avoid sensitive queries unless the AutoGLM endpoint is approved for that data and the user understands the data sharing. <br>
Risk: The script automatically retrieves and uses a local bearer token without documented scope or consent details. <br>
Mitigation: Confirm the local token service is trusted, the token is intended for this API, and the credential is narrowly scoped before running the skill. <br>
Risk: Security evidence marks the release as suspicious because token handling is underspecified. <br>
Mitigation: Review the skill and authentication flow before deployment, especially in shared or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flyfujian/autoglm-websearch) <br>
- [Publisher profile](https://clawhub.ai/user/flyfujian) <br>
- [AutoGLM Web Search API endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON API responses and Markdown summaries with reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search queries are sent to AutoGLM and execution depends on a local bearer-token service at http://127.0.0.1:53699/get_token.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
