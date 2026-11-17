## Description:

Install an alert-only OpenClaw session sentinel that reports high context use without resetting or deleting sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw developers and operators use the monitor to detect high-context sessions and notify an approved local operator through Discord. Recovery actions remain a separate decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The monitor may scan all sessions returned by OpenClaw; the --agent option does not restrict monitoring.

Mitigation: Check which sessions the OpenClaw CLI returns and review the dry-run cron entry before installing.

Risk: Discord alerts include session identifiers and token counts, and failed sends may record the recipient in local logs.

Mitigation: Verify the approved Discord operator ID and protect the session-guard state and log files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniel-refahi-ikara/skills/dr-session-cleaner)
- [Session Diagnosis Reference](references/manual-reset.md)
- [Setup Commands](references/setup-commands.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance, shell commands, a cron entry, and Discord alert text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alerts can include session identifiers and token counts; they do not include session transcripts.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
