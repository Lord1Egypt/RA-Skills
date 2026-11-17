## Description:

Operate Breakcold CRM through the hosted Breakcold MCP server from OpenClaw or ClawHub for CRM work, deals, pipeline updates, follow-up tasks, reports, prospect research, inbox contact detection, CRM setup, notes, custom fields, and multichannel inbox workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matteoolefloch](https://clawhub.ai/user/matteoolefloch)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and CRM users use this skill to operate Breakcold CRM from an agent, including follow-up task creation, pipeline movement, reporting, prospect research, inbox contact detection, and CRM setup or reorganization. It is intended for agent-assisted CRM workflows that may read inbox and CRM data and make controlled updates through the hosted Breakcold MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read inbox and CRM data and make persistent CRM changes.

Mitigation: Enable it only for trusted Breakcold workspaces and confirm workspace, channels, date range, and permitted write operations before broad use.

Risk: Recurring routines may continue making CRM updates beyond the immediate session.

Mitigation: Set explicit cadence, recap recipients, and stop conditions before enabling routines, and review routine output regularly.

Risk: CRM reorganization, contact creation, pipeline movement, and prospect research can affect many records.

Mitigation: Use previews or small batches first, then expand only after confirming the results match the user's expectations.

Risk: Generated rich HTML notes may carry formatting or sanitization risk.

Mitigation: Confirm that Breakcold sanitizes rich HTML notes before relying on automatic note generation.

## Reference(s):

- [Breakcold CRM OpenClaw homepage](https://github.com/breakcold/mcp/tree/main/skills/breakcold-crm-openclaw)
- [Fundamentals](references/fundamentals.md)
- [Action 1 - Multichannel auto-task creation](references/action-tasks.md)
- [Action 2 - Auto-movement of contacts in the pipeline](references/action-pipeline.md)
- [Action 3 - Auto-report](references/action-reports.md)
- [Action 4 - Prospect research](references/action-prospect-research.md)
- [Action 5 - Contact detection and creation from the inbox](references/action-contact-detection.md)
- [Action 6 - CRM setup and reorganization](references/action-crm-setup.md)
- [Routines and recap emails](references/routines.md)
- [Breakcold branding](references/branding.md)
- [Report design guide](references/report-design-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown, Code, Configuration]

**Output Format:** [Agent instructions, tool-call plans, CRM updates, rich HTML notes, Markdown summaries, and generated report HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Breakcold MCP authentication and optional BREAKCOLD_MCP_TOKEN configuration for clients that cannot use OAuth.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
