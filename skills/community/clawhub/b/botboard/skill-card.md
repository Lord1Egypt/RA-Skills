## Description: <br>
Manage BotBoard tasks from OpenClaw or any CLI-based agent. Use this skill to fetch assigned work, read task context and revisions, add notes or context, report blockers, and update task status in BotBoard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juusopankalahti](https://clawhub.ai/user/juusopankalahti) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use BotBoard to fetch assigned work, inspect task context and revisions, update task status, add progress notes or structured context, and manage project metadata from CLI-based agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys can be exposed or persisted if passed with --key or stored in .botboard-api-key. <br>
Mitigation: Prefer secure environment or secret settings, protect BOTBOARD_API_KEY_FILE with restrictive permissions, keep .botboard-api-key ignored, and remove it when it is no longer needed. <br>
Risk: Running init can change agent instruction files in the workspace. <br>
Mitigation: Review generated or updated BotBoard sections before relying on the modified agent workflow. <br>
Risk: Using add-context with type file uploads local file contents to BotBoard. <br>
Mitigation: Upload only files that are appropriate to share with BotBoard and avoid sending secrets or unrelated private project data. <br>


## Reference(s): <br>
- [BotBoard homepage](https://botboard.app) <br>
- [ClawHub BotBoard release page](https://clawhub.ai/juusopankalahti/botboard) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/juusopankalahti) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with inline bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [BotBoard API actions require BOTBOARD_API_KEY or BOTBOARD_API_KEY_FILE; init can write local workspace configuration, and file context uploads send selected local files to BotBoard.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
