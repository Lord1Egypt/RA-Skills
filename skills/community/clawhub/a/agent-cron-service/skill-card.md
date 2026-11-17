## Description:

Agent Cron Service helps agents create and manage hosted SettleMesh cron schedules for recurring jobs such as daily digests, uptime monitors, recurring scrapes, and periodic reports with idempotent billing and spend caps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[structureintelligence](https://clawhub.ai/user/structureintelligence)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy hosted agents, create cron schedules, manage schedule histories, and pause or resume recurring jobs without running their own scheduler infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated recurring jobs can incur third-party metered charges or continue firing until paused.

Mitigation: Confirm SettleMesh use before install, use limited-scope credentials, configure per-fire and per-day caps, and review schedules before resuming.

Risk: Installing or running an unpinned CLI can change behavior across releases.

Mitigation: Prefer a pinned settlemesh CLI version if available and avoid sudo or global installs where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/structureintelligence/skills/agent-cron-service)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command blocks and JSON CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the settlemesh CLI and SETTLE_API_KEY; scheduled jobs may make authenticated, metered network calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
