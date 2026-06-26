## Description: <br>
Provides guidance for answering OpenAI product and API questions with current official OpenAI developer documentation and citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lichaohui007](https://clawhub.ai/user/lichaohui007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical agents use this skill to look up OpenAI platform, Codex, ChatGPT Apps SDK, Realtime API, Agents SDK, and related product documentation before producing concise implementation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct an agent to modify local Codex MCP configuration and retry MCP setup with elevated permissions. <br>
Mitigation: Manually review and approve MCP configuration changes, and allow elevated-permission retries only when the local configuration change is understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lichaohui007/ddddd) <br>
- [OpenAI Developer Docs MCP server](https://developers.openai.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with citations, inline code, and fenced code blocks when supported by the referenced documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP setup commands and official documentation citations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
