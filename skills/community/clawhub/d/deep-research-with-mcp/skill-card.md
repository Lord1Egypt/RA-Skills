## Description:

Multi-source deep research agent using MCP search tools (minimax web_search or zai-mcp-server web_search_prime).

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghan0501](https://clawhub.ai/user/wanghan0501)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to plan, search, read, synthesize, and deliver cited deep research reports on requested topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary web URLs and save generated reports into the workspace.

Mitigation: Install only where MCP search, page fetching, and workspace writes are acceptable; prefer reviewed HTTPS URLs or a hardened fetcher, especially around secrets, internal networks, or sensitive project files.

## Reference(s):

- [Deep Research with MCP homepage](https://github.com/wanghan0501/deep-research-with-mcp)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub skill page](https://clawhub.ai/wanghan0501/skills/deep-research-with-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown research reports with inline citations, source lists, and methodology notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Long reports may be saved under research/[slug]/report.md according to the skill workflow.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
