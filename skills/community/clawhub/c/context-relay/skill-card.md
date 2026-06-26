## Description: <br>
Solves the memory fragmentation problem for Agents during session restarts, sub-agent boundaries, and cron/heartbeat isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain task continuity across session restarts, sub-agent boundaries, and scheduled task isolation by reading and updating project context files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent context files can expose secrets, sensitive notes, or private project state if agents store unsuitable content. <br>
Mitigation: Do not store secrets or sensitive private notes in PROJECT.md, state.json, decisions.md, or todos.json; review context files before sharing or committing them. <br>
Risk: Initialization or synchronization can overwrite or change durable project context files. <br>
Mitigation: Require user confirmation before initialization, writes, cleanup, or use of --force; prefer running the initializer without --force unless overwriting is intentional. <br>
Risk: The skill's workflow can encourage committing context changes without an explicit approval boundary. <br>
Mitigation: Require user confirmation before any git commit and review generated context changes before committing them. <br>


## Reference(s): <br>
- [Project Template Details](references/project-template.md) <br>
- [todos.json Self-Managed Todo System](references/todos-system.md) <br>
- [Cold Start Guide](references/cold-start-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/openlark/context-relay) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON templates and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update PROJECT.md, state.json, decisions.md, and todos.json when the user approves initialization or synchronization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
