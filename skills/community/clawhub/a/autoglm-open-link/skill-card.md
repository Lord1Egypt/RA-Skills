## Description: <br>
Uses the AutoGLM Open Link API to open a supplied web page URL and extract the page's main text for downstream summarization, extraction, or analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyfujian](https://clawhub.ai/user/flyfujian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch readable article or web page text from a URL, then summarize it, extract facts, or analyze the content for a user task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically uses a local bearer token and sends submitted URLs to an external API without enough scoping or user-control detail. <br>
Mitigation: Install only if you trust AutoGLM and the local token service; confirm the bearer token is intended only for this API and scoped narrowly. <br>
Risk: Submitted URLs and related retrieval targets are sent to a third-party API. <br>
Mitigation: Avoid private, internal, or sensitive targets unless the data-sharing path has been approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flyfujian/autoglm-open-link) <br>
- [AutoGLM Open Link API endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/open-link) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON response containing extracted page text; agents may present the text directly or transform it into Markdown summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a target URL and returns API errors directly when retrieval fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
