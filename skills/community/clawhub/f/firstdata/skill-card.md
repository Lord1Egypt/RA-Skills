## Description:

FirstData helps agents find official portals, APIs, download paths, and citation-ready guidance for authoritative primary data sources across 1000+ global sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ningzimu](https://clawhub.ai/user/ningzimu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use FirstData to locate authoritative primary data sources, compare source authority, and obtain official URLs, API documentation, download paths, and citation-ready access guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path includes an unpinned `npx mcporter` command.

Mitigation: Prefer the manual MCP configuration or use a pinned, trusted `mcporter` version before installation.

Risk: FIRSTDATA_API_KEY is a long-lived API token.

Mitigation: Store the token in a protected environment variable or secret manager, keep it out of source control and logs, and rotate it if exposed.

## Reference(s):

- [FirstData project homepage](https://github.com/MLT-OSS/FirstData)
- [FirstData README](https://raw.githubusercontent.com/MLT-OSS/FirstData/refs/heads/main/README.md)
- [FirstData registration guide](references/firstdata-register.md)
- [FirstData MCP endpoint](https://firstdata.deepminer.com.cn/mcp)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with URLs, API details, MCP configuration examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FIRSTDATA_API_KEY for authenticated MCP access.]

## Skill Version(s):

0.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
