## Description:

Draft, update, and publish SEO blog posts to Blogizi from a local repo using the Blogizi CLI, hosted MCP as a sandbox backup, or the public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blogizi](https://clawhub.ai/user/blogizi)

### License/Terms of Use:

AGPL-3.0-only

## Use Case:

Developers, content teams, and coding-agent users use this skill to create local Markdown posts with Blogizi frontmatter, then draft, update, or publish those posts to Blogizi after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses an account-scoped Blogizi API key and may store it in ~/.blogizi/config.json.

Mitigation: Use a safer authentication flow or environment variable when available, restrict permissions on the config file, never paste keys into chat, and rotate any key exposed through shell history or shared systems.

Risk: Publish and update operations can change live blog content.

Mitigation: Default to draft creation, review the Markdown file and dashboard preview, and publish only after explicit user confirmation.

Risk: Accounts with multiple projects can update the wrong blog if the active project slug is incorrect.

Mitigation: Confirm the project slug before draft, update, or publish operations, and use blogizi use or the project option to set the intended project.

Risk: Hosted MCP or public API workflows transmit post content and authentication headers to Blogizi.

Mitigation: Prefer the CLI when available, configure MCP credentials in the client instead of chat, and use the raw API only when CLI and MCP paths are unavailable or explicitly requested.

## Reference(s):

- [Blogizi CLI publishing docs](https://blogizi.com/docs/cli-publishing)
- [Blogizi MCP docs](https://blogizi.com/docs/mcp)
- [Blogizi Markdown frontmatter docs](https://blogizi.com/docs/markdown-frontmatter)
- [Blogizi public API docs](https://blogizi.com/docs/public-api)
- [Blogizi Obsidian docs](https://blogizi.com/docs/obsidian)
- [Blogizi agent-readable site overview](https://blogizi.com/llms.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with inline shell commands, JSON snippets, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Markdown post files and propose CLI, MCP, or API publishing steps for user review.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
