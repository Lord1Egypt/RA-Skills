## Description:

Shared OpenClaw skill for guiding ClawMover backup and restore workflows with explicit confirmation, input validation, and a manual-command-first execution policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tubo70](https://clawhub.ai/user/tubo70)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to plan and run ClawMover backup, simulated restore, and real restore workflows while validating inputs and requiring confirmation for environment-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide installation of @clawmover/cli, which can modify the host environment.

Mitigation: Confirm the package and expected publisher before installing, and prefer a pinned version or isolated environment.

Risk: Backup and restore workflows use sensitive data secret keys and verification codes.

Mitigation: Treat these values as sensitive, avoid echoing or logging them, and mask them in displayed commands unless exact command text is explicitly requested.

Risk: A real restore can modify the local OpenClaw environment.

Mitigation: Prefer simulated restore with a validated destination path before any live restore, and require explicit confirmation for real restore.

## Reference(s):

- [ClawMover](https://clawmover.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include masked sensitive values and manual-command alternatives for backup, restore, and CLI installation workflows.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
