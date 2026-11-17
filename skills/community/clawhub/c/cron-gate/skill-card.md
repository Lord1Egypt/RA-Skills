## Description:

Cron Gate helps agents set up a lightweight Python gatekeeper that checks local OpenClaw session activity before triggering configured cron jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ori-claw](https://clawhub.ai/user/ori-claw)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to avoid unnecessary LLM cron wake-ups by checking local session timestamps before triggering OpenClaw cron jobs. It is intended for OpenClaw environments where periodic tasks can be gated by cheap local activity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A system crontab entry can automatically trigger existing OpenClaw cron jobs in the background.

Mitigation: Review each SESSION_CRONS mapping before installation, run with --dry-run first, and remove the crontab entry when background triggering is no longer wanted.

Risk: Incorrect session keys, cron IDs, or gateway settings could trigger the wrong job or fail to gate an intended job.

Mitigation: Confirm session keys from the local sessions.json file, verify cron IDs through OpenClaw, and keep the gateway URL pointed at the intended local service.

## Reference(s):

- [Cron Gate on ClawHub](https://clawhub.ai/ori-claw/skills/cron-gate)
- [ori-claw publisher profile](https://clawhub.ai/user/ori-claw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local crontab setup guidance, session-to-cron mapping configuration, dry-run usage, and operational cautions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
