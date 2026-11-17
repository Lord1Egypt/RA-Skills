## Description:

Fetches CPAP therapy data from the PrismaAPP API (Lowenstein Medical) and writes localized daily Obsidian log notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanwebgit](https://clawhub.ai/user/sanwebgit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch their own PrismaAPP CPAP therapy metrics and create structured, localized daily notes in an Obsidian vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores PrismaAPP credentials locally, including a medical account password.

Mitigation: Protect config.json carefully, keep it out of version control, and use the skill only if local plaintext credential storage is acceptable.

Risk: A configurable API origin could send credentials somewhere other than the intended PrismaAPP service.

Mitigation: Remove or pin api_base to https://my.prismacloud.com before use.

Risk: Generated notes contain sensitive sleep therapy records in the configured Obsidian vault.

Mitigation: Review the vault path and log directory before running, and avoid enabling cron until the note location is confirmed.

## Reference(s):

- [Skill README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)
- [PrismaAPP API Base](https://my.prismacloud.com)
- [ClawHub Skill Page](https://clawhub.ai/sanwebgit/skills/cpap-prisma-app)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Localized Obsidian Markdown notes plus terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes one note per requested day using the configured vault path, log directory, timezone, and locale.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
