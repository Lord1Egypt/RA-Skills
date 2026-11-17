## Description:

Manage a Dex personal CRM by helping an agent find, create, update, archive, merge, and organize contacts; log notes; manage follow-ups, tags, groups, custom fields, connected calendar events, correspondence search, and contact research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ocruzv](https://clawhub.ai/user/ocruzv)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate a Dex personal CRM: maintain professional relationships, prepare meetings, organize contacts, manage follow-ups, inspect email metadata, and manage connected calendars.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local integration can give Dex and configured AI clients access to CRM data, connected email metadata, and calendar operations.

Mitigation: Install only after reviewing that access; prefer MCP browser OAuth or one explicitly selected client instead of unattended all-client setup.

Risk: Persistent bearer-token files used by the CLI can expose Dex account access if mishandled.

Mitigation: Treat local Dex token files as sensitive secrets, restrict file permissions, and rotate or clean them up when access is no longer needed.

Risk: Installing a global npm CLI can introduce supply-chain or version-drift risk.

Mitigation: Pin or review npm package versions where possible and update deliberately when the MCP server adds or changes tools.

## Reference(s):

- [Dex Homepage](https://getdex.com)
- [Dex AI MCP Server Docs](https://getdex.com/docs/ai/mcp-server)
- [Dex ClawHub Skill Page](https://clawhub.ai/ocruzv/skills/dex-skill)
- [Dex CLI Command Reference](references/cli-commands.md)
- [CRM Workflows & Relationship Management](references/crm-workflows.md)
- [Dex Tools Reference](references/tools-reference.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool inputs or outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose CRM, email, calendar, and research operations; write operations should be previewed, confirmed, and verified.]

## Skill Version(s):

2.4.2 (source: artifact frontmatter metadata.version and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
