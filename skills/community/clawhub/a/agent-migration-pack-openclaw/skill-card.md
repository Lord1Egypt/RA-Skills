## Description: <br>
Creates a complete migration package for AI agents, including identity, owner information, memory, relationships, skills, and communication style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexlinf](https://clawhub.ai/user/alexlinf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to create, validate, checksum, and package AI agent migration packs for backup, sharing, or transfer across environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated migration packs can contain sensitive profile, memory, relationship, and skill data. <br>
Mitigation: Inspect and redact generated JSON and ZIP contents before storing, sharing, or uploading a pack. <br>
Risk: Owner and relationship records may include private or third-party information. <br>
Mitigation: Confirm consent where appropriate and remove passwords, API keys, private contacts, and confidential notes before distribution. <br>
Risk: The generator currently exports the skills catalog even without --include-skills. <br>
Mitigation: Review generated skill catalog files and remove entries that should not be shared. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexlinf/agent-migration-pack-openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/alexlinf) <br>
- [Migration guide](artifact/MIGRATION-GUIDE.md) <br>
- [Original skill reference](https://xiaping.coze.site/skill/c7363f71-212f-4b34-9551-f72bf5d47044) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, JSON and TOML templates, and Python command workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates and validates local migration pack files; packed archives may include sensitive agent profile, memory, relationship, and skills data.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata, artifact manifest.toml, artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
