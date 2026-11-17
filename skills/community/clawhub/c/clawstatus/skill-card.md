## Description:

ClawStatus provides a real-time dashboard for monitoring OpenClaw devices, agents, sessions, cron jobs, models, and token usage with English and Chinese interface support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neverchenx](https://clawhub.ai/user/neverchenx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to inspect local OpenClaw health, runtime activity, scheduled jobs, model configuration, and token usage from a dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive OpenClaw status, model, session, cron, and token usage data may be exposed by the dashboard.

Mitigation: Run the dashboard only in a controlled local environment and review or redact sensitive responses before wider access.

Risk: Administrative controls can change models, run or delete cron jobs, and restart OpenClaw services.

Mitigation: Require authentication, protect or disable mutation endpoints, and avoid exposing the service on a public or shared network.

Risk: The documented example binds the dashboard to 0.0.0.0.

Mitigation: Bind to localhost by default unless network exposure has been explicitly reviewed and secured.

## Reference(s):

- [ClawStatus on ClawHub](https://clawhub.ai/neverchenx/skills/clawstatus)
- [OpenClaw project](https://github.com/anthropics/OpenClaw)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for running and managing a local dashboard service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
