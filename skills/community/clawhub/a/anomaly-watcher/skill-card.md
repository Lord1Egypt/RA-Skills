## Description:

Continuous behavioral monitoring for OpenClaw agents. Detect anomalies in command patterns, resource usage, and skill invocations against established baselines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arhadnane](https://clawhub.ai/user/arhadnane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to monitor OpenClaw agent activity, establish behavioral baselines, and surface anomalies that may indicate compromise, misconfiguration, or abuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently records broad agent activity, including prompts, tool activity, skill activity, baselines, and anomaly events.

Mitigation: Use it only in a private workspace, review what is logged, and define retention, rotation, and deletion for .security records.

Risk: The skill can write monitoring files under caller-chosen input.path locations.

Mitigation: Restrict input.path to intended workspace directories and avoid shared or sensitive paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arhadnane/skills/anomaly-watcher)
- [Publisher profile](https://clawhub.ai/user/arhadnane)

## Skill Output:

**Output Type(s):** [Analysis, Files, JSON, Guidance]

**Output Format:** [JSON responses and JSONL monitoring records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local .security baseline, anomaly, and false-positive records; baseline calibration requires at least 48 hours of data.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
