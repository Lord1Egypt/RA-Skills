## Description:

Darkhunt Observability monitors OpenClaw agent runs with real-time traces showing decisions, tool usage, performance, costs, and user attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volkodavs](https://clawhub.ai/user/volkodavs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this plugin to instrument OpenClaw agents, export OpenTelemetry traces, and review tool calls, model usage, latency, cost, and user attribution during agent runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telemetry can expose tool inputs, tool results, user identity, and credentials more broadly than a metadata-only description may imply.

Mitigation: Review payload mode before production use, prefer the minimum useful telemetry, and patch or disable tool-result and direct PII export where the workspace handles private data.

Risk: Exporting traces to an untrusted endpoint can disclose operational metadata or content from private agent runs.

Mitigation: Use only trusted OpenTelemetry endpoints and confirm authentication, workspace, and application headers before enabling exports.

Risk: OpenClaw configuration and backups can contain telemetry endpoints, authorization headers, workspace IDs, and application IDs.

Mitigation: Restrict access to OpenClaw config files and backups, and rotate credentials if those files are exposed.

## Reference(s):

- [Darkhunt Observability ClawHub listing](https://clawhub.ai/volkodavs/skills/darkhunt-observability)
- [Darkhunt Observability service](https://darkhunt.ai)

## Skill Output:

**Output Type(s):** [configuration, shell commands, telemetry traces, logs, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON configuration, and OTLP/protobuf telemetry payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports metadata, debug, and full payload modes with batching, export timeouts, and span size limits.]

## Skill Version(s):

0.3.8-build-14 (source: server release metadata; package.json reports 0.3.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
