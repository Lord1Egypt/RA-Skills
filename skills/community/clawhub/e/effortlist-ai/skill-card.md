## Description:

Manage EffortList AI folders, tasks, and todos for life organization, project tracking, and schedule management through the EffortList AI platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quarantiine](https://clawhub.ai/user/quarantiine)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage EffortList AI folders, tasks, todos, booking links, appointments, and scheduling preferences with authenticated API access. It supports planning projects, editing scheduled items, reviewing appointment workflows, and using undo or redo when changes need to be reversed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad authority over EffortList account data, schedules, booking links, and appointments.

Mitigation: Use a dedicated API key, limit autonomous execution, and revoke the key from the EffortList dashboard when access is no longer needed.

Risk: Deletes, booking-link changes, appointment changes, and public-token actions can be destructive or externally visible.

Mitigation: Require explicit user confirmation before these actions and use undo or redo workflows when supported.

Risk: Scheduling edits can create conflicts or affect protected time.

Mitigation: Check current availability, timezone, weekly schedule, minimum notice, and overlap responses before finalizing schedule changes.

Risk: Bulk operations can hit API limits or miss records in large datasets.

Mitigation: Respect the 100 requests per minute limit, inspect rate-limit headers, and use limit and offset pagination for list endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quarantiine/skills/effortlist-ai)
- [EffortList homepage](https://www.effortlist.io)
- [EffortList API docs](https://www.effortlist.io/docs)
- [EffortList security](https://www.effortlist.io/security)
- [EffortList AI Technical API Reference](artifact/references/api.md)
- [EffortList AI Omni Architecture and Lifecycle](artifact/references/architecture.md)
- [EffortList AI Security and Data Privacy](artifact/references/security.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with REST endpoint examples and configuration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EFFORTLIST_API_KEY and may direct authenticated changes to folders, tasks, todos, booking links, appointments, and availability settings.]

## Skill Version(s):

1.10.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
