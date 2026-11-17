## Description:

Install and apply ClawJection bundles when a user asks to install a ClawJection, run a ClawJection, or configure an OpenClaw instance from a ClawJection repo, archive, or local bundle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nmadeleidev](https://clawhub.ai/user/nmadeleidev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install or run ClawJection bundles that modify a local OpenClaw instance, install tools or skills, and apply ordered follow-up actions returned by the bundle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawJection bundles can run local entrypoint code that changes OpenClaw configuration, identity files, tools, skills, and auth setup.

Mitigation: Use trusted, pinned, and reviewed bundle sources, preferably in a disposable or backed-up environment, and require explicit approval before running entrypoints.

Risk: Bundle-supplied follow-up actions may continue changing the environment after the entrypoint finishes.

Mitigation: Review follow-up actions before applying them and verify installed CLIs, skills, or configuration changes before claiming success.

Risk: Secrets can be exposed if a bundle writes credentials into workspace files.

Mitigation: Keep secrets out of workspace files unless the bundle explicitly requires it and the user approves that behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nmadeleidev/skills/clawjection)
- [Publisher profile](https://clawhub.ai/user/nmadeleidev)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ordered follow-up actions based on ClawJection bundle result JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
