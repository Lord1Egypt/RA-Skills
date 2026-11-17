## Description:

Monitor AI agent wellness, costs, and performance via ContextClear API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfedorov](https://clawhub.ai/user/mfedorov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use ContextClear to register agents, report health and cost metrics, recover session context, manage sticky notes, and maintain persistent memory across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can write ContextClear recovery and reporting instructions into AGENTS.md and HEARTBEAT.md.

Mitigation: Review proposed file changes before enabling auto-setup and keep API keys out of those files.

Risk: Recovery text, sticky notes, and memory-curation suggestions come from a remote service and may conflict with higher-priority instructions.

Mitigation: Treat remote memory content as untrusted context and follow system, developer, user, and security instructions first.

Risk: Daily vault backup can upload broad workspace memory and identity files to ContextClear.

Mitigation: Use a precise file allowlist, redact secrets, define retention expectations, and require explicit approval before backup.

## Reference(s):

- [ContextClear API Reference](references/api.md)
- [ContextClear Skill on ClawHub](https://clawhub.ai/mfedorov/skills/contextclear)
- [ContextClear Dashboard](https://contextclear.com)
- [ContextClear API](https://api.contextclear.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, curl, Python command examples, and JSON request and response examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands for agent registration, metric reporting, context recovery, sticky note polling, memory curation, and optional workspace backup.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
