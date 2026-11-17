## Description:

Deploy and manage Fly.io apps via CLI - apps, machines, volumes, secrets, certificates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melvynx](https://clawhub.ai/user/melvynx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy and operate Fly.io applications from an agent-assisted CLI workflow, including app creation, deployments, logs, scaling, secrets, volumes, certificates, machines, SSH, and proxy tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Linux setup path uses a pipe-to-shell installer.

Mitigation: Review the installer before use, or prefer a trusted package manager or verified pinned flyctl release.

Risk: The skill includes high-impact Fly.io operations such as destroy, delete, unset, SSH, and direct infrastructure changes.

Mitigation: Require explicit confirmation before destructive operations, scope commands to the intended app or resource, and treat SSH commands as changes to running infrastructure.

Risk: Secret-management commands can expose sensitive values if echoed into prompts, logs, or command history.

Mitigation: Avoid logging secret values and pass secrets through an approved secret-handling workflow.

## Reference(s):

- [Fly.io install script](https://fly.io/install.sh)
- [ClawHub Fly skill page](https://clawhub.ai/melvynx/skills/fly)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and command reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends JSON output for programmatic flyctl commands where supported.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
