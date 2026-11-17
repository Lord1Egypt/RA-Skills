## Description:

Logs FlashRev mailer send and dry-run records to a configured Notion database for campaign tracking and audit queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sawera557](https://clawhub.ai/user/sawera557)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators running FlashRev mailer use this skill after send or dry-run batches to write campaign email records to Notion and query prior campaign sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign email metadata and a 300-character body preview are copied into Notion.

Mitigation: Use the skill only for campaigns appropriate for Notion logging and avoid logging sensitive campaigns unless that storage is approved.

Risk: The Notion integration token can access any workspace content granted to that integration.

Mitigation: Limit the Notion integration to the intended database and rotate or revoke NOTION_TOKEN if access is no longer needed.

Risk: Dependency installation may resolve newer package versions because the package file does not include a lockfile and uses a semver range.

Mitigation: Pin the Notion client dependency and use a package-lock.json with npm ci before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sawera557/skills/flashrev-mailer-notion-tracker)
- [Publisher profile](https://clawhub.ai/user/sawera557)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Notion sync status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js plus NOTION_TOKEN and NOTION_DATABASE_ID configuration; logs campaign email metadata and a 300-character body preview to Notion.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
