## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weina0925](https://clawhub.ai/user/weina0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to log command failures, user corrections, feature requests, and reusable learnings into project-local markdown files for later review and promotion into durable agent guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can capture sensitive project context if raw transcripts, command output, secrets, tokens, or private configuration are logged. <br>
Mitigation: Use project-local .learnings storage, record short sanitized summaries, redact sensitive values, and avoid logging secrets, private transcripts, raw command output, or sensitive project data. <br>
Risk: Promoting unreviewed learning entries into agent instruction files can preserve incorrect or misleading guidance. <br>
Mitigation: Review learning entries before promoting them into AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or new skills. <br>
Risk: Optional hook workflows can inspect prompts or command results in a workspace. <br>
Mitigation: Enable hooks only in trusted workspaces and only when the user intentionally opts into automatic reminders or error detection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weina0925/en) <br>
- [OpenClaw integration reference](references/openclaw-integration.md) <br>
- [Hook setup reference](references/hooks-setup.md) <br>
- [Usage examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and template snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or append project-local learning logs and optional hook configuration when the user enables that workflow.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
