## Description:

Explains a GetItDone task's status, notes, attachments, dependencies, and available video-frame context without changing the task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

GetItDone users can ask an agent to explain a single task, including why it is blocked and what attached recordings show in available still-frame summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task notes, attachments, dependency details, and video-frame summaries may contain sensitive information.

Mitigation: Access only tasks the user asks about and limit the response to relevant details.

Risk: Attachment links expire and may become unusable.

Mitigation: Do not present attachment links as permanent; retrieve fresh task details when needed.

## Reference(s):

- [Investigating Tasks on ClawHub](https://clawhub.ai/devino/skills/getitdone-investigating-tasks)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-language task summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; video descriptions rely on still frames rather than audio transcription.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
