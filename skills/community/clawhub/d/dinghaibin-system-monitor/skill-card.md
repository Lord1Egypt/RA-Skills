## Description:

Monitor system metrics like CPU, memory, disk, and network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Linux server health, monitor CPU, memory, disk, network, uptime, load, and process status, and configure simple resource-threshold alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Status or JSON output can include process command lines that may reveal tokens, paths, or operational details.

Mitigation: Run with the least-privileged account and avoid forwarding process output to broad logs or dashboards unless it is removed or redacted.

Risk: The security review flagged the skill as suspicious because process command lines can be exposed even when a user asks for narrower metrics.

Mitigation: Review before installing on shared, production, or privileged systems and limit use to systems where process visibility is appropriate.

## Reference(s):

- [System Monitor ClawHub release](https://clawhub.ai/dinghaibin/skills/dinghaibin-system-monitor)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status output may include system metrics, alert messages, and top-process command lines.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
