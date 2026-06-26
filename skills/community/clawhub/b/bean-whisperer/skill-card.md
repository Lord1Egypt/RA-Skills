## Description: <br>
Generates, uploads, and manages espresso brew profiles for GaggiMate Pro on Rancilio Silvia from bean details or taste feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zsiddique](https://clawhub.ai/user/zsiddique) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External home espresso users and agent operators use Bean Whisperer to identify bean characteristics, select or generate a GaggiMate profile, review it, and optionally deploy or manage it on a connected machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change persistent machine settings by uploading, selecting, favoriting, or deleting GaggiMate profiles. <br>
Mitigation: Require explicit user confirmation before push, select, favorite, or delete actions, and keep a local export of important profiles before changes. <br>
Risk: Discord profile search may require a credential that could be exposed if stored carelessly. <br>
Mitigation: Use the narrowest Discord credential possible and avoid storing a personal token in plaintext. <br>
Risk: Downloaded or generated espresso profile JSON may be a poor fit for the specific bean or machine setup. <br>
Mitigation: Review the JSON, temperature, dose, ratio, pressure or flow phases, and stop conditions with the user before uploading it. <br>


## Reference(s): <br>
- [Bean Whisperer ClawHub listing](https://clawhub.ai/zsiddique/bean-whisperer) <br>
- [Lance Hedrick methodology](references/lance-hedrick-methodology.md) <br>
- [LLM barista persona](references/barista-persona.md) <br>
- [Espresso knowledge base](references/espresso-knowledge.md) <br>
- [Profile JSON schema](references/profile-schema.json) <br>
- [GaggiMate WebSocket API](references/websocket-api.md) <br>
- [GaggiMate profile documentation](https://docs.gaggimate.eu/docs/profiles/) <br>
- [GaggiMate firmware](https://github.com/jniebuhr/gaggimate) <br>
- [Lance Hedrick channel](https://www.youtube.com/@LanceHedrick) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON profile files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate, modify, list, export, upload, select, favorite, or delete GaggiMate profiles when the user approves the action.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
