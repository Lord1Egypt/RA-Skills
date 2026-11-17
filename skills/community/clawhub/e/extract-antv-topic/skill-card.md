## Description:

为AI开发和QA设计的模型上下文协议服务器，提供AntV文档上下文和代码示例。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to route AntV-related questions, extract topics and intent, and retrieve AntV documentation context and code examples from the XiaoBenYang MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AntV-related prompts, code snippets, errors, and derived task data are sent to the XiaoBenYang MCP service.

Mitigation: Use only approved data with this skill and do not send secrets or proprietary code unless that sharing is approved.

Risk: The API key can be persisted in a local .env file in the workspace.

Mitigation: Prefer a scoped environment secret, avoid shared or committed workspaces, and remove saved keys after use.

Risk: The security summary reports copied or mismatched project content.

Mitigation: Review the artifact behavior, service dependency, and publisher ownership before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/extract-antv-topic)
- [XiaoBenYang service](https://xiaobenyang.com)
- [XiaoBenYang MCP service endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown summary of retrieved JSON results and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AntV library names, topic keywords, intent, subtasks, and token-limited documentation excerpts.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
