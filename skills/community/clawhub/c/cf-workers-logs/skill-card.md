## Description:

Query Cloudflare Workers Observability logs via API for Workers, Durable Objects, Workflows, Queues, and Cron Triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adahubble](https://clawhub.ai/user/adahubble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect recent Cloudflare Workers logs, filter errors, and investigate Worker, Durable Object, Workflow, Queue, or Cron Trigger behavior from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may search project .env files and print matching credential lines, which can expose Cloudflare API tokens in transcripts.

Mitigation: Use a narrowly scoped Cloudflare token, export required variables directly when possible, avoid recursive .env searches, and rotate any token that appears in agent output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adahubble/skills/cf-workers-logs)
- [Cloudflare Workers Observability API endpoint](https://api.cloudflare.com/client/v4/accounts/{accountId}/workers/observability/telemetry/query)
- [Cloudflare dashboard](https://dash.cloudflare.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and formatted log timelines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Cloudflare API request payloads, curl commands, parsed JSON log events, and credential setup guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
