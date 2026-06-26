## Description: <br>
USE when implementing data ingestion for Agnost AI analytics. Contains API reference, SDK guides for Python and TypeScript, and code examples for tracking AI conversations, MCP server events, and user interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AjmeraParth132](https://clawhub.ai/user/AjmeraParth132) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to integrate Agnost AI analytics into AI applications, chatbots, agents, and MCP servers. It provides SDK, API, and implementation guidance for capturing sessions, events, user interactions, latency, and metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analytics examples can capture prompts, outputs, MCP tool inputs or results, user traits, IP addresses, and other metadata. <br>
Mitigation: Decide what data is allowed to leave the system before implementation, avoid secrets or regulated data, and minimize or pseudonymize user traits such as names and emails. <br>
Risk: MCP input and output capture can expose sensitive tool data. <br>
Mitigation: Disable or redact MCP input and output capture for sensitive tools. <br>


## Reference(s): <br>
- [Agnost Official Docs](https://docs.agnost.ai) <br>
- [Agnost API Endpoint](https://api.agnost.ai) <br>
- [Agnost Dashboard](https://app.agnost.ai) <br>
- [Agnost API Reference](references/api-reference.md) <br>
- [Python SDK Reference](references/python-sdk.md) <br>
- [TypeScript SDK Reference](references/typescript-sdk.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python, TypeScript, Go, HTTP, JSON, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; examples may send analytics data to Agnost endpoints when users implement them.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter metadata is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
