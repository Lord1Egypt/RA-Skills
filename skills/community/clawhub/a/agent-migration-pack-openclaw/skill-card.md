## Description:

Creates a migration package for AI agents, including identity, owner information, memory, relationships, skills, and communication style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexlinf](https://clawhub.ai/user/alexlinf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to back up, migrate, share, or restore an AI agent's configuration across supported environments. It provides templates and commands for organizing identity, user preferences, memory, relationships, skill inventory, and style data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration packs may contain sensitive identity, owner, memory, relationship, and skill data.

Mitigation: Review generated folders and ZIP files before installing or sharing, remove bundled real examples, and redact personal details.

Risk: Relationship and contact records may include third-party information.

Mitigation: Do not share relationship or contact data unless consent and need are confirmed.

Risk: Skill inventories can reveal installed tools or configurations.

Mitigation: Verify whether skill inventory files are included and remove them when they are not required for migration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexlinf/skills/agent-migration-pack-openclaw)
- [Publisher profile](https://clawhub.ai/user/alexlinf)
- [Original skill](https://xiaping.coze.site/skill/c7363f71-212f-4b34-9551-f72bf5d47044)
- [Migration guide](MIGRATION-GUIDE.md)
- [Manifest](manifest.toml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and TOML templates plus Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces migration-pack files and ZIP archives when its bundled scripts are run.]

## Skill Version(s):

1.0.4 (source: server release metadata, manifest.toml, _meta.json, and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
