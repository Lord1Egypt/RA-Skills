## Description: <br>
Query Cloudflare Workers Observability logs via API for checking logs, debugging Workers, looking up errors, and investigating Worker, Durable Object, Workflow, Queue, and Cron Trigger behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adaHubble](https://clawhub.ai/user/adaHubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query and summarize Cloudflare Workers Observability logs from an agent terminal session while debugging Workers, Durable Objects, Workflows, Queues, and Cron Triggers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloudflare API token exposure or overly broad log access can expose sensitive operational data. <br>
Mitigation: Install only where the agent is allowed to access Workers logs, use a dedicated narrowly scoped Cloudflare API token, and keep .env files out of version control. <br>
Risk: Broad log queries may surface unnecessary sensitive log content. <br>
Mitigation: Prefer specific worker names, short time windows, and low result limits, and avoid putting secrets in application logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adaHubble/cf-workers-logs) <br>
- [Skill homepage](https://github.com/adaHubble/cf-workers-logs) <br>
- [Cloudflare Workers Observability query endpoint](https://api.cloudflare.com/client/v4/accounts/{accountId}/workers/observability/telemetry/query) <br>
- [Cloudflare dashboard](https://dash.cloudflare.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API query guidance] <br>
**Output Format:** [Markdown with inline curl commands and formatted log timelines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Cloudflare account ID and API token environment variables; defaults to short recent log queries when arguments are omitted.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
