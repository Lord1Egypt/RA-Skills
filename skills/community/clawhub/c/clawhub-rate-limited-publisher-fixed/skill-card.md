## Description:

Queue and publish local skills to ClawHub with a strict 5-per-hour cap using the local clawhub CLI and host scheduler.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to queue local Skill directories for ClawHub publishing while respecting a five-publish-attempts-per-hour limit. It provides guidance, queue configuration, and commands for running the local helper with cron or systemd.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queue entries can supply a command template that is executed as a broad shell command.

Mitigation: Use only queue files you created and trust, avoid the optional command field, and keep commands limited to publishing the resolved local skill path.

Risk: Scheduling the helper before hardening may repeatedly execute unsafe or unintended commands from the queue.

Mitigation: Do not schedule the helper until the uploader is changed to call a fixed argument list such as clawhub publish <path> with shell=False and protected state updates.

Risk: Publish failures still count against the hourly limit and can consume available attempts when authentication or CLI behavior is broken.

Mitigation: Run a manual clawhub whoami and one dry run before enabling execute mode or a scheduler.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/clawhub-rate-limited-publisher-fixed)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [OpenClaw ClawHub homepage](https://github.com/openclaw/clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON queue examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local python3 and clawhub CLI; reads queue JSON and writes adjacent state/log files when the helper is run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
