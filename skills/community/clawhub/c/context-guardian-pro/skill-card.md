## Description:

Context Guardian Pro monitors conversation context pressure and triggers summarization, long-term memory persistence, and QQ alerts when the session approaches configured limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artwebs](https://clawhub.ai/user/artwebs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to reduce context-limit failures by periodically checking session pressure, summarizing heavy sessions, saving summaries to memory, and sending restart reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic summaries may be written to OpenClaw memory when the context threshold is exceeded.

Mitigation: Review memory persistence behavior before installation and avoid storing sensitive conversation content in summaries.

Risk: QQ alert configuration can create an external notification path.

Mitigation: Keep alert messages minimal and exclude sensitive conversation details from notification content.

Risk: Periodic taskflow or cron setup can run the monitor without manual invocation.

Mitigation: Review or disable scheduled execution according to the deployment environment's operational policy.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/artwebs/skills/context-guardian-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Plain text status output with optional Markdown memory entries and alert text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task status and action_taken values; may append generated summaries to OpenClaw memory and emit QQ alert messages when thresholds are exceeded.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
