## Description:

Monitors agent health status and detects failures for fault-tolerant agent systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check OpenClaw agent and session health, identify inactive agents, and summarize local CPU and memory pressure for reliability monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes shell commands while checking sessions, system resources, and a hard-coded wrapper lifecycle script.

Mitigation: Install and run it only in a trusted local environment where OpenClaw state and the referenced wrapper skill are expected to be inspected.

Risk: The skill reads local OpenClaw agent and session files and Linux system resource files.

Mitigation: Review the local paths and monitoring scope before use, and avoid running it where agent/session metadata should remain isolated.

Risk: The public description under-discloses the shell command and wrapper lifecycle checks noted by security review.

Mitigation: Tell users that health checks include shell execution and wrapper status inspection before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/agent-health-monitor)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [JSON health reports and concise text status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include session counts, failed agents, wrapper status, CPU load, memory usage, and issue counts.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
