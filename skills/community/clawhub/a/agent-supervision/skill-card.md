## Description:

Supervise another OpenClaw agent with fixed-interval or ETA-based check-ins, progress classification, escalation, and delivery verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z157181773](https://clawhub.ai/user/z157181773)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to supervise another OpenClaw agent with recurring progress checks, ETA follow-up, stagnation detection, and concise escalation messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session history and target session keys may contain sensitive information.

Mitigation: Confirm the target sessionKey, authorization to supervise that session, and sensitivity handling before reading or sending session messages.

Risk: Poorly scoped supervision can create noisy or misdirected check-ins.

Mitigation: Confirm the frequency or ETA policy, what counts as progress, the escalation threshold, and when the supervision cron should stop.

Risk: A synchronous send timeout could be mistaken for delivery failure.

Mitigation: Read the target session after a timeout and inspect recent messages before deciding whether the supervision message failed to land.

Risk: Publishing workflow commands may install global packages from an unverified source or with excessive privileges.

Mitigation: Verify the official clawhub package source and avoid running global npm installs with elevated privileges.

## Reference(s):

- [Release Notes](references/release-notes.md)
- [ClawHub Publish Notes](references/clawhub-publish.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown guidance with concise supervision messages and JSON cron configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses fixed-format status codes; requires a target sessionKey, supervision cadence or ETA policy, progress criteria, and escalation threshold.]

## Skill Version(s):

0.1.1 (source: server release metadata and release-notes.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
