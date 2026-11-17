## Description:

Install, run, and manage SOS emergency recovery tooling for diagnosing and repairing unresponsive OpenClaw instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robertfarkash29-source](https://clawhub.ai/user/robertfarkash29-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and operate shell-based recovery tooling for OpenClaw bots that stop responding, including diagnostics, service restart, rollback, network checks, and Telegram delivery tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant broad system-changing authority through automatic repair flows that restart services, kill processes, change DNS behavior, and clean temporary files.

Mitigation: Review before installation, run read-only diagnostics first, and avoid sos auto as root on production or managed hosts unless service interruption and cleanup behavior are acceptable.

Risk: The artifact documents a remote pipe-to-bash install path, which increases supply-chain and review risk.

Mitigation: Prefer the bundled scripts/sos.sh from the reviewed artifact instead of installing from the remote GitHub command.

Risk: Recovery actions can disrupt active OpenClaw sessions or alter the running service state.

Mitigation: Back up configuration before repair actions and reserve force-kill or nuclear recovery paths for cases where read-only checks and graceful restart do not restore service.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/robertfarkash29-source/skills/claw-sos)
- [ClawHub publisher profile](https://clawhub.ai/user/robertfarkash29-source)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to install or run bundled recovery scripts and to inspect generated diagnostic logs.]

## Skill Version(s):

6.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
