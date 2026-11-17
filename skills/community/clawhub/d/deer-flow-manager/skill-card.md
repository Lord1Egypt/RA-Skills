## Description:

Deer Flow Manager helps agents install, configure, update, uninstall, start, and troubleshoot DeerFlow 2.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[braveheartzjh](https://clawhub.ai/user/braveheartzjh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage the DeerFlow 2.0 lifecycle, including setup, model configuration, updates, uninstallation, startup, and common troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and update steps can run high-impact commands or downloaded installer scripts with weak verification.

Mitigation: Review commands before execution, prefer pinned DeerFlow releases or verified commits, and inspect downloaded installer scripts before running them.

Risk: Privileged package installation and remote setup commands can expand the impact of a compromised or incorrect command.

Mitigation: Avoid sudo -E for remote scripts and use the least privilege needed for package installation.

Risk: Update and uninstall workflows can remove virtual environments, temporary files, or the DeerFlow install directory.

Mitigation: Back up config.yaml, .env, and logs before update, cleanup, or uninstall steps.

Risk: Model provider configuration can expose API keys if users paste secrets into chat or store them in broadly readable files.

Mitigation: Do not paste raw API keys into chat, and store secrets in environment variables or files with restricted permissions.

## Reference(s):

- [DeerFlow command reference](references/deer-flow-commands.md)
- [DeerFlow GitHub repository](https://github.com/bytedance/deer-flow.git)
- [ClawHub skill page](https://clawhub.ai/braveheartzjh/skills/deer-flow-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command tables, file paths, service ports, and model configuration templates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
