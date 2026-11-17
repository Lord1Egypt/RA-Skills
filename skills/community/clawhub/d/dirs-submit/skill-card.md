## Description:

Dirs Submit helps an agent use the `ship` CLI to log in, submit URLs to supported directory services, preview site metadata, check versions, and guide self-update behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allinaigc](https://clawhub.ai/user/allinaigc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when they need an agent to operate the `ship` CLI for URL submission, metadata preview, login recovery, subscription-error handling, and version checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and self-update flows can replace local executable code from upstream assets.

Mitigation: Review the upstream source before installing or updating, and verify downloaded code or release assets before execution.

Risk: Reusable service tokens are stored in `~/.config/ship/config.json`.

Mitigation: Treat the config file as sensitive, keep it out of logs, backups, and source control, and revoke or remove tokens when they are no longer needed.

## Reference(s):

- [Dirs Submit on ClawHub](https://clawhub.ai/allinaigc/skills/dirs-submit)
- [Project Homepage](https://github.com/RobinWM/ship-skills#dirs-submit)
- [API Reference](references/api.md)
- [Config Reference](references/config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and natural-language result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service error details such as authorization or subscription guidance when the CLI reports them.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
