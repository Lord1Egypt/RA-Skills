## Description: <br>
Doubao Assistant helps agents design Doubao model integrations for streaming chat, function calling, retrieval-augmented generation, batch processing, prompt templates, and usage analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and automation teams use this skill to plan and implement Doubao-backed assistant workflows, including conversational APIs, tool calling, RAG knowledge retrieval, batch request management, and analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests read and exec access and includes broad examples for tool execution and data access. <br>
Mitigation: Use it only in workspaces where read and exec access are acceptable, and restrict execution to reviewed, allowlisted tools. <br>
Risk: Function-calling examples include state-changing operations such as ticket creation. <br>
Mitigation: Require explicit user approval before any create, modify, delete, ticketing, file-writing, or command execution action. <br>
Risk: Doubao and vector database credentials may be needed for normal operation. <br>
Mitigation: Store credentials in environment variables or a secrets manager and avoid hardcoding secrets in skill files, scripts, or generated examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/doubao-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, configuration examples, and structured JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API integration plans, tool schemas, RAG configuration, batch-processing patterns, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
