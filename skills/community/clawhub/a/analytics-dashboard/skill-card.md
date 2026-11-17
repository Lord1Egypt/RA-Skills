## Description:

Analytics Dashboard helps agents query operational dashboards through a configured dashboard-mcp server for realtime statistics, system health, tenant overviews, content queues, event subscriptions, agent status, and daily briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to retrieve dashboard data for live service status, tenant activity, queues, recent events, health checks, and agent status. It is intended for environments with an authorized and trusted dashboard-mcp configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can surface operational, tenant, event, health, and agent-status data from the configured dashboard-mcp server.

Mitigation: Install it only where dashboard-mcp is trusted and users are authorized to view that data.

Risk: Documentation contains a stray Cookie-management sentence and limited data-handling guidance.

Mitigation: Ask the publisher to remove the unrelated sentence and clarify how sensitive dashboard results should be handled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/analytics-dashboard)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [dashboard-mcp server reference](mcps/dashboard-mcp/server.py)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON dashboard results with concise natural-language summaries when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only dashboard responses may include tenant, event, health, and agent-status data from the configured dashboard-mcp server.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
