## Description:

cron402 helps agents operate explicitly requested paid remote webhook schedules through cron402 or agentcron.site, including wallet checks, schedule previews, job creation, top-ups, inspection, pause, resume, and deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[userdefault13](https://clawhub.ai/user/userdefault13)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they have explicitly chosen cron402 or agentcron.site to create and manage paid remote webhook jobs. It guides agents through schedule preview, user confirmation, wallet readiness, credit management, status checks, and credential-safe job administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid create and top-up actions spend real USDC from the configured wallet.

Mitigation: Use a dedicated low-balance wallet, check funding first, preview the schedule for free, and require explicit user confirmation before each paid action.

Risk: Remote job configuration can include URLs, headers, bodies, notify URLs, or query strings that may contain sensitive data.

Mitigation: Review these fields before job creation, avoid reusable admin credentials and session cookies, redact secret values in agent output, and rotate target credentials if they may have been disclosed.

Risk: A remote cron job can continue firing after the agent session or local machine is offline.

Mitigation: Report the job ID, schedule, next run times, and credit behavior so the user can inspect, pause, resume, top up, or delete the job later.

## Reference(s):

- [cron402 ClawHub Skill](https://clawhub.ai/userdefault13/skills/cron402)
- [abracadabra Companion Skill](https://clawhub.ai/userdefault13/skills/abracadabra)
- [cron402 OpenAPI](https://cron402-api.user-defaults.workers.dev/v1/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confirmation prompts, schedule summaries, job identifiers, and redacted handling of credentials or secret-bearing fields.]

## Skill Version(s):

1.1.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
