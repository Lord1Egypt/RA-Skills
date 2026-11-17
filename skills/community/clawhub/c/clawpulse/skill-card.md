## Description:

ClawPulse connects an OpenClaw agent to the ClawPulse community analytics dashboard and can collect and push aggregate token, model, tool, cost, message, and session statistics without message content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pierreeurope](https://clawhub.ai/user/pierreeurope)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers use this skill to install and configure ClawPulse, authenticate with GitHub, push aggregate local session statistics, and optionally schedule recurring updates to the community dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub credential reuse could grant the CLI access through an existing GitHub CLI token.

Mitigation: Prefer the documented interactive device-flow setup and confirm requested GitHub scopes before storing a token.

Risk: Silent recurring cron pushes can create ongoing telemetry from local session files.

Mitigation: Enable scheduled pushes only after confirming the aggregate data collected and the desired recurrence.

Risk: The globally installed openclaw-pulse package runs with access to local session files and stored credentials.

Mitigation: Inspect or pin the package version before installation and before granting access to session data or credentials.

## Reference(s):

- [ClawPulse dashboard](https://clawpulse.vercel.app)
- [ClawPulse personal dashboard](https://clawpulse.vercel.app/dashboard)
- [ClawPulse community leaderboard](https://clawpulse.vercel.app/community)
- [openclaw-pulse npm package](https://www.npmjs.com/package/openclaw-pulse)
- [Project source link listed by skill](https://github.com/pierreeurope/clawpulse)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, authentication, data collection, and cron scheduling guidance.]

## Skill Version(s):

0.3.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
