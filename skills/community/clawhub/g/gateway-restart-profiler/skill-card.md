## Description:

Profiles OpenClaw Gateway restart performance by restarting the gateway, parsing startup logs, and generating timing reports with optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tstj007](https://clawhub.ai/user/tstj007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to measure OpenClaw Gateway restart phases, identify slow startup stages, and produce text and HTML reports for troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the profiler restarts OpenClaw Gateway and can interrupt active work.

Mitigation: Run it only during an approved maintenance or troubleshooting window after confirming that a restart is acceptable.

Risk: The skill text asks agents to run commands with elevated privileges.

Mitigation: Prefer running the Linux profiler without elevation as the OpenClaw user, and grant additional privileges only after reviewing the command and local environment.

Risk: The documented Windows PowerShell profiler is not included in the artifact for review.

Mitigation: Do not use the advertised Windows command unless the missing PowerShell script is supplied and reviewed.

Risk: Generated HTML reports load Chart.js from a CDN.

Mitigation: Open reports only in environments where external network loading is acceptable, or replace the CDN dependency with a reviewed local asset.

## Reference(s):

- [Gateway Restart Profiler on ClawHub](https://clawhub.ai/tstj007/skills/gateway-restart-profiler)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Console text plus generated TXT and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include phase timing data, visual charts, and optimization suggestions.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
