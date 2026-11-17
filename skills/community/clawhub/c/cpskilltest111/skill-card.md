## Description:

Captures learnings, errors, and corrections so agents can maintain durable learning logs and promote high-value patterns into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockcloud](https://clawhub.ai/user/blockcloud)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, missing capabilities, and useful discoveries in structured learning files. It helps preserve recurring knowledge and promote reviewed learnings into project or workspace memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived learnings may persist sensitive, private, incorrect, or misleading context into future agent instructions.

Mitigation: Prefer project-local storage, redact secrets and private user context, and manually review every promoted entry before it becomes durable instruction.

Risk: Broad automatic hooks may inject reminders or learning workflows into sessions where they are not appropriate.

Mitigation: Avoid global hook configuration; enable hooks only for reviewed projects and keep hook output minimal.

Risk: Cross-session transcript reads or sends can expose context beyond the current task.

Mitigation: Use cross-session sharing only with explicit approval for that session.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command, hook, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or update .learnings/*.md files and promote reviewed entries into workspace or project instruction files.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
