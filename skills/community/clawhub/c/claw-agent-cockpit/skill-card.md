## Description:

CLAW Agent 智控驾驶舱 deploys a local operations dashboard for OpenClaw Coding Plan users to monitor API quota, forecast usage, analyze token trends, manage Cron jobs, track Agent status, and watch subscription expiry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mumuli2021](https://clawhub.ai/user/mumuli2021)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy and operate a local OpenClaw Coding Plan dashboard for API quota monitoring, usage forecasting, token analysis, Agent status tracking, and Cron task management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local dashboard services can expose workspace files and unauthenticated mutable APIs if bound to a network.

Mitigation: Install in an isolated workspace, bind services to 127.0.0.1 or place them behind authentication, and do not expose ports 8888 or 8889.

Risk: Dashboard-rendered data and background collection can introduce unsafe display behavior or unexpected monitoring activity.

Mitigation: Sanitize dashboard-rendered data and treat the recommended Cron job as an opt-in background collector.

Risk: Unpinned runtime dependencies can change local service behavior over time.

Mitigation: Pin PM2 or use a reviewed local dependency before deploying the services.

## Reference(s):

- [Cron Setup Guide](references/cron-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown deployment guidance with shell command snippets, JavaScript and HTML dashboard files, PM2 configuration, and JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local dashboard service, API service, quota tracker, Agent data updater, seed data files, and Cron setup guidance.]

## Skill Version(s):

1.2.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
