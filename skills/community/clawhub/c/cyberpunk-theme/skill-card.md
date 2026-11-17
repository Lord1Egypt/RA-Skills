## Description:

Installs, repairs, and customizes a cyberpunk theme for OpenClaw's chat and dream interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasanuowa](https://clawhub.ai/user/kasanuowa)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and workspace maintainers use this skill to install or restore a cyberpunk chat and dream theme and replace five avatar and background images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation changes the target workspace and live OpenClaw Control UI by default.

Mitigation: Use --skip-apply to stage changes first, and review backups before relying on rollback.

Risk: A fresh install without local default images may download assets from ClawHub.

Mitigation: Provide all five image overrides or use existing local assets if network retrieval is undesirable.

## Reference(s):

- [ClawHub cyberpunk-theme release](https://clawhub.ai/kasanuowa/skills/cyberpunk-theme)
- [Theme slots and image guidance](references/theme-slots.md)
- [Theme configuration example](references/theme-config.example.json)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for installation, repair, and replacement of theme images.]

## Skill Version(s):

1.0.28 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
