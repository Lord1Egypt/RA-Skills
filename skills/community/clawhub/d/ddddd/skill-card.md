## Description:

Use when the user asks how to build with OpenAI products or APIs and needs up-to-date official documentation with citations, prioritizing OpenAI docs MCP tools and restricting fallback browsing to official OpenAI domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lichaohui007](https://clawhub.ai/user/lichaohui007)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to answer OpenAI product and API implementation questions with current official documentation and citations. It covers Codex, Responses API, Chat Completions, Apps SDK, Agents SDK, Realtime API, gpt-oss, and related model capability or limit questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause persistent MCP tool configuration changes.

Mitigation: Require explicit user approval before running `codex mcp add` or making persistent agent-tool configuration changes.

Risk: The skill text directs the agent to retry with elevated permissions if MCP installation fails.

Mitigation: Require explicit approval before any elevated-permission retry and explain what persistent change will be made.

## Reference(s):

- [OpenAI Developer Docs MCP](https://developers.openai.com/mcp)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with citations and optional code or shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses official OpenAI documentation as the source of truth when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
