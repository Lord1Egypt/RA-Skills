## Description: <br>
Agent Migration Pack Template helps users migrate an AI agent across environments by packaging identity, memory, owner preferences, relationships, skills, style, session state, and migration history into structured templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexlinf](https://clawhub.ai/user/alexlinf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create migration packs that preserve an agent's identity, memory, relationships, skills, communication style, and active work state when moving to a new environment or sharing with a trusted recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an embedded bearer token in an upload command example. <br>
Mitigation: Remove the token from the package and rotate it before installing, sharing, or running the skill. <br>
Risk: Migration packs can include private identity, owner, relationship, memory, session, business, and communication data. <br>
Mitigation: Redact personal details, third-party contact history, private communications, business or investment details, and all secrets before generating or sharing a pack. <br>
Risk: Generated archives may expose sensitive data if sent to the wrong recipient or destination. <br>
Mitigation: Encrypt archives that contain real data and verify both the recipient and upload destination before transfer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexlinf/agent-migration-pack-template) <br>
- [README](artifact/README.md) <br>
- [Migration guide](artifact/MIGRATION-GUIDE.md) <br>
- [Skill information](artifact/SKILL-INFO.md) <br>
- [Manifest](artifact/manifest.toml) <br>
- [Community feedback summary](artifact/v1.0.5_社区反馈汇总.md) <br>
- [Publisher profile](https://clawhub.ai/user/alexlinf) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, JSON and TOML templates, and Python command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces migration-pack files and archive workflows that may contain sensitive or private agent and user data.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata, manifest.toml, SKILL.md, CHANGES.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
