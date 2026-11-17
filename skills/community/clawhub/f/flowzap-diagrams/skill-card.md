## Description:

Generate, validate, and publish workflow, sequence, and architecture diagrams using the FlowZap Code DSL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flowzap-xyz](https://clawhub.ai/user/flowzap-xyz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn natural-language requests, HTTP logs, OpenAPI specs, or code snippets into FlowZap workflow, sequence, process, and architecture diagrams. With the FlowZap MCP server configured, agents can validate FlowZap Code, create playground URLs, diff diagram versions, and apply structured diagram changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using flowzap-mcp through npx introduces normal third-party package supply-chain risk.

Mitigation: Use the pinned flowzap-mcp@1.3.6 package, verify published integrity values, and prefer a reviewed or pinned install source.

Risk: Generated or agent-provided FlowZap Code is sent to flowzap.xyz when validation or playground creation is requested.

Mitigation: Redact secrets, credentials, private URLs, and proprietary process details before creating playground links.

Risk: Playground URLs expose submitted diagram code to anyone with the link until the short-lived session expires.

Mitigation: Share playground URLs only with intended recipients and avoid placing sensitive content in generated diagrams.

## Reference(s):

- [FlowZap Code full spec](https://flowzap.xyz/flowzap-code)
- [FlowZap MCP server docs](https://flowzap.xyz/docs/mcp)
- [FlowZap Code JSON syntax schema](https://flowzap.xyz/api/flowzap-code-schema.json)
- [FlowZap LLM context file](https://flowzap.xyz/llms-full.txt)
- [flowzap-mcp npm package](https://www.npmjs.com/package/flowzap-mcp/v/1.3.6)
- [FlowZap Code syntax reference](references/syntax.md)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with raw .fz FlowZap Code, install/configuration snippets, validation results, and playground URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can use the FlowZap MCP server to validate diagrams, create shareable playground URLs, export structured graph JSON, diff diagram versions, and apply structured changes.]

## Skill Version(s):

1.3.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
