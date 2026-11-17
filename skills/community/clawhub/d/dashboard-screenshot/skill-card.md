## Description:

Captures a full-page OpenClaw dashboard screenshot and sends a concise status report through QQBot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzh19701008](https://clawhub.ai/user/zzh19701008)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators use this skill to check whether the local dashboard is running, capture a full-page dashboard image, and share current bot status, token usage, scheduled tasks, and gateway health through QQBot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dashboard screenshots can expose private operational details and may be sent automatically to a fixed QQBot recipient.

Mitigation: Use the skill only with an approved QQBot target, confirm the recipient before sending, and redact or avoid dashboards that contain sensitive operational data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzh19701008/skills/dashboard-screenshot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown status report with shell commands and a PNG dashboard screenshot file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow may start a local dashboard service, use browser automation, save a full-page PNG screenshot, and send it through QQBot.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
