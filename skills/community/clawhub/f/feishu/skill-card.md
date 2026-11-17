## Description:

Feishu is a workplace collaboration orchestration skill that turns Feishu messages, approvals, meetings, documents, tables, calendars, and email into prioritized, executable action chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agisearch](https://clawhub.ai/user/agisearch)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, managers, project leads, and cross-functional coordination owners use this skill to summarize Feishu activity, diagnose collaboration bottlenecks, draft follow-ups, extract meeting actions, analyze tables, and coordinate next steps while preserving authorization boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad workplace integration can expose or modify sensitive Feishu messages, approvals, calendars, documents, and table records if configured with excessive app scopes.

Mitigation: Install only with Feishu app scopes that match the intended use, and keep default operation in counselor mode for read-only summaries and drafts.

Risk: Confirmed write actions such as sending messages, editing tables, coordinating schedules, or advancing approvals can affect workplace decisions and relationships.

Mitigation: Use executive mode only after explicit authorization, and require second confirmation for upward reporting, cross-department public reminders, final approval decisions, key table edits, and irreversible schedule changes.

Risk: Missing context can lead to premature reminders, incorrect ownership assumptions, or updates that conflict with the current source of truth.

Mitigation: Diagnose the collaboration layer first, ask for missing group, approval, document, table, or stakeholder context, and prefer drafts or recommendations until the relevant facts are confirmed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agisearch/skills/feishu)
- [Skill Instructions](artifact/skill.md)
- [Examples](artifact/examples.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown with structured summaries, draft messages, action lists, risk notes, and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET in the host environment for Feishu-connected operation; otherwise it should fall back to general advice mode.]

## Skill Version(s):

1.0.5 (source: server release metadata, skill frontmatter, and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
