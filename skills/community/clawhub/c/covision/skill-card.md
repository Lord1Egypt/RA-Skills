## Description:

Covision helps agents prepare for client work using the signed-in user's accessible Covision tasks, meetings, and published knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[covision-admin](https://clawhub.ai/user/covision-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams with Covision access use this skill to prepare for client meetings, review assigned or overdue tasks, and search published Covision knowledge while staying within the signed-in user's permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Covision meeting, task, and knowledge results may contain confidential organizational information.

Mitigation: Use the skill only in contexts where information available to the signed-in Covision account may be surfaced.

Risk: Users may assume the agent can modify Covision records.

Mitigation: Treat the connector as read-only and do not state that tasks, meetings, or records were created, changed, assigned, or sent.

Risk: Covision access may be unavailable or insufficient for a requested meeting, organization, or time range.

Mitigation: State when access is unavailable, avoid guessing outside Covision, and ask a focused follow-up when available results do not resolve the request.

## Reference(s):

- [Covision skill page](https://clawhub.ai/covision-admin/skills/covision)
- [Publisher profile](https://clawhub.ai/user/covision-admin)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text responses with cited Covision record titles, dates, or URLs when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only responses are bounded by the signed-in user's Covision permissions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
