## Description:

This skill helps developers design and build Model Context Protocol (MCP) servers for Claude by gathering requirements, recommending a deployment model and tool-design pattern, and handing off or scaffolding the appropriate implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan MCP server architecture, choose between remote HTTP, MCP app, MCPB, and local stdio deployment models, and produce practical scaffolding or handoff guidance for Claude-compatible integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable scaffolds can expose public MCP endpoints without enough access control.

Mitigation: Add authentication to public endpoints, validate origins, and require appropriate consent checks before deployment.

Risk: File resource examples can expose unintended local files if copied without restrictions.

Mitigation: Restrict file resources to an explicit approved root and reject traversal and absolute paths.

Risk: Generated scaffold dependencies can drift between builds.

Mitigation: Pin dependencies before deploying or publishing generated MCP servers.

## Reference(s):

- [Auth for MCP Servers](references/auth.md)
- [Deploy to Cloudflare Workers](references/deploy-cloudflare-workers.md)
- [Elicitation - spec-native user input](references/elicitation.md)
- [Remote Streamable-HTTP MCP Server Scaffold](references/remote-http-scaffold.md)
- [Resources and Prompts](references/resources-and-prompts.md)
- [Server capabilities](references/server-capabilities.md)
- [Tool Design](references/tool-design.md)
- [Version pins](references/versions.md)
- [Claude connector documentation export](https://claude.com/docs/llms-full.txt)
- [Claude connector authentication](https://claude.com/docs/connectors/building/authentication)
- [Claude connector testing](https://claude.com/docs/connectors/building/testing)
- [Claude connector review criteria](https://claude.com/docs/connectors/building/review-criteria)
- [Claude connector submission](https://claude.com/docs/connectors/building/submission)
- [Claude connector what to build](https://claude.com/docs/connectors/building/what-to-build)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include architecture recommendations, MCP scaffolds, deployment steps, and handoff summaries.]

## Skill Version(s):

1.0.0 (source: release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
