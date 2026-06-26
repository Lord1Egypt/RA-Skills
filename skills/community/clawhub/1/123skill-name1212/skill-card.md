## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suncrespo](https://clawhub.ai/user/suncrespo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture command failures, user corrections, feature requests, and recurring lessons in local markdown notes so future sessions can reuse them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local learning notes can persist sensitive details from errors, corrections, or command output. <br>
Mitigation: Use the skill only when persistent learning notes are desired, redact secrets and private data, and review .learnings before sharing or reusing the workspace. <br>
Risk: Optional hooks can inspect prompts or command output and add persistent reminders. <br>
Mitigation: Prefer project-level hook configuration, use narrow matchers such as debug|error|fix, and avoid command-output detection in sensitive sessions. <br>
Risk: Promoted memory files can influence later agent behavior with stale or incorrect guidance. <br>
Mitigation: Review promoted AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, and MEMORY.md entries before relying on them in future sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suncrespo/123skill-name1212) <br>
- [OpenClaw integration guide](references/openclaw-integration.md) <br>
- [Hook setup guide](references/hooks-setup.md) <br>
- [Entry examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local .learnings markdown files and optional hook configuration when the user enables those workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
