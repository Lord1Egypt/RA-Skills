## Description: <br>
Sync OpenClaw fleet runtime/heartbeat/cron status to Cloudflare KV and serve dashboard-ready data via Worker API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reed1898](https://clawhub.ai/user/reed1898) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up and operate the Agent Fleet Dashboard data plane, including Cloudflare Worker and KV setup, collector cron scheduling, dashboard environment wiring, and migration of high-frequency fleet state out of Git. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deploy and cron commands can execute code from local Worker and collector projects outside this documentation skill. <br>
Mitigation: Review the referenced projects before running npm deploy or collector commands, and document how to remove installed cron entries. <br>
Risk: Ingest, read, dashboard, and report tokens could be exposed through files, logs, screenshots, or client-side environment variables. <br>
Mitigation: Use dedicated Cloudflare, Vercel, or system secret storage; keep tokens server-side; redact logs and shared snippets; rotate credentials immediately if exposed. <br>
Risk: Dashboard sync may expose unnecessary operational data if collector payloads or event buffers are too broad. <br>
Mitigation: Limit uploaded data to operational telemetry, validate payloads, truncate long error fields, redact secret-like patterns, and keep event buffers bounded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reed1898/agent-dashboard-sync) <br>
- [Worker Setup](references/worker-setup.md) <br>
- [Collector + Cron](references/collector-cron.md) <br>
- [Env Matrix](references/env-matrix.md) <br>
- [KV Schema](references/schema.md) <br>
- [Security Rules](references/security-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, cron, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces runbook guidance for Worker deployment, KV schema setup, environment variables, collector cron installation, and security checks.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
