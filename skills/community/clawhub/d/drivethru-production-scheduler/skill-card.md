## Description:

Schedules Odoo MRP production batches by ranking open jobs, surfacing art and receipt blockers, and applying machine and time slots when the available evidence is reliable enough.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

Production planners and manufacturing operators use this skill to re-rank Odoo MRP production batches, handle rush orders, identify art or receipt blockers, and place jobs on eligible machines when timing can be justified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Odoo scheduling writes can reorder queues or place batches on machines in ways that affect shop-floor work.

Mitigation: Require explicit approval before queue reordering, individual schedule writes, or bulk scheduling unless a documented automation policy and rollback process is in place.

Risk: The MCP client uses a bearer token and can expose broad manufacturing access if the token or endpoint is misconfigured.

Mitigation: Use a least-privileged Odoo MCP token, restrict server-side tools to the required manufacturing actions, use an approved HTTPS ODOO_MCP_URL, and keep ODOO_MCP_TOKEN out of chat and logs.

Risk: Machine slots based on uncertain art readiness, receipt timing, or duration estimates can produce unreliable schedules.

Mitigation: Leave slots empty when confidence is low, surface art and receipt blockers, prefer starts on or after expected_ready_date, and use atomic bulk scheduling for multi-update passes.

## Reference(s):

- [Scheduling algorithm](references/scheduling_algorithm.md)
- [Receipt readiness](references/receipt_readiness.md)
- [Odoo](https://www.odoo.com)
- [ClawHub skill page](https://clawhub.ai/zmtucker/skills/drivethru-production-scheduler)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown or text responses with shell command examples and JSON MCP call results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform live Odoo scheduling writes when configured and explicitly approved.]

## Skill Version(s):

0.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
