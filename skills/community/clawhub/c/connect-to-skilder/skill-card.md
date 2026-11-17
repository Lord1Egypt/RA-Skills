## Description:

Connects an agent to Skilder over MCP using the official remote endpoint and OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skilder](https://clawhub.ai/user/skilder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure supported agent hosts to connect to Skilder's remote MCP server, complete OAuth, and report available Roles and Skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs an agent to change MCP configuration and initiate OAuth without asking first.

Mitigation: Use it only when you intentionally want Skilder added as an MCP server, review the exact config command or file change, and approve the OAuth flow yourself.

Risk: A newly added remote MCP server may expose tools the user has not inspected.

Mitigation: Prefer the narrowest session or project scope, inspect the listed remote tools before using them, and keep removal instructions for the added server entry.

## Reference(s):

- [Skilder Skills repository](https://github.com/skilder-ai/skills)
- [ClawHub skill page](https://clawhub.ai/skilder/skills/connect-to-skilder)
- [Skilder MCP endpoint](https://app.skilder.ai/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger OAuth browser sign-in and remote MCP tool discovery.]

## Skill Version(s):

1.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
