## Description:

Connect to Ben McAdams's personal MCP server for his resume, portfolio, and blog notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benmcgit](https://clawhub.ai/user/benmcgit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure an MCP client for public access to Ben McAdams's resume, portfolio, and blog notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional stdio setup uses an unpinned npx package bridge.

Mitigation: Prefer the direct URL MCP configuration when supported; if stdio is required, pin and review the mcp-remote package before running it.

## Reference(s):

- [Ben McAdams Homepage](https://benmcadams.info)
- [Ben McAdams MCP Endpoint](https://benmcadams.info/api/mcp)
- [ClawHub Skill Page](https://clawhub.ai/benmcgit/skills/ben-mcadams-mcp)

## Skill Output:

**Output Type(s):** [Configuration, Shell commands, Guidance, JSON, Markdown]

**Output Format:** [Markdown with JSON and bash code blocks; MCP tool responses may include JSON, Markdown, links, and text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public MCP endpoint; no credentials required.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
