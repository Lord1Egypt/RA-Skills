## Description:

Helps developers back up, restore, and migrate macOS or Linux development environments, including configuration, repositories, credentials, software, and AI agent state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futrixdev](https://clawhub.ai/user/futrixdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to select and document what to carry from a macOS or Linux machine, create a local encrypted backup, and restore it on another machine with review before sensitive or executable content is applied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backup can contain SSH keys, cloud credentials, and agent sessions.

Mitigation: Review exactly what is carried; keep the passphrase out of agent transcripts and restore credentials without overwriting existing files.

Risk: Staging and restore directories hold plaintext copies of sensitive files.

Mitigation: Review the staging location and delete plaintext directories after confirming the encrypted backup or completed restore.

Risk: Restored agent hooks, MCP servers, skills, and plugins can execute code in future sessions.

Mitigation: Review their commands and scripts with the user before restoring them.

Risk: Installing the backup tool or replaying a software list can introduce unreviewed code.

Mitigation: Review the installer dry run, prefer the bundled or pinned installer, verify packages through their managers, and confirm installations.

## Reference(s):

- [EnvRelay homepage](https://envrelay.com/)
- [EnvRelay skill release](https://clawhub.ai/futrixdev/skills/envrelay)
- [Credential handling](artifact/references/credential-locations.md)
- [Backup manifest and restore checks](artifact/references/manifest.md)
- [AI agent backup and restore](artifact/references/ai-agents.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell commands and manifest guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides creation of a local encrypted backup; the user enters the passphrase directly.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
