## Description:

Use when setting up clawtel to report token usage from a project that calls the Anthropic API (SDK, Claude Code, or any tapes-wrapped agent) to the claw.tech leaderboard. Covers install, env vars, tapes wiring, verification, and running as a persistent service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bdougie](https://clawhub.ai/user/bdougie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and configure clawtel so Anthropic API usage captured by tapes can be reported to the claw.tech leaderboard. It also helps diagnose missing heartbeats and configure persistent service operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes mutable remote installer commands, including a curl-to-shell path.

Mitigation: Prefer the pinned release and checksum workflow, inspect the installer before use, and install only from sources the operator trusts.

Risk: The optional systemd example runs a downloaded telemetry binary as a persistent root service.

Mitigation: Use a user-owned install location where possible, consider a dedicated unprivileged service account with systemd sandboxing, and review the service before enabling it.

Risk: The setup reports token telemetry from local tapes data to claw.tech.

Mitigation: Confirm the documented security footprint and export CLAW_INGEST_KEY only when telemetry reporting is intended.

## Reference(s):

- [clawtel homepage](https://github.com/bdougie/clawtel)
- [clawtel releases](https://github.com/bdougie/clawtel/releases)
- [clawtel install script](https://raw.githubusercontent.com/bdougie/clawtel/main/scripts/install.sh)
- [tapes installer](https://download.tapes.dev/install)
- [claw.tech](https://claw.tech)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash, JSON, INI, and environment variable snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install, verification, troubleshooting, and service setup steps; does not execute commands.]

## Skill Version(s):

1.2.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
