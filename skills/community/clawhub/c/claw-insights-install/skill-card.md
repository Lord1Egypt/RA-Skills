## Description:

Installs and helps operate Claw Insights, a local read-only observability dashboard for OpenClaw agents with session replay, token and tool tracking, and shareable status snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucal6](https://clawhub.ai/user/lucal6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, configure, verify, upgrade, and troubleshoot the Claw Insights dashboard for a local OpenClaw gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path recommends executing a remote shell script.

Mitigation: Use a pinned, verifiable package or inspect the installer before running it.

Risk: The dashboard reads local OpenClaw transcripts, logs, cron metadata, and stores metrics.

Mitigation: Install only for trusted local use, keep authentication enabled, and restrict access to localhost or a protected tunnel.

Risk: Snapshots or API responses can expose private session content.

Mitigation: Review snapshots and API output before sharing them outside the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucal6/skills/claw-insights-install)
- [Configuration Reference](references/configuration.md)
- [Troubleshooting](references/troubleshooting.md)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers local installation, service management, verification, upgrade, configuration, and troubleshooting commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
