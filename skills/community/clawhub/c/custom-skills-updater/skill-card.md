## Description:

Manage manually installed skills (non-ClawHub). Supports checking updates, updating, and listing custom skills from GitHub or local sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qvshuo](https://clawhub.ai/user/qvshuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to inventory manually installed non-ClawHub skills, check GitHub or local sources for updates, and apply approved updates while maintaining REGISTRY.yaml.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite manually installed skill instructions during approved updates.

Mitigation: Review each proposed update summary before approval and keep backups or version control for manually installed skills.

Risk: GitHub archive updates lack clearly documented path and archive containment safeguards.

Mitigation: Use only trusted repositories and add strict path validation and safe archive extraction before relying on archive-based updates.

Risk: Untrusted registry entries or source paths can direct the updater to unsafe sources.

Mitigation: Review REGISTRY.yaml entries carefully and avoid untrusted skill names, repositories, branches, or source paths.

## Reference(s):

- [README](artifact/README.md)
- [Registry Example](artifact/REGISTRY.example.yaml)
- [ClawHub Skill Page](https://clawhub.ai/qvshuo/skills/custom-skills-updater)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update REGISTRY.yaml and skill files only after explicit user approval; unattended runs defer updates.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
