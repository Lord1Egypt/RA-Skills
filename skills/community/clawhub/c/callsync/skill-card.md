## Description:

Look up a team's business calls, recordings and AI call summaries in CallSync, and keep its CRM up to date (contacts, follow-up tasks, notes). Use when the user asks about calls their team made or received, what a customer said, missed calls to return, call summaries, or wants to add a contact, a note or a follow-up task in CallSync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[callsync](https://clawhub.ai/user/callsync)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and customer-facing teams use this skill to find calls, recordings, transcripts, and AI summaries, and to review or update CallSync CRM contacts, tasks, and notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Call records can contain customer phone numbers, transcripts, and private business details; recording links can be opened by anyone who has them.

Mitigation: Share call details and recording links only with the user who requested them, and keep the workspace API key private, out of URLs, and out of printed output.

Risk: Creating or updating CRM contacts, tasks, and notes changes team records.

Mitigation: Identify the intended contact, summarize the proposed change, and get user approval before writing; avoid retrying a note request that may already have succeeded.

## Reference(s):

- [CallSync REST API reference](references/api.md)
- [CallSync website](https://callsyncapp.com)
- [CallSync dashboard](https://dash.callsyncapp.com)
- [CallSync remote MCP server](https://mcp.callsyncapp.com/connect)
- [CallSync n8n node](https://www.npmjs.com/package/n8n-nodes-callsync)
- [CallSync Activepieces integration](https://www.npmjs.com/package/@callsyncapp/piece-callsync)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Natural-language summaries and guidance, with JSON requests and responses for API operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
