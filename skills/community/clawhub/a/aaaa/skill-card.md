## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gakkiismywife](https://clawhub.ai/user/gakkiismywife) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture corrections, command failures, feature requests, and recurring workflow lessons in durable learning files. It also guides promotion of broadly useful learnings into agent memory or project instruction files after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived content into learning logs and future agent instruction files. <br>
Mitigation: Keep learning logs project-scoped, redact secrets and personal data before logging, and require human review before promoting entries into AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, CLAUDE.md, or Copilot instructions. <br>
Risk: Optional hooks inject reminders or inspect command output to suggest logging errors. <br>
Mitigation: Review hook files before enabling them, enable hooks only in intended workspaces, and avoid global installation unless durable learning behavior is desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gakkiismywife/aaaa) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .learnings markdown entries and optional agent instruction files when a user enables those workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
