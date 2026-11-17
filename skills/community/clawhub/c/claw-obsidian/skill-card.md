## Description:

Read, search, create, edit, and safely refactor an Obsidian Markdown vault directly through files, without Obsidian or an Obsidian CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanjelin](https://clawhub.ai/user/lanjelin)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to manage notes, attachments, and links in a local Obsidian vault with reviewable changes and vault-specific rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and change files in the configured vault.

Mitigation: Install only if granting read/write access to that vault is acceptable; review proposed changes before applying them.

Risk: Optional shell hooks can run local commands with user permissions, including during reads and previews.

Mitigation: Leave OBSIDIAN_PRE_COMMAND and OBSIDIAN_POST_COMMAND unset unless their exact scripts have been reviewed.

Risk: A configured vault rules file may contain sensitive or unsuitable instructions.

Mitigation: Point OBSIDIAN_VAULT_RULES only at a dedicated, non-sensitive Markdown rules file.

## Reference(s):

- [Source repository](https://github.com/Lanjelin/openclaw-obsidian)
- [ClawHub skill listing](https://clawhub.ai/lanjelin/skills/claw-obsidian)
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment)
- [OpenClaw skills configuration](https://docs.openclaw.ai/tools/skills-config)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance and JSON operation results; requested notes are Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Vault operations require a configured local vault and Python 3.10+ on Linux or macOS.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
