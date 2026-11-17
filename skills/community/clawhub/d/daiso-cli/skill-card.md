## Description:

Daiso CLI helps agents search Daiso, Korean convenience store, mart, Olive Young, Megabox, Lotte Cinema, and CGV data through the Daiso CLI or MCP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmmhmmhm](https://clawhub.ai/user/hmmhmmhm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to choose and run Daiso CLI commands or configure the public MCP endpoint for Korean retail, inventory, cinema, store, and product lookups. It is useful when the agent needs structured lookup results, follow-up IDs, or concise summaries from live external services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill repeatedly recommends running an unpinned npm CLI, so future unreviewed package code could execute on the user's machine.

Mitigation: Prefer a pinned reviewed package version such as daiso@1.0.6, review the dependency source and update process before installation, and run it in a sandboxed environment.

Risk: CLI execution may expose local context or credentials if run from sensitive directories.

Mitigation: Use minimal credentials and avoid running the CLI from sensitive directories unless the dependency source is trusted.

## Reference(s):

- [Daiso CLI Command Map](references/cli-command-map.md)
- [Daiso MCP Project Homepage](https://github.com/hmmhmmhm/daiso-mcp)
- [Daiso Public MCP Endpoint](https://mcp.aka.page)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, CLI arguments, MCP endpoint configuration, and concise lookup summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented command flags and preserved product, store, theater, or movie identifiers for follow-up lookup.]

## Skill Version(s):

1.0.6 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
