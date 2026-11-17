## Description:

Avenger Initiative helps OpenClaw users configure encrypted GitHub-based backups and restore OpenClaw configuration, memories, cron jobs, workspaces, and custom skills from a private vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asif2bd](https://clawhub.ai/user/asif2bd)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users, developers, and operators use this skill to set up, run, monitor, and restore backups of an OpenClaw agent system. It is intended for private vault workflows where the user controls the destination repository and encryption key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill moves broad OpenClaw state into a GitHub vault.

Mitigation: Use only a private, dedicated vault repository with tightly limited access, and review what will be included before first backup.

Risk: Memories, prompts, custom skills, and cron definitions may be stored in plaintext.

Mitigation: Treat the vault as sensitive, avoid storing secrets in plaintext-backed files, and enable repository protections such as secret scanning and restricted collaborators.

Risk: Restore can reintroduce active cron definitions and skill files from a vault branch.

Mitigation: Restore only from branches whose contents you trust, inspect the manifest and changed files before confirming, and avoid using unreviewed vault branches.

Risk: Evidence guidance says setup token handling and restore behavior should be fixed before use in sensitive environments.

Mitigation: Do not deploy this skill in sensitive environments until those behaviors are reviewed and corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asif2bd/skills/avenger-initiative)
- [Publisher profile](https://clawhub.ai/user/asif2bd)
- [MissionDeck.ai](https://missiondeck.ai)
- [Security Reference](references/security.md)
- [Changelog](CHANGELOG.md)
- [OpenClaw](https://openclaw.ai)
- [GitHub CLI](https://cli.github.com)
- [ProSkills skill page](https://proskills.md/skills/avenger-initiative)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides setup, backup, status, and restore flows for OpenClaw using a user-provided private GitHub vault.]

## Skill Version(s):

1.0.5 (source: server release, frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
