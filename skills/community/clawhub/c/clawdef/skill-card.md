## Description:

ClawDef is a self-hosted token optimization dashboard for OpenClaw that tracks token usage, estimates costs, supports provider setup, budget controls, waste detection, and local model switching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gs921302](https://clawhub.ai/user/gs921302)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and administrators use ClawDef to monitor local token usage, estimate costs, configure model providers, enforce budgets, and choose lower-cost models from a localhost dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local SQLite database may contain sensitive monitoring data, including tool arguments and account records.

Mitigation: Run ClawDef only as the intended OpenClaw user on a trusted machine and treat the database as sensitive data with restricted local access.

Risk: Provider credential handling and custom provider URLs can expose API keys to an untrusted destination.

Mitigation: Use custom provider URLs only when the destination is trusted with the associated API key.

Risk: Service installation guidance can be overprivileged if run as a root systemd service.

Mitigation: Avoid the root systemd service as written and run the dashboard with least-privilege user permissions.

Risk: The first-run administrator account controls dashboard actions and should not remain uninitialized.

Mitigation: Initialize the admin account immediately after first launch and keep the service bound to localhost unless explicitly reviewed.

## Reference(s):

- [ClawDef ClawHub skill page](https://clawhub.ai/gs921302/skills/clawdef)
- [Node.js](https://nodejs.org)
- [Chart.js](https://www.chartjs.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on a local OpenClaw dashboard and related setup, configuration, and operating steps.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
