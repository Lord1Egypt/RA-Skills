## Description:

Coordinates multi-agent expert discussions through an orchestrator, agenda checklist tracking, and three-round Diverge, Discuss, and Converge cycles for each agenda item.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luciuscao](https://clawhub.ai/user/luciuscao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to run structured expert discussions for complex problems that benefit from multiple perspectives, agenda tracking, consensus building, and action planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves complete discussion transcripts into workspace files.

Mitigation: Use it only when transcript retention is acceptable, and avoid secrets, credentials, regulated personal data, or confidential material unless that content may be written into reports.

Risk: Long-running subagent activity can produce large discussion outputs that need review.

Mitigation: Monitor the discussion workspace and review generated agenda, transcript, report, and action-plan files after the session.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luciuscao/skills/deep-discussion)
- [Discussion Protocol](artifact/references/discussion-protocol.md)
- [Agenda Checklist Guide](artifact/references/agenda-tracking.md)
- [Orchestrator Facilitation Guide](artifact/references/facilitation-guide.md)
- [Session Management Guide](artifact/references/session-management.md)
- [Convergence Criteria](artifact/references/convergence-criteria.md)
- [Deep Discussion Report Template](artifact/references/output-template.md)
- [Expert Roles](artifact/references/expert-roles.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates agenda.md, discussion-log.md, report.md, and action-plan.md under workspace/deep-discussion/{topic-slug}/.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-03-14; artifact frontmatter version 3.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
