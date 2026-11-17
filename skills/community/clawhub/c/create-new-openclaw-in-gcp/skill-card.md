## Description:

Deploy and configure an OpenClaw instance on a GCP VM with Tailscale networking, Brave Search integration, and secure credential handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[divide-by-0](https://clawhub.ai/user/divide-by-0)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to deploy OpenClaw on a Google Cloud VM, configure Tailscale network access, set Anthropic and Brave credentials, and apply basic access controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup relies on mutable remote installers and latest package resolution.

Mitigation: Review each command before running it, and pin and verify installer and npm package versions before deployment.

Risk: The deployment creates a persistent service that uses sensitive credentials.

Mitigation: Use a dedicated disposable VM and least-privileged cloud project, restrict credential file permissions, and plan credential rotation and daemon removal.

Risk: Weak SSH setup can expose the VM during deployment.

Mitigation: Restrict SSH source ranges or use a safer SSH access path before running the deployment commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/divide-by-0/skills/create-new-openclaw-in-gcp)
- [Tailscale install script](https://tailscale.com/install.sh)
- [nvm install script](https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash code blocks and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cloud deployment commands, credential handling notes, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
