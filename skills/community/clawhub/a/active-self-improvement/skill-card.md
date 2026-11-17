## Description:

Active self-improvement loop that reads learnings, errors, batch outputs, and memory, detects recurring patterns, and updates skills, protocols, behavior, memory, tickets, or reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn repeated errors, corrections, stale memory, delegation drift, and unused opportunities into proposed or applied improvements to agent behavior and supporting files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically rewrite agent skills, behavior guidance, permanent memory, reminders, tickets, and routing protocols.

Mitigation: Run in dry-run or proposal mode by default and require explicit approval before writes to skills, AGENTS.md, SOUL.md, permanent memory, routing protocols, cron, tickets, or reminders.

Risk: Incorrect pattern detection could persist misleading guidance or stale facts into future agent behavior.

Mitigation: Review proposed evidence links, exact edits, risk level, reversibility, and recurrence counts before accepting changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown proposals, file edits, and concise status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write directly to skills, behavior files, permanent memory, tickets, reminders, and routing guidance unless used in dry-run or approval-gated mode.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact frontmatter says 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
