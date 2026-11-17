## Description:

Query DeepWiki MCP to get AI-grounded answers about any public GitHub repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to ask natural-language questions about public GitHub repositories, list DeepWiki documentation topics, and retrieve indexed wiki content for codebase understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository names and user questions are sent to DeepWiki through outbound HTTP requests.

Mitigation: Use the skill for public repositories and avoid prompts containing private code, secrets, customer data, incident details, or proprietary architecture.

Risk: Broad automatic triggers may route repository questions to DeepWiki without an explicit privacy confirmation.

Mitigation: Consider tightening triggers or requiring explicit user confirmation before outbound queries.

## Reference(s):

- [DeepWiki](https://deepwiki.com)
- [DeepWiki MCP Documentation](https://docs.devin.ai/work-with-devin/deepwiki-mcp)
- [DeepWiki MCP Endpoint](https://mcp.deepwiki.com/mcp)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [ClawHub Skill Page](https://clawhub.ai/chunhualiao/skills/deepwiki-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text returned from DeepWiki, with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source references, topic lists, or full wiki content for public repositories.]

## Skill Version(s):

1.0.0 (source: server release evidence, skill.yml, CHANGELOG released 2026-02-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
