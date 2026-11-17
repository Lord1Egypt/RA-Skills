## Description:

Deploy and manage the EVEZ OpenClaw mesh across GCP and Vultr with scripts for provider integration, infrastructure setup, and health monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure OpenClaw provider integrations, set up a GCP free-tier node, and monitor an OpenClaw gateway in a small multi-cloud fleet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The GCP setup script can create or modify cloud resources.

Mitigation: Run it only against a test or explicitly approved GCP project and review the planned resource changes before execution.

Risk: The GCP installer path downloads and executes a remote OpenClaw installer.

Mitigation: Avoid that path unless the installer source is pinned and verified.

Risk: Provider API keys may be exposed if passed directly on the command line or stored insecurely.

Mitigation: Do not pass real provider API keys on the command line; use an approved secret-handling process.

Risk: The watchdog can restart gateway processes persistently.

Mitigation: Run it only as an unprivileged OpenClaw service account and restrict it to the intended gateway process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/evez-fleet)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash scripts and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cloud setup and restart commands should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
