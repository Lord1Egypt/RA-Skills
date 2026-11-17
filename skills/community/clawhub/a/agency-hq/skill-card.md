## Description:

Agency HQ provides a pixel art dashboard that visualizes AI agent status, activity feeds, and personality-driven banter in OpenClaw live mode or standalone demo mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spockthegreatbot](https://clawhub.ai/user/spockthegreatbot)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use Agency HQ to monitor OpenClaw agent activity through a visual office dashboard, or to demonstrate a simulated agent team without connecting to live local data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can read private OpenClaw agent logs and host telemetry and expose them through unauthenticated web endpoints.

Mitigation: Keep demo mode enabled unless live monitoring is required; when live mode is needed, bind the service to localhost or place it behind authentication and avoid exposing the Next.js port to a network.

Risk: Agent session content may include sensitive prompts or operational details.

Mitigation: Limit which agent IDs are configured, validate those IDs before deployment, and avoid displaying raw prompt content in shared or public dashboards.

Risk: Dependency vulnerabilities may affect a long-running dashboard.

Mitigation: Review dependency scan results during release intake and keep Next.js, React, and related packages updated.

## Reference(s):

- [Agency HQ ClawHub Release](https://clawhub.ai/spockthegreatbot/skills/agency-hq)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown setup guidance with shell commands and a Next.js TypeScript dashboard project]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in demo mode with simulated data or live mode reading local OpenClaw session files and host telemetry.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
