## Description:

AgentPatch is a tool marketplace for AI agents that provides access to external capabilities such as web search, image generation, email, maps, YouTube transcripts, stock data, and more through one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fullthom](https://clawhub.ai/user/fullthom)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to discover, configure, and run AgentPatch tools for external tasks such as search, image generation, email, maps, market data, web scraping, and profile lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes agents toward a dynamic third-party tool marketplace that includes email, inbox, scraping, profile, and other externally visible capabilities.

Mitigation: Review the selected AgentPatch tool before execution, use only a scoped API key, and require confirmation before email or other externally visible actions.

Risk: Prompts, account data, or other sensitive information may be sent to external AgentPatch tools.

Mitigation: Avoid sending sensitive prompts or private account data unless necessary for the task and approved by the user.

Risk: Installing or invoking the AgentPatch CLI introduces third-party package and runtime behavior into the agent environment.

Mitigation: Install the CLI in an isolated environment with a pinned, reviewed version when possible.

## Reference(s):

- [AgentPatch homepage](https://agentpatch.ai)
- [AgentPatch ClawHub listing](https://clawhub.ai/fullthom/skills/agentpatch)
- [AgentPatch MCP endpoint](https://agentpatch.ai/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AgentPatch CLI commands, MCP server configuration, environment variable setup, and operational guidance for tool use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
