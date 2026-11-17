## Description:

Syncs OpenClaw fleet runtime, heartbeat, and cron status to Cloudflare KV and serves dashboard-ready data through a Worker API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reed1898](https://clawhub.ai/user/reed1898)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to set up and run an Agent Fleet Dashboard data plane, including Cloudflare KV storage, Worker ingest/read APIs, collector cron scheduling, environment configuration, and migration away from Git-backed high-frequency state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Collector cron examples can expose ingest tokens if real values are placed directly in crontab, logs, screenshots, or shared commands.

Mitigation: Use secret managers or protected system profiles for runtime tokens, keep placeholders in shared snippets, redact logs, and rotate any exposed token immediately.

Risk: The sync pipeline handles fleet telemetry and operational status that may reveal infrastructure details if over-collected or over-retained.

Mitigation: Send only operational telemetry, omit chat content, PII, and credential-bearing command output, truncate error fields, and keep event buffers bounded.

Risk: Public ingest and read endpoints can be abused if authentication, transport, payload, or rate controls are misconfigured.

Mitigation: Require HTTPS and bearer authentication, validate JSON schema and payload size, reject invalid tokens with 401 responses, and add basic rate limiting.

## Reference(s):

- [Worker Setup](references/worker-setup.md)
- [Collector + Cron](references/collector-cron.md)
- [Env Matrix](references/env-matrix.md)
- [KV Schema (v1)](references/schema.md)
- [Agent Dashboard Sync - Security Rules](references/security-rules.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, cron, JSON, and environment-variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No LLM output is required in the collector path; examples use placeholders for secrets and local paths.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
