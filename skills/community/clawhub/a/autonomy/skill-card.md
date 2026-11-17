## Description:

Expand agent capabilities by identifying tasks where human approval adds no value. Systematic delegation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Employees, developers, and agent operators use this skill to identify repeated conversation-based bottlenecks, propose task delegation, and track approved delegation pilots without observing activity outside the conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage agents to take over impactful workflows with reduced notification and unclear guardrails.

Mitigation: Keep approvals narrow, written, task-specific, and reversible; require separate review, logging, and rollback controls before allowing autonomy for production, access, financial, deletion, external communication, or sensitive account changes.

Risk: Delegation proposals can become overbroad if the agent treats one approval as blanket permission.

Mitigation: Require explicit user approval for each scope increase and use the documented pilot, tracking, and rollback process before moving to higher autonomy levels.

Risk: Pattern detection could drift into surveillance if an implementation looks outside the conversation.

Mitigation: Limit observations to explicit user statements, repeated conversation requests, and user complaints; do not monitor files, systems, calendar, email, or other activity without separate permission.

## Reference(s):

- [Autonomy Skill Page](https://clawhub.ai/ivangdavila/skills/autonomy)
- [bottlenecks.md](artifact/bottlenecks.md)
- [expansion.md](artifact/expansion.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with short templates and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and maintain local markdown tracking files under ~/autonomy after user approval.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
