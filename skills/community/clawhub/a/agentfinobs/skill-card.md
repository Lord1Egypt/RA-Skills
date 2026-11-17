## Description:

AI Agent Financial Observability monitors, budgets, analyzes, and exports spending metrics across AI agents and payment rails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oc127](https://clawhub.ai/user/oc127)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Agentfinobs to record agent transactions, enforce spending budgets, detect unusual spend, compute financial metrics, and export observability data for dashboards or monitoring systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dashboard and Prometheus endpoints can expose sensitive financial observability data if made reachable on a shared network.

Mitigation: Bind endpoints to localhost where possible, or protect them with network controls and authentication before using them in cloud, container, LAN, or shared environments.

Risk: JSONL files, webhook payloads, dashboard responses, and metrics may include agent IDs, task IDs, counterparties, descriptions, tags, amounts, revenue, PnL, and timing data.

Mitigation: Treat exported and persisted records as sensitive financial data; restrict access, redact where appropriate, and send webhooks only to trusted endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oc127/skills/agentfinobs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for using a Python financial observability package that can emit JSONL records, webhook payloads, HTTP dashboard responses, and Prometheus metrics.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
