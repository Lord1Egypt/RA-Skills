## Description:

Use when building a new MCP server in TypeScript, Python, or C# that exposes tools to LLMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, implement, test, and evaluate MCP servers that expose tools to LLM clients across TypeScript, Python, and C# stacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example MCP server patterns could be copied into unsafe deployments without enough review.

Mitigation: Review and harden generated MCP server code before use, especially examples involving file resources, credential prompts, or destructive tool behavior.

Risk: Dependency and command examples may introduce supply-chain or runtime risk if executed unpinned.

Mitigation: Pin package versions, verify packages on official registries, and review commands before running them.

Risk: Generated tools that modify external services can cause unintended changes if authorization and scope checks are missing.

Mitigation: Require explicit authorization checks, validate inputs at the tool boundary, and annotate destructive tools clearly before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afonsoft/skills/building-mcp-servers)
- [Skill metadata repository URL](https://github.com/afonsoft/skills)
- [MCP Server Development Guide](SKILL.md)
- [MCP Server Best Practices](references/mcp_best_practices.md)
- [Node/TypeScript MCP Server Implementation Guide](references/node_mcp_server.md)
- [Python MCP Server Implementation Guide](references/python_mcp_server.md)
- [.NET/C# MCP Server Implementation Guide](references/dotnet_mcp_server.md)
- [MCP C# SDK 2.0 What's New](references/dotnet_mcp_v2.md)
- [Quick Start: Language Implementations](references/quick-start.md)
- [Transport, Authentication, and Migration](references/transport-and-auth.md)
- [MCP Server Evaluation Guide](references/evaluation.md)
- [Model Context Protocol documentation](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with code blocks, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose MCP server code, dependency installation commands, authentication patterns, and evaluation artifacts for reviewer approval.]

## Skill Version(s):

1.0.7 (source: server release metadata; skill frontmatter metadata.version is 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
