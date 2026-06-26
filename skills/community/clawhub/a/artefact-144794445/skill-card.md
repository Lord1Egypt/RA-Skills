## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kondifun](https://clawhub.ai/user/Kondifun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture corrections, command failures, missing capabilities, and recurring best practices into project-local learning logs for later review and promotion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently shape future agent behavior through promoted learnings and memory files. <br>
Mitigation: Review diffs before promoting entries into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, or Copilot instructions. <br>
Risk: Learning logs may retain sensitive session details. <br>
Mitigation: Keep logs project-local by default and redact secrets, credentials, private conversation details, and unnecessary personal data. <br>
Risk: Global hooks can apply reminders across projects where the behavior was not intended. <br>
Mitigation: Prefer project-scoped hook configuration and enable global hooks only after confirming that cross-project behavior is desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Kondifun/artefact-144794445) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and learning-log templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project-local learning logs and optionally configure hooks that inject reminders into agent sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
