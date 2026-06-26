## Description: <br>
Captures agent learnings, errors, corrections, and feature requests in markdown logs so future sessions can review and promote durable guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Keyserkazi1](https://clawhub.ai/user/Keyserkazi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding agents use this skill to record failures, user corrections, knowledge gaps, and recurring workflow lessons as structured markdown entries. Teams can review those entries and promote broadly useful guidance into agent instruction files or reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived learnings may persist sensitive or personal information in durable markdown logs or promoted instruction files. <br>
Mitigation: Sanitize entries before saving or sharing, and do not store secrets, credentials, personal data, customer content, raw transcripts, or sensitive command output. <br>
Risk: Broadly scoped hooks can inject reminders too often or across workspaces where durable memory is not desired. <br>
Mitigation: Inspect hook scripts before enabling them and prefer project-level, narrowly matched hooks over global every-prompt activation. <br>
Risk: Promoted learnings may encode incorrect or over-broad guidance for future agents. <br>
Mitigation: Review learning entries before promotion and keep promoted rules concise, specific, and tied to verified recurring patterns. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Logging Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured local learning-log entries and optional reminder text for configured hooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
