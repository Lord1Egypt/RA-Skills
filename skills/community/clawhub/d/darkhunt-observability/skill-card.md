## Description: <br>
Darkhunt Observability exports OpenClaw agent activity as OpenTelemetry traces and logs so operators can inspect decisions, tool use, performance, token usage, cost, and user attribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volkodavs](https://clawhub.ai/user/volkodavs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this plugin to add observability to OpenClaw agent runs, including trace timelines, tool calls, model usage, latency, cost estimates, and user or channel context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telemetry may expose agent content, tool data, user identity, saved credentials, or prompt snippets, especially outside metadata mode. <br>
Mitigation: Install only for trusted OTLP endpoints, keep payload_mode set to metadata for sensitive conversations, and use debug or full only when the destination and retention policy are acceptable. <br>
Risk: Configuration is stored in ~/.openclaw/openclaw.json and may include authorization headers, workspace IDs, and application IDs. <br>
Mitigation: Treat the OpenClaw configuration file as sensitive, restrict local file permissions, and rotate tokens if the file is exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volkodavs/darkhunt-observability) <br>
- [Darkhunt Observability](https://darkhunt.ai) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, shell commands, telemetry, guidance] <br>
**Output Format:** [OpenTelemetry protobuf exports, JSON configuration, and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports traces and optional logs to a configured OTLP endpoint; payload_mode controls whether metadata only, truncated content, or fuller conversation content is included.] <br>

## Skill Version(s): <br>
0.3.8-build-14 (source: server release evidence; package version 0.3.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
