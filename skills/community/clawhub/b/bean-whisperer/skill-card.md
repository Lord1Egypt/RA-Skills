## Description:

Generate, explain, manage, and optionally deploy espresso brew profiles for GaggiMate Pro and compatible machines based on coffee bean details and taste feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zsiddique](https://clawhub.ai/user/zsiddique)

### License/Terms of Use:

MIT-0

## Use Case:

External users and home espresso developers use this skill to turn bean photos, bean names, or shot-taste feedback into machine-ready GaggiMate profile JSON and profile-management commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted community profiles may contain unsuitable temperature, pressure, flow, duration, or stop values.

Mitigation: Manually inspect and adjust every downloaded profile before saving, selecting, or pushing it to a machine.

Risk: Profile push, select, favorite, or delete commands can alter machine state or remove profiles.

Mitigation: Confirm the exact profile ID and intended action before running profile-management commands, and export or back up important profiles first.

Risk: Discord profile search requires a credential.

Mitigation: Provide a Discord credential only when necessary, keep it out of prompts and logs, and remove or rotate it when access is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zsiddique/skills/bean-whisperer)
- [Lance Hedrick Methodology](references/lance-hedrick-methodology.md)
- [LLM Barista Persona](references/barista-persona.md)
- [Espresso Knowledge Base](references/espresso-knowledge.md)
- [Profile JSON Schema](references/profile-schema.json)
- [GaggiMate WebSocket API](references/websocket-api.md)
- [GaggiMate](https://gaggimate.eu/)
- [Lance Hedrick](https://www.youtube.com/@LanceHedrick)
- [GaggiMate Profile Docs](https://docs.gaggimate.eu/docs/profiles/)
- [GaggiMate Firmware](https://github.com/jniebuhr/gaggimate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown explanations with JSON profile files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce machine profile JSON, profile-management commands, and parameter guidance for review before deployment.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
