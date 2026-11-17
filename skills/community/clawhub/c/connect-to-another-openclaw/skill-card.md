## Description:

Connect to and manage another OpenClaw server remotely via SSH, including health checks, skill synchronization, gateway restarts, and channel monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangbb-coder](https://clawhub.ai/user/fangbb-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to administer OpenClaw instances they control over SSH, check remote health, troubleshoot gateway port conflicts, compare or sync skills, and inspect QQBot-related sessions or logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote administration can affect servers and local environments if pointed at the wrong host or used with broad privileges.

Mitigation: Restrict use to OpenClaw servers you own or administer, use a dedicated least-privilege SSH account and key, and require explicit approval before process termination or skill sync actions.

Risk: Unsafe defaults and command-construction issues may allow a compromised host or crafted skill list to run unintended commands.

Mitigation: Review or fix the skill before installation, enable SSH host-key verification, avoid automatic confirmation with --yes, and validate and quote skill names before local or remote installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangbb-coder/skills/connect-to-another-openclaw)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented status text with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses required host and action parameters plus optional SSH user, key, port, skill, and confirmation flags.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
