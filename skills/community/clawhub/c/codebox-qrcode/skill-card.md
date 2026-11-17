## Description:

Generate, manage, and track QR codes via CodeBox API, including dynamic QR codes with style templates, scan analytics, batch generation, and lifecycle management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdfsdjj145](https://clawhub.ai/user/gdfsdjj145)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to create styled QR codes, batch-generate codes, update or delete dynamic QR codes, and retrieve scan analytics through the CodeBox API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dynamic QR codes are trackable and may collect scan analytics such as device, time, and location-derived information.

Mitigation: Use static QR codes when tracking is unnecessary and disclose analytics collection where appropriate.

Risk: Dynamic QR code generation consumes CodeBox credits.

Mitigation: Confirm dynamic mode and expected volume before creating important or large batches of QR codes.

Risk: The CodeBox API key grants access to QR code generation and management actions.

Mitigation: Keep CODEBOX_API_KEY in the environment, avoid sharing it inline, and verify update or delete operations before execution.

## Reference(s):

- [CodeBox API Reference](references/api.md)
- [CodeBox Website](https://www.codebox.club)
- [CodeBox API Docs](https://www.codebox.club/docs/api)
- [CodeBox SDK](https://www.codebox.club/docs/sdk)
- [CodeBox MCP Server](https://www.codebox.club/docs/mcp)
- [ClawHub Skill Page](https://clawhub.ai/gdfsdjj145/skills/codebox-qrcode)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CodeBox API URLs, QR code image URLs, short URLs, and analytics summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
