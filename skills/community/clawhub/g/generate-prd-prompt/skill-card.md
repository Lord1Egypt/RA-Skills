## Description:

Mercury Spec Ops MCP Server 是一个基于模块化架构的动态提示生成和模板组装工具，适用于AI助手与专业内容的交互，支持31种技术栈、10种分析维度和34个模板部分的动态生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI assistant users use this skill to generate product requirements, codebase analysis, and bug analysis prompts or markdown templates for selected technology stacks and focus areas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt inputs, project context, bug details, and the API key may be sent to the XiaoBenYang MCP API.

Mitigation: Use only with data approved for that service, avoid secrets and private source code, and review the endpoint before use.

Risk: The API key may be stored in a local plaintext .env file.

Mitigation: Prefer a secure environment or secret mechanism, ensure .env is not committed or shared, and avoid untrusted .env files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/generate-prd-prompt)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text summarized from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY credential and may include user-supplied project context, technology stack, analysis focus, severity, or bug context.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
