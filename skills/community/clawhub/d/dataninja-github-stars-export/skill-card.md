## Description:

Export GitHub starred repositories by category and sync them to a Notion database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nick-tsyen](https://clawhub.ai/user/nick-tsyen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual GitHub users use this skill to export starred repositories into Markdown and sync the exported list into a structured Notion database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Notion sync can archive existing database rows when rerun against an existing database.

Mitigation: Run it only against a dedicated test or backup database first, and add confirmation or dry-run safeguards before using it with valuable Notion data.

Risk: The Notion API calls disable TLS certificate verification while using the Notion token.

Mitigation: Remove verify=False and keep TLS verification enabled before providing a Notion integration token.

Risk: The skill requires authenticated GitHub CLI access and a Notion integration token.

Mitigation: Use least-privilege credentials, scope the Notion integration to a dedicated page or database, and revoke tokens after testing if they are no longer needed.

## Reference(s):

- [Exporting Stars](references/export_stars.md)
- [Syncing to Notion](references/sync_stars.md)
- [GitHub CLI](https://cli.github.com/)
- [jq](https://jqlang.github.io/jq/)
- [Notion Developers](https://developers.notion.com/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown files, shell commands, Python script execution, and local JSON sync state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces assets/starred_lists.md and may create or update a Notion database when run with credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
