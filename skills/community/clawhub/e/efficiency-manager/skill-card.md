## Description:

Efficiency Manager is a local execution coach that captures activities, reviews time use, suggests next moves, and drafts realistic day plans from task inputs, deadlines, and energy patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and agents use this skill to log local activity, review where time went, choose a next task, and draft realistic schedules from task inputs and activity history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local activity records that may include sensitive work or personal time details.

Mitigation: Use it only where a shared local activity log is acceptable, avoid logging sensitive details, and review stored records under ~/.openclaw/efficiency-manager when needed.

Risk: Delete and config commands can change local history or settings.

Mitigation: Use state-changing commands deliberately, confirm the target record or setting first, and prefer list or report commands before modifying data.

Risk: The planning and next-task guidance is lightweight and may not account for all deadlines, conflicts, or calendar constraints.

Mitigation: Treat schedules and recommendations as drafts, review them against real commitments, and avoid relying on them as calendar-grade optimization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/efficiency-manager)
- [API Reference](artifact/references/api.md)
- [Scoring Heuristics](artifact/references/scoring.md)
- [Scheduling Heuristics](artifact/references/scheduling.md)
- [Data Model](artifact/references/data-model.md)
- [Benchmarks](artifact/references/benchmarks.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and JSON returned by local wrapper commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local shared activity logs under ~/.openclaw/efficiency-manager; planning outputs are lightweight drafts, not calendar-grade optimization.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
