## Description:

Improves ACP bridge availability and autonomous agent session management by addressing persistence, provider environment injection, host cron scheduling, and shared workspace locking gaps in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to keep OpenClaw ACP sessions recoverable across bridge restarts, prepare autonomous sessions with required provider environment variables, schedule approved host-side cron jobs, and coordinate shared workspace writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider API keys may be exposed to autonomous recipient sessions.

Mitigation: Use short-lived scoped credentials, run dry-run allowlist checks before injection, restrict target sessions, and avoid PROXY_URL or CUSTOM_* entries unless reviewed.

Risk: Recurring host-level cron commands can bypass sandbox isolation.

Mitigation: Require explicit human approval, fixed allowlisted jobs, logging, expiration, and a documented removal path before scheduling any host-side cron command.

Risk: Workspace locks are advisory and can leave stale ownership if agents fail to release them.

Mitigation: Use acquire-work-release patterns with try/finally release handling and periodic stale session cleanup before shared workspace writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/skills/firm-acp-bridge)
- [Skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, JSON]

**Output Format:** [Markdown with JSON examples and inline command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational patterns for ACP session persistence, provider environment handling, cron scheduling, workspace locking, and session health monitoring.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
