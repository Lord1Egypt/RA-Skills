## Description:

Use folkctl to inspect and update folk.app CRM data through its REST API. Covers people, companies, groups, members, custom fields, deals, custom objects, batch create/update/delete, users, notes, tasks, interactions, person enrichments, credits, legacy reminders, webhooks, and official MCP setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-edel](https://clawhub.ai/user/j-edel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use folkctl to inspect and manage folk.app CRM records, groups, tasks, interactions, and webhooks through Folk's REST API. It also guides safe previews and confirmation for writes, deletes, group replacement, and credit-using enrichments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation evidence is incomplete because two local references were unresolved.

Mitigation: Review the installation source and resolve the missing references before making the Folk API key available to folkctl.

Risk: Commands can delete records, replace group memberships, or spend workspace credits on enrichments.

Mitigation: Preview writes with --dry-run --json and confirm the exact records, group effects, or enrichment fields and credit use before execution.

## Reference(s):

- [folkctl project homepage (metadata.clawdis)](https://github.com/j-edel/folkctl)
- [Pinned folkctl install source (metadata.clawdis)](https://github.com/j-edel/folkctl/tree/442c1c5e992a0f51c9689341813fd1c319b3b5e2)
- [folkctl v0.3.0 release](https://github.com/j-edel/folkctl/releases/tag/v0.3.0)
- [Folk MCP tools reference](https://developer.folk.app/mcp/tools)
- [Folk reminders-to-tasks migration guide](https://developer.folk.app/migrations/reminders-to-tasks)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mutation previews, paginated records, and per-record batch results.]

## Skill Version(s):

0.3.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
