## Description:

Sets up an active-passive OpenClaw failover gateway with a standby node that auto-promotes on primary failure, auto-demotes on recovery, and uses health monitoring, systemd services, channel splitting, and Git workspace sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ember-claw](https://clawhub.ai/user/ember-claw)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to deploy and test a standby OpenClaw gateway for high availability, disaster recovery, and redundant access when the primary node is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent root-level monitoring can expand operational impact if misconfigured or compromised.

Mitigation: Review before installation, run the monitor under a dedicated least-privilege account, and apply systemd hardening.

Risk: Remote installer commands may execute unverified code on the target server.

Mitigation: Prefer verified package repositories or pinned checksums before running installation commands.

Risk: Health checks and failover signals may be spoofed or unreliable if not authenticated.

Mitigation: Use authenticated health checks over a private network and test failover behavior before production use.

Risk: Optional secret synchronization handles sensitive production credentials.

Mitigation: Treat rsync secret transfer as production credential handling and restrict access, storage, and logging.

## Reference(s):

- [Tailscale](https://tailscale.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown deployment guidance with bash, JSON, and systemd configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a shell health-monitor script and deployment steps for a standby OpenClaw gateway.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
