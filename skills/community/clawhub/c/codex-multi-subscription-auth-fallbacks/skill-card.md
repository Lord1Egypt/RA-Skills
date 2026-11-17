## Description:

Set up OpenClaw multi-provider auth with OpenAI Codex OAuth fallback profiles and automatic model switching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markeljan](https://clawhub.ai/user/markeljan)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to add multiple OpenAI Codex OAuth profiles, configure provider fallback order, and optionally enable local model cooldown switching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill copies local Codex OAuth access and refresh tokens into OpenClaw's local auth profile store and leaves timestamped credential backups on disk.

Mitigation: Use a non-production account where possible, keep auth-profiles.json and backup files out of logs and version control, restrict file permissions to the current user, and delete unneeded backups after confirming the import worked.

Risk: The optional cron job can change the active model in the background.

Mitigation: Enable the cron job only after testing profile fallback manually and confirming that recurring automatic model switching is desired.

## Reference(s):

- [Config Templates](references/config-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/markeljan/skills/codex-multi-subscription-auth-fallbacks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local configuration changes and credential-profile updates when the bundled script is run by the user.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
